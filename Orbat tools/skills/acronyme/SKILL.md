---
name: acronyme
description: "Système de nomenclature militaire modulaire V4 (et extensions V5 en cours) : les codes maison de Florian pour types, rôles et armements. Déclencher IMPÉRATIVEMENT dès que Florian tape /acronyme, ou dès que l'utilisateur mentionne un acronyme militaire, un code de véhicule, une unité, un navire, un aéronef, une structure, un personnage, ou demande de nommer / classifier / identifier / vérifier / étendre un élément dans ce système — y compris à partir d'un matériel réel (nom de véhicule). Également applicable au projet sci-fi Cosmotter pour la classification de vaisseaux spatiaux. Utiliser même si la demande semble simple (ex: \"c'est quoi le code pour X ?\", \"est-ce que Y entre en conflit avec Z ?\", \"comment noter un transport de troupes ?\"). Ne couvre pas les libellés d'unités d'armées réelles (3./IR 9, 501e RCC…) : c'est orbat-nommage ; la conversion d'un ORBAT JSON entier en codes relève d'orbat-acronymize.\n"
---

# Système de Nomenclature Militaire V4

*Dernière révision : 2026-10-10.*

## Sommaire

- **Gouvernance** : Principe général · Règles cardinales (et exceptions de la règle 2) · Autorité de validation · Workflow de vérification
- **Grammaire (résumé)** : séparateurs, gabarits, portée, calibre, fusions — détail dans `references/grammaire.md`
- **Renvois** : tables de référence · identification · état des décisions · chronologie · procédures

> ⚠️ **Avant toute proposition ou validation de code, lire `decisions.md`** (état courant compact : décisions établies, cas confirmés sans conflit, désambiguïsation positionnelle, collectifs, codes non résolus) **et appliquer `procedures.md`** (les 8 procédures de validation). Ne jamais rouvrir un cas déjà tranché ni reproduire un revirement.
> **Outils obligatoires** : avant de proposer un code `X`, lancer `python scripts/check.py --code X` (existe-t-il ? sous quels sens ? doublon ?) ; après toute modification du skill, `python scripts/build_index.py` puis `python scripts/check.py` (0 erreur exigée).
> L'historique daté est dans `chronologie.md` : **ne pas le lire en entier**, y chercher l'historique d'un code précis à la demande (`grep -n "CODE" chronologie.md`).

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
1. **Strictement unique** dans son bassin (Types ou Rôles/Armements) — aucune collision de sens possible, même hors contexte. Critère **non négociable**, sauf la liste fermée d'exceptions ci-dessous.
2. **Le plus compact possible** parmi les candidats uniques. Départage par cohérence si ex-æquo.

- **En lecture** (déchiffrer un code fourni) : accepter et décoder correctement l'officiel **et** toutes ses alternatives.
- **En écriture** (produire/proposer un code) : n'utiliser **que** l'officiel, jamais une alternative.

Les notations alternatives peuvent avoir des collisions entre elles, gérables par le contexte — **seul l'officiel doit rester rigoureusement sans ambiguïté.** (Conséquence pour la vérification : ne signaler que les collisions entre **officiels** ; une collision d'alternatives n'est pas un défaut — cf. `procedures.md` P2.)

**Exceptions — liste fermée (actée le 2026-10-10).** Ces codes sont officiels pour plusieurs sens dans un même bassin, départagés par la **position** dans l'acronyme ou par le **Type porteur**. Ce ne sont pas des collisions : selon Florian, « ce sont plus une réécriture du même acronyme dans une section différente, mais ça signifie la même chose ». Ne pas les signaler en P2, ne pas les rouvrir, ne rien ajouter à cette liste sans décision de Florian. Détail : `decisions.md` § 2 et § 3.

| Code | Sens départagés | Départage |
|---|---|---|
| `TA` | Tank amphibie (Type) · Observation artillerie (Rôle) · Acquisition (groupement) | Position |
| `RAD` | Guidage `(RAD)` · Transmission `-RAD` (groupement) · Radar (Rôle naval) | Position |
| `T` | Tank (Type) · Torpilleur (Rôle isolé) · Traçante (suffixe `.T`) | Position |
| `MUN` | Cargaison de munitions (véhicule) · Élément d'approvisionnement (personnel) | Type porteur |
| `CAV` | Monture (Type) · Cavalerie (Rôle/groupement) | Position |
| `G` | Obusier (armement) · Gunship (rôle aérien) | Type porteur |
| `F` | Fusil (armement) · Fusilier (rôle) | Type porteur |
| `C` | Canon · Canonnier (Rôles) ; Croiseur (Type naval) | Position / Type porteur |
| `ART` | Artillerie · Bombardement côtier | Type porteur |
| `MA` | Marines (groupement) · Soutien amphibie (Rôle naval) | Domaine |
| `EXC` | Extraction (groupement) · Exploitation-minage (structure) | Domaine |
| `ESC` | Escadron (terrestre/maritime) · Escadrille (aérien) | Domaine |

