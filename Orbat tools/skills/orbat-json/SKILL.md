---
name: orbat-json
description: >
  Lecture, écriture, restructuration et analyse d'ORBAT (Order of Battle) au
  format JSON orbat-mapper.app (`type: "ORBAT-mapper"`). Déclencher dès que
  Florian tape /orbat-json, /orbat, /orbat_maker ou /orbat-compact (anciens
  alias), fournit un fichier ORBAT `.json` ou une image d'ORBAT / de symboles
  militaires (APP-6/2525C), ou demande de : créer/lire/comprendre un ORBAT,
  compter ou sommer du matériel/personnel/ravitaillement, décoder un sidc,
  convertir une image en JSON, lire un scénario temporel (positions, pertes,
  consommations), condenser un ORBAT (fusion d'échelons, comptage par
  élément), ou regrouper des unités sous un nouvel échelon. Déclencher aussi
  pour des demandes courtes ("combien de chars ?", "lis cet ORBAT", "condense
  au peloton", "regroupe ces compagnies en bataillons", "c'est quoi ce
  symbole ?"). Pour un ORBAT au format tableur xlsx ODIN/JTDS (feuille
  `UNIT INFO`), c'est le skill `orbat-xlsx` qu'il faut — les deux s'enchaînent
  pour la conversion xlsx → JSON.
---

# ORBAT JSON — lecture, écriture, restructuration (format orbat-mapper.app)

Scission (juillet 2026) de l'ancien skill unique `orbat_maker`, séparé en deux
skills : **`orbat-json`** (ce skill — format natif de Florian) et **`orbat-xlsx`**
(format tableur ODIN/JTDS). Si un classeur avec une feuille **`UNIT INFO`** est
fourni, ce n'est pas ce skill — passer à `orbat-xlsx`.

## Source unique des acronymes — `orbat-tools:acronyme`

> 🔴 **RÈGLE ABSOLUE (Florian, août 2026) — dès qu'un acronyme est nécessaire,
> invoquer `orbat-tools:acronyme`.** Sans exception, sans dérogation, quel que soit
> le champ concerné (`name`, `shortName`, `equipment`, `personnel`, `description`) et
> quel que soit l'échelon. Il n'existe **aucune autre source d'acronymes** pour ce
> skill : ni mémoire de Claude, ni codes vus plus haut dans la conversation, ni codes
> repris d'un ORBAT antérieur, ni table locale, ni sigle forgé « parce qu'il est
> évident ». Le besoin d'un acronyme est en lui-même le déclencheur : on s'arrête, on
> charge le skill, on cherche, puis on écrit.

**Ce skill ne contient aucune liste d'acronymes.** Échelons, types de formation,
rôles, codes de matériel, abréviations d'unité : tout vient du skill
`orbat-tools:acronyme` et de lui seul (`../acronyme/references/groupements.md`,
`references/INDEX.md`, `identification/lexique.json`). Aucune table recopiée, ni dans
les `.md`, ni en dur dans les scripts — sinon elle diverge silencieusement dès que
Florian prend une décision dans `acronyme`. Détail et points d'entrée :
`references/naming.md` Règle 2 et Règle 7 § 7.1.

**Comment faire, concrètement** — à chaque fois qu'on s'apprête à écrire une forme
abrégée quelconque :

1. Invoquer le skill avec l'outil `Skill`, argument `orbat-tools:acronyme`. C'est une
   étape d'exécution, pas une intention : ne jamais s'en dispenser au motif qu'on
   « connaît le système ».
2. Chercher le code dans l'ordre de la Règle 7 § 7.1 (`INDEX.md` → lexiques → tables
   thématiques → `METHODE.md`).
3. Code trouvé → l'écrire tel quel. Code absent → **ne rien inventer** : c'est un cas
   Règle 7 § 7.2, on soumet à Florian et on attend son arbitrage.

**Aucune exception.** L'ancienne dérogation accordée à la table d'abréviations
françaises de prose du champ `name` (ex-naming.md Règle 7 § 7.6) est **supprimée** :
elle constituait un second vocabulaire concurrent, exactement ce que la source unique
existe pour empêcher. Le champ `name` s'écrit désormais soit en **mots français
entiers**, soit avec le **code officiel de `acronyme`** — jamais avec une abréviation
maison.

## Symboles d'unité — lire `symbologie.md` avant d'attribuer des icônes

`references/sidc.md` donne la **grammaire** des 20 chiffres ;
`references/symbologie.md` donne le **sens** : les cinq couches d'un symbole (cadre,
icône principale, secteur 1 = capacité, secteur 2 = mobilité, échelon), l'origine des
formes, les erreurs fréquentes, et surtout le **contexte historique** — un même mot
d'arme ne donne pas le même symbole selon l'époque de la source. À lire
systématiquement pour tout ORBAT historique.

