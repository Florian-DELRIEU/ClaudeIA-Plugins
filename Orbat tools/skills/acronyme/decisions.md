# Journal des décisions — Nomenclature V4

Ce fichier contient l'**historique daté** des décisions de nomenclature : décisions établies, cas confirmés sans conflit, codes non résolus, collectifs actés. Il est lu à la demande, pas à chaque déclenchement du skill.

> **À LIRE avant toute proposition de code.** Le `SKILL.md` renvoie ici : ne jamais proposer, valider ou réordonner un code sans avoir vérifié qu'aucune décision datée ci-dessous ne le concerne. C'est le garde-fou qui empêche de rouvrir un cas tranché ou de reproduire un revirement (cf. procédure P3 dans `procedures.md`).

## Table des matières

1. Décisions établies (V4 + extensions)
2. Cas confirmés sans conflit
3. Désambiguïsation positionnelle
4. Acronymes collectifs actés
5. Codes encore non résolus
6. Résolutions datées (chronologie)

---

## 1. Décisions établies (V4 + extensions validées)

Ces décisions ont été explicitement validées et priment sur toute interprétation naïve.

| Décision | Détail |
|----------|--------|
| `N` = Nucléaire (propulsion) | Motorisation nucléaire, tous contextes |
| `NK` = Nucléaire (armement) | Armement nucléaire (nuke) ⚠️ Distinct de N |
| `NV` = Nocturne (rôle) | Capacité vision nocturne |
| `NVG` = Vision nocturne (équipement) | Jumelles/lunettes spécifiques ⚠️ Distinct de NV |
| `STH` ≠ `SD` | `STH` = furtivité visuelle/radar · `SD` = silence/discrétion (armes supprimées) |
| `C` = Croiseur (naval) | Terminologie navale conservée |
| `CAV` = Cheval (Type) / Cavalerie (Rôle) | `CAV` en position Type = monture individuelle (remplace l'ancien `C`) · `CAV` en position Rôle/Groupement = cavalerie · désambiguïsation par position |
| `GUN` = servants nus · `AT` = infanterie antichar portable · `HW` = unité articulée autour d'armes lourdes | **Actée le 2026-08-10.** Critère unique : **où se trouve l'arme**. Les rôles `*-MOR` / `*-C.AT` embarquent la pièce et valent `pièce + *-GUN` ; **interdiction de cumuler** l'élément embarquant et la ligne d'équipement (double comptage silencieux). Les échelons au-dessus de l'élément gardent leur mission (`CIE-AT`, `PLT-ART`…). Détail : `identification/personnel.md` § Doctrine `GUN`/`AT`/`HW` |
| `MUN` = élément d'approvisionnement munitions · `LOG` = élément d'approvisionnement générique · `AM` = individu porteur intégré à une équipe | **Actée le 2026-08-10.** Résout la fausse collision `MUN` / `AM` : niveaux différents (élément vs individu), **pas de revirement**. `AM` reste l'officiel du rôle individuel (2026-08-03) ; la mention « `MUN` alternatif de `AM` » est retirée de `infanterie.md`. Ne pas cumuler `AM` et `SQ-MUN` pour les mêmes hommes. `MUN` = cargaison sur un véhicule reste un troisième sens (`terrestres.md`) |
| Calibre noté **avec point** : `MOR.60`, `C.57`, `G.105`, `CA.20` | **Actée le 2026-08-10.** Résout la contradiction entre `SKILL.md` § Notation numérique (avec point) et `terrestres.md` / `grammaire.md` § Convention calibre (collée). `ACR#` étant réservé au nombre physique (roues, pattes), `C90` s'y lisait « 90 roues ». La forme collée reste lisible, ne plus l'écrire |
| `AN` (anti-navire) | Redondant si l'armement implique déjà la fonction anti-navire → omettre |
| Transport maritime | `TT` troupes · `TR` matériel générique · `MAT` · `MUN` |
| Cargaisons spécifiques | Symboles chimiques entre parenthèses : `TR(H₂O)`, `TR(CH₄)` |
| Hiérarchie gunship | Suffixe `G` : `KG`, `FFG`, `PFG`, `DDG`, `CG` |
| `FF` = corvette trans-océanique | Distincte de `PF` (polyvalente) |
| Doctrine > taille (naval) | Le type est déterminé par la doctrine et l'indépendance opérationnelle, pas le tonnage |
| `BB` vs `CA` | `BB` tient la ligne / absorbe les dommages · `CA` frappe et conserve une capacité de désengagement |
| `-B` vs `-MEC` (groupements) | `-B` = force principale = chars · `-MEC` = infanterie transportée par VBTT. Deux types distincts, non combinables avec `.` |
| `MCAA` | Fusion prédéfinie MCA + AA. Canon automatique moyen à usage anti-aérien |
| `SPAA` / `AAG` / `SPAAG` / `SPAAM` | Collectifs AA automoteurs actés le 2026-08-02 — voir § 4. `SPAA` = Type (tourelle admise, exception à `SP`) · `AAG` = collectif AA canon (exclut `AAGM`) · `SPAAG`/`SPAAM` = sous-ensembles canon/missile de `SPAA` |
| `RAD` — 3 sens, désambiguïsés par position/contexte | (1) Guidage missile `(RAD)` (`infanterie.md` § Missiles) · (2) Transmission/signal `-RAD` (`groupements.md`) · (3) Radar naval `RAD` en rôle (`maritimes.md`). Réutilisation assumée (2026-08-02) |
| `TA` — 3 sens, désambiguïsés par position | (1) Type = tank amphibie (`terrestres.md`) · (2) Rôle = observation artillerie (`terrestres.md`) · (3) Groupement/appui = acquisition cible `-ACQ / TA` (`groupements.md`). Réutilisation assumée (2026-08-02) |
| `STP` = Spatioport | Officialisé le 2026-08-03. Libère `SP`, désormais **Automoteur** (terrestre) et rien d'autre. `SP` = spatioport reste lisible sur d'anciens fichiers, ne plus produire |
| `GH` = Grenade à main | Officialisé le 2026-08-03. Libère `G`, qui reste commun à Gunship (aérien) et Canon/Obusier (terrestre) — faux conflit assumé |
| `FZD` = Fuze Delay (munition à retard) | Officialisé le 2026-08-03. Libère `FUS`, qui reste l'alternatif de `F` = Fusil / Fusilier |
| `PN` = Personnage générique | Officialisé le 2026-08-03. `P` reste alternatif dans le **bassin Type**. Le Chasseur (aérien) est désormais `FC` (2026-08-04) : `P` est libéré dans le bassin Rôle |
| `FC` = Chasseur (Rôle aérien) | Officialisé le 2026-08-04, remplace `P` (libéré) — `F` collisionne avec Fusil/Fusilier. Famille `F*` : `FI` = Intercepteur, `FCH` = Chasseur lourd. `P`/`F` restent alternatifs en lecture |
| `MA` = Soutien amphibie (Rôle naval) | Officialisé le 2026-08-03, remplace `SA`. Coexiste avec `MA`/`-MA` = Marines (Type/groupement), bassins différents. `SA` reste Space Plane/SSTO et Supériorité aérienne côté aérien, **non affectés** |
| `AM` = Assistant munitions | Officialisé le 2026-08-03, `MUN` rétrogradé en alternatif. Résout le doublon Types/Rôles de `infanterie.md`. Sans rapport avec `MUN` = cargaison munitions (`terrestres.md`) |
| `SPT` = Support (groupement) | Officialisé le 2026-08-03. L'ancien `SPT` = Assistant tireur (`infanterie.md`) est **supprimé** — remplacé selon le cas par `AM`, `GUN` ou un rôle existant comme `TEA` |
| `Z` = Zone générique | Officialisé le 2026-08-03. `Z` = Zombie rétrogradé en alternatif informel |
| `I-CAV` = Cavalier | Pas de Type dédié : composition explicite Infanterie + Cavalerie. L'ancien Type `C` = Cavalier est retiré (voir `CAV`) |
| `T` — Torpilleur vs Traçante | Aucun code créé : **désambiguïsation positionnelle** (voir § 3) |
| `INF` = Infanterie (Type/groupement) | **Officialisé le 2026-08-04, confirmé le 2026-08-05.** Remplace `I` (collisionne avec Industriel/Incendiaire/Intercepteur). `I` reste lu Infanterie par défaut en position Type, mais n'est plus produit — voir § 6, revirement du 2026-08-05 |
| Famille `F*` aérien : `FC`/`FI`/`FCH` | Chasseur / Intercepteur / Chasseur lourd. **Révision du 2026-08-30** : le Chasseur lourd passe de `FH` à `FCH` — `FH` est requis dans le bassin Armement pour le Fusil de calibre supérieur (`infanterie.md`), collision réelle entre deux officiels du même bassin. `FCH` est un acronyme atomique déclaré, sans rapport avec le gabarit universel `.H` (un chasseur au gabarit lourd s'écrirait `FC.H`). `FH`/`HF` restent lisibles sur les anciens fichiers, ne plus produire |
| `IND` Industriel · `ARTS` Artistes · `MKT` Commercial | Officialisés le 2026-08-04 (`structures.md`). Libèrent `I` (→ Incendiaire, munition), `ART` (reste Artillerie) et `COM` (reste Communication aérien) |
| `PLT` = Peloton · `PLR` = Planète tellurique | 2026-08-04. `PLT` prend Peloton (`groupements.md`) ; Planète tellurique bascule sur `PLR` (provisoire — voir § 5) |
| `ASW` = Anti-sous-marin (Rôle naval) | Officialisé le 2026-08-04 (terme OTAN consacré), devant `K`/`HK` gardés en lecture |
| `EQP` = Équipe (élément de personnel) | **Officialisé le 2026-08-05**, inchangé. `EQU` alternatif (lecture seule). `TE` **réhabilité comme alternatif le 2026-08-09** (la réserve du 2026-08-05 est levée : un code isolé se lit Type, cf. SKILL.md § 3) — voir § 6 |
| `HGR` = Hangar (structure) | **Officialisé le 2026-08-05.** `H` rétrogradé en alternatif |
| `HAB` = Habitations (rôle structure) | **Officialisé le 2026-08-05.** `CIV` (et `H`) rétrogradés en alternatifs |
| `DET` = Détachement (échelon) | **Officialisé le 2026-08-05.** Le sens Détention/prison (`structures.md`) perd `DET` → voir § 5 (point ouvert) |
| **Famille `V*` : aucune grammaire générative** | **Acté le 2026-08-09. ⚠️ Revirement : remplace la règle de composition `V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}` antérieure, supprimée ce jour de `grammaire.md`, `terrestres.md` et `SKILL.md`.** Cette « règle » n'était pas une règle du système mais la méthode personnelle de Florian pour *inventer* de nouveaux codes ; écrite comme universelle, elle poussait à générer des codes non déclarés et à mal lire les codes existants. **Ne jamais la réappliquer de mémoire.** Quatre conséquences : (1) tous les codes `V*` (`V`, `VL`, `VM`, `VU`, `VB`, `VH`, `VTT`, `VBCI`, `VHMCI`…) sont des **acronymes atomiques déclarés individuellement**, ni dérivables ni décomposables ; (2) la table « Acronymes combinés » de `terrestres.md` est une **liste figée**, pas un patron de composition ; (3) **aucune exception de gabarit propre à `V*`** — les seuls gabarits universels sont `.L`/`.M`/`.H`/`.SH`, applicables à tout Type ; (4) le palier lourd d'une voiture s'écrit `V.H`, **jamais** `VH` (qui reste le semi-chenillé) |
| `V` / `VB` — pas de collision | **Acté le 2026-08-09.** `V` = voiture blindée à roues · `VB` = véhicule blindé chenillé. Deux acronymes atomiques distincts, aucun lien de dérivation. L'ancienne note de collision de `chassis-types.md` reposait sur une lecture erronée de la grammaire supprimée : elle est retirée, sans mitigation de remplacement |
| `V4L` / `V8CI` redéclarés | **Acté le 2026-08-09.** Ces deux codes n'existaient que comme exemples du § 1 supprimé de `grammaire.md`. Florian a choisi de les **conserver** : ils sont redéclarés comme acronymes atomiques dans `terrestres.md` (`V4L` = voiture légère 4 roues · `V8CI` = combat d'infanterie 8 roues) |
| **Aucune réservation par contexte (époque, univers, thème)** | **Actée le 2026-08-16.** Un regroupement thématique (table, section, titre comme « Médiéval », « SF », « Cosmotter »…) n'est jamais une contrainte d'usage, seulement un classement de confort. Un acronyme est utilisable dans n'importe quel contexte dès lors que sa description correspond. Seule une mention explicite **dans la description elle-même** (`VOL` = « souvent 1800s », `CN` = « napoléonien / pré-industriel ») reste une indication de contexte typique, jamais un verrou — ces deux cas sont conservés tels quels sur confirmation de Florian. Nouvelle règle cardinale n°4 dans `SKILL.md`. Détail des fichiers concernés en § 6 |
| `P` / `PS` / `PA` = Pistolet / semi-auto / auto | **Trois codes officiels distincts, pas un groupe d'alias.** Décidé le 2026-08-04, consigné le 2026-08-30. `P` = arme de poing sans précision de mécanisme, `PS` = un coup par pression, `PA` = capable de rafale. Écrire `P` quand la source ne précise pas le mécanisme : ne jamais « préciser » en `PS`/`PA` par défaut, ce serait inventer une information. `P` est officiel dans le bassin Armement ; ses autres occurrences restent des **alternatifs lisibles mais non produits** : `PLT / P` = Peloton (`groupements.md`), `PROD / P` = Production (`structures.md`), `FC / P / F` = Chasseurs (`aeriens.md`), `PN / P` = Personnage générique (bassin **Type**, voir la ligne `PN` ci-dessus). Aucune collision entre officiels |

---

## 2. Cas confirmés sans conflit (documentés comme tels)

Ces codes portent plusieurs sens **et c'est normal** : faux conflits, vérifiés puis classés comme tels. Ne pas les rouvrir, ne pas proposer de les renommer.

**Principe** : même code, **même concept au fond**, décliné selon le Type qui le porte. `F` = Fusil (arme) et `F` = Fusilier (personnage) ne sont pas concurrents — `I-F` = Infanterie + Fusil = Fusilier.

| Code | Sens coexistants | Pourquoi ce n'est pas un conflit |
|---|---|---|
| `F` | Fusil (arme) / Fusilier (rôle d'infanterie) | Le rôle *est* « celui qui porte l'arme » — `I-F` |
| `C` (Rôle) | Canonnier (personne) / Canon (armement) | Même déclinaison arme → servant |
| `G` | Gunship (aérien) / Canon-Obusier (terrestre) | Variante prenant le sens de sa racine |
| `ART` (Type) | Artillerie / Bombardement côtier | Même sens, Types porteurs différents |
| `MA` (Type) | Marines / Soutien amphibie | Même domaine doctrinal, bassins Type/Rôle différents |
| `LOG` | Logistique, tous domaines | Sens unique, simplement transverse |
| `ML` / `MS` | Poseur / Démineur de mines | Deux codes distincts, pas deux sens d'un même code |
| `EXC` | Extraction (groupement) / Exploitation-minage (rôle structure) | **Double sens assumé (2026-08-05)** : les deux voulus, désambiguïsés par bassin/contexte |
| `ESC` | Escadron (unité terrestre/maritime) / Escadrille (escadron aérien) | **Double sens contextuel (2026-08-05)** : une escadrille EST un escadron aérien — même concept décliné par domaine. (`ESC` = Escouade a été retiré → `SQ`) |

> À distinguer des vrais conflits (deux concepts sans rapport sur un même code), réglés par nouveau code, rétrogradation en alternatif, ou désambiguïsation positionnelle.

---

## 3. Désambiguïsation positionnelle — `T` = Torpilleur vs Traçante

Certains conflits se règlent **sans créer de code**, par la seule position d'écriture. Acté le 2026-08-03 sur `T`, en miroir de la convention réelle (`AP-T`, `API-T`) :

| Écriture | Lecture | Exemple |
|---|---|---|
| `T` **isolé**, attaché à un Type via `-` (position Rôle autonome) | **Torpilleur** | `K-T` = corvette-torpilleur |
| `.T` **en suffixe** d'un code de munition (fusion, jamais seul) | **Traçante** | `AP.T`, `HE.T`, `FMJ.T` |

Troisième voie à côté de « créer un nouveau code » et « rétrograder en alternatif » : quand deux sens ne peuvent jamais occuper la même position grammaticale, ils partagent le code sans ambiguïté. Même mécanique que `CAV` (Type/Rôle), `TA` et `RAD` (§ 1).

> ✅ **Tranché (2026-08-04)** : une munition *uniquement* traçante s'écrit `FMJ.T`. `.T` accolé à une munition = **toujours** Traçante ; `T` isolé n'est jamais une traçante.

---

## 4. Acronymes collectifs actés

Voir `SKILL.md` § Acronymes collectifs pour le cadre à deux tiers (Tier 1 implicite / Tier 2 explicite). Détail des collectifs actés :

### Collectifs AA automoteurs (2026-08-02)

| Code | Nature | Définition |
|---|---|---|
| `SPAA` | Type | Tout automoteur à rôle AA principal, tout châssis. **Exception à `SP`** : tourelle admise (terme trop consacré) |
| `AAG` | Rôle/Armement | Tout armement AA **à canon** : `AAC`/`AACA`/`AA-RTG`. **Exclut** `AAGM` (missile) |
| `SPAAG` | Fusion | `SP+AA+G` = automoteur AA à canon, tout type. Ex. Gepard = `VB-2AACA` |
| `SPAAM` | Fusion | `SP+AA+M` = pendant missile de `SPAAG`. Ex. Roland = `VB-AAGM` |

`SPAAG`/`SPAAM` sont les deux sous-ensembles exhaustifs de `SPAA` (canon/missile).

### Collectifs Types véhicules (2026-08-04)

| Code | Nature | Définition |
|---|---|---|
| `APC` | Type collectif | Tout véhicule à rôle `TT`, tout châssis : `VTT`/`VBTT`/`VHTT`/`VU-TT`. `VUTT` = alias de `VU-TT` |
| `IFV` | Type collectif | Tout véhicule à rôle `CI` de la famille `V` uniquement. `TCI`/`TVCI` exclus |
| `AA` (Type) | Type collectif | Batterie AA déployable, sans châssis. Équivalent de `STAA`. Pendant véhiculé = `SPAA` |
| `ART` (Type) | Type collectif | Pièce d'artillerie déployable, sans châssis. Équivalent de `START`. Pendant véhiculé = `SPART` |

---

## 5. Codes encore non résolus (à traiter en session ultérieure)

Conflits **identifiés et assumés comme ouverts** : le sens listé garde provisoirement un code déjà attribué, ou attend un code. Ne pas inventer de remplaçant — signaler tel quel si la question se pose, attendre une décision de Florian.

| Code / plage | Sens en attente | Statut |
|---|---|---|
| `SPHE` vs `SPG` | Chevauchement possible (obus HE générique vs obusier dédié) | À clarifier si besoin (`terrestres.md`) |
| `BM` (naval) | Placement exact Type/Rôle | À confirmer (`maritimes.md`) |
| `PLR` | Planète tellurique | Provisoire — pourra céder au futur système d'identification planétaire (`structures.md`) |
| `GEN.F` / `GEN.A` | Génie franchissement / assaut | Rangées sans code officiel dans `groupements.md` |
| **`___` portée courte** | Cran « Short range » du bassin Portée | **Ouvert le 2026-08-05** : `SRG` effacé de ce bassin (rendu à la fusée géostationnaire). Code à définir (`SKILL.md` § Portée) |
| **`C.AT` / `CAT`** (canon antichar) | Forme à retenir pour un canon antichar en tant que pièce | **Ouvert le 2026-08-10** : `C.AT` (fusion `.` de `C` + `AT`, deux codes attestés) est employé dans les exemples de `personnel.md` car l'opérateur `.` est générique et ne demande pas de déclaration. La forme collée `CAT` n'existe nulle part (absente de l'INDEX et des lexiques) et resterait interdite tant qu'elle n'est pas posée en fusion atomique dans `terrestres.md` § Acronymes combinés. À trancher : déclarer `CAT`, ou s'en tenir à `C.AT` et à la forme éclatée `ST-C.57` + `SQ-GUN` qui n'en a pas besoin |
| **Codes composés dans `BCFB_2`** | Journalisation au lexique | **Ouvert le 2026-08-10**, en attente de validation de Florian. Tous construits d'éléments attestés, aucun vocabulaire nouveau, mais absents des lexiques. **Équipement** : `ST-C.57`, `ST-G.105`, `ST-MMG`, `ST-HMG`, `ST-LMG`, `MOR.81`, `MOR.60`. **Personnel** : `SQ-HQ`, `SQ-SIG`, `SQ-LOG`, `SQ-MAIN`, `SQ-CRW`, `EQP-MED` (`SQ-GUN`, `EQP-GUN` et `SQ-MUN` ont été journalisés ce jour) |
| **`UAV`** (bassin rôle infanterie) | Engin ou opérateur ? | **Ouvert le 2026-08-10** : `infanterie.md` lit `UAV` = « Technicien drone » (l'opérateur), `groupements.md` § Types d'unités (petites unités) lit « Drone » (l'engin). Divergence apparue par recopie, révélée en dédoublonnant les deux tables. À trancher — les deux lectures sont défendables selon le bassin |
| **`ASS`** (Assaut, petites unités) | Consolidation | **Ouvert le 2026-08-10** : présent dans `groupements.md` § Types d'unités (petites unités) mais absent de `infanterie.md`, alors que tous ses voisins de table y sont définis. À rapatrier dans `infanterie.md` ou à retirer |
| **`MOR.M` / `MOR.H`** | Gabarit vs calibre pour les mortiers | **Ouvert le 2026-08-10** : ces deux entrées notent le mortier par gabarit (`M` ≈ 80 mm, `H` ≈ 105 mm). Elles ne deviennent pas fausses — le gabarit reste le repli légitime quand le calibre est inconnu — mais dès que le calibre est connu, `MOR.81` / `MOR.105` sont les formes à écrire. À arbitrer : garder les deux registres, ou migrer. ⚠️ Le **séparateur**, lui, est tranché : renommées `MOR-M`/`MOR-H` → `MOR.M`/`MOR.H` le 2026-08-10, le gabarit se fusionne par `.` et jamais par `-` |
| **Détention / prison** | Rôle structure (`structures.md`) | **Ouvert le 2026-08-05** : `DET` attribué à Détachement → besoin d'un code, OU maintien de `DET` en alternatif désambiguïsé par position (échelon vs rôle) |

---

## 6. Résolutions datées (chronologie)

### 2026-09-16 (aérostats : familles `BL`/`DR`)

Trou comblé : aucun code n'existait pour ballons et dirigeables (`aeriens.md`).

- `BL` = Ballon, générique (nouveau Type aérien). Décliné par une lettre collée en suffixe, sur le patron déjà établi `SR`/`SRS`/`SRO`/`SRI`/`SRG` et `U`/`UE`/`UH`/`UV`.
- Trois variantes officielles, **toutes sur le même axe** (mode de déploiement) : `BLC` captif (amarré/treuil), `BLB` barrage (fixe, obstacle), `BLM` mobile (vol libre, dérive au vent). `BLM` ne présume pas du type d'enveloppe (air chaud, hélium…) — écarté d'un premier jet où `M` codait spécifiquement « montgolfière », pour rester sur un seul axe de classification plutôt que de mélanger déploiement et type de gaz.
- `MGF` (Montgolfière) reste un **alternatif de lecture uniquement**, pointant vers `BLM` — jamais produit en écriture.
- `DR` = Dirigeable, générique (nouveau Type aérien). **Décision explicite : pas de sous-type pour l'instant.** Les variantes structurelles envisagées (rigide/zeppelin, souple, semi-rigide) ont été écartées : jugées redondantes avec le gabarit `.L`/`.M`/`.H`/`.SH` déjà existant plutôt que porteuses d'une information distincte. Si la distinction s'avère utile plus tard, l'option à privilégier est une précision entre parenthèses (`DR(R)`/`DR(S)`/`DR(M)`, sur le patron `A(J-SS)`) plutôt que des Types atomiques séparés.
- `ZEP` (Zeppelin) reste un **alternatif de lecture uniquement**, pointant vers `DR` — jamais produit en écriture.
- Gaz porteur (hélium/hydrogène/air chaud) explicitement mis de côté — non codé pour l'instant, à reprendre si besoin.

### 2026-08-30 (armes personnelles : familles `F`/`FM`/`MG`, principe d'emploi, `FCH`)

Session de cadrage de la taxonomie des armes personnelles d'infanterie, à partir d'un diagramme de synthèse de Florian.

- **Principe fondateur acté** : dans les familles d'armes personnelles, le code décrit le **poste tenu**, pas le modèle. Une même arme change de code selon sa configuration (HK416 = `F` en standard, `FMG` avec chargeur de grande capacité).
- **Deux axes** : rôle (standard `F` / suppression `FM`) × puissance (calibre standard / calibre supérieur, suffixe `H` collé).
- `FH` = Fusil de calibre supérieur, `FMH` = FM de calibre supérieur. **Fusions atomiques déclarées**, rejoignant le moule préexistant `TEH`/`TEL`. Ne s'appliquent qu'aux génériques `F` et `FM` ; pour un `FV`/`FS`/`FA`/`FMG`, passer par `.H` ou la convention calibre (`FS.762`).
- **`FCH` remplace `FH` = Chasseur lourd** (`aeriens.md`) : collision réelle entre deux officiels du bassin Rôles/Armements. Le côté aérien cède, code récent et peu diffusé.
- `FMA` redéfini : arme d'assaut à cadence élevée, efficacité effondrée au-delà de ~100 m, redoutable en milieu clos. Catégorie devenue peu commune.
- **`FAM` supprimé** — anagramme de `FMA` de sens quasi opposé, piège de lecture. Au mieux alternatif en lecture, jamais produit.
- **`PM` et `SMG` séparés** : `PM` = machine pistol (Uzi, Škorpion), `SMG` = arme d'épaule à calibre pistolet (MP5, MP40, PPSh). `PA` recentré sur le pistolet de poing capable de rafale ; l'exemple « Uzi » qui l'illustrait dans le PDF V4 est erroné et retiré.
- **`P` / `PS` / `PA` consignés comme trois codes distincts** (décision du 2026-08-04, jamais écrite jusqu'ici). Le format `| P / PS / PA |` de `infanterie.md` et la mention « `P` reste alternatif des deux » de `decisions.md` § 5 les traitaient à tort comme un groupe d'alias. `P` devient officiel dans le bassin Armement ; la ligne correspondante sort des codes non résolus.
- `LMG`/`MMG`/`HMG` confirmés **fusions atomiques déclarées** (gabarit préfixé, exception assumée) ; leur définition intègre désormais la contrainte de servants (`MMG` → `AM` obligatoire, `HMG` → équipe dédiée).
- La famille pistolet **n'est pas** rattachée à la famille `MG`, malgré leur adjacence sur l'axe calibre.

### 2026-08-18 (cavalerie : la diagonale seule — correction d'une icône livrée)

Florian a relevé qu'un ORBAT livré portait une **icône composite** pour de la
cavalerie, alors qu'il veut la **diagonale seule**. Consigne actée.

Diagnostic : l'erreur venait du `sidc_dictionary.json` lui-même et de `sidc.md`, qui
décrivait l'entité `120500` comme « Blindés / chars / **cavalerie** » en citant
*Cuirassiers* et *Hussards* en exemples. Le dictionnaire code effectivement les
régiments de Cuirassiers, Dragons, Chasseurs et Spahis en `120500` (ellipse = chars) et
le 3e Hussards en `120501` (ellipse + diagonale). Ces entrées faisaient précédent et se
recopiaient.

Répartition retenue :

| Usage | Entité | Icône |
|---|---|---|
| Cavalerie / reconnaissance — **défaut** | `121300` | diagonale seule |
| Reconnaissance blindée (vraiment sur blindés) | `120501` | ellipse + diagonale |
| Blindés / chars | `120500` | ellipse |
| Reconnaissance montée (*HM RECON*) — à confirmer | `121303` | sous-type de `1213` |

- `orbat-json/references/sidc.md` : table d'entités corrigée (« cavalerie » retiré de
  `120500`, ajout de `121300` et `121303`, `120501` requalifié en reco **blindée**),
  plus un encadré rouge « Cavalerie = la diagonale seule » signalant explicitement que
  le dictionnaire porte le mauvais précédent et **ne doit pas être imité** sur ce point.
- `orbat-json/references/symbologie.md` : nouveau § 3.1 bis avec la table de décision,
  la règle « ne pas empiler de briques que la source ne justifie pas », et l'erreur
  ajoutée à la liste § 4.

**Trouvaille à valider** : l'entité `121303` du dictionnaire est employée pour des
éléments *HM RECON / HM REC SQD / HM REC SEC* — « HM » se lisant très probablement
*horse-mounted*. C'est un sous-type de `1213` (reconnaissance), donc cohérent avec la
diagonale, et ce serait la réponse au besoin « cavalerie à cheval d'avant 1940 » noté
comme non résolu plus haut le même jour. **À confirmer par rendu** avant emploi.

### 2026-08-18 (symbologie : construction des icônes et contexte historique)

Florian a constaté des erreurs récurrentes d'attribution d'icônes sur les ORBAT qu'il
fournit, et a demandé une recherche documentaire pour que le skill sache **construire**
un symbole et **tenir compte de l'époque**. Exemple donné : la cavalerie des années
1800-1900 n'est pas la même chose que la « cavalerie » d'après-guerre, qui désigne en
réalité des blindés.

Aucun impact sur le système de nomenclature ; nouveau matériel côté `orbat-json` :

- **Nouveau fichier `orbat-json/references/symbologie.md`.** Cinq sections : (1)
  anatomie d'un symbole en cinq couches — cadre, icône principale, secteur 1
  (capacité, haut du cadre), secteur 2 (mobilité, bas du cadre), amplificateur
  d'échelon — plus les positions 7 (statut à 6 valeurs) et 8 (QG/task force/leurre à
  8 valeurs), et le fait que le champ 9-10 encode **la mobilité** et non un échelon
  quand son 1er chiffre vaut 3/4/5 ; (2) origine des formes (US Army Corps of
  Engineers, 1917 — croix = bretelles du fantassin, barre diagonale = bandoulière de
  sabre du cavalier, point = boulet, ellipse = chenille) et **principe de composition
  par empilement** ; (3) **contexte historique**, avec le cas canonique de la
  cavalerie en trois périodes et une table des autres pièges d'époque (artillerie
  hippomobile, infanterie portée vs mécanisée, Panzergrenadier, train hippomobile,
  reconnaissance avant 1914…) ; (4) erreurs constatées ; (5) procédure obligatoire
  d'attribution en 6 points, avec interdiction d'inventer une entité.
- `orbat-json/references/sidc.md` : renvoi vers `symbologie.md` en tête ; tables
  **corrigées et complétées** — statut (6 valeurs au lieu de 2), QG/TF/leurre (8
  valeurs au lieu d'une mention vague), modificateurs requalifiés en secteur 1
  (capacité) / secteur 2 (mobilité) avec l'avertissement de ne pas les confondre,
  et note sur le double usage du champ 9-10.
- `orbat-json/SKILL.md` : nouvelle étape 0 « dater la source et charger la
  symbologie » avant la passe d'identification, section de renvoi dédiée.
- `orbat-json/references/naming.md` : Règle 8 passe à **11 contrôles**, le nouveau
  portant sur la cohérence des `sidc` (rôle réel, époque, échelon, codes non attestés
  signalés).

**Limite documentée dans le fichier** : les codes d'entité des familles historiques
(cavalerie montée, reconnaissance montée, artillerie hippomobile) ne sont attestés ni
dans `sidc_dictionary.json` ni dans les sources ouvertes consultées. Ils relèvent donc
de la procédure « proposer, signaler, faire valider » — jamais affirmer. Le
dictionnaire est à enrichir à chaque code confirmé par Florian.

### 2026-08-18 (contrôle de conformité à la source, obligatoire avant livraison)

Décision de Florian : à chaque fois qu'un travail de génération ou de modification
d'ORBAT est réputé **terminé**, dérouler une passe de vérification systématique
confrontant le fichier produit à la **source** utilisée (effectifs, quantités,
structure). Corriger d'office ce qui peut l'être ; **avertir explicitement à la
livraison** de ce qui n'a pas pu être corrigé.

Motif : `validate.py` (et `validate` côté xlsx) ne contrôlent que la **structure** —
schéma, références de catalogue, sidc. Un ORBAT peut passer la validation à 0 erreur
et être faux sur tous les effectifs. Rien ne couvrait cet angle jusqu'ici.

Aucun impact sur le système de nomenclature ; ce sont les skills de génération qui
sont modifiés :

- `orbat-json/references/naming.md` : nouvelle **Règle 8 — Contrôle de conformité à la
  source**, en 4 sections. § 8.1 quand le déclencher (création, remaniement,
  restructuration, édition de masse des `count`) et rejeu après correction ; § 8.2
  table de réconciliation en 10 contrôles (totaux généraux via `aggregate.py`, totaux
  par formation, effectifs des feuilles, complétude structurelle, échelons, codes
  attestés, catalogues, nommage, lacunes § 7.2, `validate.py`) avec la distinction
  **écart** vs **lacune de source** ; § 8.3 correction d'office, sauf source ambiguë
  ou correction impliquant d'inventer un acronyme → arbitrage de Florian ; § 8.4
  **rapport de livraison obligatoire en 3 blocs** (✅ vérifié / ⚠️ corrigé /
  🔴 non résolu), blocs vides écrits « néant » plutôt qu'omis.
- `orbat-json/SKILL.md` : contrôle inscrit comme point 3 de la procédure par défaut et
  greffé sur l'étape 5 (après `validate.py`, avant `present_files`).
- `orbat-xlsx/SKILL.md` : même obligation en § Créer / éditer, renvoyant à la Règle 8
  pour la procédure complète.

### 2026-08-16 (source unique d'acronymes imposée aux skills ORBAT)

Florian a posé comme **règle absolue** que tout acronyme écrit par les skills de
génération d'ORBAT vienne de ce skill (`orbat-tools:acronyme`) et de lui seul :
« lorsque le skill a besoin de créer un acronyme, ça le renvoie directement vers
`/orbat-tools:acronyme` ». Le besoin d'un acronyme est en lui-même le déclencheur
d'invocation du skill — pas la mémoire, pas les codes vus plus haut dans la
conversation, pas ceux d'un ORBAT antérieur.

Aucun changement dans le système de nomenclature lui-même ; ce sont les skills
consommateurs qui sont alignés. Modifications hors de ce skill :

- `orbat-json/SKILL.md` : encadré « règle absolue » en tête de § Source unique, avec
  la marche à suivre en 3 étapes (invoquer → chercher § 7.1 → § 7.2 si absent) ;
  suppression de la mention « seule exception assumée » ; § Codes équipement/personnel
  étendu à **tout** acronyme produit, pas seulement aux codes de TOE.
- `orbat-json/references/naming.md` : même encadré en tête de fichier, primant sur les
  Règles 1-7 ; Règle 2 recomposée autour du renvoi ; Règle 4 — les sigles verbatim de
  la source (`HHC`…) ne sont plus repris par défaut en `shortName` (ils vont en
  `description`, le `shortName` prend le code v4), et `Team`/`Pair`/`Group`/`Crew` se
  résolvent désormais via `groupements.md` + `identification/personnel.md` au lieu
  d'être laissés en anglais.
- **`naming.md` § 7.6 — table d'abréviations françaises de prose supprimée** (`Cie`,
  `Bat`, `Rgt`, `Div`, `Bde`, `EM`, `Esc`, `Bie`, `Plt`, `Sect`, `Inf`, `Bld`, `Méca`,
  `Art`, `Rec`, `Gén`, `Trans`). C'était le seul vocabulaire concurrent restant,
  explicitement exempté de la source unique. Le champ `name` s'écrit désormais soit en
  mots français entiers, soit avec un code officiel de ce skill — pas de troisième voie.
- `orbat-xlsx/SKILL.md` : même encadré dans § Créer / éditer.

Rien à répercuter dans `orbat-acronymize` (il s'appuyait déjà exclusivement sur les
lexiques et `METHODE.md`) ni dans `orbat-app` / `orbat-historique` (aucune production
de code).

### 2026-08-16 (suppression des réservations thématiques/d'époque)

Florian a rejeté le principe même qu'un regroupement thématique ou historique (« Médiéval »,
« Pré-industriel », « SF / Warhammer », « Sci-Fi », « Extensions Cosmotter ») puisse réserver
un acronyme à un contexte. Nouvelle **règle cardinale n°4** ajoutée à `SKILL.md` : seule une
mention explicite dans la description d'un acronyme vaut indication de contexte (jamais un
verrou) ; le regroupement en table/section n'en est jamais une.

- **Cosmotter** n'est qu'un prétexte ayant fait naître plusieurs acronymes spatiaux (`VG`,
  `TG`, `SC`, `ORB`, `CS`, `SF`…) — ils ne sont pas réservés à ce projet. Section `SKILL.md`
  § Extensions Cosmotter renommée **Extensions spatiales** et reformulée en conséquence.
- Titres de section neutralisés (contenu des tables inchangé, sauf mention contraire) :
  `terrestres.md` § Médiéval → **Armes de siège** ; § Pré-industriel (XVIIe–XIXe siècle) →
  **Canon ancien (semi-statique)**, intro d'époque supprimée ; § SF / Warhammer →
  **Marcheurs & véhicules antigrav**. `infanterie.md` § Armes médiévales → **Armes de
  corps-à-corps et de tir non guidées** ; § Armes SF → **Armes à énergie et exotiques** ;
  § Effets SF / génériques → **Effets génériques**. `maritimes.md` § Rôles sci-fi
  (vaisseaux) → **Rôles vaisseaux (missions spécialisées)**. `structures.md` § Sci-Fi —
  Géographie spatiale → **Géographie spatiale**.
- **Cas conservés tels quels** (mention d'époque explicite dans la description, pas dans un
  titre de section) : `VOL` = « Voltigeur, infanterie légère (souvent 1800s) »
  (`infanterie.md`) ; `CN` = « Canon napoléonien / pré-industriel » (`terrestres.md`).
  Validés par Florian comme modèle de ce qui reste légitime.
- `groupements.md` : ligne `-IB` corrigée — retrait de « (moderne) », `VCI` → `IFV` (forme
  collective désormais générale pour tout véhicule à rôle CI de la famille `V`, cf. § 4
  Acronymes collectifs). `-IBH` non touché (hors périmètre de la demande, reste `VBCI`).
- Fichiers déjà conformes, non modifiés : `chassis-types.md`, `METHODE.md`, `personnel.md`,
  `identification/README.md`, `grammaire.md`, `materiaux.md`, `entrainement.md` (déjà
  rédigés « toute nation, toute époque »). `identification/lexique-40k.json` confirmé comme
  simple outil de recherche par univers, pas une frontière de sens.
- Point laissé ouvert, non traité aujourd'hui : `maritimes.md` § Notes Cosmotter (Sci-Fi) —
  note sur la transposition de logiques doctrinales (pas des acronymes), signalée hors
  périmètre par Florian.

### 2026-08-10 (doctrine `GUN`/`AT`/`HW`, doctrine `MUN`/`LOG`/`AM`, convention de calibre)

Décisions prises pendant la construction de l'ORBAT
`BCFB_2_Amalgame_Regiment_DBA_1945.json`, appliquées depuis le correctif
`CORRECTIF_acronyme_2026-08-10.md`.

**1. `GUN` / `AT` / `HW` — critère « où se trouve l'arme ».** Ne contredit pas
`infanterie.md`, qui définissait déjà `GUN` comme « quiconque met en œuvre un système
d'armes » : la décision en tire les conséquences, qui n'étaient pas appliquées. Un
servant de canon antichar est `SQ-GUN`, pas `SQ-AT` ; un servant de mortier est
`EQP-GUN`, pas `EQP-HW`. Règle de non-double-comptage posée. Frontière `GUN` / `CRW`
(pièce tractée vs automoteur) laissée ouverte.

**2. `MUN` / `LOG` / `AM`.** Fausse collision résolue sans revirement : `AM` est un
rôle **individuel** qui ne produit pas de code d'élément, `MUN` est le rôle dominant
d'un **élément**. Retrait de la mention « `MUN` reste alternatif en lecture » de la
ligne `AM` d'`infanterie.md`, qui décrivait une équivalence inexistante.

**3. Convention de calibre — forme à point.** `C.90` et non `C90`. La forme collée
contredisait `SKILL.md` § Notation numérique (`ACR#` = nombre physique).

**4. Gabarit fusionné par `.` — correction de séparateur.** `MOR-M` et `MOR-H` écrivaient le gabarit avec le séparateur de **rôle** (`-`) au lieu de la **fusion** (`.`), en contradiction avec `SKILL.md` § Gabarits universels et avec le précédent `CH.L` où l'infixe direct est explicitement interdit. Renommées `MOR.M` / `MOR.H`. Ce sont les deux seules entrées de lexique concernées ; `chassis-types.md` corrigé en conséquence.

**5. Dédoublonnage structurel (audit du 2026-08-10).**
- `references/terrestres.md` : le bloc dupliqué signalé le 2026-08-05 et laissé
  ouvert est **supprimé**. Les deux copies avaient divergé : la première contenait
  six lignes de fusion (`SPC`, `SPART`, `SPAAG`, `SPAAM`, `TD`, `VTL/VTM/VTH`)
  recopiées de § Acronymes combinés et mal rattachées à § Armement terrestre, la
  seconde portait trois notes de fond absentes de la première (`MCA.AA` vs `MCAA`,
  critère mécanique `C` vs `CA`, convention calibre). La seconde copie est
  conservée ; la seule ligne unique à la première — le pointeur « Règles de
  construction associées » vers `grammaire.md` — a été réinjectée et nettoyée de
  ses résidus de cellule de tableau. Contrôle de non-perte : 165 lignes distinctes
  avant, 165 après. Fichier passé de 333 à 216 lignes.
- `references/groupements.md` § Types d'unités (petites unités) : la table
  recopiait les rôles de `infanterie.md` et avait divergé (`TP`, `UAV`). Elle est
  requalifiée en **rappel d'aiguillage** par un encadré, `infanterie.md` faisant
  foi. Deux anomalies révélées au passage, journalisées en § 5 : la divergence
  `UAV` et l'absence de `ASS` dans `infanterie.md`.

- Fichiers modifiés : `references/infanterie.md` (lignes `GUN`, `AT`, `HW`, `AM`),
  `references/groupements.md` (ligne `HW`, répercussion — la définition y était
  dupliquée à l'identique), `identification/personnel.md` (table § Rôle dominant +
  encadré de doctrine + note `AM`), `references/terrestres.md` (§ Convention calibre,
  ligne `MUN` ×2, exemples travaillés), `references/grammaire.md` (§ 3 Convention
  calibre — **non prévu par le correctif**, portait le même texte collé),
  `identification/README.md` (§ faux positifs), `identification/lexique.json`
  (ajout `SQ-GUN`, `EQP-GUN`, `SQ-MUN` ; notes de `SQ-AT` et `SQ-HW` précisées ;
  migration `VTT-CA20` → `VTT-CA.20` et `VTT-MOR80` → `VTT-MOR.80`),
  `references/INDEX.md` régénéré. Dédoublonnage de `terrestres.md` et de la table
  « petites unités » de `groupements.md` (voir point 5).
- **Anomalie constatée, non corrigée :** `references/terrestres.md` contient toujours
  un bloc dupliqué hérité d'une ancienne version (déjà signalé le 2026-08-05 et
  volontairement non traité). Les modifications de ce jour ont été appliquées aux
  **deux** occurrences pour ne pas créer de divergence interne.

