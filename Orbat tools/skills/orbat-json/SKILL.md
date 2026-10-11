---
name: orbat-json
description: "Lecture, écriture, restructuration et analyse d'ORBAT au format JSON orbat-mapper.app (`type: \"ORBAT-mapper\"`), et décodage/construction des symboles d'unité (sidc APP-6D/2525). Déclencher dès que Florian tape /orbat-json, /orbat, /orbat_maker ou /orbat-compact, fournit un ORBAT `.json` ou une image d'ORBAT / de symboles militaires, ou demande de : créer/lire un ORBAT, compter matériel/personnel/ravitaillement, décoder ou composer un sidc, convertir une image en JSON, lire un scénario temporel, condenser un ORBAT, regrouper des unités sous un nouvel échelon, régler la visibilité par zoom. Aussi pour des demandes courtes (\"combien de chars ?\", \"lis cet ORBAT\", \"condense au peloton\", \"c'est quoi ce symbole ?\"). Pas pour : l'interface du site orbat-mapper.app (→ `orbat-app`), un classeur xlsx ODIN/JTDS (→ `orbat-xlsx`, les deux s'enchaînent pour xlsx → JSON), la conversion d'un ORBAT entier noms réels → acronymes (→ `orbat-acronymize`).\n"
---

# ORBAT JSON — lecture, écriture, restructuration (format orbat-mapper.app)

Issu de la scission (juillet 2026) de l'ancien skill `orbat_maker`. Frontières :
classeur avec feuille **`UNIT INFO`** → `orbat-xlsx` ; question sur l'interface du
site → `orbat-app` ; libellés réels des formations (vocabulaire et numérotation
d'échelons par armée) → `orbat-nommage` ; renommage de tout le matériel d'un ORBAT
en acronymes → `orbat-acronymize`.

## Source unique des acronymes — `orbat-tools:acronyme`

> 🔴 **RÈGLE ABSOLUE (Florian, août 2026) — dès qu'un acronyme est nécessaire,
> invoquer `orbat-tools:acronyme`** (outil `Skill`), quel que soit le champ (`name`,
> `shortName`, `equipment`, `personnel`, `description`) et l'échelon. Aucune autre
> source : ni mémoire, ni codes vus plus haut dans la conversation, ni ORBAT
> antérieur, ni table locale, ni sigle « évident ». Le besoin d'un acronyme est le
> déclencheur : on s'arrête, on charge le skill, on cherche, puis on écrit.

1. Invoquer le skill — étape d'exécution, jamais dispensée au motif qu'on « connaît
   le système ».
2. Chercher dans l'ordre de `references/naming.md` § 7.1 (`../acronyme/references/INDEX.md`
   → lexiques → tables thématiques → `METHODE.md`).
3. Code trouvé → l'écrire tel quel. Code absent → **ne rien inventer** : cas § 7.2,
   soumis à Florian, on attend son arbitrage.

Ce skill ne contient **aucune liste d'acronymes**, ni dans les `.md` ni en dur dans
les scripts (elle divergerait dès la prochaine décision dans `acronyme`). Il n'y a
**aucune exception** : l'ancienne table d'abréviations de prose du champ `name` est
supprimée — `name` s'écrit en mots français entiers ou avec un code officiel
(naming.md § 7.6).

**Lecture ou écriture.** Pour **lire** un ORBAT existant (Tâches 1, 3, 5), s'appuyer
sur les descriptions du catalogue du fichier ; ne charger `acronyme` que si Florian
demande de décoder ou valider un code (un ORBAT reçu peut employer des codes hors
système). Pour **écrire** (Tâche 4, toute nouvelle entrée de catalogue, tout
`shortName`, tout code cité en `description`), charger `acronyme` systématiquement,
en étape 1.

Historique de ces règles : `references/historique-decisions.md`.

## Avant tout : format et symbologie

- **`references/format.md`** — structure exacte (enveloppe, side → groups → subUnits
  récursifs, catalogues, `state`, `style.limitVisibility`). À lire dès qu'on manipule
  un fichier réel. En une phrase : `sides[] → groups[] → subUnits[]…` ; chaque unité
  porte `id`, `name`, `sidc` (20 chiffres) et optionnellement `equipment`/`personnel`
  en `[{name, count}]` qui réfèrent aux catalogues racine. Sommer = parcourir un
  sous-arbre et additionner.
