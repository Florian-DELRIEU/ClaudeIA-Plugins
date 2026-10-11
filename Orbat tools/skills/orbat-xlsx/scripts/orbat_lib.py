"""
orbat_lib.py — utilitaires partagés pour manipuler les fichiers ORBAT
exportés depuis orbat-mapper.app (type "ORBAT-mapper").

Format résumé :
  racine -> sides[] -> (groups[] -> subUnits[]) et/ou (units[])
  chaque unité : {id, name, sidc, subUnits[], equipment[{name,count}],
                  personnel[{name,count}], state[], ...}
  catalogues racine : equipment[{name,description}], personnel[{name,description}]

Toutes les fonctions sont sans effet de bord sauf mention contraire.
"""
import os
import json
import random
import string
import datetime

ID_ALPHABET = string.ascii_letters + string.digits


def load(path):
    """Charge un ORBAT JSON depuis un chemin."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(orbat, path):
    """Écrit un ORBAT JSON (indent=1, comme l'export du site)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(orbat, f, ensure_ascii=False, indent=1)


def gen_id(n=10):
    """Génère un id de la forme utilisée par orbat-mapper (10 caractères)."""
    return "".join(random.choice(ID_ALPHABET) for _ in range(n))


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Parcours de l'arbre
# ---------------------------------------------------------------------------
def iter_units(orbat, with_path=False):
    """
    Itère sur TOUTES les unités de l'ORBAT (récursif).
    Si with_path=True, yield (unit, path) où path est la liste des noms
    depuis le side jusqu'au parent inclus.
    """
    def rec(u, path):
        if with_path:
            yield u, path
        else:
            yield u
        for su in u.get("subUnits", []) or []:
            yield from rec(su, path + [u.get("name", "?")])

    for side in orbat.get("sides", []):
        base = [side.get("name", "?")]
        for u in side.get("units", []) or []:
            if u.get("name") is None and "rootUnitName" in u:
                continue  # placeholder de side (anciennes versions)
            yield from rec(u, base)
        for g in side.get("groups", []) or []:
            gpath = base + [g.get("name", "?")]
            for su in g.get("subUnits", []) or []:
                yield from rec(su, gpath)


def find_unit(orbat, key):
    """
    Retrouve une unité par son id exact, ou à défaut par nom exact,
    ou à défaut par nom partiel (insensible à la casse). Renvoie l'unité ou None.
    """
    key_l = key.lower()
    by_name = None
    by_partial = None
    for u in iter_units(orbat):
        if u.get("id") == key:
            return u
        if by_name is None and (u.get("name") or "").lower() == key_l:
            by_name = u
        if by_partial is None and key_l in (u.get("name") or "").lower():
            by_partial = u
    return by_name or by_partial


def subtree_units(root):
    """Itère sur une unité et toute sa descendance."""
    yield root
    for su in root.get("subUnits", []) or []:
        yield from subtree_units(su)


# ---------------------------------------------------------------------------
# Catalogues
# ---------------------------------------------------------------------------
def catalog_map(orbat, kind):
    """
    kind='equipment'|'personnel' -> {name: description} (catalogues racine).
    kind='supplies' -> lit supplyCategories {name: description}.
    """
    if kind == "supplies":
        return {e["name"]: e.get("description", "") for e in orbat.get("supplyCategories", []) or []}
    return {e["name"]: e.get("description", "") for e in orbat.get(kind, []) or []}


# ---------------------------------------------------------------------------
# Agrégation
# ---------------------------------------------------------------------------
def aggregate(units, kind="equipment"):
    """
    Somme les counts par name sur un itérable d'unités (état de BASE, hors timeline).
    kind = 'equipment' | 'personnel' | 'supplies'. Renvoie un dict {name: total}.
    """
    totals = {}
    for u in units:
        for item in u.get(kind, []) or []:
            totals[item["name"]] = totals.get(item["name"], 0) + item.get("count", 0)
    return totals


# ---------------------------------------------------------------------------
# Dimension temporelle (scénarios : champ state[] des unités)
# ---------------------------------------------------------------------------
# Un state[] est une liste d'entrées datées :
#   {id, t (ISO), location [lng,lat], via [[lng,lat]...], title,
#    status, sidc, symbolOptions,
#    update {equipment|personnel|supplies:[{name,onHand}]},  # valeurs ABSOLUES
#    diff   {equipment|personnel|supplies:[{name,onHand}]}}  # DELTAS
RESOURCE_KINDS = ("equipment", "personnel", "supplies")


def base_resources(unit, kind):
    """Quantités de base (champ `count`) d'une unité pour une catégorie."""
    return {it["name"]: it.get("count", 0) for it in unit.get(kind, []) or []}


def sorted_states(unit):
    """Entrées de state triées chronologiquement par `t`."""
    return sorted(unit.get("state", []) or [], key=lambda s: s.get("t", ""))


def resource_at(unit, kind, t=None):
    """
    Quantités d'une unité pour `kind` à l'instant `t` (ISO str) en rejouant la timeline.
    `update` pose des valeurs absolues (onHand), `diff` applique un delta.
    t=None -> état final. Renvoie {name: quantité}.
    """
    cur = base_resources(unit, kind)
    for st in sorted_states(unit):
        if t is not None and st.get("t", "") > t:
            break
        for it in (st.get("update", {}) or {}).get(kind, []) or []:
            cur[it["name"]] = it.get("onHand", 0)
        for it in (st.get("diff", {}) or {}).get(kind, []) or []:
            cur[it["name"]] = cur.get(it["name"], 0) + it.get("onHand", 0)
    return cur


def position_at(unit, t=None):
    """Dernière `location` [lng,lat] connue à l'instant t (ou finale si t=None). None si jamais positionnée."""
    pos = None
    for st in sorted_states(unit):
        if t is not None and st.get("t", "") > t:
            break
        if "location" in st:
            pos = st["location"]
    return pos


def unit_timeline(unit):
    """
    Liste lisible des moments-clés d'une unité : [(t, title, location, changements)].
    `changements` est une liste de chaînes décrivant update/diff/status/sidc.
    """
    out = []
    for st in sorted_states(unit):
        ch = []
        for tag in ("update", "diff"):
            blk = st.get(tag) or {}
            for kind, items in blk.items():
                ch.append(f"{tag}.{kind}: " +
                          ", ".join(f"{i['name']}={i.get('onHand')}" for i in items))
        if st.get("status"):
            ch.append(f"statut={st['status']}")
        if st.get("sidc"):
            ch.append("changement de symbole")
        out.append((st.get("t"), st.get("title"), st.get("location"), ch))
    return out


def scenario_events(orbat):
    """Événements globaux triés : [(startTime, title)]."""
    return sorted(((e.get("startTime"), e.get("title")) for e in orbat.get("events", []) or []),
                  key=lambda x: x[0] or "")


def vanished_elements(units):
    """
    Repère, parmi un itérable d'unités (ex. iter_units(orbat) ou subtree_units(root)),
    celles dont la DERNIÈRE entrée de state[] a `location: null`.

    Convention observée (confirmée par Florian sur « Opération Orage ») : quand une
    unité « mère » subit une perte (ex. un véhicule détruit) puis se décompose
    temporairement en plusieurs éléments suivis individuellement (escouades démontées,
    véhicules restants trackés à part), ces éléments enfants finissent typiquement par
    disparaître de la carte (`location: null`) au moment où ils se RÉEMBARQUENT / se
    REGROUPENT dans l'icône de l'unité mère — et non par destruction. La mère reprend
    alors sa propre timeline de position juste après.

    Pour distinguer d'une vraie perte : une perte se traduit par un `update`/`diff`
    NÉGATIF sur equipment/personnel (sur la mère ou l'élément lui-même), généralement
    AVANT ou AU déclenchement du détachement — pas par une simple disparition de
    position sans aucune variation de quantité associée.

    Renvoie la liste des unités concernées (chacune avec son `state` complet, à
    inspecter pour confirmer l'absence de perte associée).
    """
    out = []
    for u in units:
        sts = sorted_states(u)
        if sts and "location" in sts[-1] and sts[-1]["location"] is None:
            out.append(u)
    return out


# ---------------------------------------------------------------------------
# Nommage : indicateur de TOE vide et abréviations d'échelon (voir naming.md)
# ---------------------------------------------------------------------------
def mark_empty_subtrees(orbat, tag=" Ø"):
    """
    Suffixe `name` et `shortName` avec `tag` (par défaut " Ø", cf. naming.md
    Règle 3) sur toute unité dont le SOUS-ARBRE ENTIER (elle-même + toute sa
    descendance) ne porte ni `equipment` ni `personnel` nulle part.

    Condition stricte : une unité avec au moins une sous-unité non vide n'est
    PAS marquée, même si elle n'a rien en propre -- seuls les sous-arbres
    réellement et totalement vides le sont (calcul récursif post-ordre).

    À appeler en fin de construction (Tâche 4), après apply_word_substitutions
    le cas échéant, juste avant validate.py. Renvoie la liste des noms marqués.
    """
    def _is_empty(u):
        subs = u.get("subUnits") or []
        children_empty = [_is_empty(su) for su in subs]
        self_has_content = bool(u.get("equipment")) or bool(u.get("personnel"))
        subtree_empty = (not self_has_content) and all(children_empty)  # True aussi si pas d'enfants
        if subtree_empty:
            if not u.get("name", "").endswith(tag):
                u["name"] = (u.get("name") or "") + tag
            if u.get("shortName") and not u["shortName"].endswith(tag):
                u["shortName"] = u["shortName"] + tag
        return subtree_empty

    marked = []
    for side in orbat.get("sides", []):
        for g in side.get("groups", []) or []:
            for u in g.get("subUnits", []) or []:
                if _is_empty(u):
                    marked.append(u["name"])
        for u in side.get("units", []) or []:
            if u.get("name") and _is_empty(u):
                marked.append(u["name"])
    return marked


def apply_word_substitutions(orbat, subst_pairs, fields=("name", "shortName")):
    """
    Remplace, par mot entier (regex `\\b...\\b`), une liste de (pattern, remplacement)
    dans les champs choisis (par défaut name+shortName) de TOUTES les unités de
    l'ORBAT. Utilisé pour convertir des mots d'échelon d'une source externe vers
    une convention maison (cf. naming.md Règle 4).
    """
    import re
    for u in iter_units(orbat):
        for field in fields:
            val = u.get(field)
            if not val:
                continue
            for pattern, repl in subst_pairs:
                val = re.sub(pattern, repl, val)
            u[field] = val


# ---------------------------------------------------------------------------
# Mots d'échelon d'une source anglaise -> acronymes du skill `acronyme` (v4).
#
# SOURCE UNIQUE DES CODES : `../../acronyme/references/groupements.md` § Échelons.
# Ce module ne doit PAS contenir de liste d'acronymes en dur (risque de divergence
# dès que Florian modifie une décision dans le skill `acronyme`). Ce qui vit
# légitimement ici, c'est la cartographie « forme anglaise -> NOTION d'échelon » ;
# la notion est ensuite résolue en code par lecture du fichier.
#
# Voir naming.md Règle 4 pour le piège FR/EN sur "Section" (échelon escouade ici,
# pas peloton) et le périmètre volontairement exclu (Team/Pair/Group/Crew).
# ---------------------------------------------------------------------------

# Cartographie propre aux skills ORBAT : forme source (EN) -> notion d'échelon (FR).
EN_SOURCE_WORD_TO_ECHELON = [
    (r"\bBattalion\b", "bataillon"), (r"\bBn\b", "bataillon"),
    (r"\bCompany\b", "compagnie"), (r"\bCoy\b", "compagnie"),
    (r"\bPlatoon\b", "peloton"), (r"\bPlt\b", "peloton"),
    (r"\bTroop\b", "peloton"), (r"\bTp\b", "peloton"),
    (r"\bSection\b", "escouade"), (r"\bSect\b", "escouade"),
    (r"\bDetachment\b", "détachement"), (r"\bDet\b", "détachement"),
    (r"\bBattery\b", "batterie"), (r"\bBty\b", "batterie"),
]

DEFAULT_GROUPEMENTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "acronyme", "references", "groupements.md")


