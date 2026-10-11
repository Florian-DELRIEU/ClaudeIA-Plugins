#!/usr/bin/env python3
"""
short_names.py — dérive le `shortName` des unités d'un ORBAT JSON
(orbat-mapper.app) selon references/naming.md : Règle 2, § 7.5, § 7.7.

    python3 short_names.py orbat.json [--all] [--dry-run] [--output OUT]

  (défaut)   ne remplit que les unités SANS shortName ;
  --all      recalcule le shortName de toutes les unités ;
  --dry-run  affiche les changements sans rien écrire ;
  --output   écrit dans OUT (sinon : en place), puis valide le résultat
             (contrôles de validate.py) — code de sortie 1 s'il reste une ERREUR.

Forme produite (§ 7.5) : `{numéro ou lettre} {ÉCHELON}-{TYPE}[ — garnison][ Ø]`
  « 23e Compagnie d'Infanterie »          -> `23e CIE-INF`
  « Bataillon "A" Blindé »                -> `"A" BT-ARM`
  « 1ère Division Blindée — Allemagne »   -> `1ère DIV-ARM — Allemagne`
  « Compagnie de commandement et de soutien » -> `CIE-HQ.SPT`

Comment (implémentation type de naming.md) : une passe finale sur l'arbre ; le
nom est lu par une liste ordonnée de motifs, du plus spécifique au plus
générique (« infanterie blindée » avant « infanterie »), après extraction du
suffixe « Ø » (Règle 3) et d'une garnison « — … » (Règle 2), réinjectés à la fin.
  - ÉCHELON : premier mot d'échelon du nom (FR, ou EN de la Règle 4 —
    `orbat_lib.EN_SOURCE_WORD_TO_ECHELON`), à défaut l'échelon du sidc
    (positions 9-10). Code lu dans `acronyme/references/groupements.md`
    § Échelons (`orbat_lib.load_echelon_codes`).
  - TYPE(S) : mots de type de formation, codes lus dans groupements.md
    § Types d'unité (état-major / commandement : `HQ`, lu dans
    `acronyme/references/terrestres.md`). Plusieurs types : joints par « . »
    (grammaire du système), dans l'ordre du nom.
  - NUMÉRO : ordinal ou lettre accolé(e) au mot d'échelon (« 1ère », « 2e »,
    « 1st », « 41 », « "A" », « Compagnie B »), rendu à la française
    (`1er`/`1ère` selon le genre de l'échelon, `2e`, `"A"`).
  - § 7.7 : la formation mère (nom et shortName du parent et des ancêtres)
    est retirée du nom avant lecture — jamais reprise dans le shortName ; une
    garnison identique à celle du parent n'est pas répétée. Les noms qui
    répètent leur formation mère sont signalés (à corriger dans `name`).
  - Un nom déjà écrit en codes (« 1er BT-INF ») est reconnu tel quel.

AUCUN code n'est inventé : la table des mots ci-dessous ne mappe que des MOTS
vers des NOTIONS ; le code de chaque notion est relu dans le skill `acronyme` à
chaque lancement (échec bruyant s'il est introuvable). Un mot non reconnu n'est
jamais abrégé à la volée : l'unité est signalée « à vérifier » (mots non
traduits), ou « non dérivable » (rien d'exploitable) et laissée sans shortName —
cas naming.md § 7.2, à soumettre à Florian.

Limite : « Section » est lue à la française (SEC) ; dans un nom anglais
(ordinal 1st/2nd…, Company, Platoon…) elle est lue escouade (SQ), piège FR/EN de
la Règle 4. Les numéros romains ne sont repris que suffixés (« IIe Corps »).

Bibliothèque : short_name_for(unit, parent=None, ancestors=(), codes=None) -> str|None ;
derive(...) -> dict détaillé ; repeats_parent(...) ; name_echelon(...) ; load_codes().
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbat_lib as ol  # noqa: E402

GARRISON_SEP = " — "
EMPTY_TAG = "Ø"

# ---------------------------------------------------------------------------
# Mots -> notions (PAS de codes ici : source unique = skill `acronyme`).
# Motifs appliqués au nom « replié » (sans accents, minuscules, ponctuation
# remplacée par des espaces), du plus spécifique au plus générique.
# ---------------------------------------------------------------------------
ECHELON_WORDS = [
    (r"groupement tactique interarmes?|gtia", "groupement tactique interarme"),
    (r"groupe d armees", "groupe d'armees"),
    (r"corps d armee|corps", "corps d'armee"),
    (r"armee", "armee"),
    (r"division", "division"),
    (r"brigade", "brigade"),
    (r"regiment", "regiment"),
    (r"bataillon", "bataillon"),
    (r"compagnie", "compagnie"),
    (r"escadron|escadrille", "escadron"),
    (r"batterie", "batterie"),
    (r"peloton", "peloton"),
    (r"section", "section"),
    (r"escouade", "escouade"),
    (r"equipe", "equipe"),
    (r"binome", "binome"),
    (r"detachement", "detachement"),
    (r"groupe", "groupe"),
    (r"task force", "task force"),
    (r"legion", "legion"),
    (r"croisade", "croisade"),
    (r"horde", "horde"),
    # formes anglaises sans ambiguïté (Battalion, Company… : orbat_lib, Règle 4)
    (r"army group", "groupe d'armees"),
    (r"army", "armee"),
    (r"squad", "escouade"),
    (r"team", "equipe"),
]

TYPE_WORDS = [
    (r"infanterie blindee lourde", "infanterie blindee lourde"),
    (r"infanterie blindee", "infanterie blindee"),
    (r"infanterie legere|light infantry", "infanterie legere"),
    (r"infanterie de marine", "marines"),
    (r"infanterie mecanisee|mechani[sz]ed infantry", "mecanise"),
    (r"infanterie (?:motorisee|portee)|motori[sz]ed infantry", "motorise"),
    (r"genie pontonnier", "genie pontonnier"),
    (r"genie (?:de )?franchissement", "genie franchissement"),
    (r"genie (?:de )?fortification", "genie fortification"),
    (r"genie d assaut", "genie assaut"),
    (r"genie (?:de )?minage", "genie minage"),
    (r"forces speciales|special forces", "forces speciales"),
    (r"police militaire|military police", "police militaire"),
    (r"armes combinees|interarmes|combined arms", "armes combinees"),
    (r"intervention rapide", "intervention rapide"),
    (r"transport de troupes", "transport troupes"),
    (r"etat major|quartier general|commandement|headquarters|hq|qg", "commandement"),
    (r"infanterie|infantry", "infanterie"),
    (r"chars?|blindee?s?|armou?r(?:ed)?|tanks?", "blindes"),
    (r"mecanisee?s?|mechani[sz]ed", "mecanise"),
    (r"motorisee?s?|motori[sz]ed", "motorise"),
    (r"artillerie|artillery", "artillerie"),
    (r"genie|engineers?", "genie"),
    (r"sanitaires?", "sanitaire"),
    (r"medicale?s?|medicaux|medical", "medical"),
    (r"transmissions?|signals?", "transmission"),
    (r"parachutistes?|parachute", "parachutistes"),
    (r"aeroportee?s?|airborne", "aeroportee"),
    (r"logistiques?|logistics?", "logistique"),
    (r"helicopteres?", "helicoptere"),
    (r"acquisition", "acquisition"),
    (r"reserves?", "reserves"),
    (r"administratif|administrative", "administratif"),
    (r"materiel", "materiel"),
    (r"marines?", "marines"),
    (r"montagne|mountain", "montagne"),
    (r"transports?", "transport"),
    (r"milices?", "milice"),
    (r"partisans?", "partisans"),
    (r"reconnaissance|recon", "reconnaissance"),
    (r"gendarmes?|gendarmerie", "gendarmes"),
    (r"cavalerie|cavalry", "cavalerie"),
    (r"maintenance", "maintenance"),
    (r"hopital", "hopital"),
    (r"drones?", "drone"),
    (r"forteresse", "forteresse"),
    (r"jungle", "jungle"),
    (r"arctique", "arctique"),
    (r"desert", "desert"),
    (r"soutien|support", "support"),
    (r"urbain", "urbain"),
    (r"assaut", "assaut"),
    (r"defense", "defense"),
    (r"rupture", "rupture"),
    (r"extraction", "extraction"),
]

FEMININE = {"armee", "division", "brigade", "compagnie", "batterie", "section",
            "escouade", "equipe", "task force", "legion", "croisade", "horde"}
STOPWORDS = {"de", "d", "du", "des", "la", "le", "l", "les", "et", "a", "au", "aux",
             "en", "sur", "pour", "of", "the", "and", "n", "no"}
EN_MARKERS = re.compile(
    r"\b(?:\d+(?:st|nd|rd|th|d)|company|battalion|platoon|squad|team|infantry|"
    r"armou?red|tank|artillery|engineers?|signals|headquarters|troop|battery|"
    r"detachment|coy|bn|plt|bty|mechani[sz]ed|motori[sz]ed)\b")

_PUNCT = set("-'_/.,;:()[]\"«»“”!?#&+")


# ---------------------------------------------------------------------------
# Codes (lus dans le skill acronyme)
# ---------------------------------------------------------------------------
def _rows(text, heading=None):
    """Lignes de code (acronyme/scripts/tables.py, deux formats) : (officiel,
    [significations repliées]). `heading` limite à une section."""
    T = ol.acronyme_tables()
    if heading:
        text = T.section(text, heading)
        if text is None:
            return
    for table in T.parse_text(text):
        for row in table.rows:
            yield row.officiel, [ol.fold(x).strip() for x in row.meaning.split("/") if x.strip()]


def load_codes(groupements_path=None, terrestres_path=None):
    """
    {"echelons": {notion repliée: code}, "types": {notion repliée: code}}.
    Échelons : orbat_lib.load_echelon_codes (groupements.md § Échelons).
    Types : groupements.md § Types d'unité (formation), plus `commandement`
    lu dans terrestres.md. Lève FileNotFoundError si le skill `acronyme` est
    introuvable — volontaire (source unique, naming.md).
    """
    echelons = {ol.fold(k).strip(): v
                for k, v in ol.load_echelon_codes(groupements_path).items()}
    gpath = groupements_path or ol.default_groupements_path()
    with open(gpath, encoding="utf-8") as f:
        gtext = f.read()
    types = {}
    for code, meanings in _rows(gtext, "## Types d'unité (formation)"):
        for m in meanings:
            if code and m and m not in types:
                types[m] = code
    tpath = terrestres_path or os.path.join(os.path.dirname(gpath), "terrestres.md")
    if "commandement" not in types and os.path.exists(tpath):
        with open(tpath, encoding="utf-8") as f:
            for code, meanings in _rows(f.read()):
                if code and "commandement" in meanings:
                    types["commandement"] = code
                    break
    return {"echelons": echelons, "types": types}


def _code_of(table, notion):
    """Code d'une notion : clé exacte, sinon clé unique qui la prolonge
    (« corps » -> « corps d'armee »)."""
    if notion in table:
        return table[notion]
    longer = [k for k in table if k.startswith(notion + " ")]
    return table[longer[0]] if len(longer) == 1 else None


# ---------------------------------------------------------------------------
# Lecture d'un nom
# ---------------------------------------------------------------------------
def _shadow(text):
    """Nom replié caractère par caractère (MÊME longueur que l'original, pour
    reporter les positions) : sans accents, minuscules, ponctuation -> espace."""
    out = []
    for c in text:
        f = ol.fold(c)
        f = f[0] if f else " "
        out.append(" " if (f in _PUNCT or not f.isalnum() and not f.isspace()) else f)
    return "".join(out)


def _bounded(pattern):
    return re.compile(r"(?<![a-z0-9])(?:%s)(?![a-z0-9])" % pattern)


_ECH_RE = [(_bounded(p), n) for p, n in ECHELON_WORDS]
_TYPE_RE = [(_bounded(p), n) for p, n in TYPE_WORDS]


def _en_echelon_words(english):
    out = []
    for pat, notion in ol.EN_SOURCE_WORD_TO_ECHELON:
        word = pat.replace(r"\b", "").lower()
        if word in ("section", "sect") and not english:
            continue                    # « Section » française : déjà en table FR
        out.append((_bounded(re.escape(word)), ol.fold(notion)))
    return out


def _free(spans, a, b):
    return all(b <= s or a >= e for s, e in spans)


def _strip_tag_garrison(name):
    core = (name or "").strip()
    tag = False
    if core.endswith(EMPTY_TAG):
        core, tag = core[:-len(EMPTY_TAG)].rstrip(), True
    garrison = None
    if GARRISON_SEP in core:
        core, garrison = core.split(GARRISON_SEP, 1)
        core, garrison = core.strip(), garrison.strip()
    return core, garrison, tag


_AMBIGUOUS_RE = [_bounded(p.replace(r"\b", "").lower()) for p in ol.EN_AMBIGUOUS_ECHELON_WORDS]


def _longest_hits(hits):
    """Retire les occurrences recouvertes par une occurrence plus longue : un
    motif spécifique (« groupe d'armées ») l'emporte toujours sur un motif plus
    court qu'il contient (« groupe »), qu'il ait un code ou non."""
    keep = []
    for h in hits:
        if not any(o is not h and o[0] <= h[0] and h[1] <= o[1] and (o[1] - o[0]) > (h[1] - h[0])
                   for o in hits):
            keep.append(h)
    return keep


def _match_vocab(shadow, english, codes, taken):
    """Repère échelon et types dans le nom replié. Renvoie
    (échelon (notion, code, span, statut) ou None, [(span, code)], spans consommés).
    statut : "ok" ; "sans_code" (motif reconnu mais notion absente du skill
    acronyme, ex. groupe d'armées — jamais de repli sur un motif plus court) ;
    "ambigu" (Troop/Squadron : échelon à lire dans le sidc)."""
    spans = list(taken)
    ech = None
    hits = []
    for rx, notion in _ECH_RE + _en_echelon_words(english):
        if notion == "section" and english:
            notion = "escouade"          # piège FR/EN, Règle 4
        code = _code_of(codes["echelons"], notion)
        for m in rx.finditer(shadow):
            if _free(spans, m.start(), m.end()):
                hits.append((m.start(), m.end(), notion, code,
                             "ok" if code else "sans_code"))
    for rx in _AMBIGUOUS_RE:
        for m in rx.finditer(shadow):
            if _free(spans, m.start(), m.end()):
                hits.append((m.start(), m.end(), None, None, "ambigu"))
    hits = _longest_hits(hits)
    if hits:
        s, e, notion, code, status = min(hits, key=lambda h: (h[0], -(h[1] - h[0])))
        ech = (notion, code, (s, e), status)
        spans.append((s, e))
    types, blocked = [], []
    t_hits = []
    for rx, notion in _TYPE_RE:
        code = _code_of(codes["types"], notion)
        for m in rx.finditer(shadow):
            if _free(spans, m.start(), m.end()):
                t_hits.append((m.start(), m.end(), code))
    for s, e, code in sorted(_longest_hits(t_hits), key=lambda h: (h[0], -(h[1] - h[0]))):
        if not _free(spans + blocked, s, e):
            continue
        if code:
            spans.append((s, e))
            types.append(((s, e), code))
        else:
            blocked.append((s, e))       # motif sans code : ses mots restent « non traduits »
    return ech, types, spans


def _distinctive(text, codes):
    """Vrai si `text` contient autre chose que des mots d'échelon/type et des
    mots vides (nombre, nom propre, sigle…) : seul un tel nom de parent peut
    être « répété » au sens du § 7.7."""
    sh = _shadow(text)
    english = bool(EN_MARKERS.search(sh))
    _, _, spans = _match_vocab(sh, english, codes, [])
    for m in re.finditer(r"[a-z0-9]+", sh):
        if _free(spans, m.start(), m.end()) and m.group() not in STOPWORDS:
            return True
    return False


def _parent_refs(parent, ancestors):
    refs = []
    for node in ([parent] if parent else []) + list(ancestors or []):
        if not node:
            continue
        if isinstance(node, str):
            cands = [node]
        else:
            cands = [node.get("name"), node.get("shortName")]
        for c in cands:
            core, _, _ = _strip_tag_garrison(c or "")
            if len(core) >= 2 and core not in refs:
                refs.append(core)
    return refs


def _find_refs(name_core, refs, codes):
    """Spans du nom (replié) occupés par une référence à la formation mère."""
    sh = _shadow(name_core)
    found, spans = [], []
    for ref in sorted(refs, key=len, reverse=True):
        words = re.findall(r"[a-z0-9]+", _shadow(ref))
        if not words or not _distinctive(ref, codes):
            continue
        rx = _bounded(r"\s+".join(re.escape(w) for w in words))
        for m in rx.finditer(sh):
            if (m.end() - m.start()) >= len(sh.strip()):
                continue                       # le nom EST la référence
            if _free(spans, m.start(), m.end()):
                spans.append((m.start(), m.end()))
                if ref not in found:
                    found.append(ref)
    return found, spans


_ORD_FR = re.compile(r"(?<![\w])(\d+)\s?(ère|ere|re|er|ème|eme|è|e|°)(?![\w])", re.I)
# 2d / 3d : forme de l'US Army (orbat-nommage, nations.md US-11), à côté de 2nd / 3rd.
_ORD_EN = re.compile(r"(?<![\w])(\d+)(st|nd|rd|th|d)(?![\w])", re.I)
_ROMAN = re.compile(r"(?<![\w])([IVXLC]+)(er|ème|e)(?![\w])")
_PLAIN = re.compile(r"(?<![\w.,/])(\d+)(?![\w.,/])")
_LETTER_Q = re.compile(r"[\"«“]\s*([A-Z])\s*[\"»”]")
_LETTER = re.compile(r"(?<![\w'’\"«“])([A-Z])(?![\w'’\"»”])")


def _ordinal(n, feminine):
    return ("1ère" if feminine else "1er") if n == 1 else f"{n}e"


def _numbers(core, taken):
    """Candidats numéro : [(start, end, rendu(feminine)->str, sorte)]."""
    out = []

    def add(m, kind, render):
        if _free(taken, m.start(), m.end()) and _free([(s, e) for s, e, _, _ in out],
                                                      m.start(), m.end()):
            out.append((m.start(), m.end(), render, kind))

    for m in _ORD_FR.finditer(core):
        n, suf = int(m.group(1)), ol.fold(m.group(2))
        if n == 1 and suf == "er":
            add(m, "ord", lambda f: "1er")
        elif n == 1 and suf in ("ere", "re"):
            add(m, "ord", lambda f: "1ère")
        else:
            add(m, "ord", lambda f, n=n: _ordinal(n, f))
    for m in _ORD_EN.finditer(core):
        add(m, "ord", lambda f, n=int(m.group(1)): _ordinal(n, f))
    for m in _ROMAN.finditer(core):
        add(m, "ord", lambda f, t=m.group(0): t)
    for m in _LETTER_Q.finditer(core):
        add(m, "letter", lambda f, L=m.group(1): f'"{L}"')
    for m in _PLAIN.finditer(core):
        add(m, "plain", lambda f, n=int(m.group(1)): _ordinal(n, f))
    for m in _LETTER.finditer(core):
        add(m, "bare", lambda f, L=m.group(1): f'"{L}"')
    return sorted(out, key=lambda x: x[0])


def _code_tokens(core, codes, taken):
    """Noms déjà écrits en codes (« 1er BT-INF », « CIE-HQ.SPT ») :
    renvoie (échelon (notion, code, span) ou None, [(span, code)], spans)."""
    ech_codes = set(codes["echelons"].values())
    type_codes = set(codes["types"].values())
    ech, types, spans = None, [], []
    for m in re.finditer(r"[A-Z][A-Z0-9.]*(?:-[A-Z0-9.]+)*", core):
        tok = m.group()
        if len(tok) < 2 or not _free(taken, m.start(), m.end()):
            continue
        if m.start() > 0 and core[m.start() - 1].isalnum():
            continue
        if m.end() < len(core) and core[m.end()].isalnum():
            continue
        parts = tok.split("-")
        head, rest = parts[0], parts[1:]
        subtypes = [p for r in rest for p in r.split(".")]
        if head in ech_codes and ech is None and all(p in type_codes for p in subtypes):
            ech = (None, head, (m.start(), m.end()), "ok")
            types += [((m.start(), m.end()), r) for r in rest]
            spans.append((m.start(), m.end()))
        elif not rest and all(p in type_codes for p in head.split(".")) and head not in ech_codes:
            types.append(((m.start(), m.end()), head))
            spans.append((m.start(), m.end()))
    return ech, types, spans


def _sidc_notion(unit):
    code = ol.echelon_of(unit) if isinstance(unit, dict) else None
    lab = ol.ECHELON_LABEL_FR.get(code or "")
    return (ol.fold(lab), code) if lab else (None, None)


def derive(unit, parent=None, ancestors=(), codes=None):
    """
    Dérive le shortName d'une unité. `parent` : unité (ou nom) mère directe ;
    `ancestors` : autres ancêtres (unités ou noms) dont la répétition est
    interdite (§ 7.7) ; `codes` : résultat de load_codes() (lu si None).
    Renvoie un dict : short_name (str ou None), echelon (code, origine
    "nom"|"sidc"|None), types, number, garrison, empty_tag, residual (mots non
    traduits), parent_repeated (références à la formation mère trouvées dans
    le nom), reason (si non dérivable).
    """
    codes = codes or load_codes()
    name = unit.get("name") if isinstance(unit, dict) else str(unit)
    core, garrison, tag = _strip_tag_garrison(name or "")
    res = {"short_name": None, "echelon": (None, None), "types": [], "number": None,
           "garrison": None, "empty_tag": tag, "residual": [], "parent_repeated": [],
           "reason": None}
    if not core:
        res["reason"] = "nom vide"
        return res

    refs, ref_spans = _find_refs(core, _parent_refs(parent, ancestors), codes)
    res["parent_repeated"] = refs

    shadow = _shadow(core)
    english = bool(EN_MARKERS.search(shadow))
    c_ech, c_types, c_spans = _code_tokens(core, codes, ref_spans)
    taken = ref_spans + c_spans
    w_ech, w_types, spans = _match_vocab(shadow, english, codes, taken)

    ech = c_ech or w_ech
    if c_ech and w_ech and w_ech[2][0] < c_ech[2][0]:
        ech = w_ech
    if ech is c_ech and w_ech:
        spans = [s for s in spans if s != w_ech[2]]   # mot d'échelon non retenu : résiduel
    types = sorted(c_types + w_types)
    ech_origin = "nom" if ech else None
    notion = ech[0] if ech else None
    ech_code = ech[1] if ech else None
    ech_span = ech[2] if ech else None
    status = ech[3] if ech else None
    if status == "sans_code":
        # motif spécifique reconnu (« groupe d'armées ») dont la notion n'a pas
        # de code : jamais de repli sur un motif plus court (« groupe » -> GRP).
        word = core[ech_span[0]:ech_span[1]]
        res["residual"] = [word]
        res["reason"] = (f"échelon « {word} » reconnu mais sans code dans le skill acronyme — "
                         "à vérifier, pas de repli sur un mot plus court (naming.md § 7.2)")
        return res
    if status == "ambigu":
        # Troop / Squadron : sens selon l'armée (orbat-nommage) -> échelon du sidc
        word = core[ech_span[0]:ech_span[1]]
        notion, _ = _sidc_notion(unit)
        ech_code = _code_of(codes["echelons"], notion) if notion else None
        if not ech_code:
            res["residual"] = [word]
            res["reason"] = (f"« {word} » : échelon ambigu (US ≠ UK, voir orbat-nommage) et pas "
                             "d'échelon exploitable au sidc — à vérifier")
            return res
        ech_origin = "sidc"
    elif ech and notion is None:   # code d'échelon écrit tel quel : retrouver sa notion
        notion = next((k for k, v in codes["echelons"].items() if v == ech_code), None)
    if not ech:
        notion, sidc_code = _sidc_notion(unit)
        if notion:
            ech_code = _code_of(codes["echelons"], notion)
            ech_origin = "sidc" if ech_code else None
    feminine = (notion or "") in FEMININE

    # numéro : accolé au mot d'échelon, sinon un ordinal ou une lettre entre
    # guillemets n'importe où, sinon un nombre en tête du nom.
    num_spans = []
    cands = _numbers(core, spans)
    pick = None
    if ech_span is not None:          # mot d'échelon du nom (même ambigu) : numéro accolé
        es, ee = ech_span
        before = [c for c in cands if c[1] <= es and not core[c[1]:es].strip()]
        after = [c for c in cands if c[0] >= ee and not core[ee:c[0]].strip()]
        pick = (before or after or [None])[0]
    if pick is None:
        anywhere = [c for c in cands if c[3] in ("ord", "letter")]
        lead = [c for c in cands if c[3] == "plain" and not core[:c[0]].strip()]
        pick = (anywhere or lead or [None])[0]
    if pick:
        res["number"] = pick[2](feminine)
        num_spans.append((pick[0], pick[1]))

    type_codes = []
    for _, code in types:
        for c in code.split("."):
            if c not in type_codes:
                type_codes.append(c)
    res["types"] = type_codes
    res["echelon"] = (ech_code, ech_origin)

    # mots non traduits (signalés, jamais abrégés à la volée)
    used = spans + c_spans + ref_spans + num_spans
    for m in re.finditer(r"[a-z0-9]+", shadow):
        if _free(used, m.start(), m.end()) and m.group() not in STOPWORDS:
            res["residual"].append(core[m.start():m.end()])

    if ech_code and type_codes:
        body = f"{ech_code}-{'.'.join(type_codes)}"
    elif ech_code:
        body = ech_code
    elif type_codes:
        body = ".".join(type_codes)
    else:
        res["reason"] = ("ni échelon ni type reconnus dans le nom (ni échelon au sidc) — "
                         "aucun code à reprendre du skill acronyme (naming.md § 7.2)")
        return res
    sn = f"{res['number']} {body}" if res["number"] else body
    if garrison:
        p_garr = None
        if isinstance(parent, dict):
            p_garr = _strip_tag_garrison(parent.get("name") or "")[1]
        if garrison != p_garr:
            res["garrison"] = garrison
            sn += GARRISON_SEP + garrison
    if tag:
        sn += " " + EMPTY_TAG
    res["short_name"] = sn
    return res


def short_name_for(unit, parent=None, ancestors=(), codes=None):
    """shortName dérivé (naming.md Règle 2, § 7.5, § 7.7), ou None si rien
    d'exploitable — jamais une abréviation inventée. Voir derive()."""
    return derive(unit, parent, ancestors, codes)["short_name"]


def repeats_parent(unit, parent=None, ancestors=(), codes=None):
    """Références à la formation mère trouvées dans `name` (§ 7.7) ; [] si aucune."""
    codes = codes or load_codes()
    core, _, _ = _strip_tag_garrison(unit.get("name") or "")
    return _find_refs(core, _parent_refs(parent, ancestors), codes)[0]


def name_echelon(name, codes=None):
    """Notion d'échelon (repliée, ex. « compagnie ») lue dans un nom, ou None."""
    codes = codes or load_codes()
    core, _, _ = _strip_tag_garrison(name or "")
    sh = _shadow(core)
    c_ech, _, c_spans = _code_tokens(core, codes, [])
    w_ech, _, _ = _match_vocab(sh, bool(EN_MARKERS.search(sh)), codes, c_spans)
    if c_ech and (not w_ech or c_ech[2][0] < w_ech[2][0]):
        return next((k for k, v in codes["echelons"].items() if v == c_ech[1]), None)
    return w_ech[0] if w_ech else None


# ---------------------------------------------------------------------------
# Parcours
# ---------------------------------------------------------------------------
def walk(orbat):
    """(unité, parent direct (unité ou group), [ancêtres plus lointains]) pour
    toutes les unités de l'arbre (les groups de tête de side ne sont pas des
    unités : pas de shortName, mais leur nom compte comme formation mère)."""
    def rec(u, chain):
        parent = chain[-1] if chain else None
        yield u, parent, chain[:-1]
        for su in u.get("subUnits", []) or []:
            yield from rec(su, chain + [u])

    for side in orbat.get("sides", []) or []:
        for u in side.get("units", []) or []:
            if u.get("name") is None and "rootUnitName" in u:
                continue
            yield from rec(u, [])
        for g in side.get("groups", []) or []:
            for su in g.get("subUnits", []) or []:
                yield from rec(su, [g])


def apply(orbat, recompute=False, codes=None):
    """Pose les shortName (en place). Renvoie le journal :
    {"changes": [(unité, ancien, nouveau)], "non_derivables": [(unité, raison)],
     "a_verifier": [(unité, shortName, mots)], "repetitions": [(unité, refs)]}."""
    codes = codes or load_codes()
    log = {"changes": [], "non_derivables": [], "a_verifier": [], "repetitions": []}
    for u, parent, anc in walk(orbat):
        d = derive(u, parent, anc, codes)
        if d["parent_repeated"]:
            log["repetitions"].append((u, d["parent_repeated"]))
        if u.get("shortName") and not recompute:
            continue
        if d["short_name"] is None:
            log["non_derivables"].append((u, d["reason"]))
            continue
        if d["residual"]:
            log["a_verifier"].append((u, d["short_name"], d["residual"]))
        old = u.get("shortName")
        if old != d["short_name"]:
            log["changes"].append((u, old, d["short_name"]))
            u["shortName"] = d["short_name"]
    return log


def main():
    ap = argparse.ArgumentParser(
        description="Dérive le shortName des unités d'un ORBAT JSON (naming.md Règle 2, "
                    "§ 7.5, § 7.7) avec les codes du skill acronyme.",
        epilog="Par défaut ne remplit que les unités sans shortName et écrit en place, "
               "puis valide (code de sortie 1 s'il reste une ERREUR de validate.py).")
    ap.add_argument("orbat", help="fichier ORBAT JSON")
    ap.add_argument("--all", action="store_true",
                    help="recalculer le shortName de TOUTES les unités (pas seulement les manquants)")
    ap.add_argument("--dry-run", action="store_true", help="afficher les changements sans écrire")
    ap.add_argument("--output", metavar="OUT", help="fichier de sortie (défaut : écrase l'entrée)")
    args = ap.parse_args()

    try:
        codes = load_codes()
    except (FileNotFoundError, ValueError) as e:
        sys.exit(f"❌ {e}")
    orbat = ol.load(args.orbat)
    log = apply(orbat, recompute=args.all, codes=codes)

    print(f"{len(log['changes'])} shortName posé(s) / modifié(s) :")
    for u, old, new in log["changes"]:
        print(f"  {u.get('name')!r} : {old or '—'} -> {new}")
    if log["a_verifier"]:
        print(f"\n⚠️  {len(log['a_verifier'])} shortName à vérifier (mots du nom sans code "
              "dans le skill acronyme — non abrégés, naming.md § 7.2) :")
        for u, sn, words in log["a_verifier"]:
            print(f"  {u.get('name')!r} -> {sn}   [non traduit : {', '.join(words)}]")
    if log["non_derivables"]:
        print(f"\n🔴 {len(log['non_derivables'])} unité(s) laissée(s) sans shortName :")
        for u, why in log["non_derivables"]:
            print(f"  {u.get('name')!r} : {why}")
    if log["repetitions"]:
        print(f"\n⚠️  {len(log['repetitions'])} nom(s) répétant la formation mère "
              "(naming.md § 7.7 — à corriger dans `name`) :")
        for u, refs in log["repetitions"]:
            print(f"  {u.get('name')!r} reprend {', '.join(repr(r) for r in refs)}")

    if args.dry_run:
        print("\n[dry-run] Aucun fichier écrit.")
        return
    import validate as vd
    out = args.output or args.orbat
    ol.save(orbat, out)
    print(f"\nÉcrit dans {out}\n\n--- Validation du résultat (validate.py) ---")
    errors, warns, n = vd.check(orbat)
    vd.report(errors, warns, n)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