- **`references/sidc.md`** — grammaire des 20 chiffres. **`references/symbologie.md`**
  — sens des couches (cadre, icône, secteur 1 capacité, secteur 2 mobilité, échelon)
  et **contexte historique** : à lire pour tout ORBAT historique.
- **`references/naming.md`** — conventions de `name`/`shortName`/`description`
  (Règles 1-7) et contrôle de conformité (Règle 8).
- **`references/restructuration.md`** — Tâches 7 à 9 en détail.

Les fichiers réels peuvent peser des dizaines de Mo (30 000+ unités) : **toujours
passer par les scripts ou Python**, jamais à l'œil. De même, `sidc_dictionary.json`
(499 entrées) ne se lit pas en entier : `sidc_lookup.py`.

## Outils fournis (`scripts/`)

`python3 scripts/<outil> --help` fait foi pour les options. Ces scripts sont **la
seule copie** du plugin : `orbat-xlsx` et `orbat-acronymize` les importent
(localisation automatique ; `ORBAT_TOOLS_ROOT` = racine du plugin, en repli). Tests :
`python3 -m unittest discover -s tests` depuis la racine du plugin.

| Script | Usage |
|---|---|
| `aggregate.py ORBAT [--unit U] [--kind equipment\|personnel\|supplies\|all] [--at DATE\|--final] [--json]` | Somme le matériel/personnel/ravitaillement, d'un sous-arbre, à un instant donné |
| `timeline.py ORBAT [--unit U] [--events]` | Récit d'un scénario : jalons, journal d'une unité, éléments disparus |
| `validate.py ORBAT` | Structure réimportable : ids, sidc, catalogues, codes en double, `state` lisible, descriptions vides |
| `conformite.py ORBAT [--source totaux.json] [--at DATE] [--unit ID]` | Rapport de conformité Règle 8 ; code de sortie 1 si écarts |
| `sidc_lookup.py TERME [--set NN] [--limit N]` · `--code NNNNNN [--set NN]` · `--decode SIDC20` | Chercher une entité dans `sidc_dictionary.json` ou décoder un sidc |
| `short_names.py ORBAT [--all] [--dry-run] [--output OUT]` | Génère les `shortName` (naming.md Règle 2, §§ 7.5, 7.7) |
| `new_orbat.py --name N --out F` | Enveloppe vierge ; en bibliothèque : `build_sidc`, `make_unit`, `make_group`, `make_org_unit`, `make_side`, `new_orbat`, puis `orbat_lib.save` |
| `add_legends.py ORBAT` | Légende `**CODE : Nom réel**` agrégée par échelon (blocs Équipement / Personnel), déduite du catalogue ; prose conservée, idempotent (défaut) |
| `add_local_legends.py ORBAT SPEC [--avec-quantites]` | Légende par feuille depuis une table fournie, overrides d'hétérogénéité ; quantités seulement sur demande ; format de spec dans la docstring (naming.md Règle 6) |
| `condense_orbat.py ORBAT TABLE --target ECHELON` | Condensation + élémentarisation (Tâche 7) |
| `group_units.py ORBAT SPEC` | Regroupement sous un nouvel échelon (Tâche 8) |
| `apply_relative_visibility.py ORBAT` | Visibilité par zoom selon la profondeur relative (Tâche 9) |
| `legends.py`, `orbat_lib.py` | Modules (pas de CLI) : `legends.py` est le **seul** endroit qui met en forme une légende |

Les scripts qui écrivent écrasent le fichier par défaut ; `--dry-run` / `--output`
quand ils les proposent.

## Tâche 1 — Lire / comprendre un ORBAT JSON

1. Lire `references/format.md` si pas déjà fait.
2. Charger avec `orbat_lib.load` ; aperçu : nom, version, nombre d'unités, tailles des
   catalogues, arborescence des camps/groupes.
3. Répondre à la question. Pour une hiérarchie, indenter par profondeur et afficher
   l'échelon (depuis le `sidc`, Tâche 6).

## Tâche 2 — Lire un ORBAT depuis une IMAGE → JSON importable

Mode par défaut choisi par Florian : **reconstruire un JSON réimportable**.

1. Analyser l'image : hiérarchie (qui est sous qui), et pour chaque symbole
   l'**échelon** (barres/points au-dessus du cadre) et le **type** (icône interne) —
   `references/sidc.md`, `references/symbologie.md`.
2. Composer chaque `sidc` avec `build_sidc`. Pour l'entité, chercher un code déjà
   employé par Florian : `sidc_lookup.py "<terme>"` (ou `--code` pour vérifier une
   entité) ; choisir le plus proche et signaler les incertitudes plutôt que deviner.
