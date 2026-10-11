#!/usr/bin/env python3
"""Génère un index alphabétique de tous les acronymes du skill /acronyme.

Parcourt les tables Markdown de references/ + identification/chassis-types.md et
les deux lexiques JSON, puis écrit references/INDEX.md : pour chaque code, le
fichier où il apparaît. Régénérable à volonté — ne jamais éditer INDEX.md à la
main, il est écrasé à chaque exécution.

Usage : python scripts/build_index.py [racine_du_skill]
"""
import json, re, sys, pathlib
from collections import defaultdict

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# Un code : commence par une lettre, composé de lettres/chiffres, avec éventuels
# séparateurs internes . / - ( ) # ² ₂ etc. On accepte l'astérisque final (marqueur
# "en attente"). On rejette les cellules qui sont manifestement du texte (espaces).
TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:[./-][A-Za-z0-9#()]+)*\*?$")

def clean(cell):
    return cell.replace("`", "").strip()

def emit(raw, path, index):
    """Découpe une cellule 'A / B / C' en codes individuels et les indexe."""
    for token in re.split(r"\s*/\s*", raw):
        token = token.strip()
        # retirer un ⚠ ou annotations résiduelles
        token = token.split("—")[0].split("(")[0].strip() if " " in token else token
        if token and TOKEN_RE.match(token) and not token.isdigit():
            index[token].add(path.name)

def scan_md(path, index):
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= set("|-: "):
            continue
        cells = [clean(c) for c in s.strip("|").split("|")]
        if not cells or cells[0].lower() in ("acronyme", "code", "signification",
                                             "désignation", "format", "marqueur"):
            continue
        emit(cells[0], path, index)

def scan_json(path, index):
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in data:
        if isinstance(key, str) and not key.startswith("_"):
            index[key].add(path.name)

def main():
    index = defaultdict(set)
    md_files = sorted((ROOT / "references").glob("*.md"))
    ct = ROOT / "identification" / "chassis-types.md"
    if ct.exists():
        md_files.append(ct)
    for f in md_files:
        if f.name != "INDEX.md":
            scan_md(f, index)
    for lex in ("lexique.json", "lexique-40k.json"):
        p = ROOT / "identification" / lex
        if p.exists():
            scan_json(p, index)

    out = ROOT / "references" / "INDEX.md"
    lines = [
        "# Index alphabétique des acronymes",
        "",
        "> ⚠️ **Fichier généré — ne pas éditer à la main.** Régénérer avec "
        "`python scripts/build_index.py`. Chaque code pointe vers le(s) fichier(s) "
        "où il apparaît (1re colonne des tables + clés de lexiques).",
        "",
        f"Total : {len(index)} codes.",
        "",
        "| Code | Fichier(s) |",
        "|---|---|",
    ]
    for code in sorted(index, key=lambda s: (s.upper(), s)):
        lines.append(f"| `{code}` | {', '.join(sorted(index[code]))} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"INDEX.md écrit : {len(index)} codes -> {out}")

if __name__ == "__main__":
    main()