<!-- exceptions-regle-2: TA RAD T MUN CAV G F C ART MA EXC ESC -->

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

- Seule une restriction **écrite explicitement dans la description de l'acronyme lui-même** vaut indication de contexte (ex. `VOL` = « souvent 1800s », `infanterie.md`) — et même alors, elle reste une indication typique, pas un verrou.
- Les univers fictifs (Warhammer 40K, Cosmotter…) sont des **occasions** ayant fait naître certains acronymes (notamment côté spatial) — ils ne les réservent pas à cet univers. Voir § Extensions spatiales.
- Les lexiques d'identification séparés (`lexique.json` / `lexique-40k.json`) sont des **outils de recherche par contexte de matériel**, pas des définitions concurrentes ni des frontières de sens : un code a le même sens dans les deux.

> Actée le 2026-08-16 — voir `decisions.md` § 1 et `chronologie.md` (entrée du 2026-08-16).

---

## Autorité de validation — Florian seul

**Claude vérifie, ne valide ni n'ajoute jamais unilatéralement.** Le rôle de Claude s'arrête à : identifier les conflits, signaler les redondances, proposer des alternatives argumentées. La décision d'adopter un acronyme — et de le journaliser dans un lexique ou une table — appartient exclusivement à Florian. Tant qu'il n'a pas confirmé, un acronyme discuté reste une **proposition vérifiée**, pas une décision actée : ne pas l'ajouter aux « Décisions établies », aux lexiques, ni le traiter comme acquis ensuite.

Les étapes concrètes d'une validation sont dans **`procedures.md`** — la mise en œuvre de cette autorité.

---

## Workflow de vérification (à appliquer systématiquement)

Quand l'utilisateur propose ou demande un acronyme :

