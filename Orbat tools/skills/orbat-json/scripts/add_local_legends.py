#!/usr/bin/env python3
"""
add_local_legends.py — Annote chaque UNITÉ FEUILLE (pas le sous-arbre agrégé)
d'un sous-ensemble d'un ORBAT JSON (format orbat-mapper.app) avec une légende
"CODE = Nx Désignation réelle", en Équipement/Personnel séparés, à partir
d'une table de correspondance fournie — PAS déduite du catalogue racine.

Complète `add_legends.py` (Tâche 4 point 6 du skill), qui reste l'outil par
défaut quand un code catalogue a une désignation réelle univoque dans tout le
fichier. Utiliser add_local_legends.py à la place dès que l'une de ces
conditions s'applique (voir naming.md Règle 6) :

  1. Code partagé entre plusieurs camps du même fichier (le nom réel diffère
     selon le camp — ne peut pas vivre dans le catalogue racine, voir naming.md
     Règle 5 "piège codes partagés").
  2. Besoin du COMPTE par ligne (`* MBT = 4x T-55`), pas juste le nom.
  3. Besoin de sections Équipement / Personnel séparées plutôt qu'un seul bloc.
  4. Hétérogénéité locale à une unité précise (`* VTT-LMG = 1x BTR-60PB / 1x
     OT-64 SKOT`), impossible avec une désignation catalogue unique.

Établi sur l'ORBAT « Arma 3 - Altis » (juillet 2026, FIA — matériel hétéroclite
partagé avec France/AAF/CSAT sur plusieurs codes).

--- Différence clé avec add_legends.py ---
add_legends.py agrège tout le sous-arbre à chaque échelon (un bataillon liste
tous les codes de ses enfants). add_local_legends.py ne fait AUCUNE agrégation
remontante : seules les unités qui portent directement leur `equipment`/
`personnel` propre (les feuilles) reçoivent une légende. C'est volontaire — le
but est justement de distinguer des feuilles hétérogènes entre elles, une
agrégation remontante gommerait cette information.

--- Fichier de spec (JSON) ---
{
  "root": "<id ou nom de l'unité racine du sous-arbre à traiter>",
  "equipment_models": {"CODE": "Désignation réelle", ...},
  "personnel_models": {"CODE": "Désignation réelle", ...},
  "overrides": [
    {
      "path": ["Nom enfant niveau 1", "Nom enfant niveau 2", ..., "Nom unité cible"],
      "equipment": {"CODE": "Nx Désignation réelle spécifique à cette unité"},
      "personnel": {"CODE": "..."}
    }
  ],
  "clean_legacy_containers": true
}

`path` est relatif à `root` (liste des noms d'enfants successifs, root exclu).
`clean_legacy_containers` (optionnel, défaut false) : si vrai, tout nœud SANS
equipment/personnel propre dont la description existante ne contient QUE le
marqueur "Équipement :"/"Personnel :" et des lignes "* CODE = CODE" (aucune
autre prose) est nettoyé (description supprimée) — cas typique d'un texte
hérité d'une ancienne conversion acronyme→acronyme laissé sur un nœud
conteneur. Ne touche jamais un nœud qui a du contenu propre ou une description
qui contient autre chose que ce motif strict.

Usage:
    python3 add_local_legends.py <orbat.json> <spec.json> [--output OUT.json] [--dry-run]

Par défaut, écrase le fichier d'entrée.
"""
import json
import argparse
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import orbat_lib as ol

LEGACY_LINE_RE = re.compile(r"^\* [A-Za-z0-9\-/]+ = [A-Za-z0-9\-/]+$")