## Avant tout : connaître le format

La structure exacte est dans `references/format.md` (enveloppe, side → groups →
subUnits récursifs, catalogues `equipment`/`personnel`, champ `state`). **La lire dès
qu'on manipule un fichier réel.** En une phrase :

> `sides[] → groups[] → subUnits[]…` (récursif). Chaque unité porte `id`, `name`,
> `sidc` (20 chiffres), et optionnellement `equipment`/`personnel` en `[{name, count}]`
> qui réfèrent aux catalogues racine. Sommer = parcourir un sous-arbre et additionner.

Les fichiers réels peuvent être volumineux (jusqu'à des dizaines de Mo, 30 000+ unités).
**Toujours passer par les scripts ou Python** ; ne jamais essayer de tout lire à l'œil.

## Outils fournis (`scripts/`)

Lancer avec `python3` ; ils sont autonomes (juste la lib partagée `orbat_lib.py`).

- **`aggregate.py`** — somme équipement, personnel et/ou **supplies**.
  - tout : `python3 scripts/aggregate.py ORBAT.json`
  - une partie : `--unit "<nom ou id>"` (sous-arbre), `--kind equipment|personnel|supplies|all`
  - **état temporel** : `--final` (rejoue la timeline) ou `--at "<date ISO>"`
  - `--json` pour une sortie machine.
- **`timeline.py`** — lit un scénario comme un récit : `events` globaux + journal d'une
  unité (`--unit`), positions, titres narratifs, changements. `--events` pour les jalons seuls.
- **`validate.py`** — vérifie qu'un fichier est sain et réimportable (ids uniques, sidc
  20 chiffres, codes présents aux catalogues, **unicité de chaque code dans une même
  liste et dans les catalogues racine**, entrées `state` horodatées).
  `python3 scripts/validate.py ORBAT.json`
- **`new_orbat.py`** — construit un ORBAT import-ready. En CLI : enveloppe vierge
  (`--name --out`). Comme **bibliothèque** quand on génère depuis une demande :
  `build_sidc`, `make_unit`, `make_group`, `make_org_unit`, `make_side`, `new_orbat`, puis
  `orbat_lib.save`.
  **⚠️ Format strict de `equipment=`/`personnel=` : liste de TUPLES `(code, count)`,
  jamais de dicts `{"name":..,"count":..}`.** Un dict y est désassemblé silencieusement
  en ses deux clés (`for n, c in items` sur un dict à 2 clés itère ses clés, pas ses
  valeurs) — piège confirmé sur l'ORBAT « Arma 3 - Altis » (juillet 2026), produisant des
  entrées corrompues sans erreur visible. Depuis ce correctif, `make_unit`/`make_org_unit`
  lèvent une `TypeError` explicite si un dict est passé — ne jamais contourner ce
  garde-fou, corriger l'appel.
- **`add_legends.py`** — annote chaque échelon avec la légende (code → nom réel) de
  tout le matériel/personnel présent dans son sous-arbre (agrégée), déduite des
  descriptions du catalogue racine, sans compte ni mapping externe. **Étape par défaut
  en fin de Tâche 4** (voir point 6 ci-dessous) — mais voir `add_local_legends.py`
  ci-dessous pour les cas où elle ne suffit pas.
- **`add_local_legends.py`** — variante locale (par unité feuille, pas agrégée), avec
  **compte par ligne**, sections **Équipement/Personnel séparées**, et **overrides
  d'hétérogénéité par unité**, à partir d'une table de correspondance fournie (pas du
  catalogue racine). À utiliser à la place d'`add_legends.py` dès qu'un code est
  **partagé entre plusieurs camps du même fichier**, ou que Florian veut le compte / la
  séparation Équipement-Personnel / une hétérogénéité locale. Voir `references/naming.md`
  Règle 6 pour le détail des critères, et la docstring du script pour le format de spec
  et l'usage complet.
- **`condense_orbat.py`** — condensation d'échelon + élémentarisation du personnel
  (Tâche 7).
- **`group_units.py`** — regroupement d'unités-sœurs sous un nouvel échelon
  intermédiaire (Tâche 8).
- **`apply_relative_visibility.py`** — visibilité cartographique par zoom, basée sur
  la profondeur relative de l'unité dans son propre camp (pas sur le type d'échelon).
  Voir `references/format.md` section `style.limitVisibility` pour la règle complète,
  et Tâche 9 ci-dessous pour l'usage.

## Tâche 1 — Lire / comprendre un ORBAT JSON

1. Lire `references/format.md` si pas déjà fait.
2. Charger avec `orbat_lib.load`, donner un aperçu : nom, version, nombre d'unités,
   tailles des catalogues, arborescence des camps/groupes (échelons supérieurs).
