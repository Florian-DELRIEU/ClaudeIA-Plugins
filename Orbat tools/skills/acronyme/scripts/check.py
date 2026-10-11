#!/usr/bin/env python3
"""Contrôle de cohérence du skill /acronyme.

    python scripts/check.py              # contrôle complet ; code de sortie 1 s'il y a des erreurs
    python scripts/check.py --accepter-collisions   # enregistre les collisions actuelles
                                         # (après arbitrage de Florian uniquement)
    python scripts/check.py --code X     # tous les sens de X (officiel / alternatif, bassin,
                                         # fichier:ligne) et ses collisions — À LANCER AVANT
                                         # TOUTE PROPOSITION DE CODE (existe-t-il ? doublon ?)

Contrôles (ERREUR = bloquant, AVERT. = à examiner) :
  1. collisions entre OFFICIELS d'un même bassin (règle cardinale n°2) : seuls les couples
     (code, sens) enregistrés dans scripts/collisions_connues.json sont tolérés (exception
     de la règle 2, cas confirmé § 2, ou point ouvert § 5 → avertissement) ; tout sens
     nouveau, même sur un code de la liste d'exceptions, est une ERREUR ;
  2. alternatif qui est l'officiel d'un autre sens dans le même bassin (avert.) ;
  3. casse : code non entièrement en majuscules (avert. ; cas « à arbitrer » de § 5 signalés) ;
  4. calibres collés (`CA30` au lieu de `CA.30`) ;
  5. renvois internes cassés (`fichier.md` § Section : fichier ou titre introuvable) ;
  6. `parts` des lexiques absents de l'INDEX ;
  7. clés de lexique écrites avec un alternatif au lieu de l'officiel (avert.) ;
  8. mentions « à confirmer / provisoire / à trancher… » dont aucun code n'est au § 5 (avert.) ;
  9. INDEX.md à jour (sinon : relancer build_index.py).

Bibliothèque standard seule. Importable : run_checks(skill_dir) -> (erreurs, avertissements).
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tables as T  # noqa: E402
import build_index  # noqa: E402

GABARITS = {"L", "M", "H", "SH", "U", "2L", "2M", "2H"}
EXCEPTIONS_RE = re.compile(r"<!--\s*exceptions-regle-2:\s*([^>]*?)\s*-->")
OPEN_WORDS = re.compile(r"à confirmer|à clarifier|à trancher|à arbitrer|provisoire|point ouvert",
                        re.I)
# armements qui prennent un calibre : `CA.30`, jamais `CA30`
CALIBRE_RE = re.compile(r"(?<![A-Za-z0-9.#])\d*((?:L|M|H)?(?:CAA|CA|C|G|MOR|MG|HMG|MMG|LMG|FS|FA|FV|"
                        r"FMG|FM|F|AAC|AACA|RTG))(\d{2,3})(?![\d.])")
# ligne qui parle d'une forme collée à titre historique : non contrôlée
CALIBRE_HISTO = re.compile(r"coll[ée]|abandonn|renomm|→|lisible|lecture|ancien", re.I)
REF_RE = re.compile(r"`?((?:references/|identification/)?([A-Za-z0-9_-]+\.md))`?"
                    r"\s*(?:\(\s*)?§\s*\**([^,;)|*`«»\n]{1,60})")
SKIP_REF_FILES = {"chronologie.md", "INDEX.md"}   # historique / généré : renvois d'époque


# ---------------------------------------------------------------------------
# Données
# ---------------------------------------------------------------------------
def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def exceptions(skill):
    m = EXCEPTIONS_RE.search(_read(os.path.join(skill, "SKILL.md")))
    return set(m.group(1).split()) if m else set()


def open_points(skill):
    """(codes cités en 1re colonne du § 5 de decisions.md, texte du § 5)."""
    text = _read(os.path.join(skill, "decisions.md"))
    sec = T.section(text, "## 5.") or ""
    codes = set()
    for line in sec.splitlines():
        if line.startswith("|"):
            first = line.strip("|").split("|")[0]
            codes.update(T.norm_code(c) for c in re.findall(r"`([^`]+)`", first))
    return codes, sec


def confirmed(skill):
    """Codes classés « cas confirmés sans conflit » (1re colonne du § 2 de decisions.md)."""
    sec = T.section(_read(os.path.join(skill, "decisions.md")), "## 2.") or ""
    codes = set()
    for line in sec.splitlines():
        if line.startswith("|"):
            first = line.strip("|").split("|")[0]
            codes.update(T.norm_code(c) for c in re.findall(r"`([^`]+)`", first))
    return codes


def known_path(skill):
    return os.path.join(skill, "scripts", "collisions_connues.json")


def known_collisions(skill):
    """{(bassin, code): {"sens": [ids], "raison": str}} — collisions déjà arbitrées."""
    p = known_path(skill)
    if not os.path.exists(p):
        return None                       # fichier absent : mode dégradé (voir check_collisions)
    data = json.loads(_read(p))
    return {(e["bassin"], e["code"]): e for e in data.get("collisions", [])}


def sense_id(r):
    """Identité stable d'un sens : fichier + signification nettoyée (pas de n° de ligne)."""
    return "%s::%s" % (os.path.basename(r.path or "?"), _clean(r.meaning)[:80])