def build_desc(equip, pers, equip_models, pers_models, override):
    """equip/pers : listes [{'name':code,'count':n}, ...] telles que sur l'unité."""
    blocks = []
    if equip:
        lines = ["Équipement :"]
        for e in equip:
            code, n = e["name"], e["count"]
            ov = (override or {}).get("equipment", {})
            label = ov.get(code, f"{n}x {equip_models.get(code, '?')}")
            lines.append(f"* {code} = {label}")
        blocks.append("\n".join(lines))
    if pers:
        lines = ["Personnel :"]
        for p in pers:
            code, n = p["name"], p["count"]
            ov = (override or {}).get("personnel", {})
            label = ov.get(code, f"{n}x {pers_models.get(code, '?')}")
            lines.append(f"* {code} = {label}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) if blocks else None


def is_pure_legacy_text(desc):
    """Vrai si `desc` ne contient QUE des marqueurs de section et des lignes
    "* CODE = CODE" (motif d'une ancienne table acronyme->acronyme), rien
    d'autre. Conservateur : le moindre texte en plus => pas nettoyé."""
    if not desc:
        return False
    lines = [l.strip() for l in desc.split("\n") if l.strip()]
    if not lines:
        return False
    for l in lines:
        if l in ("Équipement :", "Personnel :"):
            continue
        if LEGACY_LINE_RE.match(l):
            continue
        return False
    return True


def build_override_index(overrides):
    """path (tuple de noms) -> {'equipment': {...}, 'personnel': {...}}"""
    idx = {}
    for spec in overrides or []:
        idx[tuple(spec["path"])] = {
            "equipment": spec.get("equipment", {}),
            "personnel": spec.get("personnel", {}),
        }
    return idx


def walk(node, equip_models, pers_models, override_index, path, clean_legacy, log):
    equip = node.get("equipment") or []
    pers = node.get("personnel") or []
    override = override_index.get(tuple(path))

    if equip or pers:
        # Vérifier que tous les codes utilisés sont bien couverts par la table
        missing = [e["name"] for e in equip if e["name"] not in equip_models]
        missing += [p["name"] for p in pers if p["name"] not in pers_models]
        missing = [c for c in missing if not (override and (
            c in override.get("equipment", {}) or c in override.get("personnel", {})))]
        if missing:
            log.setdefault("missing_codes", []).append((node.get("name", "?"), missing))
        node["description"] = build_desc(equip, pers, equip_models, pers_models, override)
        log.setdefault("annotated", []).append(node.get("name", "?"))
    elif clean_legacy and is_pure_legacy_text(node.get("description")):
        node.pop("description", None)
        log.setdefault("cleaned", []).append(node.get("name", "?"))

    for su in node.get("subUnits", []) or []:
        walk(su, equip_models, pers_models, override_index, path + [su.get("name", "?")],
             clean_legacy, log)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file")
    parser.add_argument("spec_file", help="JSON : root, equipment_models, personnel_models, overrides, clean_legacy_containers")
    parser.add_argument("--output", help="Fichier de sortie (par défaut : écrase orbat_file)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    orbat = ol.load(args.orbat_file)
    with open(args.spec_file, "r", encoding="utf-8") as f:
        spec = json.load(f)

    root = ol.find_unit(orbat, spec["root"])
    if root is None:
        print(f"Unité racine introuvable : {spec['root']!r}", file=sys.stderr)
        sys.exit(1)

    equip_models = spec.get("equipment_models", {})
    pers_models = spec.get("personnel_models", {})
    override_index = build_override_index(spec.get("overrides"))
    clean_legacy = bool(spec.get("clean_legacy_containers", False))

    log = {}
    # le nœud racine lui-même est traité avec path=[] (aucun override possible dessus)
    walk(root, equip_models, pers_models, override_index, [], clean_legacy, log)

    if log.get("annotated"):
        print(f"{len(log['annotated'])} unité(s) annotée(s) :")
        for name in log["annotated"]:
            print(f"  - {name}")
    if log.get("cleaned"):
        print(f"\n{len(log['cleaned'])} nœud(s) conteneur nettoyé(s) (texte hérité) :")
        for name in log["cleaned"]:
            print(f"  - {name}")
    if log.get("missing_codes"):
        print(f"\n⚠️  Code(s) sans correspondance dans la table (ignorés dans la description, à compléter) :", file=sys.stderr)
        for name, codes in log["missing_codes"]:
            print(f"  {name} : {codes}", file=sys.stderr)
    if not log.get("annotated") and not log.get("cleaned"):
        print("Rien à faire (aucune unité avec equipment/personnel propre sous la racine).")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return

    out_path = args.output or args.orbat_file
    ol.save(orbat, out_path)
    print(f"\nÉcrit dans {out_path}")


if __name__ == "__main__":
    main()
