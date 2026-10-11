#!/usr/bin/env python3
"""
group_units.py — Regroupe des unités-soeurs existantes d'un ORBAT JSON
(format orbat-mapper.app) sous de nouveaux échelons intermédiaires.

Cas d'usage typique : Florian a 12 compagnies à plat sous un régiment et veut
les répartir en 3 bataillons de 4 compagnies chacun. Ce script crée les 3
unités "bataillon" (avec un `sidc` cohérent, échelon inférée de l'entité des
compagnies groupées) et y déplace les compagnies correspondantes, à la place
qu'elles occupaient dans le régiment.

Usage:
    python3 group_units.py <orbat.json> <grouping_spec.json>
        [--output OUT.json] [--dry-run]

grouping_spec.json (une entrée par regroupement à effectuer, exécutés dans
l'ordre) :
[
  {
    "parent_name": "114th Cadian Regiment — Mechanised",
    "select_regex": "^\\d+(st|nd|rd|th) Mechanised Infantry Company$",
    "group_size": 4,
    "new_echelon": "bataillon",
    "new_names": ["1st Battalion", "2nd Battalion", "3rd Battalion"]
  }
]

- `parent_name` : nom (ou sous-chaîne) de l'unité/Group dont on regroupe des
  enfants directs. Recherché dans tout l'arbre, premier match retenu.
- `select_regex` : motif (re.search) appliqué au `name` des enfants directs de
  `parent_name` pour sélectionner ceux à regrouper — dans leur ordre d'origine.
- `group_size` : nombre d'unités sélectionnées par nouveau groupe (le dernier
  paquet peut être plus petit — un avertissement est émis si `group_size` ne
  divise pas le total).
- `new_echelon` : nom d'échelon pour les nouvelles unités (voir table du
  script condense_orbat.py : escouade, section, peloton, compagnie, bataillon,
  regiment, brigade, division...).
- `new_names` (optionnel) : noms explicites pour chaque nouveau groupe, dans
  l'ordre. Si absent ou trop court, génère `"{n}e {new_echelon capitalisé}"`
  (ex. "1e Bataillon") pour les groupes restants.
- `entity` (optionnel) : code entité à 6 chiffres pour le `sidc` des nouvelles
  unités. Par défaut, hérité de l'entité (position 11-16) du premier enfant
  sélectionné de chaque groupe (suppose une composition homogène, cas
  standard). Passer une valeur explicite pour un groupe hétérogène.
"""
import json
import re
import argparse
import random
import string

ECHELON = {
    "equipe": "11", "team": "11", "crew": "11",
    "escouade": "12", "groupe": "12", "squad": "12",
    "section_us": "13",
    "section": "13", "sec": "13",   # SEC = grosse escouade, elem. terminal (2026-08-09)
    "peloton": "14", "platoon": "14", "plt": "14",   # PLT = conteneur, > SEC
    "compagnie": "15", "company": "15", "batterie": "15", "escadron": "15",
    "bataillon": "16", "battalion": "16",
    "regiment": "17", "groupement": "17",
    "brigade": "18",
    "division": "21",
    "corps": "22",
    "armee": "23", "armée": "23",
    "groupe_armees": "24",
    "commandement": "26",
}

ORDINALS_FR = ["1er", "2e", "3e", "4e", "5e", "6e", "7e", "8e", "9e", "10e",
               "11e", "12e", "13e", "14e", "15e", "16e", "17e", "18e", "19e", "20e"]


