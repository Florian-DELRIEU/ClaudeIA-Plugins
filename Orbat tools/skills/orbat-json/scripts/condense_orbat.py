#!/usr/bin/env python3
"""
condense_orbat.py — Réduit la taille d'un ORBAT JSON (format orbat-mapper.app)
en deux passes :

1. CONDENSATION D'ÉCHELON : fusionne tout échelon strictement inférieur au
   niveau cible (par défaut peloton) dans son ancêtre le plus proche qui est
   au niveau cible ou au-dessus. L'échelon d'une unité est lu sur son `sidc`
   (positions 9-10, voir skill orbat-json/references/sidc.md). Les échelons fusionnés
   disparaissent de l'arbre ; leurs equipment/personnel/supplies sont sommés
   (par nom) dans l'ancêtre retenu.

2. ÉLÉMENTARISATION DU PERSONNEL : convertit les effectifs bruts (comptés en
   têtes) en comptage par élément (escouade/groupe), selon une table de
   conversion fournie (ex. Escouade de Guardsmen = 10, Groupe = 5). Décompose
   chaque effectif en préférant les plus gros éléments d'abord ; tout reliquat
   qui ne rentre dans aucun palier reste en comptage brut sous le code
   d'origine, avec un avertissement.

Usage:
    python3 condense_orbat.py <orbat.json> <squad_sizes.json>
        [--target peloton|compagnie|section|escouade|bataillon|...]
        [--output OUT.json] [--dry-run] [--no-condense] [--no-elementize]

squad_sizes.json :
{
  "I": {
    "elements": [
      {"code": "SQ-INF", "size": 10, "description": "Escouade de Guardsmen (10 hommes)"},
      {"code": "GRP-INF", "size": 5,  "description": "Groupe/demi-escouade de Guardsmen (5 hommes)"}
    ]
  }
}

Par défaut, écrase le fichier d'entrée. Idempotent sur la condensation (un
échelon déjà au niveau cible ou au-dessus n'est jamais refusionné) ; NON
idempotent sur l'élémentarisation si on la relance sur un fichier déjà
élémentarisé (les codes SQ-INF/GRP-INF ne sont pas dans squad_sizes.json en
tant que clé de départ, donc ils ne seront pas re-décomposés — sûr par
construction tant que les codes d'éléments ne réapparaissent pas comme clé
racine du fichier de tailles).
"""
import json
import argparse

ECHELON_NAMES = {
    "equipe": "11", "crew": "11",
    "escouade": "12", "groupe": "12", "squad": "12",
    "section": "13", "sec": "13",   # SEC = grosse escouade, elem. terminal (2026-08-09)
    "peloton": "14", "platoon": "14", "plt": "14",   # PLT = conteneur, > SEC
    "compagnie": "15", "batterie": "15", "escadron": "15", "company": "15",
    "bataillon": "16", "battalion": "16",
    "regiment": "17", "groupement": "17",
    "brigade": "18",
    "division": "21",
    "corps": "22",
    "armee": "23", "armée": "23",
    "groupe_armees": "24",
    "commandement": "26",
}


def echelon_of(node):
    """Retourne le code échelon (str, 2 chiffres) d'un noeud, ou None si absent
    (ex. le Group de tête, qui n'a pas de sidc)."""
    sidc = node.get("sidc")
    if not sidc or len(sidc) < 10:
        return None
    return sidc[8:10]


def echelon_rank(code):
    """Rang numérique comparable (les codes sont déjà croissants avec la
    hiérarchie, cf. sidc.md)."""
    try:
        return int(code)
    except (TypeError, ValueError):
        return -1


def resolve_target(target_str):
    key = target_str.strip().lower().replace(" ", "_").replace("é", "e")
    if key in ECHELON_NAMES:
        return ECHELON_NAMES[key]
    if key.isdigit() and len(key) == 2:
        return key
    raise ValueError(f"Échelon cible inconnu : {target_str!r}")


def collect_all_quantities(node, totals):
    """Somme récursivement equipment/personnel/supplies de tout le sous-arbre
    de `node` (node compris) dans le dict `totals` (par clé 'equipment'/
    'personnel'/'supplies' -> {name: count})."""
    for key in ("equipment", "personnel", "supplies"):
        for item in node.get(key, []) or []:
            name = item.get("name")
            count = item.get("count", 0) or 0
            if name is None:
                continue
            totals.setdefault(key, {})
            totals[key][name] = totals[key].get(name, 0) + count
    for child in node.get("subUnits", []) or []:
        collect_all_quantities(child, totals)


