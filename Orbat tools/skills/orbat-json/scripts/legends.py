"""
legends.py — module UNIQUE de légende « code → matériel réel » dans les
`description` d'unités (naming.md Règle 7 § 7.3 et 7.4).

Format canonique, le seul produit par les scripts du plugin :

    <phrase(s) de contexte — prose libre, conservée telle quelle>

    Équipement :
    * **CODE : Désignation réelle**

    Personnel :
    * **CODE : Désignation réelle**

- sans quantité (le nombre vit dans equipment/personnel de l'unité) ;
- une ligne par code ; Équipement et Personnel en blocs séparés ;
- hétérogénéité : plusieurs désignations jointes par « / »
  (`**VTT-LMG : BTR-60PB / OT-64 SKOT**`) ;
- la prose déjà présente dans la description est TOUJOURS conservée : seuls
  les anciens blocs de légende (ancien format `* CODE = …` compris) sont
  remplacés. Relancer un script est donc sans effet de bord (idempotent).

Utilisé par add_legends.py, add_local_legends.py et
orbat-acronymize/scripts/apply_rename_map.py.
"""
import re

EQUIP_HEADER = "Équipement :"
PERS_HEADER = "Personnel :"
HEADERS = (EQUIP_HEADER, PERS_HEADER)

# Lignes de légende reconnues (nouveau ET ancien format) -> (code, libellé).
_NEW_RE = re.compile(r"^\*\s+\*\*(.+?)\s:\s(.*)\*\*$")
_OLD_RE = re.compile(r"^\*\s+([^=]+?)\s=\s(.*)$")


# Forme d'un acronyme (VBTT, SQ-INF, MBT-105, CA.20…) : majuscules/chiffres et
# séparateurs du système, sans espace ni minuscule.
_CODE_LIKE_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-/()#]*$")


def _is_legend_code(code, known_codes):
    """Une ligne est une ligne de légende (donc remplaçable) si son code est
    connu du catalogue OU a la forme d'un acronyme — couvre les anciennes
    légendes dont le code a été renommé depuis. « Chef », « Adjoint »… restent."""
    return known_codes is None or code in known_codes or bool(_CODE_LIKE_RE.match(code))


def _parse_line(line):
    s = line.strip()
    m = _NEW_RE.match(s) or _OLD_RE.match(s)
    return (m.group(1).strip(), m.group(2).strip()) if m else None


def format_line(code, label):
    return f"* **{code} : {label}**"


def format_block(header, entries):
    """entries : liste ordonnée de (code, libellé)."""
    if not entries:
        return ""
    return "\n".join([header] + [format_line(c, l) for c, l in entries])


def build_legend(equipment_entries=(), personnel_entries=()):
    """Bloc de légende canonique (chaîne vide si rien à légender)."""
    blocks = [b for b in (format_block(EQUIP_HEADER, list(equipment_entries)),
                          format_block(PERS_HEADER, list(personnel_entries))) if b]
    return "\n\n".join(blocks)


def _iter_blocks(lines):
    """Découpe en blocs (en-tête, [lignes à puce qui suivent]) / ligne libre."""
    i = 0
    while i < len(lines):
        if lines[i].strip() in HEADERS:
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("*"):
                j += 1
            yield lines[i].strip(), lines[i + 1:j]
            i = j
        else:
            yield None, [lines[i]]
            i += 1


def strip_legend(description, known_codes=None):
    """
    Retire de `description` les lignes de légende (« * **CODE : …** » ou
    l'ancien « * CODE = … ») placées sous un en-tête « Équipement : » /
    « Personnel : », et renvoie la prose restante.

    `known_codes` (ensemble des codes du catalogue) : seules les lignes dont
    le CODE en fait partie OU a la forme d'un acronyme (majuscules/chiffres,
    ex. un ancien code renommé depuis) sont retirées — une liste écrite à la
    main sous « Personnel : » (« * Chef = Cne Dupont ») est donc préservée.
    L'en-tête n'est supprimé que si plus aucune puce ne reste dessous. Sans
    `known_codes`, toute ligne au format légende est retirée.
    """
    if not description:
        return ""
    kept = []
    for header, body in _iter_blocks(description.split("\n")):
        if header is None:
            kept.extend(body)
            continue
        rest = []
        for line in body:
            parsed = _parse_line(line)
            if parsed and _is_legend_code(parsed[0], known_codes):
                continue
            rest.append(line)
        if rest:
            kept.append(header)
            kept.extend(rest)
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_legend(description, known_codes=None):
    """{"equipment": {code: libellé}, "personnel": {...}} lus dans les blocs de
    légende existants (deux formats). Sert à reprendre une légende déjà posée."""
    out = {"equipment": {}, "personnel": {}}
    if not description:
        return out
    for header, body in _iter_blocks(description.split("\n")):
        if header is None:
            continue
        kind = "equipment" if header == EQUIP_HEADER else "personnel"
        for line in body:
            parsed = _parse_line(line)
            if parsed and (known_codes is None or parsed[0] in known_codes):
                out[kind][parsed[0]] = parsed[1]
    return out


def set_legend(node, equipment_entries=(), personnel_entries=(), known_codes=None):
    """
    Remplace la légende de `node["description"]` par la légende canonique,
    en conservant la prose (voir strip_legend pour `known_codes` — à passer :
    l'ensemble des codes du catalogue, plus ceux qu'on écrit). Si aucune
    entrée : retire l'ancienne légende et garde la prose (supprime la clé si
    la description devient vide). Renvoie la nouvelle description (ou None).
    """
    if known_codes is not None:
        known_codes = set(known_codes) | {c for c, _ in equipment_entries} \
            | {c for c, _ in personnel_entries}
    prose = strip_legend(node.get("description") or "", known_codes)
    legend = build_legend(equipment_entries, personnel_entries)
    desc = "\n\n".join(p for p in (prose, legend) if p)
    if desc:
        node["description"] = desc
        return desc
    node.pop("description", None)
    return None


def is_pure_legend(description, known_codes=None):
    """Vrai si la description ne contient QUE des blocs de légende (aucune prose)."""
    return bool((description or "").strip()) and not strip_legend(description, known_codes)


def catalog_codes(orbat):
    """Ensemble des codes des catalogues racine (equipment, personnel, supplies)."""
    return {e.get("name") for k in ("equipment", "personnel", "supplyCategories")
            for e in orbat.get(k, []) or []}


def extract_real_name(description):
    """
    Désignation réelle en tête d'une description de catalogue (Règle 5) :
    texte avant « — » (ou « - » entouré d'espaces). None si vide.
    """
    if not description:
        return None
    desc = description.strip()
    for sep in (" — ", " - "):
        if sep in desc:
            return desc.split(sep, 1)[0].strip() or None
    return desc or None