def load_echelon_codes(groupements_path=None):
    """
    Lit `acronyme/references/groupements.md` § Échelons et renvoie
    {notion d'échelon en minuscules -> code v4 canonique}.

    Choix du code, dans l'ordre (décision Florian du 2026-08-09) :
      1. la forme explicitement annotée dans la colonne Note, motif ``\`XXX\` officiel``
         (ex. Bataillon `BT / BN` + note "`BT` officiel" -> BT) ;
      2. à défaut, le PREMIER code de la cellule « Acronyme ».
    Supposer que la première forme est officielle était faux : `D / DIV` donnait `D`
    alors que `DIV` est la forme officielle. L'annotation prime toujours.

    Lève FileNotFoundError si le skill `acronyme` n'est pas installé à côté :
    c'est volontaire — mieux vaut échouer bruyamment que renommer un ORBAT entier
    avec des codes périmés.
    """
    import re as _re
    path = groupements_path or DEFAULT_GROUPEMENTS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            "Table des échelons introuvable : %s\n"
            "Le skill `orbat-tools:acronyme` est la source unique des acronymes ; "
            "l'installer/le localiser, ou passer groupements_path explicitement." % path)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    start = text.find("## Échelons")
    if start == -1:
        raise ValueError("Section '## Échelons' absente de %s" % path)
    end = text.find("\n## ", start + 1)
    block = text[start:end if end != -1 else len(text)]

    codes = {}
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in ("acronyme", "code"):
            continue
        forms = [f.strip().strip("`") for f in cells[0].split("/") if f.strip()]
        if not forms:
            continue
        code = forms[0]
        note = cells[2] if len(cells) > 2 else ""
        m = _re.search(r"`([^`]+)`\s+officiel", note)
        if m and m.group(1).strip() in forms:
            code = m.group(1).strip()
        for meaning in cells[1].split("/"):
            meaning = meaning.strip().lower()
            if meaning and meaning not in codes:
                codes[meaning] = code
    if not codes:
        raise ValueError("Aucun échelon lu dans %s" % path)
    return codes


