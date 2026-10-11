#!/usr/bin/env python3
"""
condense_orbat.py — Réduit la taille d'un ORBAT JSON (format orbat-mapper.app)
en deux passes :

1. CONDENSATION D'ÉCHELON : fusionne tout échelon strictement inférieur au
   niveau cible (par défaut peloton) dans son ancêtre le plus proche qui est
   au niveau cible ou au-dessus. L'échelon d'une unité est lu sur son `sidc`
   (positions 9-10, voir skill orbat-json/references/sidc.md). Les échelons fusionnés
   disparaissent de l'arbre ; leurs equipment/personnel/supplies sont sommés
   (par nom) dans l'ancêtre retenu. Leur TIMELINE (state[]) n'est pas perdue :
   chaque variation de quantité (update/diff) est transférée à l'ancêtre sous
   forme de `diff` au même instant — les totaux à toute date restent exacts
   (aggregate.py --at). Les positions/statuts propres aux unités fusionnées,
   eux, ne sont pas représentables dans l'ancêtre : ils sont comptés et
   signalés. Seul un sidc dont les positions 9-10 commencent par 1 ou 2 est lu
   comme un échelon (3x/4x/5x = mobilité d'un matériel, cf. sidc.md).

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
      (la "description" est OBLIGATOIRE : elle devient l'entrée de catalogue,
       qui doit nommer l'élément réel — naming.md Règle 5)
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
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbat_lib as ol

# Table des échelons : orbat_lib.ECHELON (unique). Gardé pour compatibilité.
ECHELON_NAMES = ol.ECHELON


def echelon_of(node):
    """Code échelon (2 chiffres) d'un noeud, ou None si son sidc n'en porte pas
    (Group de tête sans sidc, ou pos 9-10 = mobilité 3x/4x/5x d'un matériel).
    « 00 » (échelon non renseigné : élément isolé, véhicule suivi à part,
    unité ODIN d'échelon inconnu) reste fusionnable au plus bas rang, comme
    avant la 0.25.0."""
    sidc = str(node.get("sidc") or "")
    if len(sidc) == 20 and sidc.isdigit() and sidc[8:10] == "00":
        return "00"
    return ol.echelon_of(node)


def echelon_rank(code):
    """Rang numérique comparable (les codes sont déjà croissants avec la
    hiérarchie, cf. sidc.md)."""
    try:
        return int(code)
    except (TypeError, ValueError):
        return -1


def resolve_target(target_str):
    return ol.echelon_code(target_str)


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


def _states_to_diffs(node):
    """Voir orbat_lib.states_to_diffs (update absolus -> diff, avant fusion)."""
    ol.states_to_diffs(node)


def _transfer_timeline(node, child, log):
    """Transfère à `node` les variations de quantités de tout le sous-arbre de
    `child` (sous forme de diff au même instant). Compte ce qui est perdu.
    Un Group de tête (sans sidc) ne reçoit pas de timeline — format non
    garanti à l'import : les variations sont alors signalées comme perdues."""
    if not node.get("sidc"):
        n = sum(1 for u in ol.subtree_units(child) for k in ol.RESOURCE_KINDS
                for _, d in ol.resource_deltas(u, k) if d)
        if n:
            log.setdefault("timeline_vers_group", []).append((child.get("name", "?"), node.get("name", "?"), n))
        return
    moved, dropped = 0, 0
    for u in ol.subtree_units(child):
        for st in u.get("state", []) or []:
            if any(k in st for k in ("location", "status", "sidc", "title")):
                dropped += 1
        for kind in ol.RESOURCE_KINDS:
            for st, deltas in ol.resource_deltas(u, kind):
                if not deltas:
                    continue
                t = st.get("t")
                key = ol.parse_time(t)
                target = next((s for s in node.setdefault("state", [])
                               if ol.parse_time(s.get("t")) == key), None)
                if target is None:
                    target = {"id": ol.gen_id(), "t": t}
                    node["state"].append(target)
                lst = target.setdefault("diff", {}).setdefault(kind, [])
                for n, d in deltas.items():
                    lst.append({"name": n, "onHand": d})
                target["diff"][kind] = [{"name": it["name"], "onHand": it["count"]}
                                        for it in ol.merge_items(
                                            [{"name": i["name"], "count": i["onHand"]} for i in lst])]
                moved += 1
    if node.get("state"):
        node["state"] = ol.sorted_states(node)
    if moved:
        log.setdefault("timelines_transferees", []).append((child.get("name", "?"), node.get("name", "?"), moved))
    if dropped:
        log.setdefault("etats_non_transferables", []).append((child.get("name", "?"), dropped))


def condense(node, target_rank, log):
    """Fusionne récursivement les sous-arbres d'échelon < target_rank dans
    `node`. Modifie node['subUnits'] en place."""
    new_subunits = []
    converted = False
    for child in node.get("subUnits", []) or []:
        child_ech = echelon_of(child)
        child_rank = echelon_rank(child_ech) if child_ech is not None else 9999
        if child_ech is not None and child_rank < target_rank:
            if not converted:
                _states_to_diffs(node)   # AVANT de toucher aux quantités de base
                converted = True
            totals = {}
            collect_all_quantities(child, totals)
            merge_totals_into(node, totals)
            _transfer_timeline(node, child, log)
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
        node["personnel"] = ol.merge_items(node["personnel"])   # jamais deux lignes du même code
    if "equipment" in node:
        node["equipment"] = elementize_counts(node["equipment"], sizes_config, "equipment", new_catalog_entries, log)
        node["equipment"] = ol.merge_items(node["equipment"])
    touched = {k for k, v in sizes_config.items() if not k.startswith("_")}
    for st in node.get("state", []) or []:
        for blk in ("update", "diff"):
            for kind in ("equipment", "personnel"):
                if any(i.get("name") in touched for i in (st.get(blk) or {}).get(kind, []) or []):
                    log.setdefault("timeline_non_elementarisee", set()).add(node.get("name", "?"))
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

    orbat = ol.load(args.orbat_file)

    with open(args.squad_sizes_file, "r", encoding="utf-8") as f:
        sizes_config = json.load(f)

    if not args.no_elementize:
        manquantes = [el.get("code", "?") for k, cfg in sizes_config.items() if not k.startswith("_")
                      for el in cfg.get("elements", []) if not (el.get("description") or "").strip()]
        cg = sizes_config.get("_command_group")
        if cg and not (cg.get("description") or "").strip():
            manquantes.append(cg.get("result_code", "_command_group"))
        if manquantes:
            sys.exit("❌ Description manquante dans squad_sizes.json pour : " + ", ".join(manquantes)
                     + "\n   Elle devient l'entrée de catalogue et doit nommer l'élément réel "
                       "(naming.md Règle 5). Rien n'a été écrit.")

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
        tl = log.get("timelines_transferees", [])
        if tl:
            print(f"\n{sum(n for *_, n in tl)} variation(s) de quantité de timeline transférée(s) "
                  f"en diff vers l'ancêtre ({len(tl)} fusion(s) concernée(s)).")
        tg = log.get("timeline_vers_group", [])
        if tg:
            print(f"\n⚠️  {sum(n for *_, n in tg)} variation(s) de quantité NON transférée(s) : l'ancêtre est "
                  "un Group de tête (sans sidc), qui ne porte pas de timeline. Les quantités de base "
                  "sont justes, pas l'historique :")
            for c, g, n in tg[:30]:
                print(f"  {c} -> {g} : {n}")
        lost = log.get("etats_non_transferables", [])
        if lost:
            print(f"\n⚠️  {sum(n for _, n in lost)} entrée(s) de timeline portant position/statut/titre/"
                  "symbole sur des unités fusionnées : non représentables dans l'ancêtre, perdues :")
            for name, n in lost[:30]:
                print(f"  {name} : {n} entrée(s)")

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
        ne = sorted(log.get("timeline_non_elementarisee", []))
        if ne:
            print(f"\n⚠️  {len(ne)} unité(s) dont la timeline compte encore en têtes un code "
                  "élémentarisé (les deltas de state[] ne sont pas convertis en éléments) :")
            for name in ne[:30]:
                print(f"  {name}")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    ol.save(orbat, out_path)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
