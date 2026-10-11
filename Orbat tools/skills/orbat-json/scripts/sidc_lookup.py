#!/usr/bin/env python3
"""
sidc_lookup.py — interroger le dictionnaire SIDC de Florian
(`references/sidc_dictionary.json`, ~125 Ko) sans le lire en entier, et
décoder un sidc complet (20 chiffres, APP-6D / MIL-STD-2525D).

Trois usages :

  python3 sidc_lookup.py TERME [--set NN] [--limit N]
      Recherche plein texte, insensible à la casse et aux accents, dans les
      libellés (signification de l'entité dans `references/sidc.md`, famille
      2525D, exemples de noms d'unités du dictionnaire). Plusieurs mots =
      tous doivent figurer. Une ligne par entité :
          set | entité (6 chiffres) | libellé hiérarchique — ex. : noms…

  python3 sidc_lookup.py --code NNNNNN [--set NN]
      Libellé d'une entité, échelons et exemples attestés au dictionnaire
      (« non attestée » si le dictionnaire ne la contient pas).

  python3 sidc_lookup.py --decode SIDC20
      Décode les 20 chiffres : version, contexte, identité, symbol set,
      statut, QG/TF/leurre, échelon OU mobilité (selon le 1er chiffre des
      positions 9-10), entité, modificateurs ; avertit sur le « mauvais
      précédent » cavalerie connu (`references/sidc.md`, § Entité) et sur une
      entité non attestée au dictionnaire.

Libellé hiérarchique = famille 2525D (2 premiers chiffres : 11 C2, 12
Mouvement et manœuvre, 13 Feux, 14 Protection, 15 Renseignement, 16 Soutien)
› type (4 premiers chiffres + « 00 ») › sous-type, chaque niveau nommé par la
table « Entité » de `references/sidc.md` quand elle le documente (sinon le
code brut). Le dictionnaire, lui, ne contient que des EXEMPLES de noms : ils
servent à reconnaître un usage, jamais à déduire une entité seuls (sidc.md :
les noms génériques HQ, CMD SEC… apparaissent sous presque toutes les entités).

Bibliothèque : search(term, symbol_set=None, limit=20), lookup(entity,
symbol_set=None), decode(sidc) — renvoient des dict (voir docstrings).
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import orbat_lib as ol            # noqa: E402
from new_orbat import IDENTITY    # noqa: E402

REF_DIR = os.path.join(os.path.dirname(HERE), "references")
DICT_PATH = os.path.join(REF_DIR, "sidc_dictionary.json")
SIDC_MD_PATH = os.path.join(REF_DIR, "sidc.md")

# ---------------------------------------------------------------------------
# Tables de décodage (sidc.md § Positions, symbologie.md § 1). Les échelons
# viennent de orbat_lib.ECHELON_LABEL_FR et les identités de
# new_orbat.IDENTITY : pas de copie de ces deux tables ici.
# ---------------------------------------------------------------------------
VERSIONS = {"10": "2525D / APP-6D éd. 1"}
CONTEXTS = {"0": "réalité", "1": "exercice", "2": "simulation"}
IDENTITY_LABEL = {"pending": "en attente (pending)", "inconnu": "inconnu",
                  "ami_presume": "ami présumé", "ami": "ami", "neutre": "neutre",
                  "suspect": "suspect", "hostile": "hostile"}
IDENTITIES = {code: IDENTITY_LABEL.get(name, name) for name, code in IDENTITY.items()}
SYMBOL_SETS = {"10": "unité terrestre", "11": "civil terrestre",
               "15": "équipement terrestre", "20": "installation", "01": "air",
               "30": "mer (surface)", "35": "sous-marin", "05": "espace"}
STATUSES = {"0": "présent", "1": "planifié / anticipé", "2": "présent, pleinement capable",
            "3": "endommagé", "4": "détruit", "5": "plein à capacité"}
HQTFD = {"0": "aucun", "1": "leurre", "2": "QG", "3": "QG leurre", "4": "task force",
         "5": "task force leurre", "6": "QG de task force", "7": "QG de task force leurre"}
MOBILITY = {"31": "roues tout-chemin", "32": "roues tout-terrain", "33": "chenillé",
            "34": "roues + chenilles", "35": "tracté", "36": "rail",
            "37": "animaux de bât", "41": "engin sur neige", "42": "traîneau",
            "51": "barge", "52": "amphibie"}
# Familles d'entités des unités terrestres (symbol set 10), MIL-STD-2525D.
LAND_FAMILIES = {"11": "Commandement et contrôle", "12": "Mouvement et manœuvre",
                 "13": "Feux", "14": "Protection", "15": "Renseignement",
                 "16": "Soutien"}

# Mauvais précédent documenté dans references/sidc.md (§ Entité, encadré
# cavalerie) et symbologie.md § 3.1 bis.
CAVALRY_WORDS = ("cuirass", "cuirrass", "dragon", "chasseur", "spahi", "hussard", "cavaler",
                 "uhlan", "lancier")
BAD_PRECEDENT = {
    "120500": ("120500 = blindés / chars (ellipse). Le dictionnaire contient le "
               "« mauvais précédent » connu : régiments de Cuirassiers, Dragons, "
               "Chasseurs et Spahis codés 120500. Une unité de CAVALERIE prend "
               "121300 (diagonale seule) — ne pas recopier ces entrées "
               "(sidc.md § Entité, symbologie.md § 3.1 bis)."),
    "120501": ("120501 = reconnaissance blindée (ellipse + diagonale), réservée à "
               "de la reco RÉELLEMENT montée sur blindés. Le dictionnaire contient "
               "le « mauvais précédent » connu : 3e Hussards codé 120501. Une unité "
               "de CAVALERIE prend 121300 (diagonale seule) — sidc.md § Entité."),
}
NOTES = {
    "121303": ("121303 (reconnaissance montée, « HM RECON ») : piste pour la "
               "cavalerie à cheval d'avant 1940, À CONFIRMER PAR RENDU avant emploi "
               "(symbologie.md § 5)."),
}

_cache = {}


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------
def _entries():
    """Entrées du dictionnaire {sidc20: {...}} (chargées une fois)."""
    if "entries" not in _cache:
        with open(DICT_PATH, encoding="utf-8") as f:
            _cache["entries"] = json.load(f).get("entries", {})
    return _cache["entries"]


def _strip_md(s):
    return re.sub(r"[*`_]", "", s).strip()


def _head_label(cell):
    """Début d'une cellule de sidc.md : texte avant le premier « — » situé hors
    parenthèses, sans mise en forme Markdown."""
    s = _strip_md(cell)
    depth = 0
    for i, c in enumerate(s):
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and s.startswith(" — ", i):
            return s[:i].strip()
    return s


def entity_labels():
    """{entité: signification} lue dans la table « Entité » de sidc.md
    (dictionnaire vide si le fichier est absent : seuls les codes s'affichent)."""
    if "labels" not in _cache:
        labels = {}
        try:
            with open(SIDC_MD_PATH, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            text = ""
        for m in re.finditer(r"^\|\s*`(\d{6})`\s*\|\s*(.+?)\s*\|\s*$", text, re.M):
            labels.setdefault(m.group(1), _head_label(m.group(2)))
        _cache["labels"] = labels
    return _cache["labels"]


def _attested(symbol_set=None):
    """{(set, entité): {"sidcs": [...], "echelons": [...], "examples": [...]}}."""
    key = ("attested", symbol_set)
    if key not in _cache:
        out = {}
        for sidc, e in _entries().items():
            if len(sidc) != 20:
                continue
            sset, ent = sidc[4:6], sidc[10:16]
            if symbol_set and sset != symbol_set:
                continue
            rec = out.setdefault((sset, ent), {"sidcs": [], "echelons": [], "examples": []})
            rec["sidcs"].append(sidc)
            ech = e.get("echelon")
            if ech and ech != "-" and ech not in rec["echelons"]:
                rec["echelons"].append(ech)
            for ex in e.get("examples", []) or []:
                if ex not in rec["examples"]:
                    rec["examples"].append(ex)
        _cache[key] = out
    return _cache[key]


# ---------------------------------------------------------------------------
# Libellés
# ---------------------------------------------------------------------------
def hierarchy(entity, symbol_set="10"):
    """Liste des niveaux nommés : [famille, type, sous-type] (sans doublon)."""
    # La table « Entité » de sidc.md décrit les unités terrestres (set 10) :
    # ses libellés ne s'appliquent pas aux autres symbol sets.
    labels = entity_labels() if symbol_set == "10" else {}
    entity = str(entity)
    levels = []
    if symbol_set == "10" and entity[:2] in LAND_FAMILIES:
        levels.append(LAND_FAMILIES[entity[:2]])
    type_code = entity[:4] + "00"
    if type_code != entity:
        levels.append(labels.get(type_code, f"type {entity[:4]}"))
        levels.append(labels.get(entity, f"sous-type {entity[4:]}"))
    else:
        levels.append(labels.get(entity, f"type {entity[:4]}" if entity != "000000"
                                 else "générique"))
    return levels


def label(entity, symbol_set="10"):
    return " › ".join(hierarchy(entity, symbol_set))


def _warnings_for(entity, examples=()):
    warns = []
    if entity in BAD_PRECEDENT:
        cav = [x for x in examples if any(w in ol.fold(x) for w in CAVALRY_WORDS)]
        msg = BAD_PRECEDENT[entity]
        if cav:
            msg += " Exemples concernés : " + ", ".join(cav[:5]) + "."
        warns.append(msg)
    if entity in NOTES:
        warns.append(NOTES[entity])
    return warns


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
def search(term, symbol_set=None, limit=20):
    """
    Entités dont le libellé (hiérarchie sidc.md + exemples du dictionnaire)
    contient TOUS les mots de `term` (casse et accents indifférents).
    Renvoie [{"set", "entity", "label", "examples", "matching_examples",
              "echelons", "warnings"}], trié par nombre d'exemples concordants.
    `limit` <= 0 : pas de limite.
    """
    words = [w for w in ol.fold(term).split() if w]
    if not words:
        return []
    results = []
    for (sset, ent), rec in _attested(symbol_set).items():
        lab = label(ent, sset)
        hay_label = ol.fold(lab + " " + ent)
        matching = [x for x in rec["examples"]
                    if all(w in ol.fold(x) or w in hay_label for w in words)
                    and any(w in ol.fold(x) for w in words)]
        if not (all(w in hay_label for w in words) or matching):
            continue
        results.append({"set": sset, "entity": ent, "label": lab,
                        "examples": rec["examples"], "matching_examples": matching,
                        "echelons": rec["echelons"],
                        "warnings": _warnings_for(ent, rec["examples"])})
    results.sort(key=lambda r: (-len(r["matching_examples"]), r["set"], r["entity"]))
    return results[:limit] if limit and limit > 0 else results


def lookup(entity, symbol_set=None):
    """
    Informations sur une entité (6 chiffres). Renvoie une liste (une entrée
    par symbol set où elle est attestée ; à défaut une seule entrée, set 10
    ou `symbol_set`, avec "attested": False) :
      [{"set", "entity", "label", "attested", "echelons", "examples",
        "sidcs", "warnings"}]
    Lève ValueError si `entity` n'a pas 6 chiffres.
    """
    entity = str(entity).strip()
    if not re.fullmatch(r"\d{6}", entity):
        raise ValueError(f"entité attendue sur 6 chiffres : {entity!r}")
    out = []
    for (sset, ent), rec in sorted(_attested(symbol_set).items()):
        if ent == entity:
            out.append({"set": sset, "entity": ent, "label": label(ent, sset),
                        "attested": True, "echelons": rec["echelons"],
                        "examples": rec["examples"], "sidcs": rec["sidcs"],
                        "warnings": _warnings_for(ent, rec["examples"])})
    if not out:
        sset = symbol_set or "10"
        out.append({"set": sset, "entity": entity, "label": label(entity, sset),
                    "attested": False, "echelons": [], "examples": [], "sidcs": [],
                    "warnings": _warnings_for(entity) + [
                        "entité non attestée au sidc_dictionary.json : la signaler à "
                        "Florian et confirmer par rendu (symbologie.md § 5)."]})
    return out


def decode(sidc):
    """
    Décode un sidc de 20 chiffres. Renvoie un dict :
      {"sidc", "version", "context", "identity", "symbol_set", "status",
       "hq_tf_dummy", "echelon" | "mobility", "amplifier" (champ 9-10 brut),
       "entity", "entity_label", "mod1", "mod2", "dictionary" (entrée exacte
       ou None), "attested" (entité vue au dictionnaire pour ce set),
       "warnings": [...]}
    Chaque champ décodé est un couple (code, libellé). Lève ValueError si le
    sidc n'est pas fait de 20 chiffres.
    """
    s = str(sidc).strip()
    if not re.fullmatch(r"\d{20}", s):
        raise ValueError(f"sidc invalide (20 chiffres attendus) : {sidc!r}")
    warns = []
    ver, ctx, ident, sset = s[0:2], s[2], s[3], s[4:6]
    status, hq, amp, ent, m1, m2 = s[6], s[7], s[8:10], s[10:16], s[16:18], s[18:20]

    def field(code, table, what):
        lab = table.get(code)
        if lab is None:
            warns.append(f"{what} {code!r} inconnu(e)")
            lab = "?"
        return (code, lab)

    out = {"sidc": s,
           "version": field(ver, VERSIONS, "version"),
           "context": field(ctx, CONTEXTS, "contexte"),
           "identity": field(ident, IDENTITIES, "identité"),
           "symbol_set": field(sset, SYMBOL_SETS, "symbol set"),
           "status": field(status, STATUSES, "statut"),
           "hq_tf_dummy": field(hq, HQTFD, "code QG/TF/leurre"),
           "amplifier": amp}
    if amp[0] in "12":
        lab = ol.ECHELON_LABEL_FR.get(amp)
        if lab is None:
            warns.append(f"échelon {amp!r} inconnu")
        out["echelon"] = (amp, lab or "?")
    elif amp == "00":
        out["echelon"] = (amp, "non précisé")
    else:
        lab = MOBILITY.get(amp)
        if lab is None:
            warns.append(f"mobilité / amplificateur {amp!r} inconnu(e)")
        out["mobility"] = (amp, lab or "?")
        if sset == "10":
            warns.append("positions 9-10 en mobilité (matériel) sur un symbol set "
                         "« unité terrestre » : un échelon (1x/2x) est attendu.")
    out["entity"] = ent
    out["entity_label"] = label(ent, sset)
    out["mod1"] = (m1, "aucun" if m1 == "00" else "secteur 1 — capacité")
    out["mod2"] = (m2, "aucun" if m2 == "00" else "secteur 2 — mobilité")

    entry = _entries().get(s)
    out["dictionary"] = entry
    rec = _attested(sset).get((sset, ent))
    out["attested"] = rec is not None
    examples = list((entry or {}).get("examples", []) or []) or (rec or {}).get("examples", [])
    warns += _warnings_for(ent, examples)
    if rec is None:
        warns.append(f"entité {ent} non attestée au sidc_dictionary.json pour le set "
                     f"{sset} : à signaler à Florian, confirmer par rendu (symbologie.md § 5).")
    out["warnings"] = warns
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _short_examples(rec, n=4):
    ex = rec.get("matching_examples") or rec.get("examples") or []
    more = len(ex) - n
    txt = ", ".join(ex[:n]) + (f" (+{more})" if more > 0 else "")
    return f" — ex. : {txt}" if txt else ""


def _print_search(results, term):
    if not results:
        print(f"Aucune entité pour « {term} ».")
        return
    for r in results:
        flag = " ⚠️" if r["warnings"] else ""
        print(f"{r['set']} | {r['entity']} | {r['label']}{flag}{_short_examples(r)}")
    if any(r["warnings"] for r in results):
        print("\n⚠️ = avertissement : relancer avec --code <entité> pour le détail.")


def _print_lookup(rows):
    for r in rows:
        print(f"{r['set']} | {r['entity']} | {r['label']}")
        if r["attested"]:
            print(f"  attestée au dictionnaire : {len(r['sidcs'])} sidc ; échelons : "
                  + (", ".join(r["echelons"]) or "-"))
            print("  exemples : " + ", ".join(r["examples"][:12])
                  + (f" (+{len(r['examples']) - 12})" if len(r["examples"]) > 12 else ""))
        for w in r["warnings"]:
            print(f"  ⚠️  {w}")


def _print_decode(d):
    s = d["sidc"]
    print(f"{s[0:2]}·{s[2]}·{s[3]}·{s[4:6]}·{s[6]}·{s[7]}·{s[8:10]}·{s[10:16]}·{s[16:18]}·{s[18:20]}")
    rows = [("1-2   version", d["version"]), ("3     contexte", d["context"]),
            ("4     identité", d["identity"]), ("5-6   symbol set", d["symbol_set"]),
            ("7     statut", d["status"]), ("8     QG/TF/leurre", d["hq_tf_dummy"])]
    if "echelon" in d:
        rows.append(("9-10  échelon", d["echelon"]))
    else:
        rows.append(("9-10  mobilité", d["mobility"]))
    rows += [("11-16 entité", (d["entity"], d["entity_label"])),
             ("17-18 mod. 1", d["mod1"]), ("19-20 mod. 2", d["mod2"])]
    for lab, (code, txt) in rows:
        print(f"  {lab:<18} {code:<7} {txt}")
    if d["dictionary"]:
        print("  au dictionnaire : " + ", ".join(d["dictionary"].get("examples", [])[:8]))
    else:
        print("  au dictionnaire : sidc exact absent"
              + (" (entité attestée sous d'autres sidc : --code "
                 + d["entity"] + ")" if d["attested"] else ""))
    for w in d["warnings"]:
        print(f"  ⚠️  {w}")


def main():
    ap = argparse.ArgumentParser(
        description="Recherche dans le dictionnaire SIDC (references/sidc_dictionary.json) "
                    "et décodage d'un sidc 20 chiffres.",
        epilog="Exemples : sidc_lookup.py hussards --set 10 | "
               "sidc_lookup.py --code 121300 | sidc_lookup.py --decode 10031000151211005600")
    ap.add_argument("terme", nargs="*", help="terme(s) recherché(s) dans les libellés "
                    "(tous les mots doivent figurer ; casse et accents indifférents)")
    ap.add_argument("--set", dest="symbol_set", metavar="NN",
                    help="limiter à un symbol set (positions 5-6, ex. 10 = unité terrestre)")
    ap.add_argument("--limit", type=int, default=20, metavar="N",
                    help="nombre maximal de résultats de recherche (défaut 20, 0 = tous)")
    ap.add_argument("--code", metavar="NNNNNN", help="libellé et usages d'une entité (6 chiffres)")
    ap.add_argument("--decode", metavar="SIDC20", help="décoder un sidc complet (20 chiffres)")
    args = ap.parse_args()

    modes = sum(bool(x) for x in (args.terme, args.code, args.decode))
    if modes != 1:
        ap.error("donner exactement un TERME, --code ou --decode")
    if args.symbol_set and not re.fullmatch(r"\d{2}", args.symbol_set):
        ap.error("--set attend 2 chiffres (ex. 10)")
    try:
        if args.decode:
            _print_decode(decode(args.decode))
        elif args.code:
            _print_lookup(lookup(args.code, args.symbol_set))
        else:
            term = " ".join(args.terme)
            _print_search(search(term, args.symbol_set, args.limit), term)
    except ValueError as e:
        sys.exit(f"❌ {e}")


if __name__ == "__main__":
    main()