def build_echelon_word_subst(groupements_path=None, extra=()):
    """
    Construit la liste (pattern, remplacement) à passer à
    `apply_word_substitutions`, en résolvant chaque notion d'échelon via
    `load_echelon_codes` — donc toujours à jour vis-à-vis du skill `acronyme`.

    Remplace l'ancienne constante ECHELON_WORD_SUBST_EN_TO_NOMV4 (figée, retirée
    en août 2026 pour cause de risque de divergence de version — elle a survécu
    dix jours de plus dans la copie d'orbat-xlsx, d'où l'alignement des deux
    exemplaires le 2026-08-10).
    """
    codes = load_echelon_codes(groupements_path)
    pairs = []
    missing = []
    for pattern, notion in list(EN_SOURCE_WORD_TO_ECHELON) + list(extra):
        code = codes.get(notion)
        if code is None:
            missing.append(notion)
            continue
        pairs.append((pattern, code))
    if missing:
        raise KeyError(
            "Notions d'échelon absentes de groupements.md : %s — "
            "vérifier la table § Échelons du skill `acronyme` avant de renommer."
            % ", ".join(sorted(set(missing))))
    return pairs


if __name__ == "__main__":
    import sys
    o = load(sys.argv[1])
    print("name:", o.get("name"), "| version:", o.get("version"))
    print("unités:", sum(1 for _ in iter_units(o)))
    print("equipment catalog:", len(o.get("equipment", [])),
          "| personnel catalog:", len(o.get("personnel", [])))
