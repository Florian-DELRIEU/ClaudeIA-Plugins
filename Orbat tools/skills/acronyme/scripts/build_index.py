#!/usr/bin/env python3
"""Génère l'index alphabétique de tous les acronymes du skill /acronyme.

Lit les tables de codes (module partagé `tables.py` : format « Officiel |
Alternatifs » et ancien format `X / Y`) de references/*.md,
identification/chassis-types.md et identification/personnel.md, plus les clés
des deux lexiques JSON, puis écrit references/INDEX.md, une section par bassin
(Types, Rôles/Armements, Précisions entre parenthèses, Lexiques). Chaque code
officiel ET chaque alternatif est indexé (« alt. de X »). Les tables balisées
`<!-- bassin: aucun -->` (exemples, illustrations) ne sont pas indexées.

Régénérable à volonté — ne jamais éditer INDEX.md à la main.

Usage : python scripts/build_index.py [racine_du_skill]   (défaut : le skill qui contient ce script)
"""
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tables as T  # noqa: E402

SECTIONS = (("types", "Types (premier segment : véhicules, unités, échelons, grades, structures)"),
            ("roles", "Rôles / Armements / Équipements"),
            ("precisions", "Précisions (entre parenthèses : propulsion, vitesse, matériaux)"),
            (None, "Bassin non balisé"))


def collect(skill_dir):
    """{bassin: {code: {"statuts": set, "files": set}}} + {clé de lexique: set(fichiers)}."""
    idx = defaultdict(lambda: defaultdict(lambda: {"statuts": set(), "files": set()}))
    for r in T.rows(skill_dir):
        name = os.path.basename(r.path)
        if r.officiel:
            e = idx[r.bassin][r.officiel]
            e["statuts"].add("officiel")
            e["files"].add(name)
        for a in r.alternatifs:
            e = idx[r.bassin][a]
            e["statuts"].add("alt. de %s" % r.officiel if r.officiel
                             else "alt. (sans officiel attribué)")
            e["files"].add(name)
    lex = defaultdict(set)
    for f in ("lexique.json", "lexique-40k.json"):
        p = os.path.join(skill_dir, "identification", f)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                for k in json.load(fh):
                    if not k.startswith("_"):
                        lex[k].add(f)
    return idx, lex


def _key(s):
    return (s.upper(), s)


def render(skill_dir):
    idx, lex = collect(skill_dir)
    total = len({c for b in idx.values() for c in b} | set(lex))
    out = ["# Index alphabétique des acronymes", "",
           "> ⚠️ **Fichier généré — ne pas éditer à la main.** Régénérer avec "
           "`python scripts/build_index.py`. Un code par bassin : son statut (officiel, ou "
           "alternatif de lecture d'un officiel) et le(s) fichier(s) où il est défini. "
           "Avant de proposer un code : `python scripts/check.py --code X`.", "",
           "Total : %d codes distincts." % total, ""]
    for bassin, title in SECTIONS:
        codes = idx.get(bassin)
        if not codes:
            continue
        out += ["## %s" % title, "", "| Code | Statut | Fichier(s) |", "|---|---|---|"]
        for code in sorted(codes, key=_key):
            e = codes[code]
            st = sorted(e["statuts"], key=lambda s: (s != "officiel", s))
            out.append("| `%s` | %s | %s |" % (code, " ; ".join(st), ", ".join(sorted(e["files"]))))
        out.append("")
    out += ["## Lexiques (codes composés journalisés)", "", "| Code | Statut | Fichier(s) |",
            "|---|---|---|"]
    for k in sorted(lex, key=_key):
        out.append("| `%s` | composé | %s |" % (k, ", ".join(sorted(lex[k]))))
    return "\n".join(out) + "\n"


def index_path(skill_dir):
    return os.path.join(skill_dir, "references", "INDEX.md")


def main():
    skill = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else T.skill_dir_default()
    text = render(skill)
    with open(index_path(skill), "w", encoding="utf-8") as f:
        f.write(text)
    n = text.count("\n| `")
    print("INDEX.md écrit : %d lignes de codes -> %s" % (n, index_path(skill)))


if __name__ == "__main__":
    main()
