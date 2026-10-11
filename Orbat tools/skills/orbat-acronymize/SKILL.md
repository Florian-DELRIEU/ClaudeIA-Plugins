---
name: orbat-acronymize
description: "Convertit les noms de véhicules et de personnel d'un ORBAT JSON existant (format orbat-mapper.app) en codes du système de nomenclature militaire /acronyme (V4). Déclencher IMPÉRATIVEMENT dès que Florian tape /orbat-acronymize, fournit un fichier ORBAT JSON et demande de renommer, convertir, ou remplacer les noms de véhicules/troupes par leurs acronymes, ou formule des demandes comme \"convertis cet ORBAT en acronymes v4\", \"remplace les noms de matériel par leurs codes\", \"acronymise ce fichier\", \"renomme les unités de ce JSON avec le système d'acronymes\". S'appuie sur les skills orbat (structure du format JSON) et acronyme (système de codes et méthode d'identification) — les deux doivent être consultés avant toute conversion.\n"
---

# Acronymisation d'un ORBAT existant

## Objectif

Prendre un fichier ORBAT JSON (format `orbat-mapper.app`, voir skill `orbat-json` /
`references/format.md`) et remplacer les **noms** des entrées des catalogues
`equipment` (véhicules/matériel) et `personnel` (troupes) par leur code du
système `/acronyme` V4, en propageant le changement partout où ces noms sont
référencés dans l'arbre d'unités.

Ce skill ne modifie **que les catalogues et leurs références** — pas les noms
des unités/formations (`Unit.name` / `Unit.shortName`), qui relèvent des
conventions du skill `orbat-json` (`references/naming.md`), sauf demande explicite
de Florian en ce sens.

## Pipeline

1. **Localiser le fichier.** Si Florian n'a pas donné de chemin, demander le
   fichier ORBAT JSON à traiter.

2. **Lire les catalogues racine** `equipment` et `personnel` du fichier
   (liste de `{name, description}` — voir skill `orbat-json`, `references/format.md`,
   section "Enveloppe (racine)"). Ce sont les `name` de ces catalogues qu'il
   faut convertir — pas les noms d'unités.

3. **Pour chaque nom de catalogue, déterminer son code v4** en suivant le
   skill `acronyme` :
   - **Déterminer d'abord si la source est du matériel réel ou un univers fictif**
     (Warhammer 40,000, Cosmotter…). Consulter en priorité le lexique correspondant :
     `acronyme/identification/lexique.json` pour le matériel réel, ou
     `acronyme/identification/lexique-40k.json` pour un univers fictif — réutiliser un
     code existant si le même matériel/châssis y figure déjà (cohérence inter-fichiers,
     règle P5 de `METHODE.md`). **Ne jamais mélanger les deux lexiques** : certains
     codes (ex. `VB`) portent un sens différent selon le contexte (voir
     `chassis-types.md`, décision « VBCI vs VB — rôle combattant vs soutien »).
   - Sinon, appliquer le pipeline en 6 étapes de
     `acronyme/identification/METHODE.md` : châssis → Type
     (`identification/chassis-types.md`), rôle/armement → suffixes, gabarit,
     fusions, décisions établies (`acronyme/SKILL.md`).
   - **Attention châssis partagé combat/soutien** : quand plusieurs variantes
     d'entrée de catalogue partagent le même châssis (ex. plusieurs véhicules dérivés
     d'un même transport de troupes), vérifier laquelle combat réellement aux côtés
     d'une escouade (garde le Type de combat complet, ex. `VBCI`/`VBTT`) et lesquelles
     sont des variantes de soutien non-combattantes (sanitaire, dépannage, génie/
     logistique, artillerie, mortier, AA automoteur — dégradent vers `VB` générique,
     voir `chassis-types.md`). Ne jamais appliquer le Type de combat à une variante de
     soutien par simple réflexe de cohérence de châssis.
   - Pour le personnel, utiliser `acronyme/identification/personnel.md`
     (échelon escouade/équipe/binôme + rôle dominant).
   - Ne jamais deviner sans consulter ces fichiers — le principe du châssis
     (une même plateforme garde le même Type à travers ses variantes) est
     fréquemment source d'erreur si on code "à l'oreille".

4. **Construire le mapping** `{nom_original: code_v4}` et le présenter à
   Florian sous forme de tableau (nom d'origine → code proposé → brève
   justification) avant d'écrire quoi que ce soit. Signaler les cas ambigus
   (plusieurs codes défendables) plutôt que de trancher silencieusement.

