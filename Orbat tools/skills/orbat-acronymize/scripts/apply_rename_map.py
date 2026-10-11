#!/usr/bin/env python3
"""
apply_rename_map.py — Applique un mapping {ancien_nom: nouveau_code} à un ORBAT
JSON (format orbat-mapper.app) :

1. Renomme les entrées des catalogues racine `equipment` et `personnel`,
   conserve l'ancien nom en tête de leur `description` (naming.md Règle 5), et
   propage le changement à toutes les références de l'arbre d'unités
   (`equipment[]`/`personnel[]` ET les `update`/`diff` des timelines `state[]`).

   CONVERGENCE : quand plusieurs anciens noms partent vers le MÊME code
   (VAB et VBL -> VBTT), ou vers un code déjà présent, le script FUSIONNE :
   une seule entrée de catalogue (désignations jointes par « / »), une seule
   ligne par unité (quantités sommées), et les timelines concernées sont
   réexprimées en deltas avant fusion pour que les quantités restent exactes
   à toute date. Plus aucune fusion manuelle à faire.

2. Annote la `description` de chaque échelon avec la légende canonique
   (naming.md § 7.3, module `orbat-json/scripts/legends.py`) des codes de son
   sous-arbre, Équipement et Personnel séparés :
       Équipement :
       * **VBTT : VAB**
   La légende d'un échelon ne cite que les désignations RÉELLEMENT présentes
   dans son sous-arbre (un groupe qui n'a que des VAB n'affiche pas « VBL »).
   La prose existante (phrase de contexte § 7.4) est conservée.

3. Seulement avec --titres (opt-in, désactivé par défaut) : quand un échelon
   ne porte, EN PROPRE, qu'un seul matériel (un seul code, une seule
   désignation d'origine), enrichit son titre (`name`) avec le nom réel,
   ex. "Escadron" -> "Escadron de VAB". `--no-titles` reste accepté, sans effet
   (compatibilité avec les anciennes commandes).

4. Valide le résultat (contrôles de `orbat-json/scripts/validate.py`) et
   affiche le rapport — code de sortie 1 s'il reste des ERREURS.

Usage:
    python apply_rename_map.py <orbat.json> <mapping.json> [--output OUT.json]
                                [--dry-run] [--no-legend] [--titres]

mapping.json : {"Nom original 1": "CODE-V4-1", "Nom original 2": "CODE-V4-2", ...}
Les clés commençant par « _ » (métadonnées du brouillon de draft_mapping.py :
`_a_valider`, `_candidats`) sont ignorées ; le script refuse toutefois de
tourner tant que `_a_valider` n'est pas vide (noms encore sans code validé).

Par défaut, écrase le fichier d'entrée. Idempotent : peut être relancé sans
dupliquer légendes ou suffixes de titre déjà appliqués.

Dépend du skill `orbat-json` du même plugin (orbat_lib, legends, validate),
localisé automatiquement (variable ORBAT_TOOLS_ROOT en repli si le plugin a été déplacé).
"""
import argparse
import json
import os
import sys


def _bootstrap():
    """Rend importables les modules partagés de orbat-json/scripts."""
    here = os.path.dirname(os.path.abspath(__file__))
    tried = []
    d = here
    for _ in range(8):
        tried += [os.path.join(d, "orbat-json", "scripts"),
                  os.path.join(d, "skills", "orbat-json", "scripts")]
        d = os.path.dirname(d)
    env = os.environ.get("ORBAT_TOOLS_ROOT")   # repli seulement (plugin déplacé)
    if env:
        tried += [os.path.join(env, "skills", "orbat-json", "scripts"),
                  os.path.join(env, "orbat-json", "scripts")]
    for c in tried:
        if os.path.isfile(os.path.join(c, "orbat_lib.py")):
            sys.path.insert(0, c)
            return c
    sys.exit("❌ Skill orbat-json introuvable (orbat_lib.py). Définir ORBAT_TOOLS_ROOT "
             "sur la racine du plugin orbat-tools.\n  Essayé : " + "\n  ".join(tried))


_bootstrap()
import orbat_lib as ol  # noqa: E402
import legends as lg    # noqa: E402
import validate as vd   # noqa: E402

KINDS = ("equipment", "personnel")
VOWELS = "aàâeéèêiîïoôuùûhAÀÂEÉÈÊIÎÏOÔUÙÛH"


# ---------------------------------------------------------------------------
# Parcours
# ---------------------------------------------------------------------------
def all_nodes(orbat):
    """Toutes les unités ET les groups de tête (qui peuvent porter une description)."""
    for side in orbat.get("sides", []) or []:
        for root in list(side.get("units", []) or []) + list(side.get("groups", []) or []):
            yield from ol.subtree_units(root)