def lexiques(skill):
    out = {}
    for f in ("lexique.json", "lexique-40k.json"):
        p = os.path.join(skill, "identification", f)
        if os.path.exists(p):
            out[f] = json.loads(_read(p))
    return out


def _clean(s):
    s = re.sub(r"⚠[^|]*", "", s or "")          # avertissements : citent souvent l'AUTRE sens
    s = re.sub(r"[*`_]", "", s)
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"\s+", " ", T.fold(s)).strip(" .:—-")


def same_meaning(a, b):
    """Deux lignes décrivent-elles le même sens ? (signification de l'une contenue
    dans le texte de l'autre — tolérant aux reformulations et descriptions)."""
    ma, mb = _clean(a.meaning), _clean(b.meaning)
    if not ma or not mb:
        return True
    ta, tb = _clean(a.text), _clean(b.text)
    if ma == mb or ma in tb or mb in ta:
        return True
    wa = {w for w in re.findall(r"[a-z0-9]{4,}", ma)}
    wb = {w for w in re.findall(r"[a-z0-9]{4,}", mb)}
    return bool(wa and wb and (wa <= set(re.findall(r"[a-z0-9]{4,}", tb))
                               or wb <= set(re.findall(r"[a-z0-9]{4,}", ta))))


def by_bassin(rows):
    off = defaultdict(list)     # (bassin, code) -> lignes où il est officiel
    alt = defaultdict(list)     # (bassin, code) -> lignes où il est alternatif
    for r in rows:
        if r.officiel:
            off[(r.bassin, r.officiel)].append(r)
        for a in r.alternatifs:
            alt[(r.bassin, a)].append(r)
    return off, alt


def _distinct(rows_):
    """Groupes de lignes de sens distincts."""
    groups = []
    for r in rows_:
        for g in groups:
            if any(same_meaning(r, x) for x in g):
                g.append(r)
                break
        else:
            groups.append([r])
    return groups


# ---------------------------------------------------------------------------
# Contrôles
# ---------------------------------------------------------------------------
def current_collisions(rows):
    """{(bassin, code): [lignes officielles]} pour chaque officiel à ≥ 2 sens distincts."""
    off, _ = by_bassin(rows)
    return {k: rs for k, rs in sorted(off.items(), key=lambda kv: (str(kv[0][0]), kv[0][1]))
            if len(_distinct(rs)) >= 2}


def raison(code, exc, conf, opened):
    # un point encore ouvert prime : il doit rester visible (avertissement)
    if code in opened:
        return "point ouvert (decisions.md § 5)"
    if code in exc:
        return "exception à la règle cardinale n°2 (SKILL.md)"
    if code in conf:
        return "cas confirmé sans conflit (decisions.md § 2)"
    return "acceptée par --accepter-collisions (arbitrage de Florian à consigner)"


def check_collisions(rows, exc, opened, errors, warnings, known=None, conf=()):
    """Une collision n'est tolérée que pour les couples (code, sens) déjà listés dans
    collisions_connues.json : tout sens nouveau sur le même code = ERREUR, même pour
    un code de la liste d'exceptions ou du § 5."""
    off, alt = by_bassin(rows)
    for (bassin, code), rs in current_collisions(rows).items():
        groups = _distinct(rs)
        desc = " ≠ ".join("« %s » (%s)" % (g[0].meaning[:50], g[0].where()) for g in groups)
        msg = "collision d'officiels [%s] `%s` : %s" % (bassin, code, desc)
        if known is None:
            # mode dégradé (skill sans collisions_connues.json) : exemption par code
            if code not in exc:
                (warnings if code in opened else errors).append(
                    msg + (" — point ouvert (decisions.md § 5)" if code in opened else ""))
            continue
        entry = known.get((str(bassin), code))
        if entry is None:
            ctx = (" (code de la liste d'exceptions, mais ces sens n'y sont pas enregistrés)"
                   if code in exc else " (cité au § 5, mais ces sens n'y sont pas enregistrés)"
                   if code in opened else "")
            errors.append(msg + ctx + " — si Florian l'a arbitrée : check.py --accepter-collisions")
            continue
        ok_ids = set(entry.get("sens", []))
        ok_rows = [r for r in rs if sense_id(r) in ok_ids]
        new = [r for r in rs if sense_id(r) not in ok_ids
               and not any(same_meaning(r, k) for k in ok_rows)]
        if new:
            errors.append("collision d'officiels [%s] `%s` : sens NOUVEAU non arbitré %s — "
                          "connus : %s" % (bassin, code,
                                           ", ".join("« %s » (%s)" % (r.meaning[:50], r.where())
                                                     for r in new),
                                           "; ".join(sorted(ok_ids))[:200]))
        elif "§ 5" in entry.get("raison", ""):
            warnings.append(msg + " — point ouvert (decisions.md § 5)")