1. **Identifier la catégorie** (Type ? Rôle ? Armement ? Structure ?).
2. **Vérifier l'absence de conflit** dans la même catégorie : `python scripts/check.py --code X` (pas de doublon d'officiels hors exceptions de la règle 2 — `procedures.md` P2).
3. **Vérifier la cohérence positionnelle** (un même acronyme en Type et Rôle est OK).
4. **Appliquer les décisions établies** (`decisions.md` § 1) ; vérifier cas confirmés (§ 2) et non résolus (§ 5).
5. **Choisir le bon séparateur** : `-` reconditionnement · `/` coexistence distincte · `.` fusion.
6. **Proposer des alternatives** si conflit, avec justification.
7. **Signaler les redondances** (ex. `AN` superflu si l'armement implique anti-navire ; non-redondance Type→Rôle).
8. **Signaler toute absence de correspondance au lexique** (2026-07-30) : si le code (ou un composant `parts`) ne correspond à aucune entrée de `identification/lexique.json` / `lexique-40k.json` / `chassis-types.md`, le dire explicitement — jamais rester silencieux. Ex. « `X-Y` n'existe pas encore au lexique : composé à la volée, à journaliser si tu valides ».

---

## Grammaire — résumé

Règles complètes, exemples et cas limites : **`references/grammaire.md`** (à lire dès qu'on compose un code).

| Séparateur | Sens | Exemple |
|---|---|---|
| `-` | Rupture de configuration (reconditionnement obligatoire) ; délimite aussi Type↔Rôle | `AA - CAS - REC` |
| `/` | Coexistence distincte, simultanée | `REC / MG` |
| `.` | Fusion : un seul objet, deux natures | `SW.PW` |
| `()` | Précision circonstancielle (propulsion, cargaison, variante) | `A(J-SS)`, `TR(H₂O)` |

- **Gabarits** : `.L` / `.M` / `.H` / `.SH` sont les seuls gabarits universels, fusionnés par `.` sur tout Type ou armement (`CH.L`, `C.H`, `V.H`). Les codes à lettre de gabarit collée (`VL`, `TL`, `LMG`…) sont des atomes déclarés, jamais un modèle.
- **Calibre** : `ACR.#` avec point (`C.90`, `CA.20`) ; `ACR#` collé = nombre physique (roues, pattes) ; `#ACR` = nombre de tubes.
- **Portée** : `___` (court, sans code) · `MRG` · `LRG` · `SLRG` · `XRG`.
- **Fusions** : atomiques et non chaînables ; une fusion n'existe que si elle est déclarée ; non-redondance Type→Rôle (`TD-AT` est une faute) ; `SPG` et `ART` exclusifs.
- **Doublons** : pas deux officiels identiques dans un bassin, hors exceptions de la règle 2 ; un code peut exister en Type et en Rôle, la position tranche.
- **Pas de grammaire générative `V*`** (supprimée le 2026-08-09) : tout code `V*` est déclaré individuellement.

---

## Renvois

**Tables de référence** (décoder un code : sens de chaque acronyme) :
- `references/INDEX.md` — index généré par bassin, officiels et alternatifs (`scripts/build_index.py`)
- `scripts/check.py` — contrôle de cohérence (`--code X` : tous les sens d'un code) ; `scripts/tables.py` — lecteur des tables, partagé avec `orbat-json`
- `references/terrestres.md` — Véhicules terrestres & hélicoptères
- `references/aeriens.md` — Véhicules aériens
- `references/maritimes.md` — Navires & vaisseaux spatiaux
- `references/infanterie.md` — Personnages, grades, rôles, armes, munitions
- `references/structures.md` — Bâtiments, zones, structures
- `references/groupements.md` — Échelons, types d'unités
- `references/materiaux.md` — Matériaux et ressources
- `references/grammaire.md` — **Règles de composition** (séparateurs, duplication, gabarits, portée, notation numérique, fusions, `C`/`CA`, calibre)

**Identification** (attribuer un code à partir d'un matériel réel) :
- `identification/METHODE.md` — raisonnement (châssis → Type, pipeline, arbitrage « plus évident »)
- `identification/chassis-types.md` — table châssis → Type (multi-nations)
- `identification/personnel.md` — codage des éléments de personnel
- `identification/lexique.json` — registre `désignation réelle ↔ code v4` (réel), à consulter en premier
- `identification/lexique-40k.json` — registre équivalent pour univers fictifs (40K, Cosmotter) — un simple outil de recherche par contexte, pas une frontière de sens (règle cardinale n°4)
- `identification/entrainement.md` — protocole du mode entraînement (noms → identification notée sur 5)

**Gouvernance & mémoire du système** :
- `decisions.md` — **état courant compact** des décisions. **À lire avant toute proposition.**
- `chronologie.md` — journal daté (motifs, revirements, fichiers touchés). Consulté seulement pour l'historique d'un code, par recherche.
- `procedures.md` — **les 8 procédures de validation** à dérouler quand Florian acte une décision.

**Hors périmètre** : libellés d'unités réelles → `orbat-nommage` (fait foi pour le vocabulaire des échelons réels) ; conversion d'un ORBAT entier → `orbat-acronymize` ; structure du JSON → `orbat-json`.

---

## Extensions spatiales (introduites via le projet Cosmotter)

Le projet sci-fi Cosmotter a été l'**occasion** d'introduire ces acronymes liés au spatial — il ne les **réserve** pas à ce projet ni à un univers particulier (règle cardinale n°4).

- Acronymes : `VG` Antigrav · `TG` Char antigrav · `SC` Spacecraft · `ORB` Orbiteur · `CS` Capital ship · `SF` Chantier naval.
- Notes de transposition doctrinale naval → spatial (pas des acronymes, des logiques) : géographie côtière et menaces en environnement 2D ne se transposent **pas** telles quelles ; logique sous-marin → vaisseau furtif et hiérarchie d'escorte **se transposent**.

---

## Philosophie de conception

> S'appuie sur la terminologie militaire existante quand c'est naturel (LMG, SPAA, MBT, BLR…), adapte ou remplace quand un acronyme est trop long, redondant ou mal intégrable. L'usage de sigles « bruts » non adaptés (ex. MEDEVAC) est **exceptionnel et localisé**.

- **Concision** : sens implicite dans l'outil/type non répété (`BLR` implique breacher — pas de `BRH.BLR` ; famille BRH dans `references/grammaire.md`).
- **Non-redondance** : rôle déjà porté par le Type non réécrit.