3. Répondre à la question posée (structure, ordre de bataille, effectifs…). Pour
   présenter une hiérarchie, indenter par profondeur et afficher l'échelon (depuis le
   `sidc`, voir `references/sidc.md`).

## Tâche 2 — Lire un ORBAT depuis une IMAGE  → JSON importable

C'est le mode par défaut choisi par Florian : **reconstruire un JSON réimportable**.

1. Analyser l'image : identifier la hiérarchie (qui est sous qui), et pour chaque
   symbole, en déduire l'**échelon** (barres/points au-dessus du cadre) et le **type**
   (icône interne) — voir la correspondance dans `references/sidc.md`.
2. Pour chaque unité, composer un `sidc` 20 chiffres avec `build_sidc`. En cas de doute
   sur l'entité, consulter `references/sidc_dictionary.json` (codes réels déjà utilisés
   par Florian) et choisir le plus proche ; signaler les incertitudes plutôt que deviner.
3. Construire l'arbre avec `make_unit`/`make_group`/`make_side`/`new_orbat`, générer des
   `id` uniques (automatique), respecter les conventions de `references/naming.md`
   (pas de parenthèses dans `name`, `shortName` systématique), puis `validate.py` avant
   de livrer.
4. Livrer le fichier `.json` (via `present_files`) + un résumé des choix faits et des
   points incertains à confirmer.

## Tâche 3 — Agréger le matériel (tout ou partie)

Utiliser `aggregate.py`. « Une partie » = un sous-arbre : passer `--unit` avec le nom
(exact puis partiel) ou l'`id` de l'unité racine. Le script résout les codes vers leur
description via le catalogue et trie par quantité décroissante. Pour des regroupements
plus fins (par catégorie, par côté, par échelon), adapter en s'appuyant sur
`orbat_lib.iter_units` / `subtree_units` / `aggregate`.

## Tâche 4 — Écrire / générer un ORBAT  → toujours import-ready

Florian veut **toujours** un JSON directement réimportable dans orbat-mapper.app.

### Procédure par défaut (août 2026) — à appliquer sans qu'il la redemande

Détail complet et justifications dans `references/naming.md` **Règle 7**. Résumé
opérationnel, dans l'ordre :

0. **Dater la source et charger la symbologie, AVANT toute construction.**
   Relever l'**année, l'armée et le théâtre** de la source : c'est ce qui détermine
   les icônes, pas le nom des unités. Lire `references/symbologie.md` dès qu'un ORBAT
   est **historique** ou qu'il contient des termes d'arme traditionnels (cavalerie,
   dragons, hussards, chasseurs, cuirassiers, train…). ⚠️ « Cavalerie » en 1914 =
   **des chevaux** ; « Cavalry » en 1975 = **de la reconnaissance blindée** — même mot,
   symboles différents. En cas de doute sur l'époque ou le rôle réel : demander à
   Florian plutôt que trancher au jugé (l'erreur d'icône historique est indétectable
   pour qui n'a pas la période en tête).

0 bis. **Passe d'identification du matériel, AVANT toute construction.**
   **Invoquer d'abord le skill `orbat-tools:acronyme`** (outil `Skill`, argument
   `orbat-tools:acronyme`) — ce n'est pas optionnel et ça ne se déduit pas du contexte :
   sans lui, les 691 codes du système ne sont pas chargés et le risque d'inventer un
   acronyme est maximal. Ses fichiers sont dans le **même plugin**, à côté de ce
   skill : `../acronyme/` (`references/INDEX.md`, `identification/lexique.json`,
   `identification/METHODE.md`…).
   Ensuite, lister tout l'équipement et le personnel de la source et résoudre chaque
   ligne vers un acronyme **existant** (ordre de recherche en Règle 7 § 7.1).
   **Ne jamais inventer d'acronyme.** Un matériel sans code correspondant → ne rien
   mettre, et **soumettre la liste des cas litigieux à Florian avant de générer le
   JSON** — il tranche, puis seulement on construit (Règle 7 §§ 7.1-7.2).
1. **Nommage** (Règle 7 §§ 7.5-7.7, en plus des Règles 1-3) :
   - `shortName` = forme **acronymique** avec numéro/lettre d'ordre : `23e CIE-INF`,
     `"A" BT-INF`, `"B" BT-ARM` (⚠️ `BT` = bataillon, `BAT` = batterie ; `-B` blindé
     déprécié au profit de `ARM` — décisions du 2026-08-09 et du 2026-08-04) ;
   - `name` = **français lisible**, en mots entiers ou avec un code officiel de
     `acronyme` — jamais une abréviation maison : `23e Compagnie d'Infanterie`,
     `1er Bataillon Blindé` (ou `23e CIE-INF` si Florian veut la forme codée) ;
   - **jamais répéter la formation mère** dans les échelons inférieurs (`EM` et
     `1ère Cie`, pas `État Major DBA` et `1ère Cie DBA`).
