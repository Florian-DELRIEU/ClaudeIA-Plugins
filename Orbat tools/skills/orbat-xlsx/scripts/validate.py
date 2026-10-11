#!/usr/bin/env python3
"""
validate.py (orbat-xlsx) — raccourci vers le validateur UNIQUE du plugin,
`orbat-json/scripts/validate.py`, pour valider le JSON produit par
`xlsx_orbat.py tojson` :

    python3 scripts/validate.py OUT.json

(`tojson` lance déjà cette validation tout seul ; ce raccourci sert à revalider
un fichier retouché ensuite.) Aucune logique ici : l'ancienne copie locale
divergeait de l'original (contrôles d'unicité manquants) — elle est supprimée.
"""
import os
import runpy
import sys


def _orbat_json_scripts():
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
        if os.path.isfile(os.path.join(c, "validate.py")):
            return c
    sys.exit("Skill orbat-json introuvable. Définir ORBAT_TOOLS_ROOT sur la racine du plugin.")


target = os.path.join(_orbat_json_scripts(), "validate.py")
sys.argv[0] = target
runpy.run_path(target, run_name="__main__")
