---
name: acronyme
description: "Système de nomenclature militaire modulaire V4 (et extensions V5 en cours). Déclencher IMPÉRATIVEMENT dès que Florian tape /acronyme, ou dès que l'utilisateur mentionne un acronyme militaire, un code de véhicule, une unité, un navire, un aéronef, une structure, un personnage, ou demande de nommer / classifier / identifier / vérifier / étendre un élément dans ce système — y compris à partir d'un matériel réel (nom de véhicule, ORBAT à convertir). Également applicable au projet sci-fi Cosmotter pour la classification de vaisseaux spatiaux. Utiliser même si la demande semble simple (ex: \"c'est quoi le code pour X ?\", \"est-ce que Y entre en conflit avec Z ?\", \"comment noter un transport de troupes ?\").\n"
---

# Système de Nomenclature Militaire V4

*Dernière révision : 2026-08-16.*

## Sommaire

- **Gouvernance** : Principe général · Règles cardinales · Autorité de validation · Workflow de vérification
- **Grammaire** : Séparateurs · Règles de duplication · Cas d'application `-`/`/`/`.` · Gabarits · Portée · Compétences · Notation numérique · Composition des fusions
- **Renvois** : tables de référence · identification · journal des décisions · procédures · grammaire de composition

> ⚠️ **Avant toute proposition ou validation de code, lire `decisions.md`** (journal daté : décisions établies, cas confirmés sans conflit, codes non résolus, collectifs) **et appliquer `procedures.md`** (les 8 procédures de validation). Ne jamais rouvrir un cas déjà tranché ni reproduire un revirement.

---

## Principe général

Format de base : `{Type(Précision)} - {Rôle/Armement} - {Rôle/Armement} - …`

La section **Type** identifie la catégorie du véhicule/unité/structure.
La section **Rôle/Armement** précise la mission principale puis secondaire, par ordre d'importance décroissant.

> ⚠️ L'ordre des rôles est sémantique : `L.AA-REC` ≠ `REC-L.AA`

---

## Règles cardinales (gouvernance globale)

Ces quatre règles priment sur toute interprétation locale. Elles définissent *ce que le système valide* et *comment lire un code*.

### 1. Combinabilité totale, sans jugement sémantique

Tout Type et tout Rôle/Armement est combinable avec n'importe quel autre, **sans aucune restriction de cohérence sémantique**. Le système ne valide que la justesse **structurelle/grammaticale** d'un acronyme (bon séparateur, pas de doublon interdit, fusion bien déclarée…), jamais le sens ou la plausibilité du résultat.

- La question n'est jamais *« est-ce que cette combinaison a un sens »*, mais *« est-ce qu'on comprend ce qu'elle signifie »* (déchiffrage).
- Exemples 100 % valides bien qu'absurdes sémantiquement : `MT-CAS`, `BB-AGR`, `A-FUC`.
- S'applique à tout le système : Types et Rôles/Armements partagent chacun **un bassin unique**, libre de combinaison cross-domaine.
- **Ne jamais** signaler une combinaison comme « invalide » pour cause d'absurdité sémantique — seule une faute de construction la rend invalide.

### 2. Officiel vs Alternatif (lecture vs écriture)

Chaque acronyme ayant plusieurs notations valides doit avoir **UN SEUL officiel**.

**Critères de désignation de l'officiel** (dans l'ordre) :
1. **Strictement unique** dans son bassin (Types ou Rôles/Armements) — aucune collision de sens possible, même hors contexte. Critère **non négociable**.
2. **Le plus compact possible** parmi les candidats uniques. Départage par cohérence si ex-æquo.

- **En lecture** (déchiffrer un code fourni) : accepter et décoder correctement l'officiel **et** toutes ses alternatives.
- **En écriture** (produire/proposer un code) : n'utiliser **que** l'officiel, jamais une alternative.

Les notations alternatives peuvent avoir des collisions entre elles, gérables par le contexte — **seul l'officiel doit rester rigoureusement sans ambiguïté.** (Conséquence pour la vérification : ne signaler que les collisions entre **officiels** ; une collision d'alternatives n'est pas un défaut — cf. `procedures.md` P2.)

> Convention de travail : `*` devant l'acronyme retenu comme officiel dans les listes de travail (ex. `-B / *ARM`), à retirer une fois l'officialisation terminée.

### 3. Type par défaut pour tout acronyme isolé

La structure de base est toujours `<Type>-<Rôle1>-<Rôle2>…` : le premier élément est **toujours** un Type. Un acronyme vu **seul** se lit **par défaut comme un Type**, jamais comme un Rôle — même si ce code existe aussi en Rôle/Armement.