2. **Descriptions** (Règle 7 §§ 7.3-7.4), pour chaque unité :
   - une à deux **phrases de contexte** d'abord — ce que l'ORBAT ne montre pas, en
     priorité aux **bas échelons** (composition en rôles d'une escouade, articulation
     interne d'une compagnie sans sous-unités déclarées, réservistes, matériel
     hétérogène). Rien plutôt qu'une phrase creuse ;
   - ligne vide, puis la légende au format canonique **`**CODE : Désignation
     réelle**`**, une ligne par code, **sans quantité**.
3. **Contrôle de conformité à la source** (Règle 8), systématique dès qu'un travail est
   réputé terminé — création, remaniement, restructuration, édition de masse des
   `count`. Confronter le JSON produit à la source : totaux agrégés (`aggregate.py`),
   effectifs des unités feuilles, complétude structurelle, échelons, codes attestés.
   **Corriger d'office** tout écart trouvé, puis rejouer le contrôle. Livrer avec le
   rapport en 3 blocs — ✅ vérifié / ⚠️ corrigé / 🔴 non résolu — **jamais sans**.

Le reste de la Tâche 4 (points 1 à 6 ci-dessous) s'applique par-dessus.


1. Clarifier l'intention si besoin (camp, échelon racine, composition), sinon proposer
   une structure raisonnable et la construire.
2. Construire avec les helpers de `new_orbat.py`. Échelon par nom (`"compagnie"`,
   `"bataillon"`…) ou code ; entité 6 chiffres (réutiliser un code du dictionnaire pour
   rester cohérent avec son univers). **`make_group()` réservé à `side.groups` (tête
   uniquement) : tout niveau intermédiaire (division, brigade, regroupement...) passe
   par `make_org_unit()`/`make_unit()`, jamais `make_group()` imbriqué — piège d'import
   confirmé, voir `references/format.md`.**
3. Déclarer dans les catalogues racine tout code `equipment`/`personnel` employé, avec
   une description. **La description doit toujours commencer par la désignation réelle
   du matériel** (nom de véhicule/appareil réel ou du jeu, ex. `"MSE-3 Marid — variante
   commandement"`), suivie si besoin de `" — "` puis du contexte additionnel — jamais
   une description qui ne mentionne pas le modèle exact (naming.md Règle 5). Florian
   code toujours en acronymes `/nomenclature-v4` mais veut pouvoir retrouver, à tout
   moment et à tout niveau de l'arbre, de quel matériel précis il s'agit — pas
   seulement dans le catalogue racine (voir point 6).
   **⚠️ Sauf si le code est partagé entre plusieurs camps du même fichier** (ex. `MBT`
   utilisé à la fois par la France et un camp adverse) : dans ce cas, ne JAMAIS mettre
   de désignation réelle spécifique à un camp dans le catalogue racine (elle
   contaminerait les autres camps qui partagent le code) — voir `references/naming.md`
   Règle 5 « piège codes partagés » et Règle 6 (légende locale).
4. **Nommage** (toute unité, sans exception) : suivre `references/naming.md` —
   **jamais de parenthèses dans `name`** (pas de contexte de parenté, de garnison ni de
   note d'incertitude entre parenthèses ; la hiérarchie porte déjà le contexte, la
   garnison va après un tiret cadratin, le reste va en `description`), et **toujours**
   renseigner un `shortName` en **acronymes issus de `orbat-tools:acronyme`**
   (invoquer le skill avant d'écrire — jamais d'abréviation dérivée de tête).
   - Si la source est en anglais et que Florian veut aligner les noms sur
     `/acronyme` : `orbat_lib.apply_word_substitutions(orbat,
     orbat_lib.build_echelon_word_subst())` — la table est **relue dans
     `../acronyme/references/groupements.md` à chaque appel**, jamais figée dans
     `orbat_lib` (naming.md Règle 4 — attention au piège FR/EN sur « Section »).
   - Si des échelons peuvent être vides (TOE non détaillé par la source) :
     `orbat_lib.mark_empty_subtrees(orbat)` juste avant `validate.py`, pour
     marquer (symbole ` Ø`) les branches entières sans equipment ni personnel
     (naming.md Règle 3 — ne marque que si TOUT le sous-arbre est vide).
5. **Toujours** finir par `validate.py` (0 erreur attendu), **puis dérouler le
   contrôle de conformité à la source (naming.md Règle 8)** — `validate.py` ne
   contrôle que la structure, jamais les effectifs. Livrer ensuite le `.json` avec
   `present_files`, **accompagné du rapport de contrôle en 3 blocs** (✅ vérifié /
   ⚠️ corrigé / 🔴 non résolu, § 8.4).
