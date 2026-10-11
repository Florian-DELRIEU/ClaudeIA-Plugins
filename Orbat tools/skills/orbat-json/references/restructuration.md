# Restructuration d'un ORBAT — Tâches 7, 8, 9

Procédures détaillées des trois tâches de restructuration du skill `orbat-json`
(sorties de `SKILL.md` en octobre 2026 pour l'alléger). Elles opèrent sur un ORBAT
JSON existant et **écrasent le fichier d'origine par défaut** (`--dry-run` pour un
aperçu, `--output` pour une copie). Toute restructuration se termine par
`validate.py` **puis** le contrôle de conformité à la source (`naming.md` Règle 8,
`scripts/conformite.py`) : une fusion ou un regroupement est une modification qui
peut fausser des totaux.

---

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
   unité (position 9-10 = échelon, voir `sidc.md`). Sans `sidc`
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
   Les codes d'élément (`SQ-INF`, `GRP-INF`…) viennent de `orbat-tools:acronyme`
   comme tout acronyme (règle de source unique, `SKILL.md`).

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

   ⚠️ Chaque élément (et `_command_group`) **doit** avoir une `description`
   nommant l'élément réel : elle devient l'entrée de catalogue (naming.md
   Règle 5). Le script refuse une table incomplète, sans rien écrire.

4. **Appliquer avec le script fourni** :
   ```
   python3 scripts/condense_orbat.py <orbat.json> <squad_sizes.json> --target peloton
   ```
   Le script fait les deux passes dans l'ordre (condensation puis
   élémentarisation) et écrase le fichier d'origine par défaut — `--dry-run`
   pour un aperçu, `--output` pour une copie séparée, `--no-condense` /
   `--no-elementize` pour n'appliquer qu'une seule des deux passes. Il
   transfère la timeline des unités fusionnées et fusionne les lignes de même
   code (`orbat_lib.merge_items`).

5. **Présenter le résumé** à Florian : nombre d'unités avant/après, nombre
   d'échelons fusionnés, variations de timeline transférées à l'ancêtre et
   **entrées de timeline perdues** (positions/statuts des unités fusionnées, que
   l'ancêtre ne peut pas porter), nouveaux codes de catalogue ajoutés (les éléments),
   et surtout la liste des **reliquats** (effectifs qui ne rentrent dans
   aucun palier d'élément) — ce sont typiquement des sections de commandement
   à effectif réduit (2-4 pax) plutôt qu'une vraie escouade ; à confirmer avec
   Florian si ça doit rester en comptage brut ou être reclassé.

6. **Valider le fichier résultant** : `python3 scripts/validate.py <orbat.json>`,
   puis contrôle de conformité (Règle 8 ; `scripts/conformite.py`). Relancer
   ensuite `add_legends.py` ou `add_local_legends.py` (`SKILL.md` Tâche 4, étape 6)
   si la condensation a changé la composition des feuilles — les légendes existantes
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

---

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
   défaut — passer `"entity"` explicitement dans la spec sinon), et **identité
   (ami/hostile…), contexte et symbol set repris des enfants** (avertissement si
   ceux d'un même paquet divergent). `"new_short_names"` (liste) pose les
   `shortName` (naming.md Règles 2 et 7.5) ; à défaut le script liste les groupes à
   compléter — `scripts/short_names.py` peut alors les générer. Les enfants
   sélectionnés sont déplacés tels quels (avec tout leur sous-arbre) sous la
   nouvelle unité, à la place qu'occupait le premier d'entre eux ; les
   enfants non sélectionnés du parent restent inchangés à leur position.
   Écrase le fichier d'origine par défaut (`--output` / `--dry-run`
   disponibles comme les autres scripts).

4. **Valider** avec `python3 scripts/validate.py <orbat.json>` (puis contrôle de
   conformité, Règle 8), et relancer `add_legends.py`/`add_local_legends.py` si
   Florian veut des légendes à jour sur les nouveaux échelons créés (ils n'ont pas
   de matériel en propre, donc pas de légende tant qu'aucune passe n'est relancée
   dessus).

---

## Tâche 9 — Visibilité cartographique par profondeur relative (zoom sémantique)

Remplace l'ancien classement par nom d'échelon : le critère est la **profondeur dans
l'arbre** de chaque camp (nombre de parents), rapportée à une échelle de référence
commune fixe (`R = 5` bandes, bornes `[0, 10, 13, 16, 18, 24]`, à ne changer que sur
demande explicite de Florian). Détail complet de la règle (formule, arrondi, règles A,
A' et B de comblement) dans `format.md` section `style.limitVisibility`.

1. `python3 scripts/apply_relative_visibility.py <orbat.json>` — traite chaque camp du
   fichier indépendamment avec sa propre profondeur `D`, applique `style.limitVisibility`
   + `minZoom`/`maxZoom` à **toutes** les unités, écrase le fichier en place
   (`--dry-run` pour voir les bandes d'abord, `--output` pour une copie).
2. Toujours enchaîner avec `python3 scripts/validate.py <orbat.json>`.
3. Livrer le fichier avec `present_files`, en rappelant les bandes obtenues par camp
   (le script les affiche sur stdout).
