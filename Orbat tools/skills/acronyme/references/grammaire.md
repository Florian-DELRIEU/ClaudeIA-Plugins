# Grammaire de composition

Ce fichier regroupe **toutes les règles de construction et de lecture** d'un code — séparateurs, duplication, gabarits, portée, notation numérique, fusions — par opposition aux tables de `references/*.md` qui donnent le **sens** de chaque code. Les règles cardinales (gouvernance) restent dans `SKILL.md` ; elles priment sur tout ce qui suit.

> Depuis le 2026-10-10, ce fichier reçoit la grammaire détaillée autrefois dans `SKILL.md` (sections du même nom) : un renvoi « `SKILL.md` § Séparateurs / § Gabarits / § Portée / § Notation numérique / § Règles de composition des fusions / § Désambiguïsation positionnelle » dans une entrée ancienne désigne la section homonyme ci-dessous.

> ⚠️ **Il n'existe aucune règle générative pour la famille `V*` (véhicules terrestres).**
> `V`, `VL`, `VM`, `VU`, `VB`, `VH`, `VTT`, `VBCI`, `VHMCI`… sont des **acronymes atomiques
> déclarés individuellement** dans `references/terrestres.md` : aucun ne se dérive par règle,
> aucun ne se décompose a posteriori. L'ancienne « grammaire compositionnelle `V` »
> (`V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}`) a été **supprimée le 2026-08-09** —
> ne jamais la réappliquer de mémoire (voir `decisions.md` § 1).

## Sommaire

- Séparateurs
- Règles de duplication (non-redondance, exclusion `SPG`/`ART`)
- Cas d'application — choisir entre `-`, `/`, `.`
- Gabarits
- Portée
- Compétences
- Notation numérique
- Règles de composition des fusions (désambiguïsation positionnelle)
- Liberté des rôles et armements cross-domaine
- Famille BRH (Breacher)
- 1. Fusion de gabarit hélicoptère `CH.L/M/H`
- 2. `C` vs `CA` — critère mécanique
- 3. Convention calibre
- 4. `MCA.AA` vs `MCAA`

---

## Séparateurs

### Hiérarchie de disponibilité (Rôles & Armements)

Les trois séparateurs `-`, `/`, `.` encodent un seul critère : **la disponibilité simultanée en combat**.

<!-- bassin: aucun -->
| Séparateur | Signification | Exemple | Interprétation |
|---|---|---|---|
| **`-`** | **Rupture de configuration** | `AA - CAS - REC` | Missions distinctes, reconditionnement **obligatoire** entre elles. Jamais deux à la fois. |
| **`/`** | **Coexistence distincte** | `REC / MG` | Deux choses **séparées mais présentes simultanément**, sans reconditionnement. |
| **`.`** | **Fusion** | `SW.PW` | **Un seul objet** aux deux propriétés fusionnées. |

### Délimiteurs (structure générale)

<!-- bassin: aucun -->
| Séparateur | Usage |
|---|---|
| `-` | Aussi : délimiteur Type↔Rôle, ou Rôle↔Armement |
| `()` | **Précisions circonstancielles** (propulsion `(J)`, cargaison `(H₂O)`, variante `(6)`) |

### Groupement

- `/` sépare les **blocs**, `.` lie **à l'intérieur** d'un bloc.
- Exemple : `AA.REC / CAS` = (chasse+reco ensemble) vs (bombardement seul).

### Exemples fusionnés

<!-- bassin: aucun -->
| Écriture | Décomposition | Sens |
|---|---|---|
| `SW.PW` | Épée + Énergétique | Épée énergétique : un objet, deux natures |
| `SW / PW` | Épée / Arme énergétique | Deux armes distinctes montées ensemble |
| `SW - PW` | Épée - Arme énergétique | Épée OU arme énergétique, reconditionnement |
| `CA.MG` | Canon auto + Mitrailleuse | Système de feu unique canon + coaxiale |
| `LZ / SW.PW` | Laser / (Épée + Énergie) | Deux systèmes distincts montés ensemble |

> Dans les **tables de référence** (format du 2026-10-10), la 1re colonne « Officiel » porte le seul code à écrire, la 2e « Alternatifs » ses alias de lecture (séparés par `, `). Deux codes distincts ne partagent jamais une ligne ; chaque table est balisée par bassin (`<!-- bassin: types -->`, `roles`, `precisions`, `aucun`) — `procedures.md` P7.

---

## Règles de duplication

- **Pas de doublon d'officiels** au sein des Types · **pas de doublon d'officiels** au sein des Rôles/Armements — sauf la liste fermée d'exceptions de la règle cardinale n°2 (`SKILL.md`).
- Un même acronyme **peut apparaître** dans Type ET Rôle/Armement — la **position** désambiguïse.

### Non-redondance Type → Rôle

Un **Type porte déjà un rôle implicite**, surtout s'il vient d'une fusion. Ne pas répéter dans la section Rôle un rôle que le Type contient déjà — c'est une **faute**.

