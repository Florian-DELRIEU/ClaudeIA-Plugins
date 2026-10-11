# Chronologie des décisions — Nomenclature V4

Journal **daté** des résolutions de nomenclature, de la plus récente à la plus ancienne. Ancien § 6 de `decisions.md`, scindé le 2026-10-10 et conservé quasi verbatim.

> **Ce fichier n'est pas à lire en entier.** L'état courant (ce qui fait foi) est dans `decisions.md`, à lire avant toute proposition. Ici, on cherche l'**historique d'un code** à la demande, par recherche texte (ex. `grep -n "SPAA" chronologie.md`) — notamment pour détecter un revirement (procédure P3).
>
> Les renvois des entrées anciennes décrivent l'état des fichiers **à leur date**. Depuis le 2026-10-10 : les sections grammaticales autrefois dans `SKILL.md` (§ Séparateurs, § Gabarits, § Portée, § Notation numérique, § Règles de composition des fusions, § Désambiguïsation positionnelle…) vivent dans `references/grammaire.md` ; les anciens « `decisions.md` § 1 à § 5 » restent valides ; « `decisions.md` § 6 » désigne ce fichier.
>
> Les entrées sur la symbologie, la conformité des ORBAT et la source unique imposée aux skills ORBAT ont été déplacées vers `orbat-json/references/historique-decisions.md` (une ligne de renvoi reste ici à leur place).

---

### 2026-10-10 (renommages : collisions avec les échelons)

Arbitrages de Florian sur des collisions entre un échelon et un autre officiel du bassin Types.

