#!/usr/bin/env python3
"""
validate.py — vérifie qu'un fichier ORBAT est structurellement sain et
réimportable dans orbat-mapper.app.

Contrôles :
  - clés top-level présentes (type, version, sides, equipment, personnel, settings...)
  - chaque unité possède id, name, sidc
  - sidc = exactement 20 chiffres
  - ids uniques sur tout l'arbre
  - chaque code equipment/personnel référencé existe dans le catalogue (sinon WARN)
  - unicité de chaque code dans la liste equipment/personnel/supplies d'une
    unité (détecte les renommages en masse non fusionnés)
  - unicité de chaque code dans les catalogues racine

Usage : python validate.py ORBAT.json
Code de sortie 0 si aucune ERREUR (les WARN ne bloquent pas).
"""
import sys
import os
import re
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orbat_lib import load, iter_units, catalog_map

TOP_KEYS = ["type", "version", "name", "sides", "equipment",
            "personnel", "settings", "symbologyStandard"]
SIDC_RE = re.compile(r"^\d{20}$")


def main():
    orbat = load(sys.argv[1])
    errors, warns = [], []

    for k in TOP_KEYS:
        if k not in orbat:
            errors.append(f"clé top-level manquante : {k}")

    eq_cat = set(catalog_map(orbat, "equipment"))
    pe_cat = set(catalog_map(orbat, "personnel"))
    su_cat = set(catalog_map(orbat, "supplies"))  # supplyCategories

    # Unicité dans les catalogues racine. catalog_map() construit un dict :
    # une entrée dupliquée écrase silencieusement la précédente, et sa
    # description disparaît sans aucun signal.
    for kind, key in (("equipment", "equipment"), ("personnel", "personnel"),
                      ("supplies", "supplyCategories")):
        noms = [e.get("name") for e in orbat.get(key, []) or []]
        for code, k in Counter(noms).items():
            if k > 1:
                errors.append(
                    f"catalogue racine {kind} : {code!r} déclaré {k} fois — "
                    "catalog_map() n'en garde qu'un, la description des autres "
                    "est perdue")

    seen_ids = {}
    n = 0
    for u, path in iter_units(orbat, with_path=True):
        n += 1
        loc = " > ".join(path + [u.get("name", "?")])
        uid = u.get("id")
        if not uid:
            errors.append(f"[{loc}] id manquant")
        elif uid in seen_ids:
            errors.append(f"[{loc}] id dupliqué : {uid} (déjà sur « {seen_ids[uid]} »)")
        else:
            seen_ids[uid] = u.get("name", "?")
        if not u.get("name"):
            warns.append(f"[{loc}] name vide")
        sidc = u.get("sidc")
        if not sidc:
            errors.append(
                f"[{loc}] sidc manquant — CASSE L'IMPORT au-delà de ce niveau "
                "si ce nœud est imbriqué dans des subUnits (piège confirmé : "
                "orbat-mapper.app arrête la récursion sur un nœud sans sidc). "
                "Probable make_group() utilisé à la place de make_org_unit()/"
                "make_unit() pour un niveau intermédiaire — voir references/format.md."
            )
        elif not SIDC_RE.match(str(sidc)):
            errors.append(f"[{loc}] sidc invalide (doit être 20 chiffres) : {sidc!r}")
        for item in u.get("equipment", []) or []:
            if item.get("name") not in eq_cat:
                warns.append(f"[{loc}] equipment hors catalogue : {item.get('name')!r}")
        for item in u.get("personnel", []) or []:
            if item.get("name") not in pe_cat:
                warns.append(f"[{loc}] personnel hors catalogue : {item.get('name')!r}")
        for item in u.get("supplies", []) or []:
            if item.get("name") not in su_cat:
                warns.append(f"[{loc}] supply hors supplyCategories : {item.get('name')!r}")
        # Unicité des codes DANS une même liste. Un renommage en masse
        # (orbat-acronymize, condense_orbat, correction de vocabulaire) fait
        # converger plusieurs codes vers un seul SANS fusionner les lignes.
        # aggregate() sommant par nom, les totaux restent justes et l'anomalie
        # est invisible partout ailleurs.
        for kind in ("equipment", "personnel", "supplies"):
            noms = [i.get("name") for i in u.get(kind, []) or []]
            for code, k in Counter(noms).items():
                if k > 1:
                    errors.append(
                        f"[{loc}] {code!r} apparaît {k} fois dans {kind} — "
                        "lignes à fusionner en une seule à somme cumulée "
                        "(typiquement un renommage de code non fusionné)")
        for st in u.get("state", []) or []:
            if not st.get("t"):
                errors.append(f"[{loc}] entrée state sans horodatage `t`")

    print(f"Unités analysées : {n}")
    print(f"ERREURS : {len(errors)} | AVERTISSEMENTS : {len(warns)}\n")
    for e in errors:
        print("  ERREUR  ", e)
    for w in warns[:40]:
        print("  WARN    ", w)
    if len(warns) > 40:
        print(f"  ... (+{len(warns) - 40} autres warnings)")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