def roots_of(orbat):
    for side in orbat.get("sides", []) or []:
        yield from list(side.get("units", []) or []) + list(side.get("groups", []) or [])


# ---------------------------------------------------------------------------
# 1. Renommage
# ---------------------------------------------------------------------------
def rename_catalog(catalog, mapping, changes):
    """
    Renomme un catalogue racine et fusionne les entrées qui convergent.
    Renvoie la NOUVELLE liste. `changes` reçoit (ancien, nouveau).
    """
    parts = {}   # code -> [(désignation, contexte, renommée?)]
    order = []
    originals = {}   # code -> entrée d'origine non renommée
    firsts = {}      # code -> première entrée rencontrée (autres clés conservées)
    for entry in catalog or []:
        old = entry.get("name")
        new = mapping.get(old, old)
        desc = (entry.get("description") or "").strip()
        if new != old:
            if desc and old in desc:
                # la description nomme déjà le matériel (« T-72B3 modernisé ») :
                # elle est gardée telle quelle, jamais tronquée.
                real = lg.extract_real_name(desc)
                ctx = desc[len(real):].strip()
                ctx = ctx[1:].strip() if ctx.startswith(("—", "-")) else ctx
            else:
                real, ctx = old, desc
            part = (real, ctx, True)
            changes.append((old, new))
        else:
            real = lg.extract_real_name(desc)
            ctx = desc[len(real):].strip() if real else ""
            ctx = ctx[1:].strip() if ctx.startswith(("—", "-")) else ctx
            part = (real, ctx, False)
            originals[new] = entry
        firsts.setdefault(new, entry)
        if new not in parts:
            parts[new] = []
            order.append(new)
        parts[new].append(part)

    out = []
    for code in order:
        ps = parts[code]
        if len(ps) == 1 and not ps[0][2]:
            out.append(originals[code])          # entrée intacte
            continue
        reals, ctxs = [], []
        for real, ctx, _ in ps:
            if real and real not in reals:
                reals.append(real)
            if ctx and ctx not in ctxs:
                ctxs.append(ctx)
        desc = " / ".join(reals) + (" — " + " ; ".join(ctxs) if ctxs else "")
        base = dict(originals.get(code) or firsts[code])
        base.update({"name": code, "description": desc})
        out.append(base)
    return out


def _names_in_unit(unit, kind):
    names = [i.get("name") for i in unit.get(kind, []) or []]
    for st in unit.get("state", []) or []:
        for blk in ("update", "diff"):
            names += [i.get("name") for i in (st.get(blk) or {}).get(kind, []) or []]
    return [n for n in names if n is not None]


def unit_converges(unit, mapping):
    """Vrai si, dans cette unité, deux noms distincts aboutissent au même code."""
    for kind in KINDS:
        finals = {}
        for n in set(_names_in_unit(unit, kind)):
            finals.setdefault(mapping.get(n, n), set()).add(n)
        if any(len(src) > 1 for src in finals.values()):
            return True
    return False


