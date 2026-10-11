#!/usr/bin/env python3
"""
conformite.py — rapport de conformité d'un ORBAT JSON (references/naming.md,
Règle 8 « Contrôle de conformité à la source, avant toute livraison »).

    python3 conformite.py orbat.json [--source totaux.json] [--at DATE] [--unit ID_OU_NOM]

  --source  totaux de la SOURCE (document, PDF, TOE…) à confronter aux totaux
            agrégés du fichier. Format JSON :
              {
                "equipment": {"CODE": 12, ...},
                "personnel": {"CODE": 140, ...},
                "supplies":  {"CODE": 3, ...},                 (facultatif)
                "unites": {                                     (facultatif, § 8.2 n° 2)
                  "<id ou nom d'unité>": {"equipment": {...}, "personnel": {...}}
                }
              }
            Seules les catégories présentes sont confrontées ; un code absent
            d'un côté est un écart (quantité 0). Clés commençant par « _ » ignorées.
  --at      confronter l'état à cette date ISO 8601 (timeline rejouée), au lieu
            de l'état de base (champ `count`).
  --unit    restreindre aux totaux et aux contrôles d'unités d'un sous-arbre
            (id, nom exact, ou partie du nom) ; les contrôles de catalogue et de
            structure restent globaux.

Contrôles automatisés (check-list § 8.2) : totaux (1, 2), échelon du nom ↔
échelon du sidc (5), codes attestés dans l'INDEX du skill `acronyme` et
déclarés au catalogue (6), catalogues utilisés / déclarés / décrits (7),
nommage — pas de parenthèses, shortName partout, pas de répétition de la
formation mère, « Ø » sur les sous-arbres vides (8), sidc — entités non
attestées au dictionnaire, mauvais précédent cavalerie (10), structure —
validate.py (11), légendes § 7.3 sur les unités porteuses (12). Les contrôles
3, 4 et 9 demandent la source : ils restent « manuels » et sont rappelés dans
le bloc 🔴.

Sortie : le rapport en trois blocs de la Règle 8 § 8.4 (✅ Vérifié /
⚠️ Corrigé / 🔴 Non résolu — « néant » si vide), puis la check-list en table.
Ce script ne corrige rien : le bloc ⚠️ Corrigé est à compléter avec les
corrections faites avant ce contrôle.

Code de sortie : 1 s'il y a des ÉCARTS (totaux discordants, erreur de
validate.py, code non attesté ou non déclaré, catalogue incomplet, parenthèses
ou shortName manquant, légende manquante) ; 0 sinon — les points « à
vérifier » (heuristiques) et les lacunes de source figurent au bloc 🔴 sans
changer le code de sortie. 2 si les arguments ou le fichier source sont invalides.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbat_lib as ol          # noqa: E402
import legends as lg            # noqa: E402
import validate as vd           # noqa: E402
from aggregate import aggregate_at   # noqa: E402

KINDS = ("equipment", "personnel", "supplies")
KIND_FR = {"equipment": "équipement", "personnel": "personnel", "supplies": "supplies"}
OK, ECART, VERIF, MANUEL, NV = "✅", "🔴", "⚠️", "➖ manuel", "➖ non vérifiable"
MAX_LIST = 12


def _cap(items, n=MAX_LIST):
    items = list(items)
    return ", ".join(items[:n]) + (f" (+{len(items) - n})" if len(items) > n else "")


# ---------------------------------------------------------------------------
# Données de référence
# ---------------------------------------------------------------------------
def index_codes():
    """Codes de `acronyme/references/INDEX.md` (ensemble), ou None si introuvable."""
    try:
        path = os.path.join(ol.find_skill_dir("acronyme"), "references", "INDEX.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (FileNotFoundError, OSError):
        return None
    return set(re.findall(r"^\|\s*`([^`]+)`\s*\|", text, re.M))


def load_source(path):
    with open(path, encoding="utf-8") as f:
        src = json.load(f)
    if not isinstance(src, dict):
        raise ValueError("le fichier source doit être un objet JSON")

    def check_block(block, where):
        out = {}
        for kind, vals in block.items():
            if kind.startswith("_") or kind == "unites":
                continue
            if kind not in KINDS:
                raise ValueError(f"{where} : catégorie inconnue {kind!r} "
                                 f"(attendu : {', '.join(KINDS)})")
            if not isinstance(vals, dict) or not all(
                    isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals.values()):
                raise ValueError(f"{where}.{kind} : attendu {{\"CODE\": nombre}}")
            out[kind] = {k: v for k, v in vals.items() if not k.startswith("_")}
        return out

    res = {"totaux": check_block(src, "racine"), "unites": {}}
    for key, block in (src.get("unites") or {}).items():
        if key.startswith("_"):
            continue
        if not isinstance(block, dict):
            raise ValueError(f"unites.{key} : objet attendu")
        res["unites"][key] = check_block(block, f"unites.{key}")
    return res


def totals(units, kind, at=None):
    units = list(units)
    raw = aggregate_at(units, kind, at) if at else ol.aggregate(units, kind)
    return {k: v for k, v in raw.items() if v}


def compare(expected, got):
    """[(code, source, fichier)] des différences (codes des deux côtés)."""
    diffs = []
    for code in list(expected) + [c for c in got if c not in expected]:
        e, g = expected.get(code, 0), got.get(code, 0)
        if e != g:
            diffs.append((code, e, g))
    return diffs


def _fmt_diffs(diffs):
    return _cap(f"{c} source {e} ≠ fichier {g}" for c, e, g in diffs)


# ---------------------------------------------------------------------------
# Contrôle
# ---------------------------------------------------------------------------
def run(orbat, source=None, at=None, unit=None, codes=None, index=False):
    """
    Exécute les contrôles. `source` : résultat de load_source() ou None ;
    `unit` : racine du sous-arbre (dict) ou None ; `codes` : short_names.load_codes()
    (lu si None ; contrôles de nom dégradés si le skill acronyme manque) ;
    `index` : ensemble des codes de l'INDEX (lu si False, None = introuvable).
    Renvoie {"scope", "checks": [(n°, contrôle, statut, détail)],
             "verifie": [...], "ecarts": [...], "a_verifier": [...], "lacunes": [...]}.
    """
    rep = {"checks": [], "verifie": [], "ecarts": [], "a_verifier": [], "lacunes": []}

    def add(num, label, status, detail="", items=()):
        if items and not detail:
            detail = f"{len(items)} point(s) — voir le bloc 🔴"
        rep["checks"].append((num, label, status, detail))
        if status == OK:
            rep["verifie"].append(f"{label} — {detail}" if detail else label)
        elif status == ECART:
            rep["ecarts"] += [f"[{num}] {i}" for i in items] or [f"[{num}] {label} : {detail}"]
        elif status == VERIF:
            rep["a_verifier"] += [f"[{num}] {i}" for i in items] or [f"[{num}] {label} : {detail}"]
        else:
            rep["lacunes"].append(f"[{num}] {label} : {detail}")

    all_units = list(ol.iter_units(orbat))
    scope_units = list(ol.subtree_units(unit)) if unit else all_units
    scope_ids = {id(u) for u in scope_units}
    rep["scope"] = (f"{unit.get('name')} (id={unit.get('id')}), {len(scope_units)} unités"
                    if unit else f"ORBAT « {orbat.get('name')} », {len(scope_units)} unités")
    rep["scope"] += f" — état au {at}" if at else " — état de base"

    if codes is None:
        try:
            import short_names as sn
            codes = sn.load_codes()
        except (FileNotFoundError, ValueError, OSError):
            codes = None
    if index is False:
        index = index_codes()

    # 1 — totaux généraux (ou du sous-arbre)
    got = {k: totals(scope_units, k, at) for k in KINDS}
    lab1 = "Totaux de " + unit.get("name", "?") if unit else "Totaux généraux"
    if source and source["totaux"]:
        diffs = {k: compare(source["totaux"][k], got[k]) for k in source["totaux"]}
        bad = [f"{KIND_FR[k]} : {_fmt_diffs(d)}" for k, d in diffs.items() if d]
        if bad:
            add(1, lab1, ECART, "; ".join(bad), bad)
        else:
            add(1, lab1, OK, "; ".join(f"{KIND_FR[k]} {sum(got[k].values())} "
                                       f"({len(got[k])} codes) = source" for k in source["totaux"]))
    else:
        add(1, lab1, NV, "pas de totaux source (--source) : totaux NON confrontés — "
            + "; ".join(f"{KIND_FR[k]} {sum(v.values())}" for k, v in got.items() if v))

    # 2 — totaux par grande formation
    if source and source["unites"]:
        bad, good, missing = [], [], []
        for key, block in source["unites"].items():
            u = ol.find_unit(orbat, key)
            if u is None:
                missing.append(key)
                continue
            sub = list(ol.subtree_units(u))
            for k, exp in block.items():
                d = compare(exp, totals(sub, k, at))
                (bad if d else good).append(f"{u.get('name')} / {KIND_FR[k]}"
                                            + (f" : {_fmt_diffs(d)}" if d else ""))
        items = bad + [f"unité source introuvable dans le fichier : {m!r}" for m in missing]
        if items:
            add(2, "Totaux par grande formation", ECART, f"{len(items)} écart(s)", items)
        else:
            add(2, "Totaux par grande formation", OK, f"{len(good)} confrontation(s) concordante(s)")
    else:
        add(2, "Totaux par grande formation", MANUEL,
            "à confronter (clé « unites » de --source, ou aggregate.py --unit)")

    # 3, 4 — manuels
    add(3, "Effectifs des feuilles", MANUEL, "chaque unité terminale relue contre sa ligne de source")
    per_ech = {}
    for u in scope_units:
        lab = ol.ECHELON_LABEL_FR.get(ol.echelon_of(u) or "", "sans échelon")
        per_ech[lab] = per_ech.get(lab, 0) + 1
    add(4, "Complétude structurelle", MANUEL, "à comparer à la source : "
        + ", ".join(f"{n} {lab}" for lab, n in sorted(per_ech.items(), key=lambda x: -x[1])))

    # walk (parents) restreint au périmètre
    walked = []
    try:
        import short_names as sn
        walked = [(u, p, a) for u, p, a in sn.walk(orbat) if id(u) in scope_ids]
    except ImportError:          # pragma: no cover
        sn = None

    # 5 — échelon du nom ↔ échelon du sidc
    if codes:
        mism = []
        for u, _, _ in walked:
            notion = sn.name_echelon(u.get("name"), codes)
            sid = ol.echelon_of(u)
            if not notion or not sid:
                continue
            try:
                expected = ol.echelon_code(notion)
            except ValueError:
                alias = {"corps d'armee": "corps"}.get(notion)
                expected = ol.echelon_code(alias) if alias else None
            if expected and expected != sid:
                mism.append(f"{u.get('name')!r} : nom = {notion}, sidc = "
                            f"{sid} ({ol.ECHELON_LABEL_FR.get(sid, '?')})")
        if mism:
            add(5, "Échelons (nom ↔ sidc)", VERIF, f"{len(mism)} discordance(s)", mism)
        else:
            add(5, "Échelons (nom ↔ sidc)", OK, "échelon du nom = échelon du sidc partout où les deux existent")
    else:
        add(5, "Échelons (nom ↔ sidc)", NV, "skill acronyme introuvable")

    # 6 — codes attestés
    used = {}
    for u in scope_units:
        for k in ("equipment", "personnel"):
            for it in u.get(k, []) or []:
                used.setdefault(it.get("name"), set()).add(k)
    cat = {k: set(ol.catalog_map(orbat, k)) for k in ("equipment", "personnel")}
    not_declared = sorted(f"{c} ({'/'.join(sorted(ks))})" for c, ks in used.items()
                          if any(c not in cat[k] for k in ks))
    if index is None:
        add(6, "Codes attestés", NV, "INDEX du skill acronyme introuvable")
        if not_declared:
            add(6, "Codes déclarés au catalogue", ECART, "", [f"code non déclaré au catalogue : {c}"
                                                             for c in not_declared])
    else:
        unknown, composed = [], []
        for c in sorted(x for x in used if x):
            if c in index:
                continue
            # préfixe numérique de duplication (`2AACA`, grammaire.md) et calibre
            # (`.20`) : seuls les éléments alphabétiques doivent être attestés.
            parts = [re.sub(r"^\d+", "", p) for p in re.split(r"[-./()]", c)]
            parts = [p for p in parts if p]
            if parts and all(p in index for p in parts):
                composed.append(c)
            else:
                unknown.append(c)
        items = ([f"code non attesté dans le skill acronyme : {c}" for c in unknown]
                 + [f"code non déclaré au catalogue : {c}" for c in not_declared])
        if items:
            add(6, "Codes attestés", ECART, f"{len(items)} écart(s)", items)
        else:
            add(6, "Codes attestés", OK, f"{len(used)} code(s) présents dans l'INDEX du skill "
                "acronyme (ou composés d'éléments attestés) et déclarés au catalogue")
        if composed:
            add(6, "Codes composés hors lexique", VERIF, "",
                [f"{c} : composé d'éléments attestés, absent du lexique — à signaler à Florian, "
                 "à journaliser s'il valide (naming.md § 7.1)" for c in composed])

    # 7 — catalogues (globaux)
    used_all = {k: set() for k in KINDS}
    for u in all_units:
        for k in KINDS:
            used_all[k] |= {i.get("name") for i in u.get(k, []) or []}
            for st in u.get("state", []) or []:
                for blk in ("update", "diff"):
                    used_all[k] |= {i.get("name") for i in (st.get(blk) or {}).get(k, []) or []}
    items = []
    for k, key in (("equipment", "equipment"), ("personnel", "personnel"),
                   ("supplies", "supplyCategories")):
        for e in orbat.get(key, []) or []:
            if e.get("name") not in used_all[k]:
                items.append(f"{KIND_FR[k]} : entrée de catalogue inutilisée {e.get('name')!r}")
            if k != "supplies" and not (e.get("description") or "").strip():
                items.append(f"{KIND_FR[k]} : {e.get('name')!r} sans description "
                             "(désignation réelle en tête, Règle 5)")
        declared = set(ol.catalog_map(orbat, k))
        for n in sorted(x for x in used_all[k] - declared if x):
            items.append(f"{KIND_FR[k]} : {n!r} utilisé mais non déclaré")
    if items:
        add(7, "Catalogues", ECART, f"{len(items)} écart(s)", items)
    else:
        add(7, "Catalogues", OK, "toutes les entrées sont utilisées, déclarées et décrites")

    # 8 — nommage
    paren = [u.get("name") for u in scope_units if "(" in (u.get("name") or "")
             or ")" in (u.get("name") or "")]
    no_short = [u.get("name") or u.get("id") or "?" for u in scope_units
                if not (u.get("shortName") or "").strip()]
    items = ([f"parenthèses dans name (Règle 1) : {n!r}" for n in paren]
             + [f"shortName manquant (Règle 2) : {n!r} — short_names.py" for n in no_short])
    if items:
        add(8, "Nommage", ECART, f"{len(items)} écart(s)", items)
    else:
        add(8, "Nommage", OK, "aucune parenthèse dans name, shortName partout")
    if codes:
        reps = []
        for u, p, a in walked:
            refs = sn.repeats_parent(u, p, a, codes)
            if refs:
                reps.append(f"{u.get('name')!r} reprend {', '.join(repr(r) for r in refs)} (§ 7.7)")
        if reps:
            add(8, "Répétition de la formation mère", VERIF, "", reps)
    empties = []

    def _empty(u):
        subs = [_empty(s) for s in u.get("subUnits", []) or []]
        e = not u.get("equipment") and not u.get("personnel") and all(subs)
        if e and id(u) in scope_ids and not (u.get("name") or "").endswith("Ø"):
            empties.append(u.get("name") or "?")
        return e
    for side in orbat.get("sides", []) or []:
        for root in list(side.get("units", []) or []) + [
                s for g in side.get("groups", []) or [] for s in g.get("subUnits", []) or []]:
            _empty(root)
    if empties:
        add(8, "Indicateur de TOE vide", VERIF, "",
            [f"sous-arbre vide sans « Ø » (Règle 3) : {n!r}" for n in empties])

    # 9 — manuel
    add(9, "Lacunes assumées", MANUEL, "lignes laissées vides faute d'acronyme mentionnées "
        "en description (§ 7.2, § 7.4)")

    # 10 — sidc
    try:
        import sidc_lookup as sl
        attested = sl._attested()
        cav, unatt = [], []
        for u in scope_units:
            s = str(u.get("sidc") or "")
            if len(s) != 20 or not s.isdigit():
                continue
            if (s[4:6], s[10:16]) not in attested:
                unatt.append(f"{u.get('name')!r} : entité {s[10:16]} (set {s[4:6]}) non attestée "
                             "au sidc_dictionary.json — à signaler, confirmer par rendu")
            if s[10:16] in sl.BAD_PRECEDENT and any(
                    w in ol.fold(u.get("name")) for w in sl.CAVALRY_WORDS):
                cav.append(f"{u.get('name')!r} : nom de cavalerie en {s[10:16]} — cavalerie = 121300 "
                           "(diagonale seule) sauf reco réellement blindée (sidc.md, mauvais précédent)")
        if cav or unatt:
            add(10, "Symboles (sidc)", VERIF, "", cav + unatt)
        else:
            add(10, "Symboles (sidc)", OK, "entités attestées au dictionnaire, pas de cavalerie en "
                "120500/120501 — cohérence rôle/époque à juger sur la source")
    except (ImportError, OSError, ValueError) as e:
        add(10, "Symboles (sidc)", NV, f"dictionnaire illisible : {e}")

    # 11 — structure
    errors, warns, n = vd.check(orbat)
    if errors:
        add(11, "Structure (validate.py)", ECART, f"{len(errors)} erreur(s)", errors)
    else:
        add(11, "Structure (validate.py)", OK, f"0 erreur, {len(warns)} avertissement(s), {n} unités")

    # 12 — légendes (§ 7.3) sur les unités porteuses
    known = lg.catalog_codes(orbat)
    miss = []
    for u in scope_units:
        if not u.get("name"):
            continue
        leg = lg.parse_legend(u.get("description"))
        for k in ("equipment", "personnel"):
            lacking = [i.get("name") for i in u.get(k, []) or []
                       if i.get("name") in known and i.get("name") not in leg[k]]
            if lacking:
                miss.append(f"{u.get('name')!r} : {KIND_FR[k]} sans légende pour {', '.join(lacking)}")
    if miss:
        add(12, "Légendes (§ 7.3)", ECART, f"{len(miss)} unité(s) — add_legends.py", miss)
    else:
        add(12, "Légendes (§ 7.3)", OK, "chaque unité porteuse légende ses codes")
    return rep


def render(rep, out=sys.stdout):
    p = lambda s="": print(s, file=out)   # noqa: E731
    p("Contrôle de conformité à la source")
    p(f"({rep['scope']})")
    p("✅ Vérifié :" + (" néant" if not rep["verifie"] else ""))
    for v in rep["verifie"]:
        p(f"   - {v}")
    p("⚠️ Corrigé : néant — ce script ne corrige rien ; y reporter les corrections faites "
      "avant ce contrôle (valeur avant → après)")
    non = rep["ecarts"] + rep["a_verifier"] + rep["lacunes"]
    p("🔴 Non résolu :" + (" néant" if not non else ""))
    for e in rep["ecarts"]:
        p(f"   - ÉCART {e}")
    for e in rep["a_verifier"]:
        p(f"   - à vérifier {e}")
    for e in rep["lacunes"]:
        p(f"   - non vérifié {e}")
    p()
    p("| # | Contrôle | Résultat | Détail |")
    p("|---|---|---|---|")
    for num, label, status, detail in rep["checks"]:
        detail = (detail or "").replace("|", "\\|")
        p(f"| {num} | {label} | {status} | {detail} |")
    p()
    p(f"Écarts : {len(rep['ecarts'])} | à vérifier : {len(rep['a_verifier'])} | "
      f"non vérifiés / manuels : {len(rep['lacunes'])}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0].strip(),
        epilog=("Format de --source (JSON) : {\"equipment\": {\"CODE\": n}, \"personnel\": "
                "{\"CODE\": n}} ; facultatifs : \"supplies\": {...} et \"unites\": "
                "{\"<id ou nom>\": {\"equipment\": {...}, \"personnel\": {...}}} pour les "
                "totaux par grande formation. Code de sortie 1 s'il y a des écarts."))
    ap.add_argument("orbat", help="fichier ORBAT JSON")
    ap.add_argument("--source", metavar="totaux.json", help="totaux de la source (JSON, format ci-dessous)")
    ap.add_argument("--at", metavar="DATE", help="état à cette date ISO 8601 (timeline rejouée)")
    ap.add_argument("--unit", metavar="ID_OU_NOM", help="id ou nom de la racine du sous-arbre contrôlé")
    args = ap.parse_args()

    orbat = ol.load(args.orbat)
    if args.at:
        try:
            ol.parse_time(args.at)
        except ValueError as e:
            print(f"❌ --at : {e}", file=sys.stderr)
            sys.exit(2)
    unit = None
    if args.unit:
        unit = ol.find_unit(orbat, args.unit)
        if unit is None:
            print(f"❌ Unité introuvable : {args.unit!r}", file=sys.stderr)
            sys.exit(2)
    source = None
    if args.source:
        try:
            source = load_source(args.source)
        except (OSError, ValueError) as e:
            print(f"❌ --source : {e}", file=sys.stderr)
            sys.exit(2)
    rep = run(orbat, source=source, at=args.at, unit=unit)
    render(rep)
    sys.exit(1 if rep["ecarts"] else 0)


if __name__ == "__main__":
    main()