| Sens | Ancien code | Nouveau code | Le code ancien reste |
|---|---|---|---|
| Bêtes (Type personnage, `infanterie.md`) | `BT` | **`BET`** | `BT` = Bataillon (échelon) |
| Croisade (échelon, `groupements.md`) | `CRS` | **`CRZ`** | `CRS` = Créature de saut (Type personnage) |
| Secteur galactique (`structures.md`) | `SEC` | **`SCT`** | `SEC` = Section (échelon) |
| Armée (échelon, `groupements.md`) | `ARM` | **`ARMY`** | `ARM` = Blindés (type d'unité) |

- **Bilan P5** : `BET`, `CRZ`, `SCT`, `ARMY` vérifiés libres dans l'INDEX, les deux lexiques et toutes les tables. Les anciens codes ne sont **pas** déclarés alternatifs de lecture pour leur ancien sens (non décidé — voir `decisions.md` § 5).
- `BTV` (Bêtes volantes) et `BTU` (Bête robotique, décomposition réécrite `BET.U`) **non renommés** : hors décision, point ouvert (`decisions.md` § 5).
- **P8** : `orbat-json` lit les échelons dynamiquement dans `groupements.md` (`orbat_lib.load_echelon_codes`) — Armée → `ARMY` et Croisade → `CRZ` sans modification de code. Aucun lexique ne contenait ces codes.
- Rappel de périmètre acté le même jour : le **vocabulaire des échelons réels** (libellés d'unités d'armées existantes) relève d'`orbat-nommage`, qui fait foi ; ce skill ne code que la nomenclature maison.

### 2026-10-10 (canon : « le canon cède »)

- La notation `C (LC/MC/HC = Léger/Moyen/Lourd)` de `terrestres.md` est **supprimée**. Un canon léger/moyen/lourd s'écrit avec le gabarit universel **`C.L` / `C.M` / `C.H`**, ou par calibre (`C.105`) quand il est connu.
- `HC` = Hache et `LC` = Lance (armes de corps-à-corps, `infanterie.md`) restent les seuls sens de ces codes — cohérent avec `CAV.LC`. `MC` est libéré (aucun autre sens).
- `SKILL.md` : l'exemple `HC / CAC` (qui lisait `HC` comme canon lourd) devient `C.H / CAC` (désormais dans `references/grammaire.md`).

### 2026-10-10 (grenades : `GR` / `GE` / `GF`)

- **`GR` = Grenade à fusil** (« Grenade Rifle ») remplace `GF` sur cette ligne de `infanterie.md`.
- **`GE` = Grenade explosive** et **`GF` = Grenade à fragmentation** deviennent deux lignes distinctes (ancienne ligne `GE / GF` scindée). Motif de Florian : une grenade explosive ne vise pas d'abord à fragmenter ; une grenade à fragmentation a pour rôle de produire des fragments.
- `GF` portait jusqu'ici deux sens (grenade à fusil et frag) : il n'en garde qu'un. `GR` était libre.

### 2026-10-10 (obusier : `G` officiel)

- **`G` = Obusier officiel**, `HWZ` = alternatif de lecture uniquement. Les deux lignes `G` et `HWZ / G` de `terrestres.md` sont fusionnées en une seule (`G / HWZ`).
- `G` = Gunship reste un rôle aérien : faux conflit déjà classé (`decisions.md` § 2), et `G` figure dans la liste des exceptions à la règle cardinale n°2.

### 2026-10-10 (règle cardinale n°2 : liste explicite d'exceptions)

- `SKILL.md` § Règles cardinales n°2 reçoit une **liste fermée** des codes officiels pour plusieurs sens dans un même bassin, départagés par la position ou le Type porteur. Formulation de Florian : « ce sont plus une réécriture du même acronyme dans une section différente, mais ça signifie la même chose ; considère-les comme des exceptions ».
- Liste retenue : `TA` `RAD` `T` `MUN` `CAV` `G` (désambiguïsation positionnelle, `decisions.md` § 1 et § 3) + `F` `C` `ART` `MA` `EXC` `ESC` (cas confirmés sans conflit, `decisions.md` § 2).
- Commentaire machine-lisible ajouté sous la liste : `<!-- exceptions-regle-2: … -->`, destiné à un futur `check.py`.
- Les tables de référence : toute ligne `X / Y` qui désignait **deux codes distincts** (et non un officiel + ses alias) est scindée en lignes séparées. La refonte en colonnes « Officiel | Alternatifs » est reportée à une seconde passe. *(Annotation : six de ces scissions, faites sans base textuelle suffisante, ont été annulées le même jour — voir l'entrée « format Officiel / Alternatifs ».)*

### 2026-10-10 (corrections d'audit, sans nouveau code)

Alignements sur des décisions déjà prises, relevés par un audit de cohérence :

- **`SPG` = soutien-feu direct** partout (`terrestres.md` ligne `SPHE`, `chassis-types.md`, § 5) : la mention « obusier dédié tir indirect » contredisait l'exclusion `SPG`/`ART`.
- **`SRG` retiré de l'échelle de portée** dans `infanterie.md` § Missiles (il restait « Court ») : placeholder `___` ; les exemples `SRG.ANRM` et `SRG.SAM.(IR)` sont marqués comme anciennes écritures sans équivalent court tant que le cran n'est pas recodé.
- **`IFV`** : `chassis-types.md` disait « pas un code du système » ; aligné sur la décision plus récente (Type collectif, 2026-08-04, confirmée le 2026-08-16).
- **Gepard** : `lexique.json` `SP-AACA` → **`VB-2AACA`**, aligné sur `decisions.md` § 4 (collectifs AA du 2026-08-02) et `terrestres.md`. `SP` = automoteur **sans tourelle** ne convenait pas ; seul le collectif `SPAA` admet la tourelle. `chassis-types.md` et `METHODE.md` alignés.
- **`INF`** : clé `I` de `lexique-40k.json` → `INF` (note « INF déprécié » obsolète depuis le 2026-08-04) ; `I-CAV` → **`INF-CAV`** (`infanterie.md`, `decisions.md`) ; décomposition `IU` = `INF.U`.
- **Règle n°4** : le `_comment` de `lexique-40k.json` et `identification/README.md` disaient qu'un code pouvait prendre « un sens différent selon l'univers » — réécrits conformément à la règle n°4 (un code a un seul sens, le lexique fictif n'est qu'un outil de recherche).
- Mentions périmées : `infanterie.md` « `P` = Chasseur » (→ `FC` depuis le 2026-08-04) ; `CA30` → `CA.30` (convention calibre du 2026-08-10) ; `CH-T` → `CH-TT` dans `chassis-types.md` (déjà migré au lexique le 2026-07-30) ; `START` pour un AA tracté → `AA` (collectif) ; format de `terrestres.md` (gabarit écrit avec `-` → `.`) ; `Ma` → `MA` (`aeriens.md`, précédent du 2026-08-03).
- Grades : colonnes de la table inversées pour que le **code** soit en 1re colonne.
- `groupements.md` : `ASS` doublon fusionné en une ligne ; lignes `GEN.F` / `GEN.A` sans code court nettoyées (point ouvert maintenu).
- Renvois cassés réparés (anciennes sections `SKILL.md` § Décisions établies / § Cas confirmés / § Acronymes collectifs, désormais dans `decisions.md` ; grammaire déplacée dans `references/grammaire.md`).

### 2026-10-10 (format « Officiel / Alternatifs », bassins balisés, `check.py`)

Arbitrage de Florian : les tables de codes passent au format **Officiel | Alternatifs | Signification | …** (une ligne = un officiel et ses alias de lecture, séparés par `, `), et chaque table reçoit une balise de bassin (`<!-- bassin: types -->`, `roles`, `precisions`, `aucun`). Ce qui a été fait exactement :

- **Officiel retenu** : celui que la ligne annonçait (« `X` officiel »), sinon le premier code de l'ancienne cellule `X / Y` (convention P7). Lignes sans annotation à l'officiel discutable : § 5 « Officiel incertain ».
- **Alias déclarés seulement dans les notes** déplacés en colonne Alternatifs, sans changement de sens : `IMV` (`VLTT`), `MRAP` (`VMTT`), `MEDEVAC` (`MED`), `MGF` (`BLM`), `ZEP` (`DR`), `FH`/`HF` (`FCH`), `P`/`F` (`FC`, Rôles aériens), `P` (`PN`), `P+`/`P*` (`PN+`), `I` (`INF`, infanterie), `SP` (`STP`), `M` (`ML`, Rôles navals). `VUTT` reste alias de `VU-TT` (composition, pas une ligne de table) : il n'est indexé que par sa clé de lexique.
- **Officiel vide** (Alternatifs seuls) pour un sens sans code officiel : `GEN.F`, `GEN.A` (anciennes cellules `/ GEN.F`, `/ GEN.A`), `Z` = Zombie (alternatif informel ; l'officiel de `Z` est Zone), `SRG.ANRM` (lecture seule).
- **Scissions de la première passe annulées** (texte d'origine ambigu) : `SL`/`TL`, `RTG`/`RTM`, `TEC`/`HTC`, `LDZ`/`PLZ`, `F`/`PF`, `PN+`/`PN*` reviennent en officiel + alias, libellé d'origine restitué (« Chef d'équipe/escouade », « Frégate / Corvette polyvalente »…) ; question au § 5 « Scissions à confirmer ». Libellés précisés sans arbitrage retirés (`F` « Générique », `PF` « Corvette polyvalente », `PLZ` « Plateforme d'atterrissage », `ASS` « quelle que soit sa taille ») ; `decisions.md` § 1.3 rétablit `FF` = « corvette trans-océanique ».
- Codes des types d'unité (`groupements.md`) et des types de flottes (`maritimes.md`) écrits sans tiret de liaison (`-INF` → `INF`), sens inchangé.
- **Bassins** : échelons, grades, structures, types d'unité/de flotte/de groupe aérien = Types ; propulsion, vitesse et matériaux (codes entre parenthèses) = `precisions` ; tables d'exemples et de clarification (`grammaire.md`, matrice des armes personnelles, exemples de missiles, tables d'archétypes et « Chasseurs de char… » de `chassis-types.md`, exemples de `personnel.md`) = `aucun`.
- **Outils** : `scripts/tables.py` (lecteur unique, aussi utilisé par `orbat-json`), `scripts/check.py` (contrôles ; `--code X` avant toute proposition, insensible à la casse), INDEX par bassin avec les alternatifs, `scripts/collisions_connues.json` (collisions arbitrées : exceptions de la règle 2, cas confirmés § 2, points ouverts § 5 — tout sens nouveau fait échouer `check.py`).
- `lexique.json` : `parts` de `VTT-CA.20` / `VTT-MOR.80` décomposés (`CA` + `20`, `MOR` + `80`) et de `VUTT` (`VU` + `TT`), erreurs manifestes relevées par `check.py`.
- Nouveaux points ouverts (§ 5) : déclinaisons d'un même concept non classées, `SA` et `T` (Types), `L`/`M`/`H` (types de flotte), alias `MA` de `DC`, `FF`, ligne `V` absente des tables, clés de lexique écrites avec un alternatif, officiels incertains, scissions à confirmer.

### 2026-10-10 (scission de `decisions.md`)

- `decisions.md` garde son nom et devient l'**état courant compact** (§ 1-5), lu avant toute proposition.
- Ce fichier, `chronologie.md`, reçoit l'ancien § 6 (résolutions datées) — consulté à la demande, par recherche.
- Les entrées propres à `orbat-json` (symbologie, conformité, source unique) partent dans `orbat-json/references/historique-decisions.md`.
- `SKILL.md` allégé : la grammaire détaillée est déplacée dans `references/grammaire.md` (rien de perdu), `SKILL.md` n'en garde qu'un résumé.
- Revirement signalé a posteriori : `D`/`DIV` (voir entrées 2026-08-04 et 2026-08-09).

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

→ Déplacée vers `orbat-json/references/historique-decisions.md` (symbologie ORBAT, sans impact sur la nomenclature).

### 2026-08-18 (symbologie : construction des icônes et contexte historique)

→ Déplacée vers `orbat-json/references/historique-decisions.md` (symbologie ORBAT, sans impact sur la nomenclature).

### 2026-08-18 (contrôle de conformité à la source, obligatoire avant livraison)

→ Déplacée vers `orbat-json/references/historique-decisions.md` (procédure de livraison des skills ORBAT).

### 2026-08-16 (source unique d'acronymes imposée aux skills ORBAT)

→ Déplacée vers `orbat-json/references/historique-decisions.md`. Résumé utile ici : tout acronyme écrit par un skill de génération d'ORBAT doit venir de ce skill (`orbat-tools:acronyme`) et de lui seul ; le besoin d'un acronyme déclenche son invocation.

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
- ~~**Anomalie constatée, non corrigée :** `references/terrestres.md` contient toujours
  un bloc dupliqué hérité d'une ancienne version (déjà signalé le 2026-08-05 et
  volontairement non traité). Les modifications de ce jour ont été appliquées aux
  **deux** occurrences pour ne pas créer de divergence interne.~~
  ⚠️ *Annotation du 2026-10-10 : mention obsolète, contredite par le point 5 ci-dessus —
  le bloc dupliqué a bien été supprimé le même jour. Conservée barrée comme trace.*

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

> ⚠️ **Revirement (P3), signalé a posteriori le 2026-10-10** : l'entrée du 2026-08-04
> avait réordonné `D`/DIV (`D` officiel). La présente décision l'inverse : **`DIV`
> officiel**, `D` alternatif de lecture.

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
- Officiels réordonnés (officiel en tête des `/`) : `ARM`/-B *(Blindés ; l'échelon Armée est `ARMY` depuis le 2026-10-10)* · `MOT`/-M · `SOF`/-SF · `TRANS`/-T · `GEN`/-G · `-IL`/-ILEG · `MO`/-MTN · `HQ`/Cmdt · `D`/DIV *(⚠️ inversé le 2026-08-09 : `DIV` officiel)* · `BAT`/BTE · `JTAC`/CAS · `FRG`/FRAG · `RK`/R/RKT · `CHMED`/CHSAN · `IG`/`AA`/`ART`/`MG` (vs `ST`-préfixés) · `G`/CN (aérien).
- Suppression « contenu de contenant » : `TRF`/`TRW`, `F`/`FUEL` (carburant terrestre), `W` (eau), `CHEM`, `CTF`/`CTW`/`CTC`, section Ressources fluides de `materiaux.md`. Préservés : `CT`/`RCT`, `FUEL` = Ravitailleur (aérien), Matériaux solides.
- `LUXIR` remplace `LUX-IR` ; `(SMN)` retiré de `CLUS`.

### 2026-08-03

Officialisations : `STP` (spatioport, libère `SP`), `GH` (grenade à main, libère `G`), `FZD` (fuze delay, libère `FUS`), `PN` (personnage), `MA` (soutien amphibie, remplace `SA`), `AM` (assistant munitions), `SPT` (support), `Z` (zone). Désambiguïsation positionnelle `T` actée. Cas confirmés sans conflit classés.

### 2026-07-30

Échelle de portée `SRG/MRG/LRG/SLRG/XRG` commune à tout le système (abandon des lettres uniques `S/M/L/X` côté missiles). Règle de signalement d'absence au lexique actée (workflow étape 8). `REM-SUP` → `REM-LOG`. Normalisation casse `-Mi`→`-MI`.
