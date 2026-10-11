# Journal des versions — plugin orbat-tools

Historique technique du plugin (scripts, structure). Les décisions de
nomenclature vivent dans `skills/acronyme/decisions.md` (état courant) et
`skills/acronyme/chronologie.md` (historique daté).

## 1.0.0 — 2026-10-10 · Fin de l'audit de mise à niveau

Étapes 3 et 4 du plan d'audit d'octobre 2026, suivies d'une revue indépendante
(constats corrigés). 86 tests (`python3 -m unittest discover -s tests`),
`skills/acronyme/scripts/check.py` à 0 erreur.

**Arbitrages de Florian appliqués (acronyme)** — détail daté dans
`skills/acronyme/chronologie.md`, entrée 2026-10-10.
- Renommages : Bêtes `BT` → `BET`, Croisade `CRS` → `CRZ`, Secteur galactique
  `SEC` → `SCT`, échelon Armée `ARM` → `ARMY` (`BT`, `CRS`, `SEC`, `ARM` gardent
  leur autre sens).
- Canon léger/moyen/lourd : `C.L` / `C.M` / `C.H` (`HC` = Hache, `LC` = Lance).
- Grenades : `GR` = grenade à fusil ; `GE` (explosive) et `GF` (fragmentation)
  sont deux codes distincts.
- Obusier : `G` officiel, `HWZ` alternatif de lecture.
- Règle cardinale n°2 : liste explicite des exceptions (sens départagés par la
  position, même concept décliné).
- Toutes les tables au format `Officiel | Alternatifs`, avec bassin déclaré ;
  alias auparavant cités dans les notes (`IMV`, `MRAP`, `MEDEVAC`, `MGF`,
  `ZEP`…) passés en colonne Alternatifs. Aucun sens ajouté : les lignes
  `X / Y` dont on ne sait pas si ce sont deux codes ou un code et son alias
  restent en officiel + alias et sont listées au § 5 de `decisions.md`.

**acronyme**
- `decisions.md` devient l'état courant compact (49 → 23 Ko) ; l'historique
  daté passe dans `chronologie.md` ; les entrées propres aux ORBAT JSON dans
  `orbat-json/references/historique-decisions.md`.
- Grammaire de SKILL.md réduite à un résumé ; le détail vit dans
  `references/grammaire.md`.
- Contenu périmé corrigé : `SPG` (tir direct), `SRG`, `IFV`, Gepard
  (`VB-2AACA`), `INF-CAV`, `CA.30`, `CH-TT`, règle n°4 dans les lexiques,
  renvois cassés, doublons, points ouverts reportés au § 5.
- Nouveaux outils : `scripts/tables.py` (lecteur unique des tables),
  `scripts/check.py` (collisions par bassin, casse, calibres, renvois, lexiques,
  INDEX à jour ; `--code X` avant toute proposition), INDEX par bassin
  (officiels et alternatifs). Les collisions déjà connues (exceptions de la
  règle n°2, cas confirmés, points ouverts) sont listées couple par couple
  dans `scripts/collisions_connues.json` : tout nouveau sens en collision est
  une erreur. `check.py --accepter-collisions` ne se lance qu'après arbitrage.

**orbat-json**
- SKILL.md ramené de ~4 900 à ~2 100 mots ; Tâches 7 à 9 dans
  `references/restructuration.md` ; règle « source unique » écrite une fois.
- Nouveaux scripts : `sidc_lookup.py` (chercher une entité, décoder un sidc),
  `short_names.py` (génère les `shortName`, remplace `build_france_1980.py`
  jamais livré ; ordinaux US `2d`/`3d` reconnus ; rien n'est écrit quand un
  échelon n'a pas de code, ex. groupe d'armées), `conformite.py` (rapport de
  la Règle 8, 12 contrôles).
- Plus aucune mention de l'ancien nom `nomenclature-v4`.

**orbat-acronymize**
- Aligné sur la règle 7.2 : tout code absent du lexique est soumis à Florian ;
  rien n'entre dans `lexique.json` sans sa validation.
- `draft_mapping.py` : brouillon de mapping depuis le lexique (`_a_valider`
  pour le reste, jamais de code inventé) ; `apply_rename_map.py` refuse un
  brouillon dont `_a_valider` n'est pas vide.
- Titres enrichis (« Escadron de VAB ») seulement avec `--titres`.

**orbat-xlsx** : commentaire faux sur `120500` corrigé (`UCA---`, chars, y
était déjà mappé) ; export
XLSX du site exclu des déclencheurs ; section « Persistance » retirée.

