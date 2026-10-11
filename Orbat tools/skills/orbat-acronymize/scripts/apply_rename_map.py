#!/usr/bin/env python3
"""
apply_rename_map.py — Applique un mapping {ancien_nom: nouveau_code} à un ORBAT
JSON (format orbat-mapper.app) :

1. Renomme les entrées des catalogues racine `equipment` et `personnel`,
   conserve l'ancien nom dans leur `description`, et propage le changement à
   toutes les références (`equipment[].name` / `personnel[].name`) dans
   l'arbre d'unités (récursif, `subUnits`).

2. Annote la `description` de chaque échelon (Group/Unit) avec une légende
   des acronymes utilisés dans tout son sous-arbre, ex. :
       Équipement : MBT = Leclerc · VTT = VAB
   pour ne jamais perdre le nom réel derrière un code.

3. Quand un échelon ne porte, EN PROPRE, qu'un seul type de matériel/personnel
   (composition non mixte), enrichit son titre (`name`) avec le nom réel du
   véhicule/personnel, ex. "Escadron" -> "Escadron de VAB". N'agit que sur les
   échelons qui portent directement du matériel (feuilles typiquement), jamais
   sur un échelon mixte ou purement organisationnel.

Usage:
    python apply_rename_map.py <orbat.json> <mapping.json> [--output OUT.json]
                                [--dry-run] [--no-legend] [--no-titles]

mapping.json : {"Nom original 1": "CODE-V4-1", "Nom original 2": "CODE-V4-2", ...}

Par défaut, écrase le fichier d'entrée (pas de copie séparée), applique la
légende de description ET l'enrichissement de titre. Idempotent : peut être
relancé sans dupliquer légendes ou suffixes de titre déjà appliqués.
"""
import json
import argparse

LEGEND_MARKER = "Équipement :"
VOWELS = "aàâeéèêiîïoôuùûhAÀÂEÉÈÊIÎÏOÔUÙÛH"


def rename_catalog(catalog, mapping, changes):
    """Renomme les entrées d'un catalogue racine (equipment ou personnel)."""
    for entry in catalog:
        old_name = entry.get("name")
        if old_name in mapping:
            new_name = mapping[old_name]
            if new_name == old_name:
                continue
            old_desc = entry.get("description", "") or ""
            if old_name not in old_desc:
                entry["description"] = (old_name + (" — " + old_desc if old_desc else "")).strip(" —")
            entry["name"] = new_name
            changes.append((old_name, new_name))


def walk_units(units, mapping, changes):
    """Parcourt récursivement l'arbre d'unités et renomme les références
    equipment[].name / personnel[].name selon le mapping."""
    for unit in units:
        for key in ("equipment", "personnel"):
            for item in unit.get(key, []) or []:
                if item.get("name") in mapping:
                    item["name"] = mapping[item["name"]]
        if "subUnits" in unit:
            walk_units(unit["subUnits"], mapping, changes)


def walk_sides(sides, mapping, changes):
    for side in sides:
        if "units" in side:
            walk_units(side["units"], mapping, changes)
        for group in side.get("groups", []) or []:
            if "subUnits" in group:
                walk_units(group["subUnits"], mapping, changes)


def _own_acronyms(node, reverse_map):
    """Liste ordonnée (sans doublon) des acronymes portés EN PROPRE par ce
    noeud (equipment + personnel), en excluant tout ce qui n'est pas dans
    reverse_map (= pas issu du renommage de cette passe)."""
    own = []
    for key in ("equipment", "personnel"):
        for item in node.get(key, []) or []:
            acr = item.get("name")
            if acr in reverse_map and acr not in own:
                own.append(acr)
    return own


def _strip_old_legend(desc):
    """Retire un bloc de légende déjà présent (marqueur + puces qui suivent),
    pour permettre de relancer le script sans dupliquer la légende."""
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
    """Parcourt récursivement, ajoute la légende de description à chaque
    noeud nommé dont le sous-arbre contient au moins un acronyme, et
    enrichit le titre des noeuds à composition non mixte. Retourne la liste
    ordonnée des acronymes présents dans le sous-arbre de `node`."""
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


