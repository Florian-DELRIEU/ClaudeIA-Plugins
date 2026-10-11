# Historique des décisions ORBAT (symbologie, conformité, source unique)

> Provenance : entrées datées déplacées le 2026-10-10 depuis `skills/acronyme/decisions.md` § 6 (scission du journal) — elles concernent `orbat-json`, la symbologie et la conformité des ORBAT, pas le système d'acronymes ; texte conservé verbatim.

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