**orbat-app** : résumé du changelog du site mis à jour jusqu'en octobre 2026
(PMTiles et HTML autonome hors-ligne, mesures de coordination et KML, fin
d'OpenLayers, Select, MGRS, relief 3D, Unit changes, import MilX…) ; URL raw ;
relire le changelog si le résumé a plus de 30 jours.

**orbat-nommage / orbat-historique** : une seule table des échelons réels
(nommage fait foi) ; brigade et réforme ROAD, réformes de 1872-1875, `2d` /
`2nd` (exception USMC), FR-5 sourcés ; URL des sources ; recherche web
obligatoire hors corpus ; paragraphe de concordance des sources.

**Changements de comportement**
- `apply_rename_map.py` n'enrichit plus les titres par défaut (`--titres`).
- `Troop` / `Squadron` ne sont plus traduits d'office (« Troop » donnait
  peloton, faux pour l'US Army) : l'échelon est lu dans le sidc, sinon le nom
  est signalé « à vérifier » (orbat-nommage fait foi).
- Les anciens codes renommés (`BT` Bêtes, `CRS` Croisade, `SEC` Secteur, `ARM`
  Armée, canon `HC`/`LC`/`MC`, `GF` grenade à fusil) ne sont plus reconnus
  dans ces sens.

## 0.25.0 — 2026-10-10 · Fiabilisation des scripts

Étape 1 du plan de mise à niveau (audit d'octobre 2026). Tous les correctifs
ci-dessous sont couverts par `tests/test_orbat_tools.py`
(`python3 -m unittest discover -s tests` depuis la racine du plugin, 36 tests) :
chaque test `test_bug_…` échouait sur la 0.23.0 installée. Revue de code
indépendante + tests aléatoires (3 000 cas) sur la conservation des quantités.

**Aérostats** — réapplication de la 0.24.0 (non installée) : `BL`, `BLC`,
`BLB`, `BLM`, `DR` dans `acronyme/references/aeriens.md`.

**Une seule copie des bibliothèques**
- `orbat_lib.py` / `new_orbat.py` n'existent plus que dans `orbat-json/scripts/`.
  `orbat-xlsx` et `orbat-acronymize` les importent (localisation automatique,
  `ORBAT_TOOLS_ROOT` en repli seulement, si le plugin a été déplacé : elle ne
  peut pas masquer le plugin installé). L'ancienne copie
  `orbat-xlsx/scripts/validate.py`, qui avait perdu les contrôles d'unicité,
  est remplacée par un raccourci vers le validateur unique.
- Une seule table d'échelons (`orbat_lib.ECHELON`) au lieu de trois tables
  divergentes ; noms accentués acceptés (« Armée » faisait planter `build_sidc`).
- Un seul module de légende (`orbat-json/scripts/legends.py`) au format
  canonique `**CODE : Désignation**` (naming.md § 7.3), Équipement / Personnel
  séparés, prose de contexte conservée. Fin des 4 formats concurrents.

**Bugs corrigés**
- `apply_rename_map.py` : la convergence de plusieurs noms vers un même code
  produisait des légendes fausses (« VBTT = VBL » sur un groupe de VAB), des
  lignes et entrées de catalogue en double. Le script fusionne désormais tout
  lui-même, renomme aussi les timelines, et valide son résultat.
- Dates comparées comme du texte (`resource_at`, `position_at`, tri des
  timelines) : `--at 2025-01-01T09:05:00Z` ignorait une perte horodatée
  `…T10:00:00+01:00` (= 09:00Z). Formats acceptés : ISO avec `Z`, `+01:00`
  ou `+0100`, fractions de seconde, sans fuseau (= UTC), epoch ms. Une date
  illisible donne un message clair, plus de trace d'erreur.
- `condense_orbat.py` : timeline des unités fusionnées perdue (désormais
  transférée en `diff` à l'ancêtre, quantités exactes à toute date ; positions
  perdues signalées) ; lignes en double après élémentarisation ; entrées de
  catalogue sans description (table d'éléments incomplète désormais refusée) ;
  champ mobilité (3x/4x/5x) du sidc lu comme un échelon (un échelon `00` non
  renseigné reste fusionnable, comme avant). Un Group de tête (sans sidc) ne
  reçoit pas de timeline : les variations non transférables sont signalées.
- `group_units.py` : identité forcée à « ami » (une compagnie hostile passait
  sous un régiment ami) — reprise des enfants ; `shortName` manquants signalés
  (`new_short_names` disponible) ; « 1ère Compagnie ».
- `add_local_legends.py` écrasait la phrase de contexte ; `add_legends.py`
  rangeait le personnel sous « Équipement : ». Le nettoyage d'une ancienne
  légende ne retire que les lignes dont le code est au catalogue ou a la forme
  d'un acronyme (majuscules/chiffres) : une liste écrite à la main
  (« * Chef = Cne Dupont ») est préservée.
- `apply_rename_map.py` relancé avec un mapping complété conserve les
  légendes de la passe précédente ; une description de catalogue qui nomme
  déjà le matériel (« T-72B3 modernisé ») n'est plus tronquée.
- `apply_relative_visibility.py` : racine invisible en vue d'ensemble pour un
  camp de profondeur ≤ 3 (règle A', format.md) ; ajout de `--dry-run`/`--output`.
- `orbat-xlsx` : `tojson` plantait sur une entité sans classe ; camp créé
  « ami » pour un ORBAT hostile ; descriptions de catalogue génériques (qui
  cassaient `add_legends.py`) ; `validate` ne voyait pas les classes vides ;
  `tojson` valide désormais sa sortie.
- `validate.py` : `--help`, horodatages illisibles en erreur, descriptions de
  catalogue vides en avertissement ; fonction `check()` réutilisable.

**Limites connues (non corrigées, hors périmètre de l'étape 1)**
- Renommer un code en un autre code (`{"VBTT": "VTT"}`) préfixe l'ancien code à
  la description de catalogue (« VBTT — VAB ») au lieu de garder « VAB » en tête :
  corriger la description à la main. Défaut antérieur à la 0.25.0.
- Un `t` illisible est trié en tête de timeline : `aggregate.py --at` et
  `timeline.py` le signalent, `validate.py` le classe en erreur.

**Changement de comportement à connaître**
- `condense_orbat.py` refuse une table `squad_sizes.json` dont un élément n'a
  pas de `description` (Règle 5). Ajouter la description à l'ancienne table.
- La promesse de lecture du XML JTDS est retirée de la description
  d'`orbat-xlsx` : seul le classeur xlsx est lu.

## 0.24.0 — 2026-09-16
Famille aérostats `BL`/`DR` (non installée ; reprise dans la 0.25.0).

## 0.23.0 — 2026-08-30
Armes personnelles (familles `F`/`FM`/`MG`, `FCH`, `P`/`PS`/`PA`).
