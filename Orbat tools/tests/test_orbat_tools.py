"""
Tests de non-régression du plugin orbat-tools — bibliothèque standard seule.

    python3 -m unittest discover -s tests -v        (depuis la racine du plugin)

Chaque test qui porte un nom « test_bug_… » reproduit un défaut constaté lors
de l'audit d'octobre 2026 : s'il échoue, le défaut est revenu.
openpyxl est requis pour les tests orbat-xlsx (sautés sinon).
"""
import copy
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
JSON_SCRIPTS = os.path.join(SKILLS, "orbat-json", "scripts")
ACRO_SCRIPTS = os.path.join(SKILLS, "orbat-acronymize", "scripts")
XLSX_SCRIPTS = os.path.join(SKILLS, "orbat-xlsx", "scripts")
sys.path.insert(0, JSON_SCRIPTS)

import orbat_lib as ol   # noqa: E402
import new_orbat as no   # noqa: E402
import legends as lg     # noqa: E402
import validate as vd    # noqa: E402

try:
    import openpyxl  # noqa: F401
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


def run(script, *args, env=None):
    return subprocess.run([sys.executable, script, *map(str, args)],
                          capture_output=True, text=True, env=env)


def sample_orbat():
    """Petit ORBAT : 1 compagnie (sidc ami) avec 2 groupes VAB / VBL."""
    g1 = no.make_unit("1er Groupe", "escouade", "121100", equipment=[("VAB", 2)],
                      personnel=[("Fantassin", 8)])
    g2 = no.make_unit("2e Groupe", "escouade", "121100", equipment=[("VBL", 1), ("VAB", 1)])
    cie = no.make_unit("Compagnie", "compagnie", "121100", subUnits=[g1, g2])
    side = no.make_side("Bleu", [no.make_group("Groupe 1", [cie])])
    return no.new_orbat("Test", [side],
                        equipment=[("VAB", "VAB — véhicule de l'avant blindé"), ("VBL", "VBL")],
                        personnel=[("Fantassin", "Fantassin")])


def find(orbat, name):
    return ol.find_unit(orbat, name)


class TmpDir(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="orbat_test_")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def write(self, name, obj):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
        return path


# ---------------------------------------------------------------------------
class TestTemps(unittest.TestCase):
    def test_bug_dates_comparees_comme_du_texte(self):
        u = {"equipment": [{"name": "VAB", "count": 14}], "state": [
            {"t": "2025-01-01T10:00:00+01:00", "diff": {"equipment": [{"name": "VAB", "onHand": -8}]}},
        ]}
        # 10:00+01:00 = 09:00Z : la perte est déjà survenue à 09:05Z.
        self.assertEqual(ol.resource_at(u, "equipment", "2025-01-01T09:05:00Z")["VAB"], 6)
        self.assertEqual(ol.resource_at(u, "equipment", "2025-01-01T08:59:00Z")["VAB"], 14)

    def test_tri_chronologique_reel(self):
        u = {"state": [{"t": "2025-01-01T09:30:00Z"}, {"t": "2025-01-01T10:00:00+01:00"}]}
        self.assertEqual([s["t"] for s in ol.sorted_states(u)],
                         ["2025-01-01T10:00:00+01:00", "2025-01-01T09:30:00Z"])

    def test_formats_acceptes(self):
        a = ol.parse_time("2025-01-01T09:00:00Z")
        self.assertEqual(a, ol.parse_time("2025-01-01T10:00:00+01:00"))
        self.assertEqual(a, ol.parse_time("2025-01-01T09:00:00"))           # sans fuseau = UTC
        self.assertEqual(a, ol.parse_time(1735722000000))                     # epoch ms


class TestEchelons(unittest.TestCase):
    def test_bug_armee_accentuee_plantait(self):
        self.assertEqual(no.build_sidc("Armée", "121100")[8:10], "23")
        self.assertEqual(no.build_sidc("groupe d'armées", "000000")[8:10], "24")
        self.assertEqual(ol.echelon_code("Platoon"), "14")

    def test_table_unique(self):
        import condense_orbat as co
        import group_units as gu
        self.assertIs(co.ECHELON_NAMES, ol.ECHELON)
        self.assertIs(gu.ECHELON, ol.ECHELON)
        self.assertIs(no.ECHELON, ol.ECHELON)

    def test_mobilite_n_est_pas_un_echelon(self):
        self.assertIsNone(ol.echelon_of("10031500331211000000"))   # 33 = chenillé
        self.assertEqual(ol.echelon_of("10031000151211000000"), "15")
        self.assertIsNone(ol.echelon_of({"name": "group sans sidc"}))