def rename_units(orbat, mapping, provenance, log):
    """
    Renomme les références dans l'arbre et les timelines. `provenance`
    reçoit, par id(nœud), {kind: {code: [désignations portées en propre]}} :
      - codes renommés pendant cette passe -> anciens noms exacts ;
      - codes déjà renommés lors d'une passe précédente (code = une valeur du
        mapping) -> désignation lue dans la légende déjà posée sur l'unité,
        à défaut tous les noms que le mapping envoie vers ce code. Relancer le
        script avec un mapping complété ne fait donc rien perdre.
    """
    sources = {}
    for old, new in mapping.items():
        if old != new:
            sources.setdefault(new, []).append(old)

    def walk_prov(unit, inherited):
        # légende déjà posée : celle de l'unité, à défaut celle de l'ancêtre
        # nommé le plus proche (un nœud sans `name` n'en porte jamais).
        own_prev = lg.parse_legend(unit.get("description"), set(sources))
        previous = {k: {**inherited[k], **own_prev[k]} for k in KINDS}
        prov = {}
        for kind in KINDS:
            for item in unit.get(kind, []) or []:
                old = item.get("name")
                if old in mapping and mapping[old] != old:
                    code, names = mapping[old], [old]
                elif old in sources:
                    code = old
                    label = previous[kind].get(old)
                    names = label.split(" / ") if label else sources[old]
                else:
                    continue
                lst = prov.setdefault(kind, {}).setdefault(code, [])
                for n in names:
                    if n not in lst:
                        lst.append(n)
        if prov:
            provenance[id(unit)] = prov
        for child in unit.get("subUnits", []) or []:
            walk_prov(child, previous)

    for root in roots_of(orbat):
        walk_prov(root, {k: {} for k in KINDS})

    for unit in all_nodes(orbat):

        if unit.get("state") and unit_converges(unit, mapping):
            n = ol.states_to_diffs(unit)
            if n:
                log.setdefault("timelines_reexprimees", []).append((unit.get("name", "?"), n))

        merged = False
        for kind in KINDS:
            items = unit.get(kind)
            if not items:
                continue
            for item in items:
                if item.get("name") in mapping:
                    item["name"] = mapping[item["name"]]
            new_items = ol.merge_items(items)
            if len(new_items) != len(items):
                merged = True
            unit[kind] = new_items
        for st in unit.get("state", []) or []:
            for blk in ("update", "diff"):
                b = st.get(blk) or {}
                for kind in KINDS:
                    lst = b.get(kind)
                    if not lst:
                        continue
                    for it in lst:
                        if it.get("name") in mapping:
                            it["name"] = mapping[it["name"]]
                    names = [i.get("name") for i in lst]
                    if blk == "diff" and len(names) != len(set(names)):
                        # deltas convergents : sommés (les autres clés du 1er sont gardées)
                        out, idx = [], {}
                        for it in lst:
                            if it.get("name") in idx:
                                idx[it["name"]]["onHand"] = idx[it["name"]].get("onHand", 0) + it.get("onHand", 0)
                            else:
                                cp = dict(it)
                                idx[it.get("name")] = cp
                                out.append(cp)
                        b[kind] = out
        if merged:
            log.setdefault("lignes_fusionnees", []).append(unit.get("name", "?"))


# ---------------------------------------------------------------------------
# 2. Légendes
# ---------------------------------------------------------------------------
def annotate_units(node, provenance, log, known=None):
    """Pose la légende du sous-arbre ; renvoie {kind: {code: [désignations]}}."""
    acc = {k: {} for k in KINDS}

    def add(kind, code, names):
        lst = acc[kind].setdefault(code, [])
        for n in names:
            if n not in lst:
                lst.append(n)

    for kind, codes in provenance.get(id(node), {}).items():
        for code, names in codes.items():
            add(kind, code, names)
    for child in node.get("subUnits", []) or []:
        sub = annotate_units(child, provenance, log, known)
        for kind in KINDS:
            for code, names in sub[kind].items():
                add(kind, code, names)

    if (acc["equipment"] or acc["personnel"]) and "name" in node:
        eq = [(c, " / ".join(n)) for c, n in acc["equipment"].items()]
        pe = [(c, " / ".join(n)) for c, n in acc["personnel"].items()]
        lg.set_legend(node, eq, pe, known_codes=known)
        log.setdefault("legends", []).append((node.get("name", "?"), eq + pe))
    return acc


# ---------------------------------------------------------------------------
# 3. Titres
# ---------------------------------------------------------------------------
def enrich_titles(node, provenance, log):
    """Un seul code d'équipement porté en propre, d'une seule désignation
    d'origine -> « {name} de {désignation} ». Personnel exclu (tautologie)."""
    own = provenance.get(id(node), {}).get("equipment", {})
    # mixte = plusieurs lignes d'équipement en propre, renommées ou non (un VBL
    # hors mapping à côté d'un VAB renommé rend l'échelon mixte)
    single_line = len(node.get("equipment") or []) == 1
    if len(own) == 1 and single_line and "name" in node:
        (names,) = own.values()
        if len(names) == 1:
            real_name = names[0]
            current = node["name"]
            if real_name.lower() not in current.lower():
                prep = "d'" if real_name[0] in VOWELS else "de "
                node["name"] = f"{current} {prep}{real_name}"
                log.setdefault("titles", []).append((current, node["name"]))
    for child in node.get("subUnits", []) or []:
        enrich_titles(child, provenance, log)