def merge_totals_into(node, totals):
    for key, counts in totals.items():
        existing = {item["name"]: item for item in node.get(key, []) or []}
        for name, count in counts.items():
            if name in existing:
                existing[name]["count"] = existing[name].get("count", 0) + count
            else:
                existing[name] = {"name": name, "count": count}
        node[key] = list(existing.values())


def condense(node, target_rank, log):
    """Fusionne récursivement les sous-arbres d'échelon < target_rank dans
    `node`. Modifie node['subUnits'] en place."""
    new_subunits = []
    for child in node.get("subUnits", []) or []:
        child_ech = echelon_of(child)
        child_rank = echelon_rank(child_ech) if child_ech is not None else 9999
        if child_ech is not None and child_rank < target_rank:
            totals = {}
            collect_all_quantities(child, totals)
            merge_totals_into(node, totals)
            log.setdefault("fusions", []).append((child.get("name", "?"), node.get("name", "?")))
        else:
            condense(child, target_rank, log)
            new_subunits.append(child)
    node["subUnits"] = new_subunits


def condense_sides(orbat, target_rank, log):
    for side in orbat.get("sides", []) or []:
        for unit in side.get("units", []) or []:
            condense(unit, target_rank, log)
        for group in side.get("groups", []) or []:
            condense(group, target_rank, log)


def elementize_counts(items, sizes_config, catalog_name, new_catalog_entries, log):
    """Décompose en place la liste `items` (equipment ou personnel d'un
    noeud) selon sizes_config. Retourne la nouvelle liste."""
    result = []
    for item in items:
        name = item.get("name")
        count = item.get("count", 0) or 0
        if name not in sizes_config:
            result.append(item)
            continue
        remaining = count
        elements = sorted(sizes_config[name]["elements"], key=lambda e: -e["size"])
        produced = []
        for el in elements:
            n = remaining // el["size"]
            if n > 0:
                produced.append({"name": el["code"], "count": n})
                new_catalog_entries[el["code"]] = el.get("description", "")
                remaining -= n * el["size"]
        if remaining > 0:
            produced.append({"name": name, "count": remaining})
            log.setdefault("reliquats", []).append((name, remaining))
        if not produced:
            # count était 0 ou aucun élément ne correspond : garder tel quel
            produced = [item]
        result.extend(produced)
    return result


def merge_command_group(personnel_list, cg_cfg, new_catalog_entries, log):
    """Fusionne un officier isolé + son reliquat d'escorte (ex. OFF + un
    reliquat INF non élémentarisable) en un seul élément de commandement
    (ex. GRP-HQ), plutôt que de laisser deux entrées séparées (un officier
    compté à part et une escouade incomplète orpheline). Ne fait rien si
    l'officier n'a pas de reliquat associé (pas de groupe de commandement à
    former dans ce cas)."""
    officer_code = cg_cfg["officer_code"]
    result_code = cg_cfg["result_code"]
    combine_with = set(cg_cfg.get("combine_with", []))

    off_item = next((it for it in personnel_list if it.get("name") == officer_code), None)
    if off_item is None:
        return personnel_list
    reliquat_items = [it for it in personnel_list if it.get("name") in combine_with]
    if not reliquat_items:
        return personnel_list

    off_count = off_item.get("count", 0) or 0
    dropped_ids = {id(off_item), *(id(it) for it in reliquat_items)}
    new_list = [it for it in personnel_list if id(it) not in dropped_ids]
    new_list.append({"name": result_code, "count": off_count})
    new_catalog_entries[result_code] = cg_cfg.get("description", "")
    log.setdefault("groupes_commandement", []).append(
        (off_count, [(it.get("name"), it.get("count")) for it in reliquat_items])
    )
    return new_list


def elementize_tree(node, sizes_config, new_catalog_entries, log):
    if "personnel" in node:
        node["personnel"] = elementize_counts(node["personnel"], sizes_config, "personnel", new_catalog_entries, log)
        cg_cfg = sizes_config.get("_command_group")
        if cg_cfg:
            node["personnel"] = merge_command_group(node["personnel"], cg_cfg, new_catalog_entries, log)
    if "equipment" in node:
        node["equipment"] = elementize_counts(node["equipment"], sizes_config, "equipment", new_catalog_entries, log)
    for child in node.get("subUnits", []) or []:
        elementize_tree(child, sizes_config, new_catalog_entries, log)