class TestLegendes(unittest.TestCase):
    def test_prose_conservee_et_idempotent(self):
        node = {"description": "Unité de réservistes.\n\nÉquipement :\n* VAB = 4x VAB"}
        lg.set_legend(node, [("VBTT", "VAB")], [("INF", "Fantassin")])
        expected = ("Unité de réservistes.\n\nÉquipement :\n* **VBTT : VAB**"
                    "\n\nPersonnel :\n* **INF : Fantassin**")
        self.assertEqual(node["description"], expected)
        lg.set_legend(node, [("VBTT", "VAB")], [("INF", "Fantassin")])
        self.assertEqual(node["description"], expected)

    def test_liste_de_prose_hors_legende_intacte(self):
        node = {"description": "Points clés :\n* tient le pont\n* réserve"}
        lg.set_legend(node, [("MBT", "T-55")])
        self.assertTrue(node["description"].startswith("Points clés :\n* tient le pont\n* réserve"))


class TestAddLegends(TmpDir):
    def test_bug_personnel_range_sous_equipement(self):
        path = self.write("o.json", sample_orbat())
        r = run(os.path.join(JSON_SCRIPTS, "add_legends.py"), path)
        self.assertEqual(r.returncode, 0, r.stderr)
        g1 = find(ol.load(path), "1er Groupe")
        self.assertIn("Équipement :\n* **VAB : VAB**", g1["description"])
        self.assertIn("Personnel :\n* **Fantassin : Fantassin**", g1["description"])
        self.assertNotIn(" = ", g1["description"])


class TestAddLocalLegends(TmpDir):
    def test_bug_prose_ecrasee_et_format_ancien(self):
        o = sample_orbat()
        find(o, "1er Groupe")["description"] = "Groupe de tête, renforcé."
        path = self.write("o.json", o)
        spec = self.write("s.json", {"root": "Compagnie",
                                     "equipment_models": {"VAB": "VAB VTT", "VBL": "VBL Mk1"},
                                     "personnel_models": {"Fantassin": "Fantassin"}})
        r = run(os.path.join(JSON_SCRIPTS, "add_local_legends.py"), path, spec)
        self.assertEqual(r.returncode, 0, r.stderr)
        d = find(ol.load(path), "1er Groupe")["description"]
        self.assertTrue(d.startswith("Groupe de tête, renforcé.\n\nÉquipement :"))
        self.assertIn("* **VAB : VAB VTT**", d)
        self.assertNotIn("2x", d)
        run(os.path.join(JSON_SCRIPTS, "add_local_legends.py"), path, spec, "--avec-quantites")
        self.assertIn("* **VAB : 2x VAB VTT**", find(ol.load(path), "1er Groupe")["description"])


class TestRenommage(TmpDir):
    def _orbat_avec_timeline(self):
        o = sample_orbat()
        g2 = find(o, "2e Groupe")
        g2["state"] = [{"id": "s1", "t": "2025-01-01T10:00:00Z",
                        "update": {"equipment": [{"name": "VBL", "onHand": 0}]}}]
        return o

    def test_bug_convergence_de_codes(self):
        o = self._orbat_avec_timeline()
        before = {t: ol.resource_at(find(o, "2e Groupe"), "equipment", t)
                  for t in ("2025-01-01T09:00:00Z", "2025-01-01T11:00:00Z")}
        path = self.write("o.json", o)
        mapping = self.write("m.json", {"VAB": "VBTT", "VBL": "VBTT"})
        r = run(os.path.join(ACRO_SCRIPTS, "apply_rename_map.py"), path, mapping)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = ol.load(path)
        # catalogue : une seule entrée, désignations jointes
        cat = [e for e in out["equipment"] if e["name"] == "VBTT"]
        self.assertEqual(len(cat), 1)
        self.assertTrue(cat[0]["description"].startswith("VAB / VBL"))
        # lignes fusionnées
        g2 = find(out, "2e Groupe")
        self.assertEqual(g2["equipment"], [{"name": "VBTT", "count": 2}])
        # la légende du groupe qui n'a que des VAB ne cite pas le VBL
        g1 = find(out, "1er Groupe")
        self.assertIn("* **VBTT : VAB**", g1["description"])
        self.assertNotIn("VBL", g1["description"])
        self.assertNotIn("VBL", g1["name"])
        # le groupe mixte cite les deux
        self.assertIn("* **VBTT : VBL / VAB**", g2["description"])
        # quantités à toute date inchangées (VAB+VBL = VBTT)
        for t, res in before.items():
            self.assertEqual(ol.resource_at(g2, "equipment", t).get("VBTT", 0),
                             res.get("VAB", 0) + res.get("VBL", 0), t)
        errors, _, _ = vd.check(out)
        self.assertEqual(errors, [])

    def test_renommage_simple_inchange(self):
        path = self.write("o.json", sample_orbat())
        mapping = self.write("m.json", {"VBL": "VBL-REC"})
        r = run(os.path.join(ACRO_SCRIPTS, "apply_rename_map.py"), path, mapping, "--no-titles")
        self.assertEqual(r.returncode, 0, r.stdout)
        out = ol.load(path)
        self.assertEqual(find(out, "2e Groupe")["equipment"],
                         [{"name": "VBL-REC", "count": 1}, {"name": "VAB", "count": 1}])
        self.assertEqual(find(out, "2e Groupe")["name"], "2e Groupe")