6. **Légende de matériel par échelon — obligatoire.** Un ORBAT codé en acronymes v4 est
   illisible « en l'état » à l'échelle d'une unité si on ne peut retrouver le nom réel
   du matériel qu'en remontant au catalogue racine. Avant de livrer, choisir l'outil :
   - **Cas par défaut** (un code = un seul matériel dans tout le fichier, pas besoin de
     compte ni de séparation Équipement/Personnel) : `python3 scripts/add_legends.py
     <fichier.json>` — il ajoute à la `description` de **chaque échelon** la liste des
     codes présents dans son sous-arbre avec leur nom réel (`* CODE = Nom réel`), déduit
     directement des descriptions de catalogue (point 3). Ordre : après
     `mark_empty_subtrees` (point 4), avant `validate.py` (point 5). Script idempotent ;
     signale en warning tout code dont la description ne permet pas d'extraire un nom
     réel (à corriger côté catalogue plutôt qu'ignorer).
   - **Dès qu'un code est partagé entre camps, ou que Florian veut le compte par ligne,
     Équipement/Personnel séparés, ou une hétérogénéité locale** (naming.md Règle 6) :
     `python3 scripts/add_local_legends.py <fichier.json> <spec.json>` à la place —
     légende par unité feuille (pas agrégée), avec table de correspondance fournie
     explicitement plutôt que déduite du catalogue racine.

   **Directive « description narrative » (goût confirmé par Florian, août 2026,
   camp AAF « Arma 3 - Altis »).** Au-delà de la légende auto-générée, Florian
   apprécie qu'une **phrase de contexte** précède la légende dans `description`,
   quand une information pertinente existe :
   - **Unités feuilles (équipe/groupe)** : composition en rôles/grades réels,
     ex. `"Section Commander (Sgt/Cpl), Lead Scout Mk 25, LMG Gunner Mk 23."`.
   - **Unités intermédiaires** : composition d'ensemble ou remarque de service,
     ex. `"Bataillon mixte infanterie blindée (MCV-10 Warrior) et chars (Leopard
     2ALF), mixte réguliers / réservistes."`, ou une exception notable, ex.
     `"La 3e Recce Section n'est armée qu'à la mobilisation (réservistes)."`,
     `"Non constructible avec les groupes prédéfinis de l'éditeur ArmA 3."`.

   Cette phrase vient **avant** le bloc légende (`Équipement :` / `Personnel :`),
   séparée par une ligne vide — elle ne le remplace pas. Ne pas inventer de
   contexte sans information de la source ou de Florian ; une unité sans
   particularité connue garde juste la légende seule (pas de phrase creuse).

   **Statut mis à jour (août 2026) : cette phrase de contexte n'est plus optionnelle,
   elle fait partie de la procédure par défaut** (Règle 7 § 7.4), avec priorité aux
   échelons les plus bas dont la composition n'est lisible nulle part ailleurs.

   ⚠️ **Format de légende.** Le format canonique est désormais
   `**CODE : Désignation réelle**` (une ligne par code, **sans quantité**, Règle 7
   § 7.3). `add_legends.py` et `add_local_legends.py` produisent encore l'ancien
   `* CODE = Nx Désignation` : reformater leur sortie avant de livrer, ou corriger
   les scripts (non fait à ce jour, en attente d'un feu vert de Florian).

> ⚠️ **Renommer n'est pas fusionner.** Toute opération qui fait converger
> plusieurs codes vers un seul (conversion `orbat-acronymize`, élémentarisation
> de `condense_orbat.py`, correction de vocabulaire décidée dans `acronyme`)
> peut laisser **deux lignes du même code** dans la même unité. Les totaux
> restent justes — `aggregate()` somme par nom — donc l'anomalie ne se voit
> nulle part sauf en lisant les listes brutes. Toujours relancer `validate.py`
> après une passe de renommage, et fusionner les lignes convergentes en une
> seule à somme cumulée plutôt que de les empiler.

## Tâche 5 — Lire un scénario temporel (positions, mouvements, ressources qui changent)

Certains fichiers sont des **scénarios animés** : unités positionnées sur la carte,
déplacements, et ressources/statuts qui évoluent dans le temps (champ `state[]`,
catégorie `supplies`, `events`). Modèle complet dans `references/format.md`.

1. Vue d'ensemble narrative : `timeline.py ORBAT.json` (jalons globaux + unités actives).
2. Suivre une unité : `timeline.py ORBAT.json --unit "<nom>"` (positions, itinéraires
   `via`, titres, consommations).
3. État des ressources à un instant : `aggregate.py --at "<date ISO>"` ou `--final`
   (rejoue la timeline : `update` = absolu, `diff` = delta). Comparer base vs instant T
   montre les pertes/consommations (ex. munitions, véhicules détruits).
4. Pour des calculs sur mesure (position à T, trajet, consommation entre deux dates),
   s'appuyer sur `orbat_lib.resource_at`, `position_at`, `unit_timeline`, `scenario_events`.
5. **Détachements temporaires (démontage, véhicules trackés isolément) :** un élément
   enfant dont le `state` finit par `location: null` sans perte associée signale un
   réembarquement/regroupement dans l'unité mère, pas une destruction — convention
   détaillée dans `references/format.md`, détectée automatiquement par
   `orbat_lib.vanished_elements` et affichée par `timeline.py`. Toujours distinguer ce
   cas d'une vraie perte (chercher un `update`/`diff` négatif au même moment) avant de
   conclure dans un récit.

## Tâche 7 — Condensation d'échelon + élémentarisation du personnel

Deux opérations combinées pour produire un ORBAT plus compact, plus lisible à
gros grain, sans perdre l'information de composition :

1. **Condensation d'échelon.** Fusionner tout échelon strictement inférieur à
   un niveau cible (par défaut **peloton**, ou **compagnie** si demandé) dans
   son ancêtre le plus proche qui est à ce niveau ou au-dessus. L'échelon
   fusionné disparaît de l'arbre (`subUnits`) ; son `equipment`/`personnel`/
   `supplies` est sommé (par nom de catalogue) dans l'ancêtre retenu, qui
   devient une feuille s'il n'a plus de sous-unité à composition supérieure.

2. **Élémentarisation du personnel.** Convertir les effectifs bruts (comptés
   en têtes) en comptage par élément (escouade/groupe), selon une table de
   conversion propre à chaque type de personnel — ex. une escouade de
   Guardsmen = 10 hommes, un groupe = 5 hommes. Priorité aux plus gros
   éléments (décomposition gloutonne) ; tout reliquat qui ne rentre dans
   aucun palier reste en comptage brut sous le code d'origine, signalé pour
   revue manuelle plutôt que forcé dans un élément incomplet.

### Pipeline

1. **Localiser le fichier** et vérifier qu'il porte un `sidc` cohérent par
   unité (position 9-10 = échelon, voir `references/sidc.md`). Sans `sidc`
   fiable, la condensation ne peut pas distinguer un échelon d'un autre —
   proposer de passer par la Tâche 4 d'abord si besoin.

2. **Déterminer le niveau cible** avec Florian : peloton par défaut
   (`"le plus petit échelon possible soit le peloton"`), compagnie si le
   peloton résultant reste trop fin ou si Florian le demande explicitement
   (`"voire la compagnie"`). Noms acceptés : équipe, escouade, section,
   peloton, compagnie, bataillon, régiment, brigade, division, corps, armée
   (voir table complète dans le script).

3. **Construire la table de conversion escouade/groupe** avec Florian, une
   entrée par code de catalogue `personnel` (et `equipment` si pertinent) :
   ```json
   {
     "INF": {
       "elements": [
         {"code": "SQ-INF", "size": 10, "description": "Escouade de Guardsmen (10 hommes)"},
         {"code": "GRP-INF", "size": 5,  "description": "Groupe/demi-escouade de Guardsmen (5 hommes)"}
       ]
     }
   }
   ```
   Un code de catalogue non présent dans cette table n'est jamais
   élémentarisé (reste en comptage brut tel quel) — ne pas deviner de taille
   d'élément sans confirmation de Florian pour un nouveau type de personnel.

   **Groupes de commandement (officier + escorte).** Certains reliquats ne
   sont pas une escouade incomplète mais un vrai groupe de commandement (1
   officier + son escorte, effectif réduit — code `GRP-HQ`, voir skill
   `acronyme`, `identification/personnel.md`). Ajouter une clé réservée
   `_command_group` à la table pour fusionner automatiquement un officier
   isolé et son reliquat d'infanterie en un seul élément `GRP-HQ`, au lieu de
   laisser deux entrées séparées :
   ```json
   {
     "INF": { "elements": [ ... ] },
     "_command_group": {
       "officer_code": "OFF",
       "result_code": "GRP-HQ",
       "combine_with": ["INF"],
       "description": "Groupe de commandement (officier + escorte)"
     }
   }
   ```
   Ne s'applique que si l'unité porte à la fois l'officier **et** un
   reliquat d'un des codes listés dans `combine_with` — un officier seul
   sans reliquat n'est jamais transformé en `GRP-HQ`.

4. **Appliquer avec le script fourni** :
   ```
   python3 scripts/condense_orbat.py <orbat.json> <squad_sizes.json> --target peloton
   ```
   Le script fait les deux passes dans l'ordre (condensation puis
   élémentarisation) et écrase le fichier d'origine par défaut — `--dry-run`
   pour un aperçu, `--output` pour une copie séparée, `--no-condense` /
   `--no-elementize` pour n'appliquer qu'une seule des deux passes.

5. **Présenter le résumé** à Florian : nombre d'unités avant/après, nombre
   d'échelons fusionnés, nouveaux codes de catalogue ajoutés (les éléments),
   et surtout la liste des **reliquats** (effectifs qui ne rentrent dans
   aucun palier d'élément) — ce sont typiquement des sections de commandement
   à effectif réduit (2-4 pax) plutôt qu'une vraie escouade ; à confirmer avec
   Florian si ça doit rester en comptage brut ou être reclassé.

6. **Valider le fichier résultant** : `python3 scripts/validate.py <orbat.json>`.
   Puis relancer `add_legends.py` ou `add_local_legends.py` (Tâche 4 point 6) si
   la condensation a changé la composition des feuilles — les légendes existantes
   restent correctes (calculées par sous-arbre) mais peuvent devenir moins utiles
   si la feuille combine beaucoup de matériel différent.

### Points d'attention (condensation)

- La condensation se base **exclusivement sur le `sidc`**, jamais sur le nom
  de l'unité (« Squad », « Escouade »… ne sont pas fiables d'une source à
  l'autre, notamment sur du matériel traduit ou fictif). Un `Group` de tête
  sans `sidc` n'est jamais fusionné (il n'a pas d'échelon à comparer).
- Le résultat n'est **pas idempotent sur l'élémentarisation** si on relance
  le script avec la même table sur un fichier déjà élémentarisé et que les
  codes d'éléments (ex. `SQ-INF`) sont réutilisés comme clé de départ dans
  une nouvelle table — toujours utiliser les codes de catalogue d'origine
  (`INF`, pas `SQ-INF`) comme clé de la table de conversion.
- Ce script ne touche pas aux codes d'acronymes eux-mêmes (voir skill
  `acronyme` / `orbat-acronymize` pour ça) — il s'applique aussi bien à un
  ORBAT déjà acronymisé qu'à un ORBAT resté en noms réels.

## Tâche 8 — Regroupement d'unités existantes sous un nouvel échelon

Opération distincte (et indépendante) de la Tâche 7 : au lieu de fusionner des
échelons bas vers le haut, on **insère un nouvel échelon intermédiaire** entre
des unités-sœurs existantes et leur parent — par exemple répartir 12
compagnies à plat sous un régiment en 3 bataillons de 4 compagnies chacun.

1. **Identifier le parent** dont on regroupe des enfants directs, le motif
   (regex) qui sélectionne lesquels de ses enfants regrouper (dans leur
   ordre d'origine), la taille de chaque groupe, l'échelon des nouvelles
   unités, et — si Florian a des noms précis en tête — la liste des noms à
   leur donner (sinon génération automatique `"1er Bataillon"`, `"2e
   Bataillon"`...).

2. **Construire la spécification** :
   ```json
   [
     {
       "parent_name": "114th Cadian Regiment — Mechanised",
       "select_regex": "^\\d+(st|nd|rd|th) Mechanised Infantry Company$",
       "group_size": 4,
       "new_echelon": "bataillon",
       "new_names": ["1st Battalion", "2nd Battalion", "3rd Battalion"]
     }
   ]
   ```
   Une spec est une liste : plusieurs regroupements indépendants peuvent être
   appliqués en une seule passe (ex. regrouper aussi des escadrons en groupe
   tactique dans le même appel).

3. **Appliquer avec le script fourni** :
   ```
   python3 scripts/group_units.py <orbat.json> <grouping_spec.json>
   ```
   Chaque nouvelle unité reçoit un `sidc` cohérent : échelon demandé, entité
   héritée du premier enfant du groupe (composition homogène supposée par
   défaut — passer `"entity"` explicitement dans la spec sinon). Les enfants
   sélectionnés sont déplacés tels quels (avec tout leur sous-arbre) sous la
   nouvelle unité, à la place qu'occupait le premier d'entre eux ; les
   enfants non sélectionnés du parent restent inchangés à leur position.
   Écrase le fichier d'origine par défaut (`--output` / `--dry-run`
   disponibles comme les autres scripts).

4. **Valider** avec `python3 scripts/validate.py <orbat.json>`, puis relancer
   `add_legends.py`/`add_local_legends.py` si Florian veut des légendes à jour
   sur les nouveaux échelons créés (ils n'ont pas de matériel en propre, donc
   pas de légende tant qu'aucune passe n'est relancée dessus).

## Tâche 9 — Visibilité cartographique par profondeur relative (zoom sémantique)

Remplace l'ancien classement par nom d'échelon : le critère est la **profondeur dans
l'arbre** de chaque camp (nombre de parents), rapportée à une échelle de référence
commune fixe (`R = 5` bandes, bornes `[0, 10, 13, 16, 18, 24]`, à ne changer que sur
demande explicite de Florian). Détail complet de la règle (formule, arrondi, règles A
et B de comblement) dans `references/format.md` section `style.limitVisibility`.

1. `python3 scripts/apply_relative_visibility.py <orbat.json>` — traite chaque camp du
   fichier indépendamment avec sa propre profondeur `D`, applique `style.limitVisibility`
   + `minZoom`/`maxZoom` à **toutes** les unités, écrase le fichier en place.
2. Toujours enchaîner avec `python3 scripts/validate.py <orbat.json>`.
3. Livrer le fichier avec `present_files`, en rappelant les bandes obtenues par camp
   (le script les affiche sur stdout).

## Catégories de ressources

Trois catégories cohabitent : **`equipment`** (véhicules, armes lourdes), **`personnel`**
(escouades, équipes) et **`supplies`** (munitions, carburant ; catalogue
`supplyCategories`). Les trois se somment de la même façon ; `--kind all` les couvre.

## Codes équipement / personnel et skill `acronyme`

Les codes (`VUTT`, `V-HMG`, `BMP 2 IFV`…) sont définis dans les catalogues du fichier.
Le comportement dépend du sens de l'opération — distinction établie en août 2026, elle
remplace l'ancienne consigne « ne croiser avec `nomenclature-v4` que sur demande
explicite », devenue fausse pour la génération :

- **LECTURE d'un ORBAT existant** (Tâches 1, 3, 5 — compter, résumer, raconter) :
  s'appuyer sur les **descriptions du catalogue** du fichier. Ne charger le skill
  `orbat-tools:acronyme` que si Florian demande explicitement de décoder ou de valider
  un code. Un ORBAT reçu peut légitimement utiliser des codes hors système.
- **ÉCRITURE / GÉNÉRATION** (Tâche 4, et toute création de nouvelles entrées de
  catalogue) : **charger `orbat-tools:acronyme` systématiquement, en étape 0**, avant
  d'écrire la moindre ligne de TOE. C'est la procédure par défaut (Règle 7 § 7.1) :
  aucun code nouveau ne doit être écrit sans être attesté dans le système.
  ⚠️ Cela vaut pour **tout acronyme produit par le skill**, pas seulement les codes de
  TOE : `shortName`, abréviation d'échelon ou de type de formation, code cité dans une
  `description`. Dès qu'une forme abrégée doit être écrite, elle vient de `acronyme`
  (règle absolue en tête de ce fichier).

`nomenclature-v4` est l'ancien nom du skill `acronyme` ; toute mention résiduelle
renvoie au même système.

## Persistance des éditions du skill

Comme pour ses autres skills, les modifications de ce dossier ne survivent pas entre
sessions sans le cycle `/maj` → zip → ré-upload. Ne repackager le skill que sur demande
explicite de Florian.

## Exemples de déclenchement

- « Combien de VAB en tout dans l'ORBAT 2023 ? » → Tâche 3, `aggregate.py --kind equipment`.
- « Lis-moi la structure de ce fichier » (JSON fourni) → Tâche 1.
- « Voici une photo de mon ORBAT, fais-en le JSON » → Tâche 2.
- « Crée une compagnie d'infanterie mécanisée à 3 sections » → Tâche 4, JSON import-ready.
- « Crée une compagnie d'infanterie mécanisée à 3 sections » → **d'abord** la passe
  d'identification du matériel (Règle 7 § 7.2), cas litigieux soumis à Florian,
  **puis** le JSON.
- « C'est quoi le symbole 10031000151211005600 ? » → décodage via `references/sidc.md`.
- « Combien de munitions il reste au 2e peloton à 5h du matin ? » → Tâche 5, `aggregate.py --kind supplies --at …`.
- « Raconte-moi ce qui se passe dans ce scénario » / « où est passée la 1 CO ? » → Tâche 5, `timeline.py`.
- « Condense cet ORBAT au peloton » / « fusionne les escouades vers l'échelon supérieur » → Tâche 7, `condense_orbat.py`.
- « Compte par escouade plutôt qu'en nombre exact de soldats » → Tâche 7 (élémentarisation seule, `--no-condense`).
- « Regroupe ces 12 compagnies en 3 bataillons » → Tâche 8, `group_units.py`.
- « Applique la visibilité par zoom sur tout l'ORBAT » / « refais les niveaux de zoom » → Tâche 9, `apply_relative_visibility.py`.
- « Ce même code sert à deux camps différents, je veux le vrai modèle sur chaque unité » →
  Tâche 4 point 6, `add_local_legends.py` plutôt que `add_legends.py`.
- Un classeur avec une feuille `UNIT INFO`, un XML JTDS, ou les mots « ODIN »/« TRADOC » →
  **ce n'est pas ce skill** — passer à `orbat-xlsx`.
