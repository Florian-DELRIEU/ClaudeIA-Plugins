# Décisions — état courant (Nomenclature V4)

**État courant compact** de toutes les décisions de nomenclature validées par Florian. Ce qui est écrit ici fait foi.

> **À LIRE avant toute proposition, validation ou réordonnancement de code.** C'est le garde-fou qui empêche de rouvrir un cas tranché ou de reproduire un revirement (procédure P3, `procedures.md`).
>
> L'**historique daté** (contexte, motifs, revirements, fichiers touchés) est dans `chronologie.md` : ne pas le lire en entier, y chercher un code précis à la demande (`grep -n "CODE" chronologie.md`). Toute nouvelle décision s'écrit **ici** (état) **et** là-bas (entrée datée).

## Sommaire

1. Décisions établies
2. Cas confirmés sans conflit
3. Désambiguïsation positionnelle
4. Acronymes collectifs actés
5. Codes encore non résolus
6. Résolutions datées → `chronologie.md`

---

## 1. Décisions établies

Validées explicitement ; priment sur toute interprétation naïve. Date = dernière décision ; détail dans `chronologie.md`.

### 1.1 Gouvernance et grammaire

| Décision | Détail | Date |
|---|---|---|
| **Aucune réservation par contexte** (époque, univers, thème) | Un regroupement thématique (table, titre « Médiéval », « SF », « Cosmotter »…) n'est jamais une contrainte d'usage. Seule une mention **dans la description** de l'acronyme vaut indication de contexte typique, jamais un verrou (`VOL` « souvent 1800s », `CN` « napoléonien / pré-industriel », conservés). Règle cardinale n°4 | 2026-08-16 |
| **Exceptions à la règle cardinale n°2** | Liste fermée, `SKILL.md` § Règles cardinales n°2 : `TA` `RAD` `T` `MUN` `CAV` `G` (position) + `F` `C` `ART` `MA` `EXC` `ESC` (même concept décliné) | 2026-10-10 |
| **Famille `V*` : aucune grammaire générative** | ⚠️ Revirement : la règle `V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}` est **supprimée** (c'était la méthode personnelle de Florian pour inventer des codes). Tout code `V*` est un **acronyme atomique déclaré** ; la table « Acronymes combinés » de `terrestres.md` est une liste figée ; aucune exception de gabarit pour `V*` ; voiture blindée lourde = `V.H`, **jamais** `VH` (semi-chenillé). Ne jamais réappliquer de mémoire | 2026-08-09 |
| `V` / `VB` — pas de collision | `V` = voiture blindée à roues · `VB` = véhicule blindé chenillé. Deux atomes distincts, sans dérivation | 2026-08-09 |
| `V4L` / `V8CI` redéclarés | Conservés comme acronymes atomiques dans `terrestres.md` | 2026-08-09 |
| Gabarits universels `.L` `.M` `.H` `.SH` | Seuls gabarits universels, fusionnés par `.` sur tout Type ; jamais par `-` (`MOR-M` → `MOR.M`) ni en infixe (`CHL`/`CHM`/`CHH` interdits → `CH.L`/`CH.M`/`CH.H`) | 2026-07-30 / 2026-08-10 |
| Calibre noté **avec point** | `MOR.60`, `C.57`, `G.105`, `CA.20`, `CA.30`. `ACR#` collé = nombre physique (roues, pattes) ; la forme collée `C90` reste lisible, ne plus produire | 2026-08-10 |
| Échelle de portée commune | `___` (court, à définir) · `MRG` · `LRG` · `SLRG` · `XRG`, missiles compris (lettres uniques `S/M/L/X` abandonnées). `SRG` n'est **plus** un cran de portée (→ fusée géostationnaire) | 2026-07-30 / 2026-08-05 |
| Signalement d'absence au lexique | Workflow étape 8 : un code composé absent des lexiques est signalé comme tel, jamais passé sous silence | 2026-07-30 |
| Casse | Tous les codes en majuscules (`-Mi`→`-MI`, `Mo`→`MO`, `Ma`→`MA`, `Gén`→`GEN`) | 2026-07-30 / 2026-10-10 |
| Suppression « contenu de contenant » | `TRF`/`TRW`, `F`/`FUEL` carburant terrestre, `W` (eau), `CHEM` (cargaison), `CTF`/`CTW`/`CTC`, ressources fluides de `materiaux.md` retirés. Préservés : `CT`/`RCT`, `FUEL` = Ravitailleur (aérien) | 2026-08-04 |
| Format des tables | Colonnes « Officiel », « Alternatifs » (alias séparés par `, `), puis signification et notes ; balise de bassin au-dessus de chaque table ; `check.py` (contrôles) et `check.py --code X` (avant toute proposition) obligatoires | 2026-10-10 |
| Vocabulaire des échelons réels | Les libellés d'unités d'armées réelles relèvent d'`orbat-nommage`, qui fait foi ; ce skill ne code que la nomenclature maison | 2026-10-10 |

### 1.2 Renommages et officialisations (ancien → nouveau)

| Officiel | Sens | Ce qu'il remplace / libère | Date |
|---|---|---|---|
| `BET` | Bêtes (Type personnage) | Remplace `BT`, qui reste Bataillon | 2026-10-10 |
| `CRZ` | Croisade (échelon) | Remplace `CRS`, qui reste Créature de saut | 2026-10-10 |
| `SCT` | Secteur galactique | Remplace `SEC`, qui reste Section | 2026-10-10 |
| `ARMY` | Armée (échelon) | Remplace `ARM`, qui reste Blindés (type d'unité) | 2026-10-10 |
| `C.L` / `C.M` / `C.H` | Canon léger / moyen / lourd | Remplacent `LC`/`MC`/`HC` côté canon (« le canon cède ») : `HC` = Hache, `LC` = Lance seuls ; `MC` libéré. Calibre `C.105` préféré quand connu | 2026-10-10 |
| `GR` | Grenade à fusil (« Grenade Rifle ») | Remplace `GF` sur cette ligne | 2026-10-10 |
| `GE` · `GF` | Grenade explosive · Grenade à fragmentation | Deux codes distincts (ancienne ligne `GE / GF` scindée) | 2026-10-10 |
| `G` (`HWZ` alternatif) | Obusier | `HWZ` = alternatif de lecture uniquement ; lignes fusionnées | 2026-10-10 |
| `FCH` | Chasseur lourd (aérien) | Remplace `FH` (2026-08-04, ex-`HF`) : `FH` passe au Fusil de calibre supérieur. `FH`/`HF` lisibles en Chasseur lourd sur anciens fichiers | 2026-08-30 |
| `FC` · `FI` | Chasseur · Intercepteur (Rôles aériens) | `FC` remplace `P` ; `FI` remplace `I`. `P`/`F` lisibles en Chasseur | 2026-08-04 |
| `INF` (`I` alternatif) | Infanterie (Type/groupement) | ⚠️ Revirement de juillet (`I` officiel). `I` lu Infanterie par défaut en position Type, plus produit | 2026-08-04 (confirmé 2026-08-05) |
| `INF-CAV` | Cavalier (personnage monté) | Composition Infanterie + Cavalerie, pas de Type dédié ; ancien Type `C` = Cavalier retiré | 2026-08-03 / 2026-10-10 |
| `CAV.LC` / `CAV.BW` | Cavalier à lance / archer monté | Fusions `CLC` / `CBW` supprimées | 2026-08-04 |
| `IND` · `ARTS` · `MKT` | Industriel · Artistes · Commercial (structures) | Libèrent `I` (→ Incendiaire), `ART` (reste Artillerie), `COM` (reste Communication aérien) | 2026-08-04 |
| `PLT` · `PLR` | Peloton · Planète tellurique | `PLR` provisoire (§ 5) | 2026-08-04 |
| `ASW` | Anti-sous-marin (Rôle naval) | Devant `K`/`HK`, gardés en lecture | 2026-08-04 |
| `STP` | Spatioport | Libère `SP` = **Automoteur** (terrestre) et rien d'autre ; `SP` spatioport lisible, plus produit | 2026-08-03 |
| `GH` | Grenade à main | Libère `G` | 2026-08-03 |
| `FZD` | Fuze Delay | `FUS` reste alternatif de `F` = Fusil / Fusilier | 2026-08-03 |
| `PN` | Personnage générique | `P` alternatif dans le bassin Type | 2026-08-03 |
| `MA` | Soutien amphibie (Rôle naval) | Remplace `SA` (qui reste Space Plane / Supériorité aérienne) ; coexiste avec `MA` = Marines | 2026-08-03 |
| `AM` | Assistant munitions (individu) | `MUN` n'en est **pas** un alternatif (voir ligne `MUN` ci-dessous) | 2026-08-03 / 2026-08-10 |
| `SPT` | Support (groupement) | Ancien `SPT` = Assistant tireur supprimé (→ `AM`, `GUN` ou `TEA`). `SUP` n'est pas un code (`REM-SUP` → `REM-LOG`) | 2026-08-03 |
| `Z` | Zone générique | `Z` = Zombie rétrogradé en alternatif informel | 2026-08-03 |
| `EQP` (`EQU`, `TE` alternatifs) | Équipe | ⚠️ `TE` réhabilité comme alternatif le 2026-08-09 (revirement de la réserve du 2026-08-05) : `TE` isolé = Équipe, `TE` en Rôle = Tireur élite | 2026-08-05 / 2026-08-09 |
| `HGR` (`H` alt.) · `HAB` (`CIV`, `H` alt.) | Hangar · Habitations | — | 2026-08-05 |
| `DET` | Détachement (échelon) | Détention/prison perd `DET` → § 5 | 2026-08-05 |
| `DIV` (`D`) · `BT` (`BN`) · `SEC` (`E`) · `ESC` (`E`) | Division · Bataillon · Section · Escadron | ⚠️ `DIV` = revirement de l'ordre `D`/DIV du 2026-08-04. Ligne `SEC / ESC / E` scindée. `BT` Bataillon ≠ `BAT` Batterie | 2026-08-09 |
| `P` / `PS` / `PA` | Pistolet / semi-auto / auto | **Trois officiels distincts**, pas un groupe d'alias. `P` quand le mécanisme est inconnu (ne jamais « préciser » par défaut). Autres `P` = alternatifs : Peloton, Production, Chasseurs, Personnage | 2026-08-04 (consigné 2026-08-30) |
| `FMJ.T` | Munition uniquement traçante | `.T` accolé = toujours Traçante | 2026-08-04 |
| `LUXIR` | Éclairante IR | Remplace `LUX-IR` ; `(SMN)` retiré de `CLUS` | 2026-08-04 |
| Officiel en tête des `/` | `ARM`/-B · `MOT`/-M · `SOF`/-SF · `TRANS`/-T · `GEN`/-G · `-IL`/-ILEG · `MO`/-MTN · `HQ`/Cmdt · `BAT`/BTE · `JTAC`/CAS · `FRG`/FRAG · `RK`/R/RKT · `CHMED`/CHSAN · `IG`/`AA`/`ART`/`MG` (vs `ST`-préfixés) · `G`/CN (aérien) | 2026-08-04 |
| `BL` (`BLC`/`BLB`/`BLM`) · `DR` | Ballon (captif / barrage / mobile) · Dirigeable | Un seul axe (déploiement). `MGF` → `BLM`, `ZEP` → `DR` en lecture seule. Pas de sous-type `DR` (si besoin : `DR(R)`/`DR(S)`/`DR(M)`). Gaz porteur non codé | 2026-09-16 |

### 1.3 Doctrines et sens fixés

| Décision | Détail | Date |
|---|---|---|
| `N` ≠ `NK` | `N` = Nucléaire (propulsion) · `NK` = Nucléaire (armement) | V4 |
| `NV` ≠ `NVG` | `NV` = Nocturne (rôle) · `NVG` = Vision nocturne (équipement) | V4 |
| `STH` ≠ `SD` | `STH` = furtivité visuelle/radar · `SD` = silence/discrétion (armes supprimées) | V4 |
| `C` = Croiseur (Type naval) | Terminologie navale conservée ; `C` en Rôle = Canonnier / Canon | V4 |
| `CAV` | Type = monture individuelle (remplace l'ancien `C` = Cheval) · Rôle/groupement = cavalerie | 2026-08-03 |
| `GUN` / `AT` / `HW` | Critère : **où se trouve l'arme**. `GUN` = servants nus (pièce en `equipment`) · `AT` = infanterie antichar à armes portables · `HW` = unité articulée autour d'armes lourdes. `*-MOR` / `*-C.AT` embarquent la pièce (= pièce + `*-GUN`) : **jamais cumuler** avec la ligne d'équipement. Les échelons au-dessus gardent leur mission (`CIE-AT`). Détail : `identification/personnel.md` | 2026-08-10 |
| `MUN` / `LOG` / `AM` | `MUN` = élément d'approvisionnement munitions (`SQ-MUN`) · `LOG` = approvisionnement générique · `AM` = individu porteur intégré, sans code d'élément. Ne pas cumuler `AM` et `SQ-MUN` pour les mêmes hommes. `MUN` = cargaison sur véhicule = 3e sens (`terrestres.md`) | 2026-08-10 |
| Échelle des petits éléments | `BI` 2 · `EQP` ~3-4 · `GRP` ~4-6 · `SQ` ~7-15 · `SEC` ~15+. Indicatif : la **nature** tranche, jamais l'effectif. `SEC` = élément terminal ; `PLT` = **conteneur** (unité avec `subUnits`), strictement au-dessus. Source : `identification/personnel.md` | 2026-08-09 |
| Armes personnelles : le code décrit le **poste**, pas le modèle | Axes rôle (`F` standard / `FM` suppression) × puissance (suffixe `H` collé). `FH`, `FMH` = fusions atomiques (génériques `F`/`FM` seulement ; sinon `.H` ou calibre). `FMA` = arme d'assaut CQB. `FAM` supprimé (lecture au mieux). `PM` (machine pistol) ≠ `SMG` (arme d'épaule calibre pistolet). `LMG`/`MMG`/`HMG` atomiques (gabarit préfixé, exception assumée ; `MMG` → `AM`, `HMG` → équipe). Pistolets hors famille `MG`. Détail : `infanterie.md` | 2026-08-30 |
| `SPG` ↔ `ART` exclusifs | `SPG` = canon d'assaut / soutien-feu **direct** · `ART`/`SPART` = tir indirect longue portée. Jamais `SPG-ART` | V4 |
| `AN` (anti-navire) | Redondant si l'armement implique déjà la fonction → omettre | V4 |
| Transport maritime | `TT` troupes · `TR` matériel générique · `MAT` · `MUN` | V4 |
| Cargaisons spécifiques | Symboles chimiques entre parenthèses : `TR(H₂O)`, `TR(CH₄)` | V4 |
| Hiérarchie gunship (naval) | Suffixe `G` : `KG`, `FFG`, `PFG`, `DDG`, `CG` | V4 |
| `FF` ≠ `PF` | `FF` = corvette trans-océanique · `PF` = polyvalente (libellé d'origine ; `maritimes.md` dit « Frégate (trans-océanique), spécialisation niveau corvette » — § 5) | V4 |
| Doctrine > taille (naval) | Le type naval suit la doctrine et l'indépendance opérationnelle, pas le tonnage | V4 |
| `BB` vs `CA` | `BB` tient la ligne / absorbe · `CA` frappe et garde une capacité de désengagement | V4 |
| `-B`/`ARM` vs `-MEC` | `ARM` = force principale chars · `-MEC` = infanterie transportée par VBTT. Non combinables par `.` | V4 |
| `MCAA` | Fusion prédéfinie `MCA` + `AA` (usage AA permanent) ; `MCA.AA` = rôle AA circonstanciel | V4 |

---

## 2. Cas confirmés sans conflit

Même code, **même concept au fond**, décliné selon le Type qui le porte. Vérifiés puis classés : ne pas les rouvrir ni proposer de les renommer. Ceux qui partagent un bassin sont soit dans la liste d'exceptions de la règle n°2 (`F` `C` `G` `ART` `MA` `EXC` `ESC`), soit enregistrés comme collisions connues dans `scripts/collisions_connues.json` (`LOG`, `MS`) — `check.py` les tolère, et eux seuls.

| Code | Sens coexistants | Pourquoi ce n'est pas un conflit |
|---|---|---|
| `F` | Fusil (arme) / Fusilier (rôle) | Le rôle *est* « celui qui porte l'arme » — `INF-F` |
| `C` (Rôle) | Canonnier / Canon | Même déclinaison arme → servant |
| `G` | Gunship (rôle aérien) / Obusier (armement) | Variante prenant le sens de sa racine |
| `ART` (Type) | Artillerie / Bombardement côtier | Même sens, Types porteurs différents |
| `MA` | Marines (Type/groupement) / Soutien amphibie (Rôle naval) | Même domaine doctrinal |
| `LOG` | Logistique, tous domaines | Sens unique, transverse |
| `ML` / `MS` | Poseur / Démineur de mines | Deux codes distincts, pas deux sens |
| `EXC` | Extraction (groupement) / Exploitation-minage (rôle structure) | Double sens assumé (2026-08-05) |
| `ESC` | Escadron (terrestre/maritime) / Escadrille (aérien) | Même concept par domaine (2026-08-05). `ESC` = Escouade retiré → `SQ` |

> À distinguer des vrais conflits (deux concepts sans rapport), réglés par nouveau code, rétrogradation en alternatif ou désambiguïsation positionnelle.

---

## 3. Désambiguïsation positionnelle

Troisième voie à côté de « créer un code » et « rétrograder en alternatif » : quand deux sens ne peuvent jamais occuper la même position grammaticale, ils partagent le code sans ambiguïté.

| Code | Sens selon la position | Date |
|---|---|---|
| `T` | **Isolé**, attaché à un Type par `-` (Rôle) = Torpilleur (`K-T`) · **`.T` en suffixe** d'une munition = Traçante (`AP.T`, `HE.T`, `FMJ.T`). `T` isolé n'est jamais une traçante ; `T` en Type = Tank | 2026-08-03 / 2026-08-04 |
| `CAV` | Type = monture · Rôle/groupement = cavalerie | 2026-08-03 |
| `TA` | Type = tank amphibie · Rôle = observation artillerie · groupement = alternatif de `-ACQ` (acquisition) | 2026-08-02 |
| `RAD` | `(RAD)` guidage missile · `-RAD` transmission/signal (groupement) · `RAD` radar (Rôle naval) | 2026-08-02 |
| `MUN` | Cargaison sur véhicule · rôle dominant d'un élément de personnel (`SQ-MUN`) | 2026-08-10 |
| `TE` | Isolé (Type) = Équipe, alternatif de `EQP` · Rôle = Tireur élite (`BI-TE`) | 2026-08-09 |

---

## 4. Acronymes collectifs actés

Un collectif regroupe plusieurs codes existants sous un terme générique. Il peut être un Type ou un Rôle/Armement ; il ne remplace pas le code précis quand celui-ci est connu.

| Code | Nature | Définition | Date |
|---|---|---|---|
| `SPAA` | Type | Tout automoteur à rôle AA principal, tout châssis. **Exception à `SP`** : tourelle admise (terme consacré) | 2026-08-02 |
| `AAG` | Rôle/Armement | Tout armement AA **à canon** : `AAC` / `AACA` / `AA-RTG`. **Exclut** `AAGM` | 2026-08-02 |
| `SPAAG` | Fusion | `SP`+`AA`+`G` = automoteur AA à canon. Ex. Gepard = `VB-2AACA` | 2026-08-02 |
| `SPAAM` | Fusion | Pendant missile de `SPAAG`. Ex. Roland = `VB-AAGM`. `SPAAG`/`SPAAM` = sous-ensembles exhaustifs de `SPAA` | 2026-08-02 |
| `APC` | Type collectif | Tout véhicule à rôle `TT`, tout châssis : `VTT`/`VBTT`/`VHTT`/`VU-TT` (`VUTT` = alias de `VU-TT`) | 2026-08-04 |
| `IFV` | Type collectif | Tout véhicule à rôle `CI` de la **famille `V`** uniquement (`VCI`, `VBCI`, `VHCI`…). `TCI`/`TVCI` exclus | 2026-08-04 |
| `AA` (Type) | Type collectif | Batterie AA déployable sans châssis (≡ `STAA`). Pendant véhiculé = `SPAA` | 2026-08-04 |
| `ART` (Type) | Type collectif | Pièce d'artillerie déployable sans châssis (≡ `START`). Pendant véhiculé = `SPART` | 2026-08-04 |
| `SP` | Type (famille) | Automoteur sans tourelle ; terme générique de la famille `SPAT`/`SPHE`/`SPC`/`SPART`/`SPG`/`SPAA` (`terrestres.md`) | V4 |

---

## 5. Codes encore non résolus

Conflits **identifiés et assumés comme ouverts**. Ne pas inventer de remplaçant : signaler tel quel si la question se pose, attendre Florian (procédure P4 : tout « à confirmer » écrit ailleurs est reporté ici).

| Code / plage | Question en attente | Ouvert le |
|---|---|---|
| `SPHE` vs `SPG` | Chevauchement possible : `SPHE` = canon HE automoteur générique, `SPG` = soutien-feu direct à l'obusier (`terrestres.md`) | V4 |
| `BM` (naval) | Placement exact Type ou Rôle (`maritimes.md`) | 2026-08-04 |
| `PLR` | Planète tellurique — provisoire, pourra céder au futur système d'identification planétaire (`structures.md`) | 2026-08-04 |
| `GEN.F` / `GEN.A` | Génie franchissement / assaut : pas de code court (`groupements.md`) | V4 |
| **`___` portée courte** | Cran « court » sans code depuis que `SRG` est rendu à la fusée géostationnaire | 2026-08-05 |
| **`C.AT` / `CAT`** | Canon antichar en tant que pièce : déclarer `CAT` en fusion atomique, ou s'en tenir à `C.AT` / forme éclatée `ST-C.57` + `SQ-GUN` | 2026-08-10 |
| **Codes composés de `BCFB_2`** | Journalisation au lexique : `ST-C.57`, `ST-G.105`, `ST-MMG`, `ST-HMG`, `ST-LMG`, `MOR.81`, `MOR.60`, `SQ-HQ`, `SQ-SIG`, `SQ-LOG`, `SQ-MAIN`, `SQ-CRW`, `EQP-MED` | 2026-08-10 |
| **`UAV`** (rôle infanterie) | Engin ou opérateur ? `infanterie.md` = Technicien drone, `groupements.md` = Drone | 2026-08-10 |
| **`ASS`** (Assaut) | Défini seulement dans `groupements.md` (une ligne depuis le 2026-10-10), absent de `infanterie.md` : y rapatrier ou retirer | 2026-08-10 |
| **`MOR.M` / `MOR.H`** | Gabarit vs calibre (`MOR.81` / `MOR.105`) : garder les deux registres ou migrer. Le séparateur `.` est tranché | 2026-08-10 |
| **Détention / prison** | `DET` attribué à Détachement : nouveau code, ou `DET` alternatif désambiguïsé par position | 2026-08-05 |
| **`VB-CA` / `VB-REC` / `VB-ATGM`** (`lexique.json`) | Notes « à roues » / « VCI de reconnaissance » / vide, contradictoires avec `VB` = chenillé | 2026-08-09 |
| **Notes Cosmotter** (`maritimes.md`) | Note de transposition doctrinale (pas des acronymes) : à reformuler ou déplacer, hors périmètre du 2026-08-16 | 2026-08-16 |
| **Frontière `GUN` / `CRW`** | Pièce tractée/en position = `GUN` ; équipage d'automoteur (conduit *et* sert) = `CRW` ? À confirmer au premier ORBAT avec blindés (`personnel.md`) | 2026-08-10 |
| **`DEF`** (groupements) | Officiel à la fois pour Génie fortification (`DEF / GEN.D`) et Défense (type d'unité) dans la même table | 2026-10-10 |
| **`BTV` / `BTU`** | Bêtes volantes / Bête robotique : suivent-ils `BT` → `BET` ? | 2026-10-10 |
| **Anciens codes renommés** | `BT` (Bêtes), `CRS` (Croisade), `SEC` (Secteur), `ARM` (Armée), `HC`/`LC`/`MC` (canon), `GF` (grenade à fusil) : à garder comme alternatifs de lecture pour les anciens fichiers, ou à oublier ? | 2026-10-10 |
| **Casse mixte** | `Tk`, `CPLc`, `SGTc`, `ADJc`, `sLT`, `1eENL`, `Cmdt`, `Fe` contreviennent à la règle « tout en majuscules » (P7) | 2026-10-10 |
| **Scissions à confirmer** : `SL`/`TL`, `RTG`/`RTM`, `TEC`/`HTC`, `LDZ`/`PLZ`, `F`/`PF`, `PN+`/`PN*` | Anciennes lignes `X / Y` à deux libellés (« Chef d'équipe/escouade », « Canon rotatif / Minigun »…) : deux codes distincts, ou un officiel et son alias ? Remis en **officiel + alias** (1er code officiel) en attendant. Pour `F`/`PF` : `PFG` = « Frégate polyvalente gunship » contredit la lecture « Corvette polyvalente » | 2026-10-10 |
| **Même concept décliné, non classé** — Rôles : `AA` `AT` `ATT` `FM` `GL` `HE` `MAIN` `MED` `MIN` `RK` ; Types : `CV` `PAR` `SLE` `DC` (et `AA` Type) | `check.py` les voit comme officiels de sens différents dans un même bassin (ex. `GL` Grenadier / Lance-grenade, `MED` Médecin / Médical, `CV` Porte-avions / Groupe porte-avion). Probablement des déclinaisons d'un même concept (arme → porteur, ou par domaine/échelon), comme `F` ou `ESC` : les classer en § 2 et dans la liste d'exceptions de la règle 2, ou les départager | 2026-10-10 |
| **`SA`** (Types) | Space Plane / SSTO (Type aérien) et Supériorité aérienne (type de groupe aérien) sont officiels du même bassin depuis que les types d'unité sont classés Types (balises de bassin du 2026-10-10) | 2026-10-10 |
| **`V`** (voiture blindée) | Sens décidé (2026-08-09) mais **aucune ligne** dans les tables de `terrestres.md` ; `V` n'y existe qu'en alternatif de `VIL` (Ville, `structures.md`). Déclarer la ligne `V` ? | 2026-10-10 |
| **`T`** (Types) | Type de flotte `T` = Torpilleurs (`maritimes.md`, écrit en 2e position `FLT.N-T`) face à `T` = Tank (Type terrestre). La liste d'exceptions couvre Tank / Torpilleur (Rôle) / Traçante, pas ce type de flotte classé Types : collision non documentée jusqu'ici | 2026-10-10 |
| **`L` / `M` / `H`** (types de flotte) | Flotte légère / moyenne / lourde, écrites en 2e position (`FLT.N-L`) mais classées Types ; recoupent les gabarits universels `.L`/`.M`/`.H` : bassin `roles`, notation `FLT.N.L`, ou laisser tel quel ? | 2026-10-10 |
| **`MA`** alternatif de `DC` (`aeriens.md`) | « Surveillance des côtes » : l'alias `MA` est aussi l'officiel de Marines (types d'unité) et de Soutien invasion (types de flotte) dans le même bassin | 2026-10-10 |
| **`FF`** | `decisions.md` § 1.3 (« corvette trans-océanique ») et `maritimes.md` (« Frégate (trans-océanique), spécialisation niveau corvette ») ne disent pas la même chose | 2026-10-10 |
| **Clés de lexique écrites avec un alternatif** : `EQP-UAV.R`, `VTT-SAN`, `VU-SAN` | `R` n'est officiel nulle part (alternatif de `REG`/`RK`/`REC` : `EQP-UAV.REC` ?) ; `SAN` est l'alternatif de `MED` en Rôle (`VTT-MED` ?) | 2026-10-10 |
| **Officiel incertain** : `ISV`/`SVI`, `PL-`/`PLN`, `WRK`/`FAB`, `MIN`/`EXC`, `ML` (alias MS, GEN.M : Génie minage — d'où la collision de `ML` avec Poseur de mines), `RAD`/`SIG`, `(R/F)`, `DC`/`MA` | Passage au format « Officiel / Alternatifs » : aucune annotation ne désignait l'officiel, le premier code a été gardé (convention « officiel en tête », P7) | 2026-10-10 |

---

## 6. Résolutions datées

Déplacées dans **`chronologie.md`** (2026-10-10). Les renvois externes « `decisions.md` § 6, entrée AAAA-MM-JJ » s'y retrouvent à l'identique.