class TestCondensation(TmpDir):
    def _orbat(self):
        sq1 = no.make_unit("SQ1", "escouade", "121100", personnel=[("INF", 10)],
                           equipment=[("VAB", 1)])
        sq1["state"] = [{"id": "a", "t": "2025-01-01T09:00:00Z", "location": [1, 2],
                         "diff": {"equipment": [{"name": "VAB", "onHand": -1}]}}]
        sq2 = no.make_unit("SQ2", "escouade", "121100", personnel=[("INF", 10)],
                           equipment=[("VAB", 1)])
        sq2["state"] = [{"id": "b", "t": "2025-01-01T10:00:00+01:00",
                         "update": {"personnel": [{"name": "INF", "onHand": 4}]}}]
        plt = no.make_unit("PLT", "peloton", "121100", subUnits=[sq1, sq2],
                           personnel=[("INF", 5)])
        plt["state"] = [{"id": "c", "t": "2025-01-01T11:00:00Z",
                         "update": {"personnel": [{"name": "INF", "onHand": 3}]}}]
        cie = no.make_unit("CIE", "compagnie", "121100", subUnits=[plt])
        side = no.make_side("Bleu", [no.make_group("G", [cie])])
        return no.new_orbat("T", [side], equipment=[("VAB", "VAB")],
                            personnel=[("INF", "Fantassin")])

    def _totals(self, o, t):
        out = {}
        for u in ol.iter_units(o):
            for k in ("equipment", "personnel"):
                for n, q in ol.resource_at(u, k, t).items():
                    out[(k, n)] = out.get((k, n), 0) + q
        return {k: v for k, v in out.items() if v}

    TIMES = ("2025-01-01T08:00:00Z", "2025-01-01T09:30:00Z", "2025-01-01T10:30:00Z",
             "2025-01-01T12:00:00Z")

    def test_bug_timeline_perdue_a_la_fusion(self):
        o = self._orbat()
        expected = {t: self._totals(o, t) for t in self.TIMES}
        path = self.write("o.json", o)
        sizes = self.write("s.json", {})
        r = run(os.path.join(JSON_SCRIPTS, "condense_orbat.py"), path, sizes,
                "--target", "peloton", "--no-elementize")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = ol.load(path)
        self.assertEqual(find(out, "PLT")["subUnits"], [])
        for t in self.TIMES:
            self.assertEqual(self._totals(out, t), expected[t], t)
        self.assertIn("non représentables", r.stdout)   # la position de SQ1 est signalée
        self.assertEqual(vd.check(out)[0], [])

    def test_bug_lignes_dupliquees_apres_elementarisation(self):
        o = self._orbat()
        find(o, "PLT")["personnel"] = [{"name": "INF", "count": 25}, {"name": "SQ-INF", "count": 1}]
        path = self.write("o.json", o)
        sizes = self.write("s.json", {"INF": {"elements": [
            {"code": "SQ-INF", "size": 10, "description": "Escouade d'infanterie (10 h)"}]}})
        r = run(os.path.join(JSON_SCRIPTS, "condense_orbat.py"), path, sizes, "--no-condense")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        pers = find(ol.load(path), "PLT")["personnel"]
        noms = [p["name"] for p in pers]
        self.assertEqual(len(noms), len(set(noms)), pers)
        self.assertEqual({p["name"]: p["count"] for p in pers}, {"SQ-INF": 3, "INF": 5})

    def test_bug_description_de_catalogue_vide(self):
        path = self.write("o.json", self._orbat())
        sizes = self.write("s.json", {"INF": {"elements": [{"code": "SQ-INF", "size": 10}]}})
        r = run(os.path.join(JSON_SCRIPTS, "condense_orbat.py"), path, sizes, "--no-condense")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Description manquante", r.stdout + r.stderr)

    def test_mobilite_jamais_fusionnee_comme_echelon(self):
        o = self._orbat()
        veh = {"id": "v1", "name": "Char isolé", "sidc": "10031500331205000000",
               "subUnits": [], "equipment": [{"name": "VAB", "count": 1}]}
        find(o, "CIE")["subUnits"].append(veh)
        path = self.write("o.json", o)
        sizes = self.write("s.json", {})
        run(os.path.join(JSON_SCRIPTS, "condense_orbat.py"), path, sizes,
            "--target", "compagnie", "--no-elementize")
        self.assertIsNotNone(find(ol.load(path), "Char isolé"))


