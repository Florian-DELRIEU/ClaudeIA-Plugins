#!/usr/bin/env python3
"""Lecture des tables de codes du skill /acronyme — module partagé.

Importé par build_index.py, check.py et, côté orbat-json, par
orbat_lib.load_echelon_codes / short_names.load_codes : une seule logique de
lecture pour tout le plugin.

Deux formats de table sont reconnus :

  * format courant (2026-10-10) — 1re colonne « Officiel », 2e « Alternatifs »
    (alias de lecture séparés par « , », cellule vide si aucun) :
        | Officiel | Alternatifs | Signification | Note |
        |---|---|---|---|
        | DIV | D | Division | … |

  * ancien format — 1re colonne « Acronyme »/« Code »/« Désignation »… où
    `X / Y` liste l'officiel et ses alias ; l'officiel est la forme annoncée par
    la ligne (« `X` officiel », « **Officiel** `X` »), sinon la première.

Chaque table peut être précédée (ligne non vide immédiatement au-dessus) d'une
balise de bassin : <!-- bassin: types --> / roles / precisions / aucun.
Une table « aucun » (exemples, illustrations) ne définit aucun code.

API : parse_text(text, path) -> [Table] ; parse_file(path) ; code_files(skill_dir) ;
rows(skill_dir) -> [Row] (toutes les lignes de code du skill) ; fold(s) ; norm_code(s).
Une ligne à Officiel vide (Alternatifs remplis) décrit un sens sans code officiel
attribué : Row.officiel == "".
"""
import os
import re
import unicodedata

BASSINS = ("types", "roles", "precisions", "aucun")
BASSIN_RE = re.compile(r"<!--\s*bassin:\s*([a-zé]+)\s*-->", re.I)

# en-têtes de 1re colonne d'une table de codes à l'ancien format
OLD_CODE_HEADERS = ("acronyme", "code", "designation", "prefixe", "fusion")
# colonne portant la signification, par ordre de préférence
MEANING_HEADERS = ("signification", "sens", "arme", "mission", "grade", "element",
                   "lecture", "nature", "type", "description")

_OFFICIEL_RES = (re.compile(r"`-?([^`\s]+)`\s*\**\s*officiel", re.I),
                 re.compile(r"officiel\W{0,6}`-?([^`\s]+)`", re.I))


def fold(s):
    """Minuscules sans accents (comparaison de textes)."""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def norm_code(s):
    """Code tel qu'il se compare : sans balisage Markdown ni tiret de liaison
    initial (`-INF` dans `BT-INF` est le code `INF`)."""
    s = (s or "").replace("`", "").replace("**", "").strip()
    return s.lstrip("-").strip() if len(s) > 1 else s


def split_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_sep(line):
    return set(line.strip()) <= set("|-: ") and "-" in line


class Row:
    __slots__ = ("path", "line", "table", "bassin", "officiel", "alternatifs",
                 "meaning", "text", "cells", "fmt")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    @property
    def codes(self):
        return ([self.officiel] if self.officiel else []) + list(self.alternatifs)

    def where(self):
        return "%s:%d" % (os.path.basename(self.path or "?"), self.line)

    def __repr__(self):
        return "Row(%s %s alt=%s %s)" % (self.where(), self.officiel, self.alternatifs,
                                         self.meaning)


class Table:
    def __init__(self, path, line, heading, bassin, header):
        self.path, self.line, self.heading, self.bassin = path, line, heading, bassin
        self.header = header
        h = [fold(x).strip("* ") for x in header] if header is not None else None
        if h is None:                # lignes sans en-tête : lues à l'ancien format
            self.fmt, self.meaning_col, self.rows = "old", 1, []
            return
        if len(h) >= 2 and h[0] == "officiel" and h[1] == "alternatifs":
            self.fmt = "new"
        elif h and h[0] in OLD_CODE_HEADERS:
            self.fmt = "old"
        else:
            self.fmt = None          # table sans colonne de code (archétypes, exemples)
        self.meaning_col = None
        start = 2 if self.fmt == "new" else 1
        for name in MEANING_HEADERS:
            for i in range(start, len(h)):
                if h[i].startswith(name):
                    self.meaning_col = i
                    break
            if self.meaning_col is not None:
                break
        if self.meaning_col is None and len(h) > start:
            self.meaning_col = start
        self.rows = []

    @property
    def defines_codes(self):
        return self.fmt is not None and self.bassin != "aucun"