def elementize_sides(orbat, sizes_config, log):
    new_catalog_entries = {}
    for side in orbat.get("sides", []) or []:
        for unit in side.get("units", []) or []:
            elementize_tree(unit, sizes_config, new_catalog_entries, log)
        for group in side.get("groups", []) or []:
            elementize_tree(group, sizes_config, new_catalog_entries, log)

    # Ajouter les nouvelles entrées au catalogue racine concerné. On ne sait
    # pas a priori si un code d'élément est equipment ou personnel : on le
    # cherche dans les deux catalogues existants et on l'ajoute au même que
    # sa clé d'origine (déterminé via sizes_config), par défaut personnel.
    personnel_keys = set(sizes_config.keys())
    existing_personnel = {e["name"] for e in orbat.get("personnel", [])}
    existing_equipment = {e["name"] for e in orbat.get("equipment", [])}
    for code, desc in new_catalog_entries.items():
        if code in existing_personnel or code in existing_equipment:
            continue
        # Heuristique : si un des noms sources est un code equipment connu,
        # ranger côté equipment, sinon personnel (cas majoritaire ici).
        target_catalog = "personnel"
        for src_name, cfg in sizes_config.items():
            if src_name.startswith("_"):
                continue  # clé réservée (ex. _command_group), pas une config d'élément
            if any(el["code"] == code for el in cfg.get("elements", [])):
                target_catalog = cfg.get("catalog", "personnel")
                break
        orbat.setdefault(target_catalog, [])
        orbat[target_catalog].append({"name": code, "description": desc})
        log.setdefault("nouveaux_codes_catalogue", []).append((code, target_catalog))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file")
    parser.add_argument("squad_sizes_file")
    parser.add_argument("--target", default="peloton", help="Échelon cible minimal (défaut: peloton)")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-condense", action="store_true", help="Ne pas fusionner les échelons, seulement élémentariser")
    parser.add_argument("--no-elementize", action="store_true", help="Ne pas élémentariser, seulement fusionner les échelons")
    args = parser.parse_args()

    with open(args.orbat_file, "r", encoding="utf-8") as f:
        orbat = json.load(f)

    with open(args.squad_sizes_file, "r", encoding="utf-8") as f:
        sizes_config = json.load(f)

    log = {}

    if not args.no_condense:
        target_rank = echelon_rank(resolve_target(args.target))
        condense_sides(orbat, target_rank, log)
        fusions = log.get("fusions", [])
        print(f"{len(fusions)} échelon(s) fusionné(s) dans leur ancêtre (cible : {args.target}) :")
        for child_name, parent_name in fusions[:30]:
            print(f"  {child_name!r} -> fusionné dans {parent_name!r}")
        if len(fusions) > 30:
            print(f"  ... et {len(fusions) - 30} de plus")

    if not args.no_elementize:
        elementize_sides(orbat, sizes_config, log)
        nouveaux = log.get("nouveaux_codes_catalogue", [])
        if nouveaux:
            print(f"\n{len(nouveaux)} nouveau(x) code(s) ajouté(s) au catalogue :")
            for code, cat in nouveaux:
                print(f"  {code} ({cat})")
        groupes_cmd = log.get("groupes_commandement", [])
        if groupes_cmd:
            print(f"\n{len(groupes_cmd)} groupe(s) de commandement formé(s) (officier + reliquat fusionnés) :")
            for off_count, absorbed in groupes_cmd:
                detail = ", ".join(f"{n}×{c}" for n, c in absorbed)
                print(f"  {off_count} officier(s) + {detail}")

        reliquats = log.get("reliquats", [])
        if reliquats:
            print(f"\n⚠️  {len(reliquats)} reliquat(s) détecté(s) pendant l'élémentarisation (certains peuvent avoir été "
                  "absorbés ensuite dans un groupe de commandement ci-dessus, le reste reste en comptage brut) :")
            for name, remaining in reliquats:
                print(f"  {name} : {remaining} restant(s)")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(orbat, f, ensure_ascii=False, indent=2)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
