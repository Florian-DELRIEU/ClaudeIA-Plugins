"""
Tests du skill `acronyme` (tables, check.py, collisions connues) — bibliothèque
standard seule. Complète TestAcronymeTables de test_orbat_tools.py.

    python3 -m unittest discover -s tests -v        (depuis la racine du plugin)
"""
import importlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACRONYME = os.path.join(ROOT, "skills", "acronyme")
SCRIPTS = os.path.join(ACRONYME, "scripts")
sys.path.insert(0, SCRIPTS)

T = importlib.import_module("tables")
chk = importlib.import_module("check")
bi = importlib.import_module("build_index")


def run(*args):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, "check.py"), *args],
                          capture_output=True, text=True,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))


class SkillCopy(unittest.TestCase):
    """Copie jetable du skill réel (pour y injecter un défaut)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.skill = os.path.join(self.tmp, "acronyme")
        shutil.copytree(ACRONYME, self.skill,
                        ignore=shutil.ignore_patterns("__pycache__"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def append_row(self, rel, after_prefix, row):
        p = os.path.join(self.skill, rel)
        with open(p, encoding="utf-8") as f:
            lines = f.read().split("\n")
        i = next(i for i, l in enumerate(lines) if l.startswith(after_prefix))
        lines.insert(i + 1, row)
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        with open(bi.index_path(self.skill), "w", encoding="utf-8") as f:
            f.write(bi.render(self.skill))      # INDEX à jour : seule la collision compte

    def collision_errors(self):
        errors, _ = chk.run_checks(self.skill)
        return [e for e in errors if "collision" in e]


class TestCollisionsConnues(SkillCopy):
    def test_skill_reel_collisions_toutes_enregistrees(self):
        self.assertEqual(self.collision_errors(), [])

    def test_nouveau_sens_sur_code_deja_en_collision(self):
        # MED est une collision connue (point ouvert § 5) : un 3e sens = ERREUR
        self.append_row("references/structures.md", "| MED |",
                        "| MED | | Mécanique de démonstration | |")
        errs = self.collision_errors()
        self.assertTrue(errs, "un sens nouveau doit faire échouer check.py")
        self.assertIn("Mécanique de démonstration", " ".join(errs))

    def test_nouveau_sens_sur_code_d_exception(self):
        # T est dans la liste d'exceptions de la règle 2 : l'exception ne couvre
        # que les sens enregistrés, pas un sens inventé
        self.append_row("references/terrestres.md", "| T |", "| T | | Trottinette | |")
        self.assertTrue(any("Trottinette" in e for e in self.collision_errors()))

    def test_nouvelle_collision_sur_code_sans_collision(self):
        self.append_row("references/structures.md", "| ZAB |", "| ZAB | | Zèbre abyssal |")
        self.assertTrue(any("`ZAB`" in e for e in self.collision_errors()))

    def test_accepter_collisions_enregistre(self):
        self.append_row("references/structures.md", "| ZAB |", "| ZAB | | Zèbre abyssal |")
        out = chk.accept_collisions(self.skill)
        self.assertTrue(any(e["code"] == "ZAB" for e in out))
        self.assertEqual(self.collision_errors(), [])


class TestCodeEtTables(unittest.TestCase):
    def test_code_insensible_a_la_casse(self):
        r = run("--code", "TK")
        self.assertIn("`Tk`", r.stdout)
        self.assertNotIn("LIBRE", r.stdout)

    def test_alias_declares_en_colonne_alternatifs(self):
        for code, off in (("IMV", "VLTT"), ("MRAP", "VMTT"), ("MEDEVAC", "MED"),
                          ("ZEP", "DR"), ("MGF", "BLM"), ("HF", "FCH")):
            r = run("--code", code)
            self.assertNotIn("LIBRE", r.stdout, code)
            self.assertIn("alternatif de `%s` : `%s`" % (off, code), r.stdout)

    def test_officiel_vide(self):
        (tab,) = T.parse_text("<!-- bassin: types -->\n| Officiel | Alternatifs | Signification |\n"
                              "|---|---|---|\n| | GEN.F | Génie franchissement |\n")
        (row,) = tab.rows
        self.assertEqual((row.officiel, row.alternatifs, row.codes), ("", ["GEN.F"], ["GEN.F"]))
        r = run("--code", "GEN.F")
        self.assertIn("sans officiel attribué", r.stdout)

    def test_check_complet_zero_erreur(self):
        r = run("-q")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