class TestRegroupement(TmpDir):
    def test_bug_identite_forcee_a_ami(self):
        cies = [no.make_unit(f"{i}e Compagnie", "compagnie", "121100", identity="hostile")
                for i in range(1, 5)]
        reg = no.make_unit("Régiment", "regiment", "121100", subUnits=cies, identity="hostile")
        o = no.new_orbat("T", [no.make_side("Rouge", [no.make_group("G", [reg])], identity="6")])
        path = self.write("o.json", o)
        spec = self.write("s.json", [{"parent_name": "Régiment", "select_regex": "Compagnie",
                                      "group_size": 2, "new_echelon": "bataillon"}])
        r = run(os.path.join(JSON_SCRIPTS, "group_units.py"), path, spec)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = ol.load(path)
        bts = find(out, "Régiment")["subUnits"]
        self.assertEqual([b["name"] for b in bts], ["1er Bataillon", "2e Bataillon"])
        self.assertTrue(all(b["sidc"][3] == "6" for b in bts))
        self.assertTrue(all(b["sidc"][8:10] == "16" for b in bts))
        self.assertIn("sans shortName", r.stdout)


class TestVisibilite(TmpDir):
    def test_bug_racine_invisible_si_peu_profond(self):
        import apply_relative_visibility as av
        self.assertEqual(av.compute_side_bands(1), [[0, 24]])
        self.assertEqual(av.compute_side_bands(2)[0][0], 0)
        self.assertEqual(av.compute_side_bands(3)[0][0], 0)

    def test_exemple_documente_inchange(self):
        import apply_relative_visibility as av   # format.md : France D=4, prof. 1 = 0–13
        self.assertEqual(av.compute_side_bands(4), [[0, 13], [13, 16], [16, 18], [18, 24]])

    def test_dry_run_n_ecrit_rien(self):
        path = self.write("o.json", sample_orbat())
        before = self.read(path)
        r = run(os.path.join(JSON_SCRIPTS, "apply_relative_visibility.py"), path, "--dry-run")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.read(path), before)


