#!/usr/bin/env python3
"""
draft_mapping.py — brouillon de mapping.json pour apply_rename_map.py, pré-rempli
depuis le lexique du skill `acronyme`. N'INVENTE JAMAIS DE CODE.

Usage:
    python3 draft_mapping.py <orbat.json> [-o mapping_brouillon.json] [--40k]

Pour chaque nom des catalogues racine `equipment` et `personnel` de l'ORBAT, on
cherche le code dans `acronyme/identification/lexique.json` (matériel réel) —
ou, avec --40k, dans `lexique-40k.json` À LA PLACE (univers fictifs : 40K,
Cosmotter…). Un seul lexique est consulté par passe : c'est un choix
d'organisation (correspondances matériel ↔ code rangées par univers), pas une
différence de sens — un code signifie la même chose dans les deux (règle
cardinale n°4 du skill `acronyme`) :

  1. correspondance exacte du nom avec un `materiel_reel` du lexique ;
  2. à défaut, correspondance normalisée (casse, accents, tirets, espaces et
     ponctuation ignorés : « AMX-10 RC » = « amx10rc ») ;
  3. à défaut, même recherche sur la désignation réelle en tête de la
     `description` du catalogue (naming.md Règle 5).
  Seuls les codes du lexique de même nature (`kind` equipment/personnel) sont
  retenus.

Sortie (JSON) :
  {
    "Nom trouvé": "CODE",                 <- une entrée par nom résolu sans ambiguïté
    ...,
    "_a_valider": ["Nom sans code", ...], <- TOUS les autres : aucun code au lexique,
                                             ou plusieurs codes possibles
    "_candidats": {"Nom ambigu": ["CODE1", "CODE2"]}   <- seulement si ambiguïtés
  }
Les noms de `_a_valider` sont à résoudre par le skill `acronyme` (METHODE.md)
puis à soumettre à Florian (naming.md § 7.2 : tout code absent du lexique lui
est soumis). Les entrées de catalogue qui portent DÉJÀ un code du lexique ne
figurent pas dans le brouillon (rien à renommer). apply_rename_map.py ignore les
clés commençant par « _ » mais refuse de tourner tant que `_a_valider` n'est pas
vide — retirer la clé une fois les noms tranchés.

Résumé imprimé : n trouvés / n à valider. Écrit par défaut
`mapping_brouillon.json` à côté de l'ORBAT.
"""
import argparse
import json
import os
import re
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

KINDS = ("equipment", "personnel")
TODO_KEY = "_a_valider"
CANDIDATES_KEY = "_candidats"


def norm(name):
    """Forme normalisée : sans accents ni casse, tirets/espaces/ponctuation ôtés."""
    return re.sub(r"[^0-9a-z]", "", ol.fold(name))


def lexique_path(w40k=False):
    base = os.path.join(ol.find_skill_dir("acronyme"), "identification")
    return os.path.join(base, "lexique-40k.json" if w40k else "lexique.json")


def load_lexique(path):
    """{code: entrée} sans les clés de commentaire (« _… »)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_") and isinstance(v, dict)}


def build_index(lexique):
    """(exact, normalisé) : {kind: {nom: [codes]}} depuis `materiel_reel`."""
    exact = {k: {} for k in KINDS}
    normd = {k: {} for k in KINDS}
    for code, entry in lexique.items():
        kinds = [entry.get("kind")] if entry.get("kind") in KINDS else list(KINDS)
        for real in entry.get("materiel_reel", []) or []:
            if not isinstance(real, str) or not real.strip():
                continue
            for k in kinds:
                lst = exact[k].setdefault(real.strip(), [])
                if code not in lst:
                    lst.append(code)
                lst = normd[k].setdefault(norm(real), [])
                if code not in lst:
                    lst.append(code)
    return exact, normd


def propose(name, kind, exact, normd, description=None):
    """Liste des codes candidats pour un nom de catalogue (vide = aucun).
    Exact d'abord, puis normalisé ; si la forme normalisée révèle d'autres
    codes que la forme exacte (« Gazelle » / « gazelle »), tous sont rendus :
    l'ambiguïté est soumise à Florian, pas tranchée par la casse."""
    keys = [name]
    real = lg.extract_real_name(description)
    if real and real != name:
        keys.append(real)
    for key in keys:
        found = list(exact[kind].get(key, []))
        n = norm(key)
        for code in (normd[kind].get(n, []) if n else []):
            if code not in found:
                found.append(code)
        if found:
            return found
    return []


def draft(orbat, lexique):
    """Renvoie (mapping brouillon, liste des noms déjà codés)."""
    exact, normd = build_index(lexique)
    mapping, todo, cands, already = {}, [], {}, []
    for kind in KINDS:
        for entry in orbat.get(kind, []) or []:
            name = entry.get("name")
            if not name or name in mapping or name in todo:
                continue
            if name in lexique:
                already.append(name)
                continue
            codes = propose(name, kind, exact, normd, entry.get("description"))
            if len(codes) == 1:
                mapping[name] = codes[0]
            else:
                todo.append(name)
                if len(codes) > 1:
                    cands[name] = codes
    mapping[TODO_KEY] = todo
    if cands:
        mapping[CANDIDATES_KEY] = cands
    return mapping, already


def main():
    ap = argparse.ArgumentParser(
        description="Brouillon de mapping.json (apply_rename_map.py) pré-rempli depuis le "
                    "lexique du skill acronyme — aucun code inventé.",
        epilog="Les noms sans code (ou à plusieurs codes possibles) vont dans « _a_valider » : "
               "à résoudre via le skill acronyme et à soumettre à Florian (naming.md § 7.2).")
    ap.add_argument("orbat", help="fichier ORBAT JSON")
    ap.add_argument("-o", "--output", help="fichier brouillon (défaut : mapping_brouillon.json "
                    "à côté de l'ORBAT)")
    ap.add_argument("--40k", dest="w40k", action="store_true",
                    help="utiliser lexique-40k.json (univers fictifs) au lieu de lexique.json")
    args = ap.parse_args()

    try:
        path = lexique_path(args.w40k)
        lexique = load_lexique(path)
    except (FileNotFoundError, OSError, ValueError) as e:
        sys.exit(f"❌ Lexique introuvable ou illisible : {e}")
    orbat = ol.load(args.orbat)
    mapping, already = draft(orbat, lexique)

    out = args.output or os.path.join(os.path.dirname(os.path.abspath(args.orbat)),
                                      "mapping_brouillon.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=1)

    found = {k: v for k, v in mapping.items() if not k.startswith("_")}
    todo = mapping[TODO_KEY]
    print(f"Lexique : {path}")
    print(f"{len(found)} trouvé(s) / {len(todo)} à valider"
          + (f" / {len(already)} déjà codé(s)" if already else ""))
    for name, code in found.items():
        print(f"  {name!r} -> {code}")
    if todo:
        print("\nÀ valider (aucun code au lexique, ou plusieurs) :")
        for name in todo:
            c = mapping.get(CANDIDATES_KEY, {}).get(name)
            print(f"  {name!r}" + (f"  — candidats : {', '.join(c)}" if c else ""))
    if already:
        print("\nDéjà codés (absents du brouillon) : " + ", ".join(already))
    print(f"\nÉcrit dans {out}")


if __name__ == "__main__":
    main()
