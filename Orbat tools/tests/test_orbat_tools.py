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


# ---------------------------------------------------------------------------
# Version suivante : titres opt-in, sidc_lookup, short_names, conformite,
# draft_mapping, FUNCTION_MAP UCA---. Les codes d'échelon/type sont passés
# explicitement (CODES) : ces tests ne dépendent pas du format exact de
# acronyme/references/groupements.md.
# ---------------------------------------------------------------------------
CODES = {"echelons": {"compagnie": "CIE", "bataillon": "BT", "division": "DIV",
                      "peloton": "PLT", "section": "SEC", "escouade": "SQ",
                      "groupe": "GRP", "regiment": "REG", "armee": "ARMY"},
         "types": {"infanterie": "INF", "blindes": "ARM", "commandement": "HQ",
                   "support": "SPT"}}


class TestTitresOptIn(TmpDir):
    SCRIPT = os.path.join(ACRO_SCRIPTS, "apply_rename_map.py")

    def test_titres_desactives_par_defaut(self):
        path = self.write("o.json", sample_orbat())
        r = run(self.SCRIPT, path, self.write("m.json", {"VAB": "VBTT"}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(find(ol.load(path), "1er Groupe")["name"], "1er Groupe")

    def test_titres_sur_demande(self):
        path = self.write("o.json", sample_orbat())
        r = run(self.SCRIPT, path, self.write("m.json", {"VAB": "VBTT"}), "--titres")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = ol.load(path)
        self.assertIsNotNone(find(out, "1er Groupe de VAB"))
        self.assertEqual(find(out, "2e Groupe")["name"], "2e Groupe")   # mixte : intact

    def test_no_titles_accepte_sans_effet(self):
        path = self.write("o.json", sample_orbat())
        r = run(self.SCRIPT, path, self.write("m.json", {"VAB": "VBTT"}), "--no-titles")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(find(ol.load(path), "1er Groupe")["name"], "1er Groupe")

    def test_brouillon_non_finalise_refuse(self):
        path = self.write("o.json", sample_orbat())
        before = self.read(path)
        r = run(self.SCRIPT, path, self.write("m.json", {"VAB": "VBTT", "_a_valider": ["VBL"]}))
        self.assertEqual(r.returncode, 2)
        self.assertIn("_a_valider", r.stderr)
        self.assertEqual(self.read(path), before)

    def test_cles_de_brouillon_ignorees(self):
        path = self.write("o.json", sample_orbat())
        r = run(self.SCRIPT, path, self.write("m.json", {"VAB": "VBTT", "_a_valider": [],
                                                         "_candidats": {}}))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("_a_valider", r.stdout)
        self.assertIn("VBTT", {e["name"] for e in ol.load(path)["equipment"]})


class TestSidcLookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sidc_lookup
        cls.sl = sidc_lookup

    def test_decode_complet(self):
        d = self.sl.decode("10031000151211005600")
        self.assertEqual(d["identity"], ("3", "ami"))
        self.assertEqual(d["symbol_set"][0], "10")
        self.assertEqual(d["echelon"], ("15", "Compagnie"))
        self.assertEqual(d["entity"], "121100")
        self.assertEqual(d["mod1"][0], "56")
        self.assertNotIn("mobility", d)

    def test_decode_mobilite_au_lieu_d_echelon(self):
        d = self.sl.decode("10031500331211000000")
        self.assertEqual(d["mobility"], ("33", "chenillé"))
        self.assertNotIn("echelon", d)

    def test_mauvais_precedent_signale(self):
        for sidc in ("10031000171205000000", "10031000171205010051"):
            d = self.sl.decode(sidc)
            self.assertTrue(any("mauvais précédent" in w and "121300" in w
                                for w in d["warnings"]), d["warnings"])
        self.assertFalse(any("précédent" in w
                             for w in self.sl.decode("10031000161213000000")["warnings"]))

    def test_decode_invalide(self):
        with self.assertRaises(ValueError):
            self.sl.decode("1003100015")

    def test_recherche_casse_et_accents(self):
        ents = {r["entity"] for r in self.sl.search("HUSSARDS")}
        self.assertIn("121300", ents)
        ents = {r["entity"] for r in self.sl.search("regiment cuirassier")}
        self.assertIn("120500", ents)
        self.assertEqual(len(self.sl.search("infanterie", limit=2)), 2)
        self.assertEqual(self.sl.search("zzzz-introuvable"), [])

    def test_lookup(self):
        r = self.sl.lookup("121300", "10")[0]
        self.assertTrue(r["attested"])
        self.assertTrue(r["examples"])
        r = self.sl.lookup("999999")[0]
        self.assertFalse(r["attested"])
        self.assertTrue(any("non attestée" in w for w in r["warnings"]))

    def test_cli(self):
        script = os.path.join(JSON_SCRIPTS, "sidc_lookup.py")
        r = run(script, "--decode", "10031000151211005600")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Compagnie", r.stdout)
        r = run(script, "hussards", "--set", "10")
        self.assertIn("| 121300 |", r.stdout)
        self.assertNotEqual(run(script).returncode, 0)                       # aucun mode
        self.assertNotEqual(run(script, "--decode", "123").returncode, 0)


class TestShortNames(TmpDir):
    @classmethod
    def setUpClass(cls):
        import short_names
        cls.sn = short_names

    def sn_of(self, name, parent=None, sidc=None):
        u = {"name": name}
        if sidc:
            u["sidc"] = sidc
        return self.sn.short_name_for(u, parent, codes=CODES)

    def test_forme_7_5(self):
        self.assertEqual(self.sn_of("23e Compagnie d'Infanterie"), "23e CIE-INF")
        self.assertEqual(self.sn_of('Bataillon "A" Blindé'), '"A" BT-ARM')
        self.assertEqual(self.sn_of("1ère Compagnie"), "1ère CIE")
        self.assertEqual(self.sn_of("2ème Section"), "2e SEC")
        self.assertEqual(self.sn_of("Compagnie B"), '"B" CIE')
        self.assertEqual(self.sn_of("Compagnie de commandement et de soutien"), "CIE-HQ.SPT")

    def test_garnison_et_toe_vide(self):
        self.assertEqual(self.sn_of("1ère Division Blindée — Allemagne Ø"),
                         "1ère DIV-ARM — Allemagne Ø")
        # garnison identique à celle du parent : non répétée (§ 7.7)
        self.assertEqual(self.sn_of("1er Régiment d'Infanterie — Berlin",
                                    {"name": "1ère Division — Berlin"}), "1er REG-INF")

    def test_formation_mere_jamais_repetee(self):
        parent = {"name": "DBA"}
        self.assertEqual(self.sn_of("1ère Compagnie DBA", parent), "1ère CIE")
        # échelon absent du nom : lu dans le sidc (15 = compagnie)
        self.assertEqual(self.sn_of("État-Major DBA", parent, "10031000151211000000"), "CIE-HQ")
        self.assertEqual(self.sn.repeats_parent({"name": "1ère Compagnie DBA"}, parent,
                                                codes=CODES), ["DBA"])
        # un parent au nom générique (« Infanterie ») n'est pas une répétition
        self.assertEqual(self.sn_of("1ère Compagnie d'Infanterie", {"name": "Infanterie"}),
                         "1ère CIE-INF")
        # le code du parent n'est pas repris non plus
        self.assertEqual(self.sn_of("2e Section de la 1ère Compagnie",
                                    {"name": "1ère Compagnie", "shortName": "1ère CIE"}),
                         "2e SEC")

    def test_rien_d_invente(self):
        d = self.sn.derive({"name": "Bleu"}, codes=CODES)
        self.assertIsNone(d["short_name"])
        self.assertTrue(d["reason"])
        d = self.sn.derive({"name": "Section d'Appui"}, codes=CODES)
        self.assertEqual(d["short_name"], "SEC")
        self.assertEqual(d["residual"], ["Appui"])         # signalé, jamais abrégé
        self.assertIsNone(self.sn_of("1ère Cie"))          # « Cie » n'est pas un code

    def test_noms_anglais_et_codes(self):
        self.assertEqual(self.sn_of("1st Section"), "1ère SQ")   # piège FR/EN, Règle 4
        self.assertEqual(self.sn_of("41 TANK BN"), "41e BT-ARM")
        self.assertEqual(self.sn_of("1er BT-INF"), "1er BT-INF")

    def test_ordinaux_us_2d_3d(self):
        # forme US Army « 2d / 3d » (orbat-nommage US-11) : numéro conservé
        self.assertEqual(self.sn_of("3d Battalion"), "3e BT")
        self.assertEqual(self.sn_of("2d Company"), "2e CIE")
        self.assertEqual(self.sn_of("2nd Company"), "2e CIE")

    def test_groupe_d_armees_sans_repli(self):
        # motif spécifique sans code : jamais de repli sur « groupe » / « army »
        for name in ("Groupe d'armées Nord", "Army Group Center"):
            d = self.sn.derive({"name": name, "sidc": "10031000241211000000"}, codes=CODES)
            self.assertIsNone(d["short_name"], (name, d))
            self.assertIn("sans code", d["reason"])

    def test_troop_squadron_jamais_mappes_d_office(self):
        # US : troop = compagnie (sidc 15) ; sans échelon au sidc : à vérifier
        self.assertEqual(self.sn_of("A Troop", sidc="10031000151211000000"), '"A" CIE')
        d = self.sn.derive({"name": "A Troop", "sidc": "10031000001211000000"}, codes=CODES)
        self.assertIsNone(d["short_name"])
        self.assertIn("ambigu", d["reason"])
        self.assertEqual(self.sn_of("2d Squadron", sidc="10031000161211000000"), "2e BT")

    def test_load_codes_lit_les_types(self):
        from unittest import mock
        g = os.path.join(self.tmp, "groupements.md")
        with open(g, "w", encoding="utf-8") as f:
            f.write("## Types d'unité (formation)\n\n| Désignation | Type | Description |\n"
                    "|---|---|---|\n| ARM / -B | Blindés | `ARM` officiel |\n"
                    "| -INF / -I | Infanterie | **Officiel** `INF` |\n| -REC / R | Reconnaissance | |\n"
                    "\n## Autre\n| X | Hors section | |\n")
        t = os.path.join(self.tmp, "terrestres.md")
        with open(t, "w", encoding="utf-8") as f:
            f.write("| HQ / Cmdt | Commandement | `HQ` officiel |\n")
        with mock.patch.object(ol, "load_echelon_codes", return_value={"Compagnie": "CIE"}):
            codes = self.sn.load_codes(g, t)
        self.assertEqual(codes["echelons"], {"compagnie": "CIE"})
        self.assertEqual(codes["types"], {"blindes": "ARM", "infanterie": "INF",
                                          "reconnaissance": "REC", "commandement": "HQ"})

    def _orbat(self):
        o = sample_orbat()
        find(o, "1er Groupe")["shortName"] = "GARDÉ"
        return o

    def test_cli_defaut_ne_remplit_que_les_manquants(self):
        path = self.write("o.json", self._orbat())
        r = run(os.path.join(JSON_SCRIPTS, "short_names.py"), path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = ol.load(path)
        self.assertEqual(find(out, "1er Groupe")["shortName"], "GARDÉ")
        codes = self.sn.load_codes()
        cie = find(out, "Compagnie")
        self.assertEqual(cie.get("shortName"), self.sn.short_name_for(cie, codes=codes))
        self.assertTrue(cie.get("shortName"))
        self.assertIn("ERREURS : 0", r.stdout)

    def test_cli_all_et_dry_run(self):
        path = self.write("o.json", self._orbat())
        before = self.read(path)
        r = run(os.path.join(JSON_SCRIPTS, "short_names.py"), path, "--all", "--dry-run")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("GARDÉ", r.stdout)                  # le changement est annoncé…
        self.assertEqual(self.read(path), before)         # …mais rien n'est écrit
        out_path = os.path.join(self.tmp, "out.json")
        run(os.path.join(JSON_SCRIPTS, "short_names.py"), path, "--all", "--output", out_path)
        self.assertNotEqual(find(ol.load(out_path), "1er Groupe")["shortName"], "GARDÉ")
        self.assertEqual(self.read(path), before)


class TestConformite(TmpDir):
    @classmethod
    def setUpClass(cls):
        import conformite
        cls.cf = conformite

    def _clean(self):
        """ORBAT conforme : shortName, légendes, catalogue utilisé et décrit."""
        g1 = no.make_unit("1er Groupe", "escouade", "121100", equipment=[("VBTT", 2)],
                          personnel=[("SQ-INF", 1)], shortName="1er GRP")
        cie = no.make_unit("1ère Compagnie d'Infanterie", "compagnie", "121100",
                           subUnits=[g1], shortName="1ère CIE-INF")
        o = no.new_orbat("T", [no.make_side("Bleu", [no.make_group("G", [cie])])],
                         equipment=[("VBTT", "VAB — transport de troupes")],
                         personnel=[("SQ-INF", "Groupe de combat")])
        for u in (g1, cie):
            lg.set_legend(u, [("VBTT", "VAB")], [("SQ-INF", "Groupe de combat")])
        return o

    def _run(self, o, **kw):
        kw.setdefault("codes", CODES)
        kw.setdefault("index", {"VBTT", "SQ-INF"})
        return self.cf.run(o, **kw)

    def test_orbat_conforme(self):
        src = {"totaux": {"equipment": {"VBTT": 2}, "personnel": {"SQ-INF": 1}}, "unites": {}}
        rep = self._run(self._clean(), source=src)
        self.assertEqual(rep["ecarts"], [], rep)
        self.assertTrue(any("Totaux généraux" in v for v in rep["verifie"]))

    def test_ecarts_detectes(self):
        o = self._clean()
        g1 = find(o, "1er Groupe")
        g1["name"] = "1er Groupe (renforcé)"
        del g1["shortName"]
        o["equipment"].append({"name": "INUTILE", "description": "x"})
        src = {"totaux": {"equipment": {"VBTT": 3}}, "unites": {}}
        rep = self._run(o, source=src)
        txt = "\n".join(rep["ecarts"])
        self.assertIn("VBTT source 3 ≠ fichier 2", txt)
        self.assertIn("parenthèses", txt)
        self.assertIn("shortName manquant", txt)
        self.assertIn("INUTILE", txt)

    def test_code_non_atteste_et_legende_manquante(self):
        o = self._clean()
        find(o, "1er Groupe")["description"] = "Groupe de tête."
        rep = self._run(o, index={"VBTT"})
        txt = "\n".join(rep["ecarts"])
        self.assertIn("non attesté", txt)
        self.assertIn("SQ-INF", txt)
        self.assertIn("sans légende", txt)

    def test_compose_avec_prefixe_numerique_et_calibre(self):
        # VU-2AACA.20 (exemple de terrestres.md) : VU et AACA attestés -> pas d'écart
        o = self._clean()
        g1 = find(o, "1er Groupe")
        g1["equipment"] = [{"name": "VU-2AACA.20", "onHand": 1}]
        o["equipment"].append({"name": "VU-2AACA.20", "description": "Gepard — AA"})
        lg.set_legend(g1, [("VU-2AACA.20", "Gepard")], [("SQ-INF", "Groupe de combat")])
        rep = self._run(o, index={"VBTT", "SQ-INF", "VU", "AACA"})
        self.assertFalse([e for e in rep["ecarts"] if "VU-2AACA.20" in e], rep["ecarts"])

    def test_totaux_a_une_date_et_sous_arbre(self):
        o = self._clean()
        find(o, "1er Groupe")["state"] = [{"id": "s", "t": "2025-01-01T10:00:00Z",
                                           "diff": {"equipment": [{"name": "VBTT", "onHand": -1}]}}]
        src = {"totaux": {"equipment": {"VBTT": 1}}, "unites": {}}
        self.assertEqual(self._run(o, source=src, at="2025-01-01T11:00:00Z")["ecarts"], [])
        self.assertTrue(self._run(o, source=src)["ecarts"])          # état de base : 2
        rep = self._run(o, source=src, at="2025-01-01T11:00:00Z", unit=find(o, "1er Groupe"))
        self.assertIn("1er Groupe", rep["scope"])
        self.assertEqual(rep["ecarts"], [])

    def test_lacune_sans_source(self):
        rep = self._run(self._clean())
        self.assertEqual(rep["ecarts"], [])
        self.assertTrue(any("NON confrontés" in x for x in rep["lacunes"]))

    def test_cli_trois_blocs_et_code_de_sortie(self):
        path = self.write("o.json", self._clean())
        src = self.write("src.json", {"equipment": {"VBTT": 5}})
        r = run(os.path.join(JSON_SCRIPTS, "conformite.py"), path, "--source", src)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for head in ("✅ Vérifié :", "⚠️ Corrigé :", "🔴 Non résolu :",
                     "| # | Contrôle | Résultat | Détail |"):
            self.assertIn(head, r.stdout)
        bad = self.write("bad.json", {"equipment": {"VBTT": "cinq"}})
        r = run(os.path.join(JSON_SCRIPTS, "conformite.py"), path, "--source", bad)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)


class TestDraftMapping(TmpDir):
    SCRIPT = os.path.join(ACRO_SCRIPTS, "draft_mapping.py")

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, ACRO_SCRIPTS)
        cls.dm = importlib.import_module("draft_mapping")

    LEX = {"VBTT": {"kind": "equipment", "materiel_reel": ["VAB"]},
           "MBT": {"kind": "equipment", "materiel_reel": ["AMX-30 B2"]},
           "CH-REC": {"kind": "equipment", "materiel_reel": ["Gazelle"]},
           "CH.L-ATT": {"kind": "equipment", "materiel_reel": ["gazelle"]},
           "SQ-INF": {"kind": "personnel", "materiel_reel": ["Groupe de combat", "VAB"]},
           "_comment": "ignoré"}

    def _orbat(self):
        o = sample_orbat()
        o["equipment"] = [{"name": "VAB", "description": "VAB"},
                          {"name": "amx 30b2", "description": ""},
                          {"name": "Gazelle", "description": ""},
                          {"name": "Engin X", "description": "Truc inconnu"},
                          {"name": "VBTT", "description": "déjà codé"},
                          {"name": "Char Y", "description": "AMX-30 B2 — modernisé"}]
        o["personnel"] = [{"name": "Groupe de combat", "description": ""}]
        return o

    def test_correspondances_sans_invention(self):
        lex = {k: v for k, v in self.LEX.items() if not k.startswith("_")}
        mapping, already = self.dm.draft(self._orbat(), lex)
        self.assertEqual(mapping["VAB"], "VBTT")              # exacte, kind equipment
        self.assertEqual(mapping["amx 30b2"], "MBT")          # normalisée
        self.assertEqual(mapping["Char Y"], "MBT")            # via la description (Règle 5)
        self.assertEqual(mapping["Groupe de combat"], "SQ-INF")
        self.assertIn("Engin X", mapping["_a_valider"])
        self.assertIn("Gazelle", mapping["_a_valider"])        # ambigu : jamais tranché
        self.assertEqual(sorted(mapping["_candidats"]["Gazelle"]), ["CH-REC", "CH.L-ATT"])
        self.assertNotIn("VBTT", mapping)
        self.assertEqual(already, ["VBTT"])
        codes = {v for k, v in mapping.items() if not k.startswith("_")}
        self.assertLessEqual(codes, set(self.LEX))            # aucun code hors lexique

    def test_cli_lexique_reel(self):
        path = os.path.join(ol.find_skill_dir("acronyme"), "identification", "lexique.json")
        with open(path, encoding="utf-8") as f:
            lex = {k: v for k, v in json.load(f).items() if not k.startswith("_")}
        exact, normd = self.dm.build_index(lex)
        pick = next(((k, n, c[0]) for k in ("equipment", "personnel")
                     for n, c in exact[k].items()
                     if len(c) == 1 and len(normd[k][self.dm.norm(n)]) == 1), None)
        if pick is None:
            self.skipTest("aucune désignation univoque dans le lexique")
        kind, name, code = pick
        o = sample_orbat()
        o["equipment"], o["personnel"] = [], []
        o[kind] = [{"name": name, "description": ""},
                   {"name": "Zzz Inexistant 123", "description": ""}]
        path = self.write("o.json", o)
        out = os.path.join(self.tmp, "brouillon.json")
        r = run(self.SCRIPT, path, "-o", out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(out, encoding="utf-8") as f:
            m = json.load(f)
        self.assertEqual(m[name], code)
        self.assertEqual(m["_a_valider"], ["Zzz Inexistant 123"])
        self.assertIn("1 trouvé(s) / 1 à valider", r.stdout)
        r = run(os.path.join(ACRO_SCRIPTS, "apply_rename_map.py"), path, out)
        self.assertEqual(r.returncode, 2)                      # brouillon non finalisé


@unittest.skipUnless(HAS_OPENPYXL, "openpyxl absent")
class TestXlsxFunctionMap(unittest.TestCase):
    def test_chars_uca_vers_120500(self):
        sys.path.insert(0, XLSX_SCRIPTS)
        xo = importlib.import_module("xlsx_orbat")
        self.assertEqual(xo.FUNCTION_MAP["UCA---"], "120500")
        sidc = xo._sidc_from(xo.Unit("1 TANK CO", echelon="Company", sidc2525="SHGPUCA---*****"))
        self.assertEqual(sidc[10:16], "120500")
        self.assertEqual(sidc[8:10], "15")
        self.assertEqual(sidc[3], "6")
        import sidc_lookup as sl                 # sidc.md fait autorité : 120500 = chars
        self.assertIn("char", ol.fold(sl.entity_labels().get("120500", "")))
        with open(os.path.join(XLSX_SCRIPTS, "xlsx_orbat.py"), encoding="utf-8") as f:
            self.assertNotIn("120500 = commandement", f.read())



ACRONYME = os.path.join(SKILLS, "acronyme")
ACRONYME_SCRIPTS = os.path.join(ACRONYME, "scripts")


class TestAcronymeTables(TmpDir):
    """Format « Officiel | Alternatifs », bassins, check.py (vague 2 de l'audit)."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, ACRONYME_SCRIPTS)
        cls.T = importlib.import_module("tables")
        cls.chk = importlib.import_module("check")
        cls.bi = importlib.import_module("build_index")

    OLD = ("## Échelons\n\n| Acronyme | Signification | Note |\n|---|---|---|\n"
           "| D / DIV | Division | `DIV` officiel |\n| BT / BN | Bataillon | |\n")
    NEW = ("## Échelons\n\n<!-- bassin: types -->\n"
           "| Officiel | Alternatifs | Signification | Note |\n|---|---|---|---|\n"
           "| DIV | D | Division | |\n| BT | BN | Bataillon | |\n")

    def test_parse_deux_formats(self):
        for text, fmt, bassin in ((self.OLD, "old", None), (self.NEW, "new", "types")):
            (tab,) = self.T.parse_text(text, "g.md")
            self.assertEqual((tab.fmt, tab.bassin), (fmt, bassin))
            got = [(r.officiel, sorted(r.alternatifs), r.meaning) for r in tab.rows]
            self.assertEqual(got, [("DIV", ["D"], "Division"), ("BT", ["BN"], "Bataillon")])
        (tab,) = self.T.parse_text("<!-- bassin: aucun -->\n| Code | Lecture |\n|---|---|\n"
                                   "| `X-Y` | exemple |\n")
        self.assertFalse(tab.defines_codes)

    def test_load_echelon_codes_nouveau_et_ancien_format(self):
        for text in (self.NEW, self.OLD):
            g = os.path.join(self.tmp, "groupements.md")
            with open(g, "w", encoding="utf-8") as f:
                f.write(text + "\n## Types d'unité (formation)\n")
            self.assertEqual(ol.load_echelon_codes(g), {"division": "DIV", "bataillon": "BT"})

    def _mini_skill(self, refs, decisions_5="", exceptions="TA"):
        root = os.path.join(self.tmp, "acro")
        os.makedirs(os.path.join(root, "references"), exist_ok=True)
        os.makedirs(os.path.join(root, "identification"), exist_ok=True)
        with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("# S\n\n## Règles cardinales\n\n<!-- exceptions-regle-2: %s -->\n" % exceptions)
        with open(os.path.join(root, "decisions.md"), "w", encoding="utf-8") as f:
            f.write("# D\n\n## 5. Codes encore non résolus\n\n| Code | Q |\n|---|---|\n%s\n"
                    % decisions_5)
        with open(os.path.join(root, "references", "a.md"), "w", encoding="utf-8") as f:
            f.write(refs)
        with open(os.path.join(root, "identification", "lexique.json"), "w", encoding="utf-8") as f:
            json.dump({"ZZ-QQ": {"kind": "equipment", "parts": ["ZZ", "QQ"]}}, f)
        with open(self.bi.index_path(root), "w", encoding="utf-8") as f:
            f.write(self.bi.render(root))
        return root

    TYPES = ("## Types\n\n<!-- bassin: types -->\n| Officiel | Alternatifs | Signification |\n"
             "|---|---|---|\n| ZZ | | Zèbre |\n| ZZ | | Char lourd |\n| TA | | Tank amphibie |\n"
             "| TA | | Observation artillerie |\n| KK | Q | Kayak |\n")
    ROLES = ("## Rôles\n\n<!-- bassin: roles -->\n| Officiel | Alternatifs | Signification |\n"
             "|---|---|---|\n| KK | | Kalachnikov |\n| QQ | | Quille |\n")

    def test_collisions_par_bassin_et_exceptions(self):
        root = self._mini_skill(self.TYPES + "\n" + self.ROLES)
        errors, warnings = self.chk.run_checks(root)
        coll = [e for e in errors if "collision" in e]
        self.assertEqual(len(coll), 1, errors)               # ZZ seul : TA est une exception,
        self.assertIn("`ZZ`", coll[0])                       # KK est dans deux bassins
        # point ouvert au § 5 : rétrogradé en avertissement
        root = self._mini_skill(self.TYPES + "\n" + self.ROLES, "| `ZZ` | à trancher |")
        errors, warnings = self.chk.run_checks(root)
        self.assertFalse([e for e in errors if "collision" in e], errors)
        self.assertTrue(any("`ZZ`" in w and "point ouvert" in w for w in warnings))

    def test_calibre_colle_et_renvoi_casse(self):
        refs = (self.ROLES.replace("| QQ | | Quille |", "| QQ | | Quille, voir `VBCI-CA30` |")
                + "\n| x | y |\n\nVoir `a.md` § Rôles et `a.md` § Section fantôme.\n"
                + "## ZZ\n\n<!-- bassin: types -->\n| Officiel | Alternatifs | Signification |\n"
                  "|---|---|---|\n| ZZ | | Zèbre |\n")
        root = self._mini_skill(refs)
        errors, _ = self.chk.run_checks(root)
        self.assertTrue(any("calibre collé `CA30`" in e for e in errors), errors)
        broken = [e for e in errors if "renvoi cassé" in e]
        self.assertEqual(len(broken), 1, errors)
        self.assertIn("Section fantôme", broken[0])

    def test_index_perime_et_parts_absents(self):
        root = self._mini_skill(self.ROLES.replace("| QQ | | Quille |\n", ""))
        errors, _ = self.chk.run_checks(root)
        self.assertTrue(any("`QQ` absent de l'INDEX" in e for e in errors), errors)
        with open(self.bi.index_path(root), "a", encoding="utf-8") as f:
            f.write("| `XX` | officiel | a.md |\n")
        errors, _ = self.chk.run_checks(root)
        self.assertTrue(any("relancer" in e for e in errors), errors)

    def test_code_cli(self):
        r = run(os.path.join(ACRONYME_SCRIPTS, "check.py"), "--code", "DIV")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("OFFICIEL", r.stdout)
        self.assertIn("groupements.md", r.stdout)
        r = run(os.path.join(ACRONYME_SCRIPTS, "check.py"), "--code", "D")
        self.assertIn("alternatif de `DIV`", r.stdout)
        r = run(os.path.join(ACRONYME_SCRIPTS, "check.py"), "--code", "QWZX")
        self.assertIn("LIBRE", r.stdout)

    def test_skill_reel_sans_erreur(self):
        r = run(os.path.join(ACRONYME_SCRIPTS, "check.py"), "-q")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ERREURS : 0", r.stdout)

    def test_tables_du_skill_au_nouveau_format(self):
        for p in self.T.code_files(ACRONYME):
            for tab in self.T.parse_file(p):
                self.assertIn(tab.bassin, self.T.BASSINS, "%s:%d sans balise" % (p, tab.line))
                if tab.defines_codes:
                    self.assertEqual(tab.fmt, "new", "%s:%d ancien format" % (p, tab.line))


if __name__ == "__main__":
    unittest.main()