@unittest.skipUnless(HAS_OPENPYXL, "openpyxl absent")
class TestXlsx(TmpDir):
    def _wb(self, empty_class=False):
        sys.path.insert(0, XLSX_SCRIPTS)
        xo = importlib.import_module("xlsx_orbat")
        wb = xo.new_workbook()
        tb = xo.TemplateBuilder("IFV PLT", echelon="Platoon", unit_class="MECH INF PLT",
                                sidc2525="SHGPUCIZ--*****")
        v = tb.platform("BMP 2 IFV", unit="IFV PLT")
        tb.crew(v, "GL RFL AK74 5.45MM")
        if empty_class:
            tb.platform(None, unit="IFV PLT")
        wb.templates["IFV PLT"] = tb.rows
        xo.add_unit(wb, "1 PLT", echelon="Platoon", unit_class="MECH INF PLT",
                    sidc2525="SHGPUCIZ--*****", template="IFV PLT")
        path = os.path.join(self.tmp, "o.xlsx")
        xo.save(wb, path)
        return path

    def test_bug_classe_vide(self):
        path = self._wb(empty_class=True)
        r = run(os.path.join(XLSX_SCRIPTS, "xlsx_orbat.py"), "validate", path)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("sans classe", r.stdout)
        out = os.path.join(self.tmp, "o.json")
        r = run(os.path.join(XLSX_SCRIPTS, "xlsx_orbat.py"), "tojson", path, out)
        self.assertNotIn("Traceback", r.stderr)

    def test_bug_identite_et_catalogue(self):
        path = self._wb()
        out = os.path.join(self.tmp, "o.json")
        r = run(os.path.join(XLSX_SCRIPTS, "xlsx_orbat.py"), "tojson", path, out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        o = ol.load(out)
        self.assertEqual(o["sides"][0]["standardIdentity"], "6")    # hostile (2525C « H »)
        for e in o["equipment"] + o["personnel"]:
            self.assertTrue(e["description"].startswith(e["name"] + " — "), e)
        self.assertIn("ERREURS : 0", r.stdout)
        r = run(os.path.join(XLSX_SCRIPTS, "validate.py"), out)   # raccourci
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestStructure(TmpDir):
    def test_aucune_copie_de_bibliotheque(self):
        for skill in os.listdir(SKILLS):
            if skill == "orbat-json":
                continue
            for f in ("orbat_lib.py", "new_orbat.py"):
                self.assertFalse(os.path.exists(os.path.join(SKILLS, skill, "scripts", f)),
                                 f"copie divergente possible : {skill}/scripts/{f}")

    def test_aide_de_tous_les_scripts(self):
        scripts = [os.path.join(d, f) for d in (JSON_SCRIPTS, ACRO_SCRIPTS)
                   for f in os.listdir(d) if f.endswith(".py")
                   and f not in ("orbat_lib.py", "legends.py")]
        if HAS_OPENPYXL:
            scripts.append(os.path.join(XLSX_SCRIPTS, "xlsx_orbat.py"))
        scripts.append(os.path.join(XLSX_SCRIPTS, "validate.py"))
        for s in scripts:
            r = run(s, "--help")
            self.assertEqual(r.returncode, 0, f"{s} --help : {r.stderr[-300:]}")

    def test_plugin_deplace_avec_variable(self):
        dst = os.path.join(self.tmp, "ailleurs")
        shutil.copytree(os.path.join(SKILLS, "orbat-acronymize"), os.path.join(dst, "orbat-acronymize"))
        env = dict(os.environ, ORBAT_TOOLS_ROOT=ROOT)
        path = self.write("o.json", sample_orbat())
        mapping = self.write("m.json", {"VBL": "VBL-REC"})
        r = run(os.path.join(dst, "orbat-acronymize", "scripts", "apply_rename_map.py"),
                path, mapping, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_table_des_echelons_du_skill_acronyme(self):
        codes = ol.load_echelon_codes()
        self.assertEqual(codes.get("bataillon"), "BT")

    def test_validate_signale_t_illisible(self):
        o = sample_orbat()
        find(o, "1er Groupe")["state"] = [{"id": "x", "t": "hier soir"}]
        errors, _, _ = vd.check(o)
        self.assertTrue(any("illisible" in e for e in errors))


# ---------------------------------------------------------------------------
# Régressions trouvées par la revue indépendante de la 0.25.0
# ---------------------------------------------------------------------------
class TestRevue(TmpDir):
    def test_relance_avec_mapping_complete_garde_la_legende(self):
        path = self.write("o.json", sample_orbat())
        script = os.path.join(ACRO_SCRIPTS, "apply_rename_map.py")
        run(script, path, self.write("m1.json", {"VAB": "VBTT"}), "--no-titles")
        r = run(script, path, self.write("m2.json", {"VAB": "VBTT", "VBL": "VLB"}), "--no-titles")
        self.assertEqual(r.returncode, 0, r.stdout)
        d = find(ol.load(path), "2e Groupe")["description"]
        self.assertIn("* **VBTT : VAB**", d)
        self.assertIn("* **VLB : VBL**", d)

    def test_description_de_catalogue_non_tronquee(self):
        o = sample_orbat()
        o["equipment"].append({"name": "T-72", "description": "T-72B3 modernisé"})
        find(o, "1er Groupe")["equipment"].append({"name": "T-72", "count": 1})
        path = self.write("o.json", o)
        run(os.path.join(ACRO_SCRIPTS, "apply_rename_map.py"), path,
            self.write("m.json", {"T-72": "MBT"}), "--no-titles")
        cat = {e["name"]: e["description"] for e in ol.load(path)["equipment"]}
        self.assertEqual(cat["MBT"], "T-72B3 modernisé")

    def test_liste_manuelle_sous_personnel_preservee(self):
        node = {"description": "Personnel :\n* Chef = Cne Dupont\n* **Adjoint : Lt Martin**"}
        lg.set_legend(node, [("VAB", "VAB")], known_codes={"VAB", "INF"})
        self.assertIn("* Chef = Cne Dupont", node["description"])
        self.assertIn("* **Adjoint : Lt Martin**", node["description"])
        self.assertIn("* **VAB : VAB**", node["description"])

    def test_echelon_00_reste_fusionnable(self):
        o = TestCondensation._orbat(self)
        elt = no.make_unit("Élément isolé", "00", "121100", equipment=[("VAB", 2)])
        find(o, "CIE")["subUnits"].append(elt)
        path = self.write("o.json", o)
        run(os.path.join(JSON_SCRIPTS, "condense_orbat.py"), path, self.write("s.json", {}),
            "--target", "compagnie", "--no-elementize")
        out = ol.load(path)
        self.assertIsNone(find(out, "Élément isolé"))
        self.assertEqual({e["name"]: e["count"] for e in find(out, "CIE")["equipment"]}, {"VAB": 4})

    def test_at_illisible_message_clair(self):
        path = self.write("o.json", sample_orbat())
        r = run(os.path.join(JSON_SCRIPTS, "aggregate.py"), path, "--at", "09:05Z")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn("ISO 8601", r.stderr)

    def test_formats_horaires_du_site(self):
        ref = ol.parse_time("2025-01-01T08:05:00Z")
        self.assertEqual(ol.parse_time("2025-01-01T09:05:00+0100"), ref)
        self.assertEqual(ol.parse_time("2025-01-01T09:05:00.1234567+01:00").replace(microsecond=0), ref)
        self.assertEqual(ol.parse_time("1735718700000"), ref)

    def test_ancienne_legende_d_un_code_renomme_remplacee(self):
        o = sample_orbat()
        g1 = find(o, "1er Groupe")
        g1["description"] = "Contexte.\n\nÉquipement :\n* VBTT = VAB"   # VBTT renommé depuis
        path = self.write("o.json", o)
        run(os.path.join(JSON_SCRIPTS, "add_legends.py"), path)
        d = find(ol.load(path), "1er Groupe")["description"]
        self.assertNotIn("VBTT", d)
        self.assertEqual(d.count("Équipement :"), 1)
        self.assertTrue(d.startswith("Contexte."))

    def test_relance_noeud_sans_nom_legende_exacte(self):
        o = sample_orbat()
        g1 = find(o, "1er Groupe")
        g1["subUnits"] = [{"id": "x1", "sidc": "10031500001211000000", "subUnits": [],
                           "equipment": g1.pop("equipment")}]          # porteur sans `name`
        path = self.write("o.json", o)
        script = os.path.join(ACRO_SCRIPTS, "apply_rename_map.py")
        run(script, path, self.write("m1.json", {"VAB": "VBTT", "VBL": "VBTT"}), "--no-titles")
        run(script, path, self.write("m2.json", {"VAB": "VBTT", "VBL": "VBTT", "Fantassin": "INF"}),
            "--no-titles")
        d = find(ol.load(path), "1er Groupe")["description"]
        self.assertIn("* **VBTT : VAB**", d)
        self.assertNotIn("VBL", d)

    def test_pas_de_fausse_convergence_entre_catalogues(self):
        o = sample_orbat()
        o["equipment"].append({"name": "Fantassin", "description": "Fantassin"})
        path = self.write("o.json", o)
        r = run(os.path.join(ACRO_SCRIPTS, "apply_rename_map.py"), path,
                self.write("m.json", {"Fantassin": "FUS"}), "--no-titles")
        self.assertNotIn("recevant plusieurs désignations", r.stdout)


if __name__ == "__main__":
    unittest.main()