### 2026-08-09 (échelle des petits éléments, `SEC` vs `PLT`, `TE` réhabilité)

Formalisation des groupes de petite taille, demandée par Florian dans la foulée de la
procédure par défaut d'ORBAT.

**1. Échelle de référence des éléments** (source unique : `identification/personnel.md`
§ Échelons d'élément, table mise à jour ce jour) :

| Élément | Effectif indicatif | Nature |
|---|---|---|
| `BI` | 2 | binôme |
| `EQP` | ~3-4 | fonction à part entière, souvent rattachée à une arme ou un poste |
| `GRP` | ~4-6 | fraction/variante réduite d'une escouade |
| `SQ` | ~7-15 | escouade |
| `SEC` | ~15 et + | « grosse escouade », élément d'un seul tenant |

Les chiffres sont **indicatifs et non normatifs** : les fourchettes se recoupent
volontairement, et c'est la **nature** de l'élément qui tranche, jamais l'effectif.
Nommer `GRP` un élément de 7 hommes est valide si l'intention est « fraction
d'escouade ». Anciennes valeurs remplacées : `SQ` ~8-12, `GRP` ~3-6, `EQP` ~2-5.

**2. `SEC` est un élément, `PLT` est un conteneur.** Correction d'une confusion qui
existait dans les deux skills : `SEC` et `PLT` n'occupent **pas** le même échelon.
`BI`/`EQP`/`GRP`/`SQ`/`SEC` sont des tailles croissantes d'un même objet (un bloc
d'hommes sans sous-éléments) ; `PLT` regroupe plusieurs de ces éléments et se situe
strictement **au-dessus** de `SEC`. La différence est de nature, pas d'effectif.
Conséquence : un `PLT` se modélise en unité avec `subUnits`, jamais en ligne de
catalogue `personnel`.

**3. `TE` réhabilité comme alternatif d'Équipe** — **revirement (P3)** de la décision
du 2026-08-05 qui le réservait à Tireur élite. Motif : `SKILL.md` § 3 (« Type par
défaut pour tout acronyme isolé ») lève l'ambiguïté sans coût — `TE` seul se lit
Type, donc Équipe ; `TE` en position Rôle reste Tireur élite (`BI-TE`). Conforme
aussi au § 2 du SKILL.md, qui n'exige l'absence rigoureuse d'ambiguïté que pour les
formes **officielles**. `EQP` reste l'officiel, `EQU` et `TE` sont alternatifs.
Ne pas rouvrir ce cas dans l'autre sens sans relire cette entrée.

- Fichiers modifiés : `identification/personnel.md` (table + encadrés + note
  historique), `references/groupements.md` (lignes Équipe, Section, Peloton, Escouade,
  Binôme, et ligne Rôle `TE`), `decisions.md` § 1. `references/INDEX.md` régénéré.
- Répercuté dans le skill `orbat-json` : `references/sidc.md` (échelons `13`/`14`
  découplés), `references/naming.md` (Règle 4, piège FR/EN réécrit), et les tables
  `ECHELON_NAMES` des scripts `new_orbat.py` / `group_units.py` / `condense_orbat.py`,
  qui se contredisaient déjà entre elles sur `section`.

### 2026-08-09 (échelons : formes officielles et scission Section/Escadron)

Décisions prises par Florian lors de la mise en place de la procédure par défaut de
génération d'ORBAT (skill `orbat-json`, Règle 7), qui a révélé que plusieurs lignes
d'échelon n'avaient pas de forme officielle désignée — ambiguïté exploitée par un
parseur automatique qui prenait « la première forme » comme canonique.

| Échelon | Officiel | Valide (lecture) |
|---|---|---|
| Division | `DIV` | `D` |
| Bataillon | `BT` | `BN` |
| Section | `SEC` | `E` |
| Escadron | `ESC` | `E` |

- **`BT` (Bataillon) vs `BAT` (Batterie)** — confusion explicitement levée. Les deux
  notes de `groupements.md` se renvoient désormais l'une à l'autre. Ne jamais écrire
  `BAT-INF` pour un bataillon d'infanterie : c'est `BT-INF`.
- **Ligne `SEC / ESC / E` scindée en deux entrées.** Elle couvrait deux échelons
  distincts dans une seule ligne, ce qui rendait toute lecture automatique de la table
  ambiguë (rien ne disait quel code allait avec quelle signification). Section et
  Escadron ont maintenant chacun leur ligne.
- Fichiers modifiés : `references/groupements.md` (4 lignes), `references/INDEX.md`
  (régénéré). Répercuté côté `orbat-json` : le loader `orbat_lib.load_echelon_codes()`
  lit désormais l'annotation « X officiel » au lieu de supposer que la première forme
  de la cellule l'est.

### 2026-08-09 (suppression de la grammaire compositionnelle `V`)

- **Revirement (P3)** — la grammaire générative `V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}`,
  présentée comme actée et référencée dans trois fichiers, est **supprimée**. Elle est
  remplacée par le principe « tout code `V*` est un acronyme atomique déclaré ».
  Aucune session future ne doit la réintroduire, même partiellement.
- Fichiers modifiés : `references/grammaire.md` (§ 1 supprimé, sections 2-5 renumérotées en
  1-4, garde-fou ajouté en tête), `references/terrestres.md` (section grammaire remplacée par
  un encadré « aucune règle de composition », table des fusions requalifiée en liste figée,
  colonnes *Décomposition* réécrites, `V4L`/`V8CI` redéclarés, renvoi § 3-5 → § 2-4),
  `SKILL.md` (encadré d'exception `V*` remplacé par la règle universelle des gabarits, renvoi
  `grammaire.md` mis à jour, lectures dérivationnelles retirées de la table Non-redondance),
  `identification/chassis-types.md` (encadré « Collision de notation » supprimé, seuil `TV`
  traité séparément pour `V` et `VB`, `VBCI` requalifié en code atomique).
- **Bilan libération (P5)** — aucun code n'est libéré : `V4L` et `V8CI` sont **conservés**
  (redéclarés dans `terrestres.md` sur décision de Florian). `VH` reste occupé par
  « véhicule semi-chenillé » et n'est pas réattribué au palier lourd de `V`, qui s'écrit `V.H`.
- **Sens confirmés, à ne pas « corriger »** : `V` = voiture blindée · `VL` = voiture légère
  (quasi-civile) · `VM` = voiture blindée moyenne · `VB` = véhicule chenillé · `VH` = véhicule
  semi-chenillé · `V.H` = voiture blindée lourde (gabarit universel, pas un nouveau code).
- **Impact hors skill (P8)** — `/orbat-acronymize` vérifié : il ne contient aucune référence à
  la grammaire supprimée (il s'appuie sur les lexiques et `METHODE.md`), aucune modification
  requise. `/orbat-json` non concerné.
- **Points laissés ouverts, à trancher avec Florian** : les entrées `VB-CA` (note « à roues »),
  `VB-REC` (note « VCI de reconnaissance ») et `VB-ATGM` (sans note) de `identification/lexique.json`
  contredisent `VB` = chenillé ; et `references/terrestres.md` contient un bloc dupliqué hérité
  d'une ancienne version. Ces deux points sont **volontairement non traités** ce jour.

### 2026-08-05 (session d'audit `/maj`)

- **`INF` officiel, `I` alternatif** — confirmation et propagation du revirement. La décision du 2026-08-04 (`INF` officiel) inversait une décision de juillet (`I` officiel, `INF` déprécié) restée écrite dans `personnel.md` et `README.md`. Réalignés ce jour : `personnel.md`, `identification/README.md`, lexiques (`SQ-I`→`SQ-INF`, `GRP-I`→`GRP-INF`).
- **`EQP` officiel pour Équipe**, `EQU` alternatif. `TE` réservé à Tireur élite (retiré de la ligne Équipe de `groupements.md`). Propagé dans `personnel.md` (`EQU-*`→`EQP-*`) et lexiques.
- **`SRG` rendu à la fusée géostationnaire** ; portée courte effacée du bassin Portée, placeholder `___` (point ouvert, § 5).
- **`HGR` officiel** (Hangar), `H` alternatif. **`HAB` officiel** (Habitations), `CIV`/`H` alternatifs.
- **`EXC` double sens assumé** (Extraction + Exploitation) → § 2.
- **`ESC` double sens contextuel** (Escadron/Escadrille par domaine) → § 2.
- **`DET` officiel = Détachement** ; Détention/prison en attente de code (§ 5).

### 2026-08-04

- `HF` = Chasseur lourd → **`FH`** (suit `FC`, `H` en suffixe). ⚠️ **Révisé le 2026-08-30 : ce code est devenu `FCH`** — `FH` est passé au Fusil de calibre supérieur (`infanterie.md`).
- `CLC` / `CBW` → **supprimés**, remplacés par `CAV.LC` / `CAV.BW`.
- Munition uniquement traçante → **`FMJ.T`** explicite.
- `I` hors Intercepteur → `IND` prend Industriel et libère `I` pour Incendiaire ; Infanterie passe à `INF` ; Intercepteur devient `FI`.
- Officiels réordonnés (officiel en tête des `/`) : `ARM`/-B · `MOT`/-M · `SOF`/-SF · `TRANS`/-T · `GEN`/-G · `-IL`/-ILEG · `MO`/-MTN · `HQ`/Cmdt · `D`/DIV · `BAT`/BTE · `JTAC`/CAS · `FRG`/FRAG · `RK`/R/RKT · `CHMED`/CHSAN · `IG`/`AA`/`ART`/`MG` (vs `ST`-préfixés) · `G`/CN (aérien).
- Suppression « contenu de contenant » : `TRF`/`TRW`, `F`/`FUEL` (carburant terrestre), `W` (eau), `CHEM`, `CTF`/`CTW`/`CTC`, section Ressources fluides de `materiaux.md`. Préservés : `CT`/`RCT`, `FUEL` = Ravitailleur (aérien), Matériaux solides.
- `LUXIR` remplace `LUX-IR` ; `(SMN)` retiré de `CLUS`.

### 2026-08-03

Officialisations : `STP` (spatioport, libère `SP`), `GH` (grenade à main, libère `G`), `FZD` (fuze delay, libère `FUS`), `PN` (personnage), `MA` (soutien amphibie, remplace `SA`), `AM` (assistant munitions), `SPT` (support), `Z` (zone). Désambiguïsation positionnelle `T` actée. Cas confirmés sans conflit classés.

### 2026-07-30

Échelle de portée `SRG/MRG/LRG/SLRG/XRG` commune à tout le système (abandon des lettres uniques `S/M/L/X` côté missiles). Règle de signalement d'absence au lexique actée (workflow étape 8). `REM-SUP` → `REM-LOG`. Normalisation casse `-Mi`→`-MI`.
