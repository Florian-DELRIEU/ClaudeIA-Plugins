#!/usr/bin/env python3
"""
add_legends.py — Annote chaque échelon d'un ORBAT JSON (format orbat-mapper.app)
avec une légende de tous les codes acronymes v4 présents dans son sous-arbre,
en les faisant correspondre au nom réel du matériel/personnel.

Contrairement à `orbat-acronymize/scripts/apply_rename_map.py` (qui convertit un
ORBAT existant depuis des noms réels vers des codes, avec un mapping.json
explicite), ce script s'applique à un ORBAT **déjà codé en acronymes v4** (issu
de la Tâche 4 — écriture directe) : il déduit le nom réel de chaque code
directement depuis la `description` du catalogue racine (`equipment`/
`personnel`), sans mapping externe.

Convention attendue sur la `description` de catalogue (voir `references/
naming.md` Règle 5) : elle doit commencer par la désignation réelle du
matériel/personnel, éventuellement suivie de " — " puis d'un contexte
additionnel. Ex. :
    "MSE-3 Marid — variante commandement (transmissions renforcées)"
    -> nom réel extrait : "MSE-3 Marid"
Une description qui ne suit pas ce format (pas de nom réel identifiable) est
signalée en avertissement plutôt que silencieusement ignorée.

Ajoute, à chaque échelon (Group/Unit) dont le sous-arbre porte au moins un
code, la légende au format canonique (naming.md Règle 7 § 7.3), Équipement et
Personnel séparés, sans quantité :
    Équipement :
    * **CODE : Nom réel**

    Personnel :
    * **CODE : Nom réel**
La prose existante de la description (phrase de contexte, § 7.4) est
conservée ; seule l'ancienne légende est remplacée — idempotent.
Toute la mise en forme vient de `legends.py` (module unique).

Usage:
    python3 add_legends.py <orbat.json> [--output OUT.json] [--dry-run]

Par défaut, écrase le fichier d'entrée.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbat_lib as ol
import legends as lg


def build_reverse_map(orbat, warnings):
    """{"equipment": {code: nom réel}, "personnel": {...}} depuis les catalogues."""
    reverse = {"equipment": {}, "personnel": {}}
    for cat_key in ("equipment", "personnel"):
        for entry in orbat.get(cat_key, []) or []:
            code = entry.get("name")
            real_name = lg.extract_real_name(entry.get("description"))
            if not real_name:
                warnings.append(code)
                continue
            reverse[cat_key][code] = real_name
    return reverse


def _own_codes(node, kind, known):
    out = []
    for item in node.get(kind, []) or []:
        code = item.get("name")
        if code in known and code not in out:
            out.append(code)
    return out


def annotate_units(node, reverse, log, known=None):
    """Pose la légende du sous-arbre sur `node` ; renvoie {kind: [codes]}."""
    acc = {k: _own_codes(node, k, reverse[k]) for k in ("equipment", "personnel")}
    for child in node.get("subUnits", []) or []:
        sub = annotate_units(child, reverse, log, known)
        for k in acc:
            for c in sub[k]:
                if c not in acc[k]:
                    acc[k].append(c)
    if (acc["equipment"] or acc["personnel"]) and "name" in node:
        eq = [(c, reverse["equipment"][c]) for c in acc["equipment"]]
        pe = [(c, reverse["personnel"][c]) for c in acc["personnel"]]
        lg.set_legend(node, eq, pe, known_codes=known)
        log.setdefault("legends", []).append((node.get("name", "?"), eq + pe))
    return acc


def annotate_all(orbat, reverse, log):
    known = lg.catalog_codes(orbat)
    for side in orbat.get("sides", []) or []:
        roots = list(side.get("units", []) or []) + list(side.get("groups", []) or [])
        for root in roots:
            annotate_units(root, reverse, log, known)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file")
    parser.add_argument("--output", help="Fichier de sortie (par défaut : écrase orbat_file)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    orbat = ol.load(args.orbat_file)

    warnings = []
    reverse_map = build_reverse_map(orbat, warnings)

    if warnings:
        print(f"⚠️  {len(warnings)} code(s) de catalogue sans nom réel identifiable dans leur description "
              f"(ignorés, à corriger dans le catalogue) :", file=sys.stderr)
        for code in warnings:
            print(f"  {code!r}", file=sys.stderr)

    log = {}
    annotate_all(orbat, reverse_map, log)

    if log.get("legends"):
        print(f"{len(log['legends'])} échelon(s) annoté(s) avec une légende :")
        for name, legend in log["legends"]:
            print(f"  {name} -> " + ", ".join(f"{c} : {l}" for c, l in legend))
    else:
        print("Aucun échelon annoté (aucun code résolu ou aucune unité nommée).")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    ol.save(orbat, out_path)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