<!-- bassin: aucun -->
| Type | Rôle implicite | Ne pas écrire |
|---|---|---|
| `VBCI` | Combat d'infanterie | ~~`VBCI-CI`~~ → `VBCI` |
| `TD` | Anti-char | ~~`TD-AT`~~ → `TD` |
| `SPG` | Soutien-feu direct | ~~`SPG-ART`~~ → voir exclusion |
| `SPART` | Tir indirect longue portée | ~~`SPART-ART`~~ → `SPART` |
| `VCI` | Combat d'infanterie | ~~`VCI-CI`~~ → `VCI` |

Le rôle n'est réécrit que s'il **précise ou nuance** ce que le Type ne dit pas.

### Exclusion `SPG` ↔ `ART`

`SPG` et `ART` sont **mutuellement exclusifs** :
- **`SPG`** = canon d'assaut / soutien-feu **direct**, appui rapproché. *Ex. : StuH, M44.*
- **`ART`** (ou `SP-ART` / `SPART`) = **tir indirect longue portée**. *Ex. : Hummel, M109, AuF1.*

Un véhicule est l'un **ou** l'autre, jamais `SPG-ART`.

---

## Cas d'application — choisir entre `-`, `/`, `.`

### Pour les rôles et missions

- **`-`** : passage exigeant un reconditionnement ; rôles exclusifs à l'instant T. Ex. `AA - CAS - REC`.
- **`/`** : rôles coexistant sans reconditionnement. Ex. `AA / REC`.
- **`.`** : rôles fusionnés en un concept inséparable (rare).

### Pour les armements

- **`-`** : changer d'arme exige reconditionnement/démontage. Ex. `HCA - LM`.
- **`/`** : deux armes simultanées, distinctes. Ex. `C.H / CAC`, `LZ / SW.PW`.
- **`.`** : un seul objet à deux propriétés fusionnées. Ex. `SW.PW`, `HCA.MG`.

### Arbre de décision rapide

```
"Puis-je utiliser les deux simultanément sans modification ?"
├─ Non, reconditionnement/démontage obligatoire → utiliser `-`
├─ Oui, mais ce sont deux choses distinctes → utiliser `/`
└─ Oui, c'est la même chose ayant deux natures → utiliser `.`
```

---

## Gabarits

`L` Léger · `M` Moyen · `H` Lourd · `SH` Super-Lourd
`2L / 2M / 2H` À deux mains (L/M/H)
`U` Unnamed / Drone — véhicule sans équipage

> **`.L` / `.M` / `.H` / `.SH` sont les seuls gabarits universels**, applicables à **tout Type** (et à tout armement : `C.H` = canon lourd) via le mécanisme de fusion `.` (voir § Séparateurs). Aucune famille de Types n'a de règle de gabarit propre : en particulier, il n'existe **aucune exception de gabarit pour la famille `V*`** (décision du 2026-08-09, voir `decisions.md`). Les codes qui portent une lettre de gabarit sans point (`VL`, `VBLTT`, `TL`, `TDM`, `LMG`…) sont des **acronymes atomiques déclarés**, pas le résultat d'une composition — ne jamais en dériver un nouveau par analogie.

---

## Portée

`___` Court *(à définir — voir `decisions.md` § 5)* · `MRG` Moyen · `LRG` Long · `SLRG` Super-long · `XRG` Extrême (quasi-illimité)

> Échelle **commune à tout le système**, y compris aux missiles (notation à lettre unique `S`/`M`/`L`/`X` abandonnée le 2026-07-30, collision avec les gabarits).
> ⚠️ Le cran « Court » n'a **plus de code** depuis le 2026-08-05 : `SRG` a été rendu à la fusée géostationnaire (`aeriens.md`). Placeholder `___` en attendant décision — ne pas produire de code court pour l'instant.

---

## Compétences

`-` Inférieur au standard · `+` Standard · `*` Supérieur au standard
*(Une valeur numérique peut préciser davantage)*

---

## Notation numérique

Les chiffres précisent un acronyme selon leur position (mêmes règles que le gabarit).

<!-- bassin: aucun -->
| Format | Signification | Exemple |
|---|---|---|
| `ACR#` | Nombre physique (roues, pattes…) collé | `VB6` = 6 roues · `MK6` = 6 pattes |
| `ACR(#)` | Variante ou modèle | `VU(6)` = camion variante 6 |
| `ACR.#t` | Poids en tonnes — remplace L/M/H | `VU.3t` = camion 3 t |
| `ACR.#` | Calibre en mm (armes) | `CA.20` = canon auto 20mm |
| `#ACR` | Nombre de tubes / canons jumelés (avant) | `2CA.20` = deux canons auto 20mm |

**Ordre complet :** `{Type}{#roues}({variante})-{#tubes}{Armement}.{calibre}` — ex. `VB6(2)-2CA.20`.

**Gabarit littéral vs calibre — mutuellement exclusifs** : `MCAA` (moyen approx.) vs `CAA.20` (exact) vs `2CAA.20`.

---

## Règles de composition des fusions

Les acronymes fusionnés (`TES`, `TEAT`, `VBCI`, `MCAA`…) sont des **unités atomiques** — non chaînables.

