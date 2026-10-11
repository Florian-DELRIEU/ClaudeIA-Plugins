#!/usr/bin/env python3
"""
Applique la regle de visibilite par profondeur relative (limitVisibility) sur
un ORBAT JSON orbat-mapper.app, camp par camp.

Regle (validee avec Florian, aout 2026 — references/format.md) :
  - Echelle de reference fixe : R = 5 bandes, bornes B = [0, 10, 13, 16, 18, 24].
  - Pour un cote de profondeur reelle D (D = profondeur max de son arbre) :
      band_index(i) = round_half_up(i * R / D)   pour i = 1..D
      bande naturelle de la profondeur i = [ B[band_index(i) - 1], B[band_index(i)] ]
      (band_index(D) = R force)
  - Regle A (comblement de bande sautee) : si D < R, certaines bandes sont
    sautees. On comble en prolongeant le MAX de la profondeur precedente
    jusqu'au MIN naturel de la profondeur suivante reellement utilisee (on
    n'avance jamais le debut de la profondeur suivante).
  - Regle A' (racine, ajout 2026-10) : la profondeur 1 commence TOUJOURS a
    B[0]. Sans cela, un camp de profondeur D <= 3 n'affiche rien a faible
    zoom (D=1 -> [18,24], D=2 -> [13,18]). Sans effet pour D >= 4.
  - Regle B (feuilles) : toute unite qui est une feuille (pas de subUnits)
    voit son maxZoom force a la borne max globale (b[-1] = 24), quelle que
    soit sa profondeur naturelle, puisque rien de plus fin ne prendra le
    relais en dessous.
"""
import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP

R = 5
B = [0, 10, 13, 16, 18, 24]  # 6 bornes = R+1 = 5 bandes


def round_half_up(x):
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def band_index(i, D):
    """Indice de bande (0..R) pour la profondeur i d'un cote de profondeur D."""
    if i <= 0:
        return 0
    if i >= D:
        return R
    return round_half_up(i * R / D)


def compute_side_bands(D):
    """Renvoie une liste de (min,max) par profondeur 1..D, regle A appliquee."""
    natural = []
    for i in range(1, D + 1):
        bi = band_index(i, D)
        lo = B[bi - 1]
        hi = B[bi]
        natural.append([lo, hi])

    # Regle A' : la racine est toujours visible des le zoom minimal.
    natural[0][0] = B[0]

    # Regle A : combler les bandes sautees en etendant le max du niveau
    # precedent jusqu'au min naturel du niveau suivant.
    for i in range(len(natural) - 1):
        if natural[i][1] < natural[i + 1][0]:
            natural[i][1] = natural[i + 1][0]

    return natural


def max_depth(unit, depth=1):
    if not unit.get("subUnits"):
        return depth
    return max(max_depth(su, depth + 1) for su in unit["subUnits"])


def apply_unit(unit, depth, bands):
    lo, hi = bands[depth - 1]
    is_leaf = not unit.get("subUnits")
    if is_leaf:
        hi = B[-1]  # Regle B : toute feuille visible jusqu'au zoom max global
    unit["style"] = dict(unit.get("style") or {})
    unit["style"]["limitVisibility"] = True
    unit["style"]["minZoom"] = lo
    unit["style"]["maxZoom"] = hi
    for su in unit.get("subUnits", []):
        apply_unit(su, depth + 1, bands)


def process_side(side):
    roots = []
    for g in side.get("groups", []):
        roots.extend(g.get("subUnits", []))
    for u in side.get("units", []):
        if isinstance(u, dict) and "sidc" in u:
            roots.append(u)

    if not roots:
        return 0

    D = max(max_depth(r) for r in roots)
    bands = compute_side_bands(D)

    count = 0

    def count_units(u):
        nonlocal count
        count += 1
        for su in u.get("subUnits", []):
            count_units(su)

    for r in roots:
        apply_unit(r, 1, bands)
        count_units(r)

    return D, bands, count


def main():
    ap = argparse.ArgumentParser(
        description="Applique la visibilité par profondeur relative (style.limitVisibility), "
                    "camp par camp. Écrase le fichier sauf --output / --dry-run.")
    ap.add_argument("orbat", help="fichier ORBAT JSON")
    ap.add_argument("--output", help="fichier de sortie (défaut : écrase l'entrée)")
    ap.add_argument("--dry-run", action="store_true", help="affiche les bandes sans rien écrire")
    args = ap.parse_args()

    path = args.orbat
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    total = 0
    for side in data["sides"]:
        result = process_side(side)
        if result == 0:
            print(f"{side['name']}: aucune unite, ignore")
            continue
        D, bands, count = result
        print(f"{side['name']}: D={D}, bandes={bands}, unites stylees={count}")
        total += count

    print(f"Total unites stylees: {total}")
    if args.dry_run:
        print("[dry-run] Aucun fichier écrit.")
        return
    out = args.output or path
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Écrit dans {out}")


if __name__ == "__main__":
    main()
