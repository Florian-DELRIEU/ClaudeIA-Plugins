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
code, un bloc :
    Équipement :
    * CODE = Nom réel
    * ...
(même logique/anti-duplication que apply_rename_map.py — idempotent).

Usage:
    python3 add_legends.py <orbat.json> [--output OUT.json] [--dry-run]

Par défaut, écrase le fichier d'entrée.
"""
import json
import argparse
import sys

LEGEND_MARKER = "Équipement :"


def extract_real_name(description):
    """Extrait le nom réel en tête de description (avant ' — ' si présent)."""
    if not description:
        return None
    desc = description.strip()
    for sep in (" — ", " - "):
        if sep in desc:
            return desc.split(sep, 1)[0].strip()
    return desc


def build_reverse_map(orbat, warnings):
    reverse_map = {}
    for cat_key in ("equipment", "personnel"):
        for entry in orbat.get(cat_key, []) or []:
            code = entry.get("name")
            real_name = extract_real_name(entry.get("description"))
            if not real_name:
                warnings.append(code)
                continue
            reverse_map[code] = real_name
    return reverse_map


def _own_acronyms(node, reverse_map):
    own = []
    for key in ("equipment", "personnel"):
        for item in node.get(key, []) or []:
            acr = item.get("name")
            if acr in reverse_map and acr not in own:
                own.append(acr)
    return own


def _strip_old_legend(desc):
    lines = desc.split("\n")
    try:
        idx = next(i for i, l in enumerate(lines) if l.strip() == LEGEND_MARKER.strip())
    except StopIteration:
        return desc
    end = idx + 1
    while end < len(lines) and lines[end].strip().startswith("* "):
        end += 1
    return "\n".join(lines[:idx] + lines[end:]).strip()


def annotate_units(node, reverse_map, log):
    own = _own_acronyms(node, reverse_map)

    child_acronyms = []
    for child in node.get("subUnits", []) or []:
        for a in annotate_units(child, reverse_map, log):
            if a not in child_acronyms:
                child_acronyms.append(a)

    combined = list(own)
    for a in child_acronyms:
        if a not in combined:
            combined.append(a)

    if combined and "name" in node:
        legend_lines = [f"* {a} = {reverse_map[a]}" for a in combined]
        desc = _strip_old_legend(node.get("description", "") or "")
        legend_block = LEGEND_MARKER + "\n" + "\n".join(legend_lines)
        node["description"] = (desc + ("\n\n" if desc else "") + legend_block).strip()
        log.setdefault("legends", []).append((node.get("name", "?"), legend_lines))

    return combined


def annotate_all(orbat, reverse_map, log):
    for side in orbat.get("sides", []) or []:
        roots = list(side.get("units", []) or []) + list(side.get("groups", []) or [])
        for root in roots:
            annotate_units(root, reverse_map, log)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file")
    parser.add_argument("--output", help="Fichier de sortie (par défaut : écrase orbat_file)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.orbat_file, "r", encoding="utf-8") as f:
        orbat = json.load(f)

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
            print(f"  {name} -> {legend}")
    else:
        print("Aucun échelon annoté (aucun code résolu ou aucune unité nommée).")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(orbat, f, ensure_ascii=False, indent=2)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
