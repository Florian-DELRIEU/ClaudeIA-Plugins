# Grammaire de composition (règles génératives)

Ce fichier regroupe les **règles de construction** d'un code — comment assembler un acronyme — par opposition aux tables de `references/*.md` qui donnent le **sens** de chaque code (définitions). À lire quand on compose un gabarit d'hélicoptère ou une pièce d'artillerie.

> ⚠️ **Il n'existe aucune règle générative pour la famille `V*` (véhicules terrestres).**
> `V`, `VL`, `VM`, `VU`, `VB`, `VH`, `VTT`, `VBCI`, `VHMCI`… sont des **acronymes atomiques
> déclarés individuellement** dans `references/terrestres.md` : aucun ne se dérive par règle,
> aucun ne se décompose a posteriori. L'ancienne « grammaire compositionnelle `V` »
> (`V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}`) a été **supprimée le 2026-08-09** —
> ne jamais la réappliquer de mémoire (voir `decisions.md` § 1 et § 6).
> Les seuls gabarits universels sont `.L` / `.M` / `.H` / `.SH` (mécanisme de fusion `.`,
> `SKILL.md` § Gabarits), applicables à tout Type.

## Table des matières

1. Fusion de gabarit hélicoptère `CH.L/M/H`
2. `C` vs `CA` — critère mécanique
3. Convention calibre (préférée au gabarit)
4. `MCA.AA` vs `MCAA` — rôle circonstanciel vs fusion

---

## 1. Fusion de gabarit hélicoptère `CH.L/M/H`

Le gabarit d'un hélicoptère se note en **fusion `.`** (léger/moyen/lourd), combinable avec un rôle en suffixe : `CH.L-TT` (hélico léger de transport), `CH.L-ATT` (hélico léger d'attaque).

**Fusion `.` obligatoire, jamais infixe direct** (`CHL`/`CHM`/`CHH` interdits) : `CHM` colliderait avec `(CHM)` = Chimique (propulsion, `aeriens.md`) et avec le préfixe de `CHMED`. Décision actée le 2026-07-30 : la règle `.` s'applique uniformément aux trois gabarits (pas de traitement différencié par lettre).

---

## 2. `C` vs `CA` — critère mécanique, pas de calibre

- **`CA`** (canon automatique) = alimentation par **magasin ou bande** + capacité de **tir automatique / rafale** (ex. tourelle 20mm d'un VBCI, canon d'un CV90).
- **`C`** (canon) = pièce rechargée **obus par obus après chaque tir**, y compris avec **aide au chargement / autoloader** (ex. Leclerc, M10, canon de 90mm d'un EBR). Un chargeur automatique n'en fait **pas** un `CA` : il faut toujours engager un nouvel obus dans la culasse entre deux tirs.
- La distinction est **mécanique** (mode d'alimentation), indépendante du calibre.

> ⚠️ `C` et `G` sont deux armes distinctes, pas des alias : `C` = canon, `G` = obusier.

---

## 3. Convention calibre (préférée au gabarit)

Quand le calibre est connu, l'ajouter en suffixe **fusionné par un point** plutôt que d'utiliser `L/M/H` : `C.90` (canon 90 mm), `CA.20` (canon auto 20 mm), `C.105`, `C.155`, `MOR.81`. Le gabarit `L/M/H` reste le repli quand le calibre est inconnu ou non pertinent.

Exemples : `TD-C.90/MG`, `VBCI-CA.20/MG`, `SPG-C.155/MG`.

> ⚠️ **La forme collée (`C90`, `CA20`) est abandonnée le 2026-08-10** : elle contredisait `SKILL.md` § Notation numérique, où `ACR#` désigne un **nombre physique** (roues, pattes) — `C90` s'y lirait « 90 roues ». Conservée en lecture pour les fichiers antérieurs, ne plus produire.

---

## 4. `MCA.AA` vs `MCAA` — rôle circonstanciel vs fusion

- `MCA.AA` note un canon auto moyen en **rôle AA circonstanciel**.
- `MCAA` est la **fusion prédéfinie** pour un usage AA permanent.

Même logique pour `LCAA` et `HCAA`.