> Exemple : `CA` seul = **Croiseur lourd** (Type maritime), **pas** Canon Automatique, bien que les deux existent.

**Nuance lecture vs écriture :**
- **En lecture**, code isolé existant comme Type et Rôle → lu comme **Type** par défaut.
- **En lecture**, code n'existant **que** comme Rôle → lu comme ce Rôle **uniquement si Florian a signalé** que le contexte permet l'omission du Type. Sinon, on suppose un Type sous-entendu.
- **En écriture**, toujours inclure le Type ; jamais un code Rôle-seul, sauf ordre explicite.

### 4. Aucune réservation par contexte (époque, univers, thème)

Un regroupement thématique — table, section, titre comme « Médiéval », « SF », « Cosmotter »… — n'est **jamais** une contrainte d'usage, seulement un classement de confort pour naviguer le document. Un acronyme est utilisable dans **n'importe quel contexte** (n'importe quelle époque, n'importe quel univers) dès lors que ce qu'il décrit correspond — indépendamment de la table ou de la section où il est rangé.

- Seule une restriction **écrite explicitement dans la description de l'acronyme lui-même** vaut indication de contexte (ex. `VOL` = « souvent 1800s », `terrestres.md`) — et même alors, elle reste une indication typique, pas un verrou.
- Les univers fictifs (Warhammer 40K, Cosmotter…) sont des **occasions** ayant fait naître certains acronymes (notamment côté spatial) — ils ne les réservent pas à cet univers. Voir § Extensions spatiales.
- Les lexiques d'identification séparés (`lexique.json` / `lexique-40k.json`) sont des **outils de recherche par contexte de matériel**, pas des définitions concurrentes ni des frontières de sens.

> Actée le 2026-08-16 — voir `decisions.md` § 1 et § 6 pour le détail des fichiers concernés.

---

## Autorité de validation — Florian seul

**Claude vérifie, ne valide ni n'ajoute jamais unilatéralement.** Le rôle de Claude s'arrête à : identifier les conflits, signaler les redondances, proposer des alternatives argumentées. La décision d'adopter un acronyme — et de le journaliser dans un lexique ou une table — appartient exclusivement à Florian. Tant qu'il n'a pas confirmé, un acronyme discuté reste une **proposition vérifiée**, pas une décision actée : ne pas l'ajouter aux « Décisions établies », aux lexiques, ni le traiter comme acquis ensuite.

Les étapes concrètes d'une validation sont dans **`procedures.md`** — la mise en œuvre de cette autorité.

---

## Workflow de vérification (à appliquer systématiquement)

Quand l'utilisateur propose ou demande un acronyme :

