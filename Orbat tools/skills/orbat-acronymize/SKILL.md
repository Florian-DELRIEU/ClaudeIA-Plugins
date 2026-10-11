---
name: orbat-acronymize
description: >
  Convertit les noms de véhicules et de personnel d'un ORBAT JSON existant
  (format orbat-mapper.app) en codes du système de nomenclature militaire
  /acronyme (V4). Déclencher IMPÉRATIVEMENT dès que Florian tape
  /orbat-acronymize, fournit un fichier ORBAT JSON et demande de renommer,
  convertir, ou remplacer les noms de véhicules/troupes par leurs acronymes,
  ou formule des demandes comme "convertis cet ORBAT en acronymes v4",
  "remplace les noms de matériel par leurs codes", "acronymise ce fichier",
  "renomme les unités de ce JSON avec le système d'acronymes". S'appuie sur
  les skills orbat (structure du format JSON) et acronyme (système de codes
  et méthode d'identification) — les deux doivent être consultés avant toute
  conversion.
---

# Acronymisation d'un ORBAT existant

## Objectif

Prendre un fichier ORBAT JSON (format `orbat-mapper.app`, voir skill `orbat` /
`references/format.md`) et remplacer les **noms** des entrées des catalogues
`equipment` (véhicules/matériel) et `personnel` (troupes) par leur code du
système `/acronyme` V4, en propageant le changement partout où ces noms sont
référencés dans l'arbre d'unités.

Ce skill ne modifie **que les catalogues et leurs références** — pas les noms
des unités/formations (`Unit.name` / `Unit.shortName`), qui relèvent des
conventions du skill `orbat` (`references/naming.md`), sauf demande explicite
de Florian en ce sens.

## Pipeline

1. **Localiser le fichier.** Si Florian n'a pas donné de chemin, demander le
   fichier ORBAT JSON à traiter.

2. **Lire les catalogues racine** `equipment` et `personnel` du fichier
   (liste de `{name, description}` — voir skill `orbat`, `references/format.md`,
   section "Enveloppe (racine)"). Ce sont les `name` de ces catalogues qu'il
   faut convertir — pas les noms d'unités.

3. **Pour chaque nom de catalogue, déterminer son code v4** en suivant le
   skill `acronyme` :
   - Consulter d'abord `acronyme/identification/lexique.json` (registre
     désignation réelle ↔ code v4) — réutiliser un code existant si le même
     matériel/châssis y figure déjà (cohérence inter-fichiers, règle P5 de
     `METHODE.md`).
   - Sinon, appliquer le pipeline en 6 étapes de
     `acronyme/identification/METHODE.md` : châssis → Type
     (`identification/chassis-types.md`), rôle/armement → suffixes, gabarit,
     fusions, décisions établies (`acronyme/SKILL.md`).
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
   fichier temporaire, puis lancer le script. Il fait trois choses :

   a. **Renomme les entrées de catalogue** (en conservant l'ancien nom dans
      leur `description` pour traçabilité) et propage le renommage à toutes
      les références `equipment[].name` / `personnel[].name` dans tout
      l'arbre d'unités (`sides[].groups[].subUnits`, récursif).

   b. **Annote la `description` de chaque échelon** avec une légende de tous
      les acronymes présents dans son sous-arbre, pour ne jamais perdre le
      nom réel derrière un code — ex. `Équipement : MBT-105 = Char Leclerc ·
      VTT = VAB`. Un échelon de tête (régiment, groupe) affichera ainsi la
      légende complète de tout son matériel/personnel ; un échelon feuille
      n'affichera que le sien.

   c. **Enrichit le titre des échelons à composition de matériel non
      mixte** : si un échelon ne porte, EN PROPRE, qu'un seul type de
      véhicule (`equipment`, jamais `personnel` — un titre du style
      "Compagnie d'Infanterie de Fantassin" serait tautologique), son `name`
      est complété avec le nom réel du véhicule, ex. `"Escadron"` →
      `"Escadron de VAB"`. Sans effet sur un échelon mixte (plusieurs types
      de matériel) ou purement organisationnel (sans matériel en propre).

   Comportement idempotent : relancer le script sur un fichier déjà traité ne
   duplique ni les légendes ni les suffixes de titre.

   **Le script écrase le fichier d'origine par défaut** (comportement voulu :
   pas de copie séparée) — utiliser `--dry-run` d'abord si Florian veut un
   aperçu, `--output` s'il demande une copie séparée pour ce fichier précis,
   ou `--no-legend` / `--no-titles` pour désactiver l'une des deux
   annotations.

6. **Journaliser les nouveaux codes résolus** dans
   `acronyme/identification/lexique.json` (ajouter les paires
   désignation réelle ↔ code v4 nouvellement tranchées), pour que les
   prochains ORBAT réutilisent les mêmes codes (règle P5).

7. **Valider le fichier résultant** avec le script du skill `orbat` :
   ```
   python3 ../orbat/scripts/validate.py <orbat.json>
   ```
   (adapter le chemin relatif selon l'emplacement des skills installés).
   Corriger avant de considérer la tâche terminée si la validation échoue.

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
  vers les conventions `orbat/references/naming.md` (règle 4, table de
  traduction des échelons) — c'est un renommage de nature différente
  (échelon d'organisation, pas matériel/personnel).