def _forms_old(cell):
    """Formes d'une cellule à l'ancien format : `X / Y / Z` (séparateur espacé)."""
    parts = re.split(r"\s+/\s+", cell) if re.search(r"\s/\s", cell) else [cell]
    return [c for c in (norm_code(p) for p in parts) if c]


def _officiel_annotated(text, forms):
    for rx in _OFFICIEL_RES:
        for m in rx.finditer(text):
            c = norm_code(m.group(1))
            if c in forms:
                return c
    return None


def parse_text(text, path=""):
    """Toutes les tables du texte, avec leurs lignes (Row) déjà interprétées."""
    lines = text.split("\n")
    tables, heading, i = [], "", 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            heading = ln.lstrip("#").strip()
        if ln.strip().startswith("|") and i + 1 < len(lines) and _is_sep(lines[i + 1]):
            bassin, j = None, i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            if j >= 0:
                m = BASSIN_RE.search(lines[j])
                if m:
                    bassin = fold(m.group(1))
            t = Table(path, i + 1, heading, bassin, split_cells(ln))
            k = i + 2
            while k < len(lines) and lines[k].strip().startswith("|"):
                cells = split_cells(lines[k])
                row = _row(t, cells, lines[k], k + 1)
                if row is not None:
                    t.rows.append(row)
                k += 1
            tables.append(t)
            i = k
            continue
        if ln.strip().startswith("|") and not _is_sep(ln):
            # lignes de table sans en-tête (fragment) : ancien format, signification en 2e colonne
            t = Table(path, i + 1, heading, None, None)
            k = i
            while k < len(lines) and lines[k].strip().startswith("|") and not _is_sep(lines[k]):
                row = _row(t, split_cells(lines[k]), lines[k], k + 1)
                if row is not None:
                    t.rows.append(row)
                k += 1
            tables.append(t)
            i = k
            continue
        i += 1
    return tables


def _row(t, cells, raw, lineno):
    if t.fmt is None or not cells:
        return None
    if t.fmt == "new":
        # Officiel vide + Alternatifs remplis : sens sans code officiel attribué
        # (seule une forme de lecture existe, ex. `GEN.F`) — officiel = "".
        off = norm_code(cells[0])
        alts = [norm_code(a) for a in (cells[1] if len(cells) > 1 else "").split(",")]
        alts = [a for a in alts if a]
        if not off and not alts:
            return None
    elif not cells[0].strip():
        return None
    if t.fmt == "old":
        forms = _forms_old(cells[0])
        if not forms:
            return None
        off = _officiel_annotated(" | ".join(cells[1:]), forms) or forms[0]
        alts = [f for f in forms if f != off]
    meaning = cells[t.meaning_col] if t.meaning_col is not None and t.meaning_col < len(cells) else ""
    return Row(path=t.path, line=lineno, table=t.heading, bassin=t.bassin, officiel=off,
               alternatifs=alts, meaning=meaning, text=raw, cells=cells, fmt=t.fmt)


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        return parse_text(f.read(), path)


def section(text, heading):
    """Texte de la section `## heading` (jusqu'au prochain titre de même niveau)."""
    start = text.find(heading)
    if start == -1:
        return None
    level = len(heading) - len(heading.lstrip("#"))
    m = re.compile(r"\n#{1,%d} " % level).search(text, start + 1)
    return text[start:m.start() if m else len(text)]


def code_files(skill_dir):
    """Fichiers dont les tables définissent des codes."""
    ref = os.path.join(skill_dir, "references")
    out = sorted(os.path.join(ref, f) for f in os.listdir(ref)
                 if f.endswith(".md") and f != "INDEX.md")
    for f in ("chassis-types.md", "personnel.md"):
        p = os.path.join(skill_dir, "identification", f)
        if os.path.exists(p):
            out.append(p)
    return out


def rows(skill_dir):
    """Toutes les lignes de code du skill (tables de bassin types/roles/precisions)."""
    out = []
    for p in code_files(skill_dir):
        for t in parse_file(p):
            if t.defines_codes:
                out.extend(t.rows)
    return out


def skill_dir_default():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