5. **Appliquer le mapping** avec le script fourni :
   ```
   python3 scripts/apply_rename_map.py <orbat.json> <mapping.json>
   ```
   Écrire d'abord `mapping.json` (le mapping validé à l'étape 4) dans un
   fichier temporaire, puis lancer le script. Il fait quatre choses :

   a. **Renomme les entrées de catalogue** (en conservant l'ancien nom en tête
      de leur `description`, naming.md Règle 5) et propage le renommage à toutes
      les références de l'arbre : `equipment[].name` / `personnel[].name` **et**
      les `update`/`diff` des timelines `state[]`.
      **Convergence gérée** : si plusieurs noms d'origine partent vers le même
      code (deux camions → `VU-LOG`), le script fusionne lui-même — une entrée
      de catalogue (`"Camion A / Camion B"`), une ligne par unité à quantité
      cumulée, timelines réexprimées en deltas pour que les quantités restent
      exactes à toute date. Il affiche la liste des codes fusionnés.

   b. **Annote la `description` de chaque échelon** avec la légende canonique
      (`**CODE : Désignation réelle**`, Équipement / Personnel séparés, module
      `orbat-json/scripts/legends.py`) des codes présents dans son sous-arbre.
      Un échelon ne cite que les désignations **réellement présentes** chez lui :
      un groupe qui n'a que des VAB affiche `**VBTT : VAB**`, même si `VBTT`
      couvre aussi des VBL ailleurs. La phrase de contexte déjà présente dans la
      `description` est conservée.

   c. **Enrichit le titre des échelons à composition de matériel non
      mixte** : si un échelon ne porte, EN PROPRE, qu'un seul type de
      véhicule (`equipment`, jamais `personnel` — un titre du style
      "Compagnie d'Infanterie de Fantassin" serait tautologique), son `name`
      est complété avec le nom réel du véhicule, ex. `"Escadron"` →
      `"Escadron de VAB"`. Sans effet sur un échelon mixte (plusieurs types
      de matériel, ou un code qui regroupe plusieurs désignations) ou purement
      organisationnel (sans matériel en propre).

   d. **Valide le résultat** (mêmes contrôles que `orbat-json/scripts/validate.py`)
      et affiche le rapport ; code de sortie 1 s'il reste une erreur.

   Comportement idempotent : relancer le script sur un fichier déjà traité ne
   duplique ni les légendes ni les suffixes de titre.

   Le script importe les modules partagés du skill `orbat-json` (même plugin),
   localisés automatiquement ; si le plugin a été copié ailleurs, définir
   `ORBAT_TOOLS_ROOT` sur sa racine.

   **Le script écrase le fichier d'origine par défaut** (comportement voulu :
   pas de copie séparée) — utiliser `--dry-run` d'abord si Florian veut un
   aperçu, `--output` s'il demande une copie séparée pour ce fichier précis,
   ou `--no-legend` / `--no-titles` pour désactiver l'une des deux
   annotations.

6. **Journaliser les nouveaux codes résolus** dans le lexique approprié —
   `acronyme/identification/lexique.json` pour du matériel réel,
   `acronyme/identification/lexique-40k.json` pour un univers fictif (ajouter les
   paires désignation réelle ↔ code v4 nouvellement tranchées), pour que les
   prochains ORBAT réutilisent les mêmes codes (règle P5).

7. **Lire le rapport de validation** affiché par le script (étape 5 d) : 0 erreur
   attendue. Toute retouche manuelle ultérieure se revalide avec
   `python3 ../orbat-json/scripts/validate.py <orbat.json>`.

   > 🔴 **La convergence de codes reste le piège n°1** (deux modèles de camion →
   > `VU-LOG`). Depuis octobre 2026, `apply_rename_map.py` fusionne lui-même les
   > lignes et le catalogue ; mais une correction **à la main** après coup peut
   > réintroduire deux lignes du même code — `validate.py` le détecte. **Ne
   > jamais livrer une conversion sans rapport de validation à 0 erreur.**

8. **Résumer** à Florian : nombre d'entrées renommées, nombre de références
   propagées, nouveaux codes ajoutés au lexique, résultat de la validation.

## Points d'attention

- Un même `name` de catalogue peut être référencé par de nombreuses unités à
  travers l'arbre — c'est pour ça que le renommage passe toujours par le
  script plutôt qu'un remplacement manuel unité par unité.
- Ne jamais renommer une entrée de catalogue qui porte déjà un code v4
  valide (déjà acronymisée) — vérifier via un motif simple (présence de
  séparateurs `-`/`/`/`.` typiques du système) avant de la mettre dans le
  mapping proposé.
- Si Florian veut aussi convertir les noms d'unités/formations (`Unit.name`),
  le signaler comme hors du périmètre par défaut de ce skill et rediriger
  vers les conventions `orbat-json/references/naming.md` (règle 4, table de
  traduction des échelons) — c'est un renommage de nature différente
  (échelon d'organisation, pas matériel/personnel).