1. **Identifier la catégorie** (Type ? Rôle ? Armement ? Structure ?).
2. **Vérifier l'absence de conflit** dans la même catégorie (pas de doublon d'officiels — `procedures.md` P2).
3. **Vérifier la cohérence positionnelle** (un même acronyme en Type et Rôle est OK).
4. **Appliquer les décisions établies** (`decisions.md` § 1) ; vérifier cas confirmés (§ 2) et non résolus (§ 5).
5. **Choisir le bon séparateur** : `-` reconditionnement · `/` coexistence distincte · `.` fusion.
6. **Proposer des alternatives** si conflit, avec justification.
7. **Signaler les redondances** (ex. `AN` superflu si l'armement implique anti-navire ; non-redondance Type→Rôle).
8. **Signaler toute absence de correspondance au lexique** (2026-07-30) : si le code (ou un composant `parts`) ne correspond à aucune entrée de `identification/lexique.json` / `lexique-40k.json` / `chassis-types.md`, le dire explicitement — jamais rester silencieux. Ex. « `X-Y` n'existe pas encore au lexique : composé à la volée, à journaliser si tu valides ».

---

## Séparateurs

### Hiérarchie de disponibilité (Rôles & Armements)

Les trois séparateurs `-`, `/`, `.` encodent un seul critère : **la disponibilité simultanée en combat**.

| Séparateur | Signification | Exemple | Interprétation |
|---|---|---|---|
| **`-`** | **Rupture de configuration** | `AA - CAS - REC` | Missions distinctes, reconditionnement **obligatoire** entre elles. Jamais deux à la fois. |
| **`/`** | **Coexistence distincte** | `REC / MG` | Deux choses **séparées mais présentes simultanément**, sans reconditionnement. |
| **`.`** | **Fusion** | `SW.PW` | **Un seul objet** aux deux propriétés fusionnées. |

### Délimiteurs (structure générale)

| Séparateur | Usage |
|---|---|
| `-` | Aussi : délimiteur Type↔Rôle, ou Rôle↔Armement |
| `()` | **Précisions circonstancielles** (propulsion `(J)`, cargaison `(H₂O)`, variante `(6)`) |

### Groupement

- `/` sépare les **blocs**, `.` lie **à l'intérieur** d'un bloc.
- Exemple : `AA.REC / CAS` = (chasse+reco ensemble) vs (bombardement seul).

### Exemples fusionnés

| Acronyme | Décomposition | Sens |
|---|---|---|
| `SW.PW` | Épée + Énergétique | Épée énergétique : un objet, deux natures |
| `SW / PW` | Épée / Arme énergétique | Deux armes distinctes montées ensemble |
| `SW - PW` | Épée - Arme énergétique | Épée OU arme énergétique, reconditionnement |
| `CA.MG` | Canon auto + Mitrailleuse | Système de feu unique canon + coaxiale |
| `LZ / SW.PW` | Laser / (Épée + Énergie) | Deux systèmes distincts montés ensemble |

---

## Règles de duplication

- **Pas de doublon** au sein des Types · **pas de doublon** au sein des Rôles/Armements.
- Un même acronyme **peut apparaître** dans Type ET Rôle/Armement — la **position** désambiguïse.

### Non-redondance Type → Rôle

Un **Type porte déjà un rôle implicite**, surtout s'il vient d'une fusion. Ne pas répéter dans la section Rôle un rôle que le Type contient déjà — c'est une **faute**.

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

## Cas d'application — Choisir entre `-`, `/`, `.`

### Pour les rôles et missions

- **`-`** : passage exigeant un reconditionnement ; rôles exclusifs à l'instant T. Ex. `AA - CAS - REC`.
- **`/`** : rôles coexistant sans reconditionnement. Ex. `AA / REC`.
- **`.`** : rôles fusionnés en un concept inséparable (rare).

### Pour les armements

- **`-`** : changer d'arme exige reconditionnement/démontage. Ex. `HCA - LM`.
- **`/`** : deux armes simultanées, distinctes. Ex. `HC / CAC`, `LZ / SW.PW`.
- **`.`** : un seul objet à deux propriétés fusionnées. Ex. `SW.PW`, `HCA.MG`.

### Arbre de décision rapide

```
"Puis-je utiliser les deux simultanément sans modification ?"
├─ Non, reconditionnement/démontage obligatoire → utiliser `-`
├─ Oui, mais ce sont deux choses distinctes → utiliser `/`
└─ Oui, c'est la même chose ayant deux natures → utiliser `.`
```

---

## Gabarits (modificateurs de taille)

`L` Léger · `M` Moyen · `H` Lourd · `SH` Super-Lourd
`2L / 2M / 2H` À deux mains (L/M/H)
`U` Unnamed / Drone — véhicule sans équipage

> **`.L` / `.M` / `.H` / `.SH` sont les seuls gabarits universels**, applicables à **tout Type** via le mécanisme de fusion `.` (voir § Séparateurs). Aucune famille de Types n'a de règle de gabarit propre : en particulier, il n'existe **aucune exception de gabarit pour la famille `V*`** (décision du 2026-08-09, voir `decisions.md`). Les codes qui portent une lettre de gabarit sans point (`VL`, `VBLTT`, `TL`, `TDM`…) sont des **acronymes atomiques déclarés**, pas le résultat d'une composition — ne jamais en dériver un nouveau par analogie.

---

## Portée

`___` Court *(à définir — voir decisions.md § 5)* · `MRG` Moyen · `LRG` Long · `SLRG` Super-long · `XRG` Extrême (quasi-illimité)

> Échelle **commune à tout le système**, y compris aux missiles (notation à lettre unique `S`/`M`/`L`/`X` abandonnée le 2026-07-30, collision avec les gabarits).
> ⚠️ Le cran « Court » n'a **plus de code** depuis le 2026-08-05 : `SRG` a été rendu à la fusée géostationnaire (`aeriens.md`). Placeholder `___` en attendant décision — ne pas produire de code court pour l'instant.

---

## Compétences

`-` Inférieur au standard · `+` Standard · `*` Supérieur au standard
*(Une valeur numérique peut préciser davantage)*

---

## Notation numérique

Les chiffres précisent un acronyme selon leur position (mêmes règles que le gabarit).

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

Une lettre de composition (ex. `G`) n'a **pas de sens fixe indépendant** de sa racine : `SP`+`G` → obusier automoteur · `CH`+`G` → hélico gunship. Fonctionnement normal de la composition, pas une exception.

### Une fusion n'existe que si explicitement déclarée

Une suite de lettres qui *ressemble* à un assemblage n'a **aucun sens automatique**. Un composé n'existe que s'il a été posé et journalisé — jamais par découpage visuel a posteriori. Ex. : `BMG` non déclaré n'existe pas, même s'il « se lit » `BM`+`G`. S'articule avec le workflow étape 8.

### Désambiguïsation positionnelle

Certains conflits se règlent **sans créer de code**, par la seule position (`T` isolé = Torpilleur · `.T` suffixe = Traçante ; même mécanique que `CAV`, `TA`, `RAD`). Détail dans `decisions.md` § 3.

---

## Liberté des rôles et armements cross-domaine

Aucune restriction de domaine sur les rôles/armements (un rôle naval peut s'appliquer à un aéronef, etc.). Seuls les **Types** sont spécifiques à leur catégorie.

---

## Sections détaillées — renvois

**Tables de référence** (décoder un code : sens de chaque acronyme) :
- `references/terrestres.md` — Véhicules terrestres & hélicoptères
- `references/aeriens.md` — Véhicules aériens
- `references/maritimes.md` — Navires & vaisseaux spatiaux
- `references/infanterie.md` — Personnages, grades, rôles, armes, munitions
- `references/structures.md` — Bâtiments, zones, structures
- `references/groupements.md` — Échelons, types d'unités
- `references/materiaux.md` — Matériaux et ressources
- `references/grammaire.md` — **Règles génératives** (composer : fusion `CH`, `C`/`CA`, calibre, `MCA.AA`/`MCAA`)

**Identification** (attribuer un code à partir d'un matériel réel) :
- `identification/METHODE.md` — raisonnement (châssis → Type, pipeline, arbitrage « plus évident »)
- `identification/chassis-types.md` — table châssis → Type (multi-nations)
- `identification/personnel.md` — codage des éléments de personnel
- `identification/lexique.json` — registre `désignation réelle ↔ code v4` (réel), à consulter en premier
- `identification/lexique-40k.json` — registre équivalent pour univers fictifs (40K, Cosmotter) — un simple outil de recherche par contexte, pas une frontière de sens (voir § Règles cardinales n°4)
- `identification/entrainement.md` — protocole du mode entraînement (noms → identification notée sur 5)

**Gouvernance & mémoire du système** :
- `decisions.md` — **journal daté** : décisions établies, cas confirmés sans conflit, désambiguïsation positionnelle, collectifs, codes non résolus, chronologie. **À lire avant toute proposition.**
- `procedures.md` — **les 8 procédures de validation** à dérouler quand Florian acte une décision.

---

## Extensions spatiales (introduites via le projet Cosmotter)

Le projet sci-fi Cosmotter a été l'**occasion** d'introduire ces acronymes liés au spatial — il ne les **réserve** pas à ce projet ni à un univers particulier. Utilisables partout où leur description correspond, comme tout le reste du système (cf. § Règles cardinales n°4).

- Acronymes : `VG` Antigrav · `TG` Char antigrav · `SC` Spacecraft · `ORB` Orbiteur · `CS` Capital ship · `SF` Chantier naval.
- Notes de transposition doctrinale naval → spatial (pas des acronymes, des logiques) : géographie côtière et menaces en environnement 2D ne se transposent **pas** telles quelles ; logique sous-marin → vaisseau furtif et hiérarchie d'escorte **se transposent**.

---

## Philosophie de conception

> S'appuie sur la terminologie militaire existante quand c'est naturel (LMG, SPAA, MBT, BLR…), adapte ou remplace quand un acronyme est trop long, redondant ou mal intégrable. L'usage de sigles « bruts » non adaptés (ex. MEDEVAC) est **exceptionnel et localisé**.

- **Concision** : sens implicite dans l'outil/type non répété (`BLR` implique breacher — pas de `BRH.BLR`).
- **Non-redondance** : rôle déjà porté par le Type non réécrit.

### Famille BRH (Breacher)

| Acronyme | Logique |
|---|---|
| `BRH` | Breacher générique |
| `BRHE / BRHP / BRHG / BRHT` | BRH + cible (Explosif / Porte / Grillage / Tôle) |
| `BLR` / `CSL` | L'outil (bélier / cisailles) implique le rôle → `BRH` omis |