def _own_equipment_acronyms(node, reverse_map):
    """Comme _own_acronyms mais restreint à `equipment` (véhicules/matériel) —
    le personnel est exclu de l'enrichissement de titre car il double
    généralement déjà l'information (ex. "Compagnie d'Infanterie" portant du
    personnel "Fantassin" serait renommée en un titre tautologique)."""
    own = []
    for item in node.get("equipment", []) or []:
        acr = item.get("name")
        if acr in reverse_map and acr not in own:
            own.append(acr)
    return own


def enrich_titles(node, reverse_map, log):
    """Si ce noeud porte EN PROPRE un seul type de matériel (véhicule, pas de
    mélange, personnel exclu), enrichit son `name` avec le nom réel du
    véhicule, sauf s'il y est déjà. Descend récursivement dans subUnits."""
    own = _own_equipment_acronyms(node, reverse_map)
    if len(own) == 1 and "name" in node:
        acr = own[0]
        real_name = reverse_map[acr]
        current_name = node["name"]
        if real_name.lower() not in current_name.lower():
            prep = "d'" if real_name[0] in VOWELS else "de "
            node["name"] = f"{current_name} {prep}{real_name}"
            log.setdefault("titles", []).append((current_name, node["name"]))
    for child in node.get("subUnits", []) or []:
        enrich_titles(child, reverse_map, log)


def annotate_all(orbat, reverse_map, log, do_legend, do_titles):
    for side in orbat.get("sides", []) or []:
        roots = list(side.get("units", []) or []) + list(side.get("groups", []) or [])
        for root in roots:
            if do_legend:
                annotate_units(root, reverse_map, log)
            if do_titles:
                enrich_titles(root, reverse_map, log)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file", help="Fichier ORBAT JSON à modifier")
    parser.add_argument("mapping_file", help="Fichier JSON {ancien_nom: nouveau_code}")
    parser.add_argument("--output", help="Fichier de sortie (par défaut : écrase orbat_file)")
    parser.add_argument("--dry-run", action="store_true", help="N'écrit rien, affiche seulement le résumé des changements")
    parser.add_argument("--no-legend", action="store_true", help="Ne pas ajouter la légende d'équipement dans les descriptions d'échelon")
    parser.add_argument("--no-titles", action="store_true", help="Ne pas enrichir les titres d'échelon à composition unique")
    args = parser.parse_args()

    with open(args.orbat_file, "r", encoding="utf-8") as f:
        orbat = json.load(f)

    with open(args.mapping_file, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    reverse_map = {v: k for k, v in mapping.items()}

    changes = []
    if "equipment" in orbat:
        rename_catalog(orbat["equipment"], mapping, changes)
    if "personnel" in orbat:
        rename_catalog(orbat["personnel"], mapping, changes)
    if "sides" in orbat:
        walk_sides(orbat["sides"], mapping, changes)

    print(f"{len(changes)} entrée(s) de catalogue renommée(s) :")
    for old, new in changes:
        print(f"  {old!r} -> {new!r}")

    unmatched = [k for k in mapping if k not in [c[0] for c in changes]]
    if unmatched:
        print(f"\n⚠️  {len(unmatched)} entrée(s) du mapping non trouvée(s) dans le catalogue (vérifier l'orthographe) :")
        for k in unmatched:
            print(f"  {k!r}")

    log = {}
    if "sides" in orbat:
        annotate_all(orbat, reverse_map, log, do_legend=not args.no_legend, do_titles=not args.no_titles)

    if log.get("legends"):
        print(f"\n{len(log['legends'])} échelon(s) annoté(s) avec une légende d'équipement :")
        for name, legend in log["legends"]:
            print(f"  {name} -> {legend}")

    if log.get("titles"):
        print(f"\n{len(log['titles'])} titre(s) d'échelon enrichi(s) :")
        for old, new in log["titles"]:
            print(f"  {old!r} -> {new!r}")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(orbat, f, ensure_ascii=False, indent=2)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
