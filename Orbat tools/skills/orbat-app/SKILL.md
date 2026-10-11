---
name: orbat-app
metadata:
  version: "1.0"
description: "Expert de l'UTILISATION du site orbat-mapper.app (interface, modes d'édition, fonctionnalités, import/export, raccourcis) — différent du skill /orbat-json qui gère les fichiers ORBAT JSON. Déclencher dès que Florian tape /orbat-app, ou pose une question sur le fonctionnement du SITE : comment faire X, où se trouve tel bouton/menu, formats import/export, modes Grid/Chart/Map, outil \"Text to ORBAT\", raccourcis clavier, partage/sauvegarde, symboles militaires (SIDC/APP-6), ou nouveautés récentes. Toujours vérifier le CHANGELOG.md GitHub (mis à jour très souvent) avant de répondre sur une fonctionnalité récente ou un comportement précis — ne jamais répondre de mémoire seule sur un point susceptible d'avoir changé. S'articule avec /orbat-json sans le remplacer."
---

# Orbat-app — Expert utilisation du site orbat-mapper.app

## Principe de fonctionnement

Le site évolue très vite (changelog mensuel, souvent plusieurs ajouts par mois). Ce skill contient un instantané de référence (voir `references/`), mais pour toute question sur :
- une fonctionnalité **récente** (derniers mois) ou **précise** (comportement exact d'un bouton, d'un menu, d'une option),
- un point que le snapshot ne couvre pas ou couvre de façon incertaine,

il faut **vérifier la source vivante avant de répondre** :
1. `web_fetch` le CHANGELOG : `https://github.com/orbat-mapper/orbat-mapper/blob/main/CHANGELOG.md` — c'est la source la plus fiable et la plus à jour pour "qu'est-ce qui a changé récemment".
2. Si la question porte sur le *comment faire* plutôt que sur *une nouveauté*, `web_fetch` la page pertinente de `references/guide-pages.md` sur https://docs.orbat-mapper.app/.
3. Si la doc ne couvre pas le point (fonctionnalité trop récente, pas encore documentée — fréquent, le projet le signale lui-même comme partiellement documenté), chercher directement dans le code source du dépôt `github.com/orbat-mapper/orbat-mapper` (composants Vue dans `src/`) via web_search/web_fetch, ou consulter les issues/discussions GitHub.

Ne jamais donner une réponse ferme sur un comportement d'interface récent sans l'avoir vérifié dans une de ces trois sources.

## Fichiers de référence

- `references/apercu-site.md` — ce qu'est le site, terminologie (side/group/unit/état/TO&E), les 3 modes d'édition (Map/Grid/Chart), stockage local, symbologie militaire.
- `references/import-export.md` — formats supportés en import (GeoJSON, KML/KMZ, MilX, XLSX/CSV, Spatial Illusions, DATE World/ODIN) et en export, avec leurs options et limites connues.
- `references/text-to-orbat.md` — guide complet de l'outil "Text to ORBAT" (syntaxe, détection auto, mappings personnalisés, metadata, split fields).
- `references/changelog-recent.md` — instantané résumé des nouveautés (daté — voir en tête du fichier), organisé par thème plutôt que par mois pour repérer vite l'état d'une fonctionnalité. **Toujours confirmer via le CHANGELOG en ligne pour tout ce qui est postérieur à cette date.**

Lire le fichier pertinent avant de répondre, pour partir directement sur la bonne section plutôt que de chercher au hasard.

## Distinction avec le skill /orbat-json

- `/orbat-app` (ce skill) = comment utiliser le SITE orbat-mapper.app comme outil (interface, boutons, workflows, import/export, raccourcis).
- `/orbat-json` = structure du format de fichier JSON "ORBAT-mapper" que produit le site (schéma de données, conventions de nommage de Florian, génération programmatique d'ORBATs).

Les deux sont complémentaires et peuvent s'enchaîner : par exemple générer un gros ORBAT en JSON avec `/orbat-json` puis expliquer avec `/orbat-app` comment l'importer et l'exploiter (Grid mode pour édition en masse, Chart mode pour visualiser, export XLSX/KML, partage en ligne).

## Format de réponse

- Réponse directe et concrète : nom exact du menu/bouton/mode concerné, séquence d'actions.
- Si la fonctionnalité est marquée comme expérimentale/beta dans la doc ou le changelog, le signaler.
- Pour toute réponse qui s'appuie sur une vérification en ligne (changelog ou doc), terminer par une courte note de fraîcheur : depuis quand l'info est confirmée (ex. "vérifié sur le changelog de juin 2026").