3. Construire l'arbre selon la Tâche 4 (helpers, nommage, `validate.py`).
4. Livrer le `.json` (`present_files`) + résumé des choix et des points à confirmer.

## Tâche 3 — Agréger le matériel (tout ou partie)

`aggregate.py` ; « une partie » = un sous-arbre (`--unit` avec le nom, exact puis
partiel, ou l'`id`). Le script résout les codes via le catalogue et trie par quantité
décroissante. Regroupements plus fins (par catégorie, côté, échelon) :
`orbat_lib.iter_units` / `subtree_units` / `aggregate`.

## Tâche 4 — Écrire / générer un ORBAT → toujours import-ready

Florian veut **toujours** un JSON directement réimportable. Procédure par défaut
(août 2026), à appliquer sans qu'il la redemande ; le détail et les justifications
sont dans `references/naming.md`, cette check-list n'en est que l'ordre d'exécution :

0. **Dater la source** (année, armée, théâtre) et lire `symbologie.md` pour tout ORBAT
   historique ou tout terme d'arme traditionnel (cavalerie, dragons, hussards,
   train…) : « Cavalerie » 1914 = chevaux, « Cavalry » 1975 = reco blindée. Doute →
   demander à Florian (symbologie.md §§ 3.3, 5).
1. **Passe d'identification du matériel, avant toute construction** : invoquer
   `orbat-tools:acronyme`, résoudre chaque ligne de la source vers un code existant
   (Règle 7 § 7.1) ; cas sans code → rien d'inventé, liste soumise à Florian **avant**
   de générer (§ 7.2).
2. **Structure** : clarifier camp, échelon racine, composition si besoin, sinon
   proposer une structure raisonnable.