def gen_id(n=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


def resolve_echelon(name):
    key = name.strip().lower().replace(" ", "_").replace("é", "e")
    if key in ECHELON:
        return ECHELON[key]
    if key.isdigit() and len(key) == 2:
        return key
    raise ValueError(f"Échelon inconnu : {name!r}")


def find_node_by_name(node, name_substr, path="root"):
    if name_substr.lower() in (node.get("name") or "").lower():
        return node
    for child in node.get("subUnits", []) or []:
        r = find_node_by_name(child, name_substr)
        if r is not None:
            return r
    return None


def find_parent_anywhere(orbat, name_substr):
    for side in orbat.get("sides", []) or []:
        for unit in side.get("units", []) or []:
            r = find_node_by_name(unit, name_substr)
            if r is not None:
                return r
        for group in side.get("groups", []) or []:
            r = find_node_by_name(group, name_substr)
            if r is not None:
                return r
    return None


def entity_of(unit):
    sidc = unit.get("sidc")
    if sidc and len(sidc) >= 16:
        return sidc[10:16]
    return "000000"


def build_sidc(echelon_code, entity, identity="3"):
    # pos: 1-2 version(10) 3 contexte(0) 4 identite 5-6 symbolset(10) 7 statut(0)
    # 8 hq/tf/d(0) 9-10 echelon 11-16 entite 17-18 mod1(00) 19-20 mod2(00)
    sidc = f"10" + "0" + identity + "10" + "0" + "0" + echelon_code + entity + "00" + "00"
    assert len(sidc) == 20, f"sidc mal formé : {sidc!r} ({len(sidc)} car.)"
    return sidc


def make_group_unit(name, echelon_code, entity, subunits):
    return {
        "id": gen_id(),
        "name": name,
        "sidc": build_sidc(echelon_code, entity),
        "subUnits": subunits,
        "symbolOptions": {},
        "state": [],
    }


def apply_grouping(orbat, spec, log):
    parent = find_parent_anywhere(orbat, spec["parent_name"])
    if parent is None:
        log.setdefault("erreurs", []).append(f"Parent introuvable : {spec['parent_name']!r}")
        return

    pattern = re.compile(spec["select_regex"])
    children = parent.get("subUnits", []) or []

    matched_idx = [i for i, c in enumerate(children) if pattern.search(c.get("name") or "")]
    if not matched_idx:
        log.setdefault("erreurs", []).append(
            f"Aucun enfant de {spec['parent_name']!r} ne correspond à {spec['select_regex']!r}"
        )
        return

    matched = [children[i] for i in matched_idx]
    group_size = spec["group_size"]
    if len(matched) % group_size != 0:
        log.setdefault("avertissements", []).append(
            f"{len(matched)} unité(s) sélectionnée(s) non multiple de group_size={group_size} "
            f"(dernier groupe incomplet)"
        )

    echelon_code = resolve_echelon(spec["new_echelon"])
    new_names = spec.get("new_names", [])

    chunks = [matched[i:i + group_size] for i in range(0, len(matched), group_size)]
    new_units = []
    for i, chunk in enumerate(chunks):
        if i < len(new_names):
            name = new_names[i]
        else:
            ordinal = ORDINALS_FR[i] if i < len(ORDINALS_FR) else f"{i+1}e"
            name = f"{ordinal} {spec['new_echelon'].capitalize()}"
        entity = spec.get("entity") or entity_of(chunk[0])
        new_unit = make_group_unit(name, echelon_code, entity, chunk)
        new_units.append(new_unit)
        log.setdefault("groupes_crees", []).append(
            (name, [c.get("name", "?") for c in chunk])
        )

    # reconstruire subUnits du parent : remplacer le premier index matché par
    # les nouveaux groupes (dans l'ordre), retirer les autres index matchés,
    # laisser les enfants non matchés inchangés à leur place relative.
    first_matched = matched_idx[0]
    matched_set = set(matched_idx)
    new_subunits = []
    inserted = False
    for i, c in enumerate(children):
        if i in matched_set:
            if not inserted:
                new_subunits.extend(new_units)
                inserted = True
            continue
        new_subunits.append(c)
    parent["subUnits"] = new_subunits


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file")
    parser.add_argument("grouping_spec_file")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.orbat_file, "r", encoding="utf-8") as f:
        orbat = json.load(f)

    with open(args.grouping_spec_file, "r", encoding="utf-8") as f:
        specs = json.load(f)

    log = {}
    for spec in specs:
        apply_grouping(orbat, spec, log)

    for err in log.get("erreurs", []):
        print(f"❌ {err}")
    for warn in log.get("avertissements", []):
        print(f"⚠️  {warn}")

    groupes = log.get("groupes_crees", [])
    print(f"\n{len(groupes)} nouveau(x) groupe(s) créé(s) :")
    for name, members in groupes:
        print(f"  {name} <- {', '.join(members)}")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(orbat, f, ensure_ascii=False, indent=2)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