# ---------------------------------------------------------------------------
def load_mapping(raw):
    """
    Mapping utilisable depuis le JSON lu : les clés « _… » (métadonnées du
    brouillon de draft_mapping.py) sont écartées ; quitte (code 2) si
    `_a_valider` n'est pas vide ou si une valeur n'est pas un code (chaîne).
    """
    if not isinstance(raw, dict):
        print("❌ mapping.json doit être un objet {ancien_nom: nouveau_code}.", file=sys.stderr)
        sys.exit(2)
    todo = raw.get("_a_valider") or []
    if todo:
        print(f"❌ Brouillon non finalisé : {len(todo)} nom(s) encore dans « _a_valider » "
              f"({', '.join(map(repr, todo[:10]))}{' …' if len(todo) > 10 else ''}). "
              "Les résoudre (skill acronyme), les faire valider par Florian, puis retirer "
              "la clé avant d'appliquer.", file=sys.stderr)
        sys.exit(2)
    mapping = {k: v for k, v in raw.items() if not str(k).startswith("_")}
    bad = [k for k, v in mapping.items() if not isinstance(v, str) or not v.strip()]
    if bad:
        print("❌ Valeur(s) de mapping invalide(s) (un code attendu) pour : "
              + ", ".join(map(repr, bad)), file=sys.stderr)
        sys.exit(2)
    return mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("orbat_file", help="Fichier ORBAT JSON à modifier")
    parser.add_argument("mapping_file", help="Fichier JSON {ancien_nom: nouveau_code}")
    parser.add_argument("--output", help="Fichier de sortie (par défaut : écrase orbat_file)")
    parser.add_argument("--dry-run", action="store_true", help="N'écrit rien ; affiche le résumé et la validation")
    parser.add_argument("--no-legend", action="store_true", help="Ne pas poser la légende dans les descriptions d'échelon")
    parser.add_argument("--titres", action="store_true",
                        help="Enrichir le titre (name) des échelons à composition de matériel "
                             "unique, ex. « Escadron » -> « Escadron de VAB » (désactivé par défaut)")
    parser.add_argument("--no-titles", action="store_true",
                        help="Obsolète, sans effet : les titres ne sont plus enrichis par défaut "
                             "(voir --titres). Accepté pour compatibilité.")
    args = parser.parse_args()

    orbat = ol.load(args.orbat_file)
    with open(args.mapping_file, "r", encoding="utf-8") as f:
        raw = json.load(f)
    mapping = load_mapping(raw)

    changes, per_kind = [], {}
    for key in KINDS:
        if key in orbat:
            before = len(changes)
            orbat[key] = rename_catalog(orbat[key], mapping, changes)
            per_kind[key] = changes[before:]

    log, provenance = {}, {}
    rename_units(orbat, mapping, provenance, log)

    print(f"{len(changes)} entrée(s) de catalogue renommée(s) :")
    for old, new in changes:
        print(f"  {old!r} -> {new!r}")
    conv = {}
    for key, ch in per_kind.items():
        targets = {}
        for old, new in ch:
            targets.setdefault(new, []).append(old)
        conv.update({c: o for c, o in targets.items() if len(set(o)) > 1})
    if conv:
        print(f"\n{len(conv)} code(s) recevant plusieurs désignations (fusionnés) :")
        for c, o in conv.items():
            print(f"  {c} <- {' / '.join(o)}")

    unmatched = [k for k in mapping if k not in {c[0] for c in changes}]
    if unmatched:
        print(f"\n⚠️  {len(unmatched)} entrée(s) du mapping non trouvée(s) dans le catalogue (vérifier l'orthographe) :")
        for k in unmatched:
            print(f"  {k!r}")

    if log.get("lignes_fusionnees"):
        print(f"\n{len(log['lignes_fusionnees'])} unité(s) dont des lignes convergentes ont été fusionnées.")
    if log.get("timelines_reexprimees"):
        print(f"{len(log['timelines_reexprimees'])} timeline(s) réexprimée(s) en deltas avant fusion "
              "(quantités inchangées à toute date).")

    known = lg.catalog_codes(orbat) | set(mapping) | set(mapping.values())
    for root in roots_of(orbat):
        if not args.no_legend:
            annotate_units(root, provenance, log, known)
        if args.titres:
            enrich_titles(root, provenance, log)

    if log.get("legends"):
        print(f"\n{len(log['legends'])} échelon(s) annoté(s) avec une légende :")
        for name, legend in log["legends"][:40]:
            print(f"  {name} -> " + ", ".join(f"{c} : {l}" for c, l in legend))
        if len(log["legends"]) > 40:
            print(f"  ... (+{len(log['legends']) - 40})")
    if log.get("titles"):
        print(f"\n{len(log['titles'])} titre(s) d'échelon enrichi(s) :")
        for old, new in log["titles"]:
            print(f"  {old!r} -> {new!r}")

    print("\n--- Validation du résultat (orbat-json/scripts/validate.py) ---")
    errors, warns, n = vd.check(orbat)
    vd.report(errors, warns, n)

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
    else:
        out_path = args.output or args.orbat_file
        ol.save(orbat, out_path)
        print(f"\nÉcrit dans {out_path}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