3. **Construire** avec `new_orbat.py`. `make_group()` réservé à la tête de
   `side.groups` ; tout niveau intermédiaire passe par `make_org_unit()`/`make_unit()`
   (piège d'import, `format.md` § Group). ⚠️ `equipment=`/`personnel=` = liste de
   **tuples** `(code, count)`, jamais de dicts : un dict lève `TypeError` (garde-fou
   posé après l'ORBAT « Arma 3 - Altis », juillet 2026, où il était désassemblé
   silencieusement) — corriger l'appel, ne jamais contourner.
4. **Catalogues** : déclarer tout code employé ; la `description` commence par la
   désignation réelle (Règle 5) — sauf code partagé entre plusieurs camps du fichier
   (Règle 5, piège codes partagés → Règle 6).
5. **Nommage** : `name` sans parenthèses (Règle 1), en mots français entiers ou code
   officiel (§ 7.6), sans répéter la formation mère (§ 7.7) ; `shortName` acronymique
   numéroté partout (Règle 2, § 7.5 — `BT` bataillon ≠ `BAT` batterie, `ARM` et non
   `-B`) → `short_names.py`. Mots d'échelon d'une source anglaise : Règle 4. Puis
   `orbat_lib.mark_empty_subtrees` pour les branches entièrement vides (Règle 3).
6. **Descriptions et légendes** : phrase de contexte d'abord, surtout aux bas échelons
   (§ 7.4), puis légende canonique `**CODE : Désignation réelle**` sans quantité
   (§ 7.3). Outil : `add_legends.py` par défaut ; `add_local_legends.py` si code
   partagé entre camps, hétérogénéité locale ou compte par ligne demandé (Règle 6).
   Après `mark_empty_subtrees`, avant `validate.py` ; un code dont le catalogue ne
   donne pas de nom réel est signalé — corriger le catalogue.
7. **Vérifier et livrer** : `validate.py` (0 erreur ; il ne contrôle que la structure),
   **puis** contrôle de conformité à la source (Règle 8, `conformite.py`) ; corriger
   d'office, rejouer ; livrer avec `present_files` **et** le rapport en 3 blocs
   ✅ vérifié / ⚠️ corrigé / 🔴 non résolu (§ 8.4) — jamais sans.

> ⚠️ **Renommer n'est pas fusionner.** Faire converger plusieurs codes vers un seul
> peut laisser deux lignes du même code dans une unité (totaux justes, anomalie
> invisible sauf en lisant les listes). `apply_rename_map.py` et `condense_orbat.py`
> fusionnent eux-mêmes ; pour toute correction à la main ou par script ad hoc,
> appeler `orbat_lib.merge_items` et relancer `validate.py`, qui le détecte.

## Tâche 5 — Lire un scénario temporel (positions, mouvements, ressources)

Scénarios animés : `state[]` par unité, catégorie `supplies`, `events` (modèle complet
dans `format.md`).

1. Vue d'ensemble : `timeline.py ORBAT` (jalons + unités actives).
2. Une unité : `timeline.py ORBAT --unit "<nom>"` (positions, itinéraires `via`,
   titres, consommations).
3. Ressources à un instant : `aggregate.py --at "<date ISO>"` ou `--final` (`update` =
   absolu, `diff` = delta) ; comparer base vs instant T montre pertes et consommations.
4. Calculs sur mesure : `orbat_lib.resource_at`, `position_at`, `unit_timeline`,
   `scenario_events`.
5. **Détachements temporaires** : un élément enfant dont le `state` finit par
   `location: null` sans perte associée = réembarquement/regroupement dans la mère, pas
   une destruction (`format.md`, `orbat_lib.vanished_elements`, affiché par
   `timeline.py`). Chercher un `update`/`diff` négatif au même moment avant de
   conclure à une perte.

## Tâche 6 — Décoder ou construire un symbole (sidc)

- **Décoder** : `sidc_lookup.py --decode <sidc 20 chiffres>` (identité, set, statut,
  QG, échelon ou mobilité, entité, modificateurs) ; expliquer avec `sidc.md` et
  `symbologie.md`.
- **Construire** : décomposer en couches (fonction → icône, capacité → secteur 1,
  mobilité → secteur 2, échelon), chercher l'entité avec `sidc_lookup.py`, assembler
  avec `build_sidc` ; jamais d'entité inventée (symbologie.md § 5). Cavalerie =
  diagonale seule `121300` (sidc.md) ; les entrées cavalerie en `120500`/`120501` du
  dictionnaire sont un mauvais précédent.

## Tâches 7 à 9 — Restructuration (détail : `references/restructuration.md`)

- **Tâche 7 — Condensation + élémentarisation** : fusionner les échelons sous un
  niveau cible (peloton par défaut) et compter le personnel par élément, table validée
  par Florian → `condense_orbat.py`.
- **Tâche 8 — Regroupement** : insérer un nouvel échelon entre des unités-sœurs et
  leur parent → `group_units.py`.
- **Tâche 9 — Visibilité par zoom** : bandes `minZoom`/`maxZoom` selon la profondeur
  relative de chaque camp → `apply_relative_visibility.py`.

## Catégories de ressources

**`equipment`** (véhicules, armes lourdes), **`personnel`** (escouades, équipes) et
**`supplies`** (munitions, carburant ; catalogue `supplyCategories`) se somment de la
même façon ; `--kind all` couvre les trois.

## Exemples de déclenchement

- « Combien de VAB en tout dans l'ORBAT 2023 ? » → Tâche 3, `aggregate.py --kind equipment`.
- « Lis-moi la structure de ce fichier » (JSON fourni) → Tâche 1.
- « Voici une photo de mon ORBAT, fais-en le JSON » → Tâche 2.
- « Crée une compagnie d'infanterie mécanisée à 3 sections » → Tâche 4 : **d'abord** la
  passe d'identification du matériel, cas litigieux soumis à Florian, **puis** le JSON.
- « C'est quoi le symbole 10031000151211005600 ? » → Tâche 6, `sidc_lookup.py --decode`.
- « Combien de munitions il reste au 2e peloton à 5h du matin ? » → Tâche 5, `aggregate.py --kind supplies --at …`.
- « Raconte-moi ce scénario » / « où est passée la 1 CO ? » → Tâche 5, `timeline.py`.
- « Condense cet ORBAT au peloton » → Tâche 7 ; « compte par escouade plutôt qu'en soldats » → Tâche 7, `--no-condense`.
- « Regroupe ces 12 compagnies en 3 bataillons » → Tâche 8.
- « Applique la visibilité par zoom » / « refais les niveaux de zoom » → Tâche 9.
- « Ce code sert à deux camps, je veux le vrai modèle sur chaque unité » → Tâche 4 étape 6, `add_local_legends.py`.
- « Vérifie que mon ORBAT colle à la source » → Règle 8, `conformite.py`.
- Classeur avec feuille `UNIT INFO`, « ODIN »/« TRADOC »/« JTDS » → `orbat-xlsx`.
- « Où est le bouton pour… » / question sur l'interface du site → `orbat-app`.