> ❌ `TES.AT` interdit · ✅ une fusion comme base, puis suffixes : `TEAT.STH.SD`

### Une variante n'a de sens que collée à sa racine

Une lettre de composition (ex. `G`) n'a **pas de sens fixe indépendant** de sa racine : `SP`+`G` → canon d'assaut automoteur · `CH`+`G` → hélico gunship. Fonctionnement normal de la composition, pas une exception.

### Une fusion n'existe que si explicitement déclarée

Une suite de lettres qui *ressemble* à un assemblage n'a **aucun sens automatique**. Un composé n'existe que s'il a été posé et journalisé — jamais par découpage visuel a posteriori. Ex. : `BMG` non déclaré n'existe pas, même s'il « se lit » `BM`+`G`. S'articule avec le workflow étape 8 (`SKILL.md`).

### Désambiguïsation positionnelle

Certains conflits se règlent **sans créer de code**, par la seule position (`T` isolé = Torpilleur · `.T` suffixe = Traçante ; même mécanique que `CAV`, `TA`, `RAD`, `MUN`). Table complète dans `decisions.md` § 3 ; liste fermée des exceptions dans `SKILL.md` § Règles cardinales n°2.

---

## Liberté des rôles et armements cross-domaine

Aucune restriction de domaine sur les rôles/armements (un rôle naval peut s'appliquer à un aéronef, etc.). Seuls les **Types** sont spécifiques à leur catégorie.

---

## Famille BRH (Breacher)

<!-- bassin: aucun -->
| Écriture | Logique |
|---|---|
| `BRH` | Breacher générique |
| `BRHE` · `BRHP` · `BRHG` · `BRHT` | BRH + cible (Explosif / Porte / Grillage / Tôle) — quatre codes distincts |
| `BLR` · `CSL` | L'outil (bélier / cisailles) implique le rôle → `BRH` omis |

Principe de **concision** : un sens implicite dans l'outil ou le Type n'est pas répété (`BLR` implique breacher — pas de `BRH.BLR`). Définitions : `infanterie.md` § Rôles d'infanterie.

---

## 1. Fusion de gabarit hélicoptère `CH.L/M/H`

Le gabarit d'un hélicoptère se note en **fusion `.`** (léger/moyen/lourd), combinable avec un rôle en suffixe : `CH.L-TT` (hélico léger de transport), `CH.L-ATT` (hélico léger d'attaque).

**Fusion `.` obligatoire, jamais infixe direct** (`CHL`/`CHM`/`CHH` interdits) : `CHM` colliderait avec `(CHM)` = Chimique (propulsion, `aeriens.md`) et avec le préfixe de `CHMED`. Décision actée le 2026-07-30 : la règle `.` s'applique uniformément aux trois gabarits (pas de traitement différencié par lettre).

---

## 2. `C` vs `CA` — critère mécanique, pas de calibre

- **`CA`** (canon automatique) = alimentation par **magasin ou bande** + capacité de **tir automatique / rafale** (ex. tourelle 20mm d'un VBCI, canon d'un CV90).
- **`C`** (canon) = pièce rechargée **obus par obus après chaque tir**, y compris avec **aide au chargement / autoloader** (ex. Leclerc, M10, canon de 90mm d'un EBR). Un chargeur automatique n'en fait **pas** un `CA` : il faut toujours engager un nouvel obus dans la culasse entre deux tirs.
- La distinction est **mécanique** (mode d'alimentation), indépendante du calibre.
- Gabarit du canon : `C.L` / `C.M` / `C.H` (gabarit universel). Les anciennes formes `LC` / `MC` / `HC` sont **supprimées** le 2026-10-10 — `LC` = Lance, `HC` = Hache.

> ⚠️ `C` et `G` sont deux armes distinctes, pas des alias : `C` = canon, `G` = obusier (`HWZ` alternatif de lecture).

---

## 3. Convention calibre (préférée au gabarit)

Quand le calibre est connu, l'ajouter en suffixe **fusionné par un point** plutôt que d'utiliser `L/M/H` : `C.90` (canon 90 mm), `CA.20` (canon auto 20 mm), `C.105`, `C.155`, `MOR.81`. Le gabarit `.L/.M/.H` reste le repli quand le calibre est inconnu ou non pertinent.

Exemples : `TD-C.90/MG`, `VBCI-CA.20/MG`, `SPG-C.155/MG`.

> ⚠️ **La forme collée (`C90`, `CA20`) est abandonnée le 2026-08-10** : elle contredisait § Notation numérique, où `ACR#` désigne un **nombre physique** (roues, pattes) — `C90` s'y lirait « 90 roues ». Conservée en lecture pour les fichiers antérieurs, ne plus produire.

---

## 4. `MCA.AA` vs `MCAA` — rôle circonstanciel vs fusion

- `MCA.AA` note un canon auto moyen en **rôle AA circonstanciel**.
- `MCAA` est la **fusion prédéfinie** pour un usage AA permanent.

Même logique pour `LCAA` et `HCAA`.