def accept_collisions(skill):
    """Réécrit collisions_connues.json avec les collisions actuelles (à lancer
    uniquement après arbitrage de Florian — procedures.md P2)."""
    rows = T.rows(skill)
    exc, conf, (opened, _) = exceptions(skill), confirmed(skill), open_points(skill)
    out = []
    for (bassin, code), rs in current_collisions(rows).items():
        out.append({"code": code, "bassin": str(bassin),
                    "raison": raison(code, exc, conf, opened),
                    "sens": sorted({sense_id(r) for r in rs})})
    data = {"_comment": "Collisions d'officiels ARBITRÉES (même code, sens distincts, même "
                        "bassin). Généré par `check.py --accepter-collisions` après décision de "
                        "Florian — ne pas éditer pour faire taire une erreur. Tout sens absent "
                        "d'ici fait échouer check.py.",
            "collisions": out}
    with open(known_path(skill), "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return out


def check_alternatives(rows, exc, warnings):
    off, alt = by_bassin(rows)
    for (bassin, code), rs in sorted(alt.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        owners = off.get((bassin, code))
        if not owners or code in exc:
            continue
        for r in rs:
            if not any(same_meaning(r, o) for o in owners):
                warnings.append("alternatif [%s] `%s` de `%s` (%s) = officiel d'un autre sens : %s"
                                % (bassin, code, r.officiel or "(sans officiel)", r.where(),
                                   ", ".join("« %s » %s" % (o.meaning[:40], o.where())
                                             for o in owners[:3])))


def check_case(rows, opened_text, warnings):
    seen = set()
    for r in rows:
        for c in r.codes:
            if c in seen or not re.search(r"[a-z]", c):
                continue
            seen.add(c)
            tag = " — à arbitrer (decisions.md § 5)" if "`%s`" % c in opened_text else ""
            warnings.append("casse mixte `%s` (%s)%s" % (c, r.where(), tag))


def check_calibres(skill, rows, lex, errors):
    def scan(token, where):
        for m in CALIBRE_RE.finditer(token):
            errors.append("calibre collé `%s` (%s) : écrire `%s.%s`"
                          % (m.group(0), where, m.group(1), m.group(2)))
    for r in rows:
        for c in r.codes:
            scan(c, r.where())
    for f, data in lex.items():
        for k, v in data.items():
            if k.startswith("_"):
                continue
            scan(k, "%s clé" % f)
            for p in v.get("parts", []):
                scan(p, "%s %s.parts" % (f, k))
    for p in T.code_files(skill):
        for i, line in enumerate(_read(p).splitlines(), 1):
            if CALIBRE_HISTO.search(line):
                continue
            for tok in re.findall(r"`([^`\s]+)`", line):
                scan(tok, "%s:%d" % (os.path.basename(p), i))


def _md_files(skill):
    out = {}
    for root, _, files in os.walk(skill):
        for f in files:
            if f.endswith(".md"):
                out.setdefault(f, os.path.join(root, f))
    return out


def _headings(path):
    return [l.lstrip("#").strip() for l in _read(path).splitlines() if l.startswith("#")]


_TRAILING = {"et", "ou", "puis", "de", "du", "des", "la", "le", "les", "pour", "dans", "avec",
             "sur", "voir", "→", "—", "-", "/"}


def _heading_found(heads, sec):
    key = sec.strip().split(" (")[0].strip().rstrip(".").strip("* «»\"")
    words = key.split()
    while words and T.fold(words[-1]).strip(".,:") in _TRAILING:
        words.pop()                                  # « § Rôles et `x.md` … »
    key = " ".join(words).rstrip(".,:")
    num = re.match(r"(\d+(?:\.\d+)?)\b", key)
    if num:
        n = num.group(1)
        return any(re.match(r"%s[.\s]" % re.escape(n), h) for h in heads)
    k = T.fold(key)[:18]
    return any(k in T.fold(h) for h in heads)


def check_refs(skill, errors):
    files = _md_files(skill)
    for name, path in sorted(files.items()):
        if name in SKIP_REF_FILES:
            continue
        for i, line in enumerate(_read(path).splitlines(), 1):
            if "entrée ancienne" in line or "désigne la section homonyme" in line:
                continue                             # note de correspondance historique
            for m in REF_RE.finditer(line):
                fname, sec = m.group(2), m.group(3)
                if fname not in files:
                    if m.group(1).startswith(("references/", "identification/")):
                        errors.append("renvoi vers un fichier inexistant `%s` (%s:%d)"
                                      % (m.group(1), name, i))
                    continue                         # fichier d'un autre skill
                if fname == "SKILL.md" and re.match(r"\d", sec.strip()):
                    continue                         # « SKILL.md § 3 » = règle cardinale n°3
                if not _heading_found(_headings(files[fname]), sec):
                    errors.append("renvoi cassé `%s § %s` (%s:%d) : titre introuvable"
                                  % (fname, sec.strip()[:40], name, i))


def _index_codes(skill):
    idx, _ = build_index.collect(skill)
    allc, offi = set(), defaultdict(set)
    for bassin, codes in idx.items():
        for c, e in codes.items():
            allc.add(c)
            if "officiel" in e["statuts"]:
                offi[bassin].add(c)
    return allc, offi


def _part_ok(p, allc):
    if p in allc or p in GABARITS or re.fullmatch(r"\d+(?:t)?", p):
        return True
    m = re.fullmatch(r"\d*([A-Za-z]+)(\d+)", p)        # ACR# (pattes, roues) / #ACR (tubes)
    if m and (m.group(1) + "#") in allc:
        return True
    m = re.fullmatch(r"(\d+)([A-Za-z].*)", p)          # 2AACA = 2 tubes + AACA
    return bool(m and m.group(2) in allc)


def check_lexiques(skill, lex, rows, errors, warnings):
    allc, offi = _index_codes(skill)
    off, alt = by_bassin(rows)
    for f, data in lex.items():
        for k, v in data.items():
            if k.startswith("_"):
                continue
            for p in v.get("parts", []):
                if not _part_ok(p, allc):
                    errors.append("lexique %s : `%s` — composant `%s` absent de l'INDEX" % (f, k, p))
            comps = [c for c in re.split(r"[-./]", k) if c]
            for pos, c in enumerate(comps):
                bassin = "types" if pos == 0 else "roles"
                if c in offi.get(bassin, ()) or c in GABARITS or re.fullmatch(r"\d+t?", c):
                    continue
                owners = alt.get((bassin, c))
                if owners:
                    warnings.append("lexique %s : `%s` écrit avec l'alternatif `%s` (officiel : %s)"
                                    % (f, k, c, ", ".join(sorted({o.officiel for o in owners}))))


def check_open_mentions(skill, opened_text, warnings):
    for p in T.code_files(skill) + [os.path.join(skill, "identification", "lexique.json")]:
        if not os.path.exists(p) or p.endswith("grammaire.md"):
            continue
        for i, line in enumerate(_read(p).splitlines(), 1):
            if not OPEN_WORDS.search(line):
                continue
            codes = [T.norm_code(c) for c in re.findall(r"`([^`]+)`", line)]
            first = T.split_cells(line)[0] if line.startswith("|") else ""
            if first:
                codes.insert(0, T.norm_code(first))
            if not codes or "§ 5" in line:
                continue
            if not any(c and "`%s`" % c in opened_text for c in codes):
                warnings.append("mention ouverte hors decisions.md § 5 (%s:%d) : %s"
                                % (os.path.basename(p), i, line.strip()[:90]))


def check_index(skill, errors):
    path = build_index.index_path(skill)
    current = _read(path) if os.path.exists(path) else ""
    if current != build_index.render(skill):
        errors.append("INDEX.md pas à jour : relancer `python scripts/build_index.py`")


def run_checks(skill):
    errors, warnings = [], []
    rows = T.rows(skill)
    for r in rows:
        if r.bassin is None:
            warnings.append("table sans balise de bassin (%s, « %s »)" % (r.where(), r.table))
    exc = exceptions(skill)
    opened, opened_text = open_points(skill)
    lex = lexiques(skill)
    known = known_collisions(skill)
    if known is None:
        warnings.append("scripts/collisions_connues.json absent : collisions exemptées par code "
                        "(mode dégradé, moins strict) — le générer avec --accepter-collisions")
    check_collisions(rows, exc, opened, errors, warnings, known, confirmed(skill))
    check_alternatives(rows, exc, warnings)
    check_case(rows, opened_text, warnings)
    check_calibres(skill, rows, lex, errors)
    check_refs(skill, errors)
    check_lexiques(skill, lex, rows, errors, warnings)
    check_open_mentions(skill, opened_text, warnings)
    check_index(skill, errors)
    return list(dict.fromkeys(errors)), list(dict.fromkeys(warnings))


# ---------------------------------------------------------------------------
# --code X
# ---------------------------------------------------------------------------
def describe(skill, code):
    """Tous les sens d'un code (recherche insensible à la casse : `TK` trouve `Tk`)."""
    want = T.norm_code(code)
    rows = T.rows(skill)
    exc = exceptions(skill)
    opened, _ = open_points(skill)
    known = known_collisions(skill)
    forms = sorted({c for r in rows for c in r.codes if c.upper() == want.upper()})
    lines = ["Code `%s`" % want + ("  (forme(s) trouvée(s) : %s)" % ", ".join("`%s`" % f for f in forms)
                                   if forms and forms != [want] else "")]
    hits = [(r, c) for r in rows for c in r.codes if c.upper() == want.upper()]
    lex = lexiques(skill)
    used = sorted("%s (%s)" % (k, f) for f, d in lex.items() for k in d
                  if not k.startswith("_")
                  and want.upper() in (x.upper() for x in [k] + re.split(r"[-./]", k)))
    if not hits:
        lines.append("  absent de toutes les tables" + (" — n'existe qu'au lexique (composé)"
                                                         if used else " : code LIBRE")
                     + " (vérifier aussi les formes voisines).")
    for bassin in sorted({str(r.bassin) for r, _ in hits}):
        lines.append("  Bassin %s :" % bassin)
        offs, alts = [], []
        for r, c in hits:
            if str(r.bassin) != bassin:
                continue
            if r.officiel == c:
                offs.append(r)
                st = "OFFICIEL `%s`" % c + (" (alias : %s)" % ", ".join(r.alternatifs)
                                            if r.alternatifs else "")
            else:
                alts.append(r)
                st = ("alternatif de `%s` : `%s`" % (r.officiel, c) if r.officiel
                      else "alternatif `%s` (sans officiel attribué)" % c)
            lines.append("    - %-40s %s — %s [%s]" % (st, r.where(), _clean(r.meaning)[:60], r.table))
        if len(_distinct(offs)) > 1:
            code_ = offs[0].officiel
            e = (known or {}).get((bassin, code_))
            kind = (e["raison"] if e else "COLLISION NON ARBITRÉE")
            lines.append("    ⚠ %d sens officiels distincts dans ce bassin — %s"
                         % (len(_distinct(offs)), kind))
        if offs and alts:
            lines.append("    ⚠ aussi alternatif d'un autre officiel dans ce bassin "
                         "(toléré : seule l'unicité des officiels est exigée)")
    if used:
        lines.append("  Lexiques : " + ", ".join(used))
    if any(f in exc for f in forms):
        lines.append("  Liste fermée des exceptions de la règle n°2 : oui")
    if any(f in opened for f in forms + [want]):
        lines.append("  Cité au § 5 de decisions.md (point ouvert)")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--code", help="afficher tous les sens d'un code et ses collisions")
    ap.add_argument("--skill", default=T.skill_dir_default(), help="racine du skill acronyme")
    ap.add_argument("-q", "--quiet", action="store_true", help="n'afficher que les erreurs")
    ap.add_argument("--accepter-collisions", action="store_true",
                    help="réécrire scripts/collisions_connues.json avec les collisions actuelles "
                         "(UNIQUEMENT après arbitrage de Florian — procedures.md P2)")
    a = ap.parse_args(argv)
    if a.code:
        print(describe(a.skill, a.code))
        return 0
    if a.accepter_collisions:
        out = accept_collisions(a.skill)
        print("collisions_connues.json réécrit : %d collision(s) enregistrée(s)" % len(out))
        for e in out:
            print("  [%s] `%s` — %s" % (e["bassin"], e["code"], e["raison"]))
        return 0
    errors, warnings = run_checks(a.skill)
    for e in errors:
        print("ERREUR  " + e)
    if not a.quiet:
        for w in warnings:
            print("AVERT.  " + w)
    print("ERREURS : %d — AVERTISSEMENTS : %d" % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
