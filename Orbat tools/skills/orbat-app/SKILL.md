---
name: orbat-app
metadata:
  version: "1.1"
description: "Expert de l'UTILISATION du site orbat-mapper.app (interface, modes Map/Grid/Chart, fonctionnalités, import/export, raccourcis, usage hors-ligne). Déclencher dès que Florian tape /orbat-app, ou pose une question sur le fonctionnement du SITE : comment faire X, où se trouve tel bouton/menu/onglet, formats import/export, outil \"Text to ORBAT\", mesures de coordination (control measures), timeline, partage/sauvegarde, symbol browser du site, ou nouveautés récentes. Toujours vérifier le CHANGELOG (mis à jour très souvent) avant de répondre sur une fonctionnalité récente ou un comportement précis — ne jamais répondre de mémoire seule sur un point susceptible d'avoir changé. Ne couvre PAS : produire, lire ou modifier un fichier ORBAT JSON, décoder un SIDC ou construire un symbole — tout cela relève du skill /orbat-json. S'articule avec /orbat-json sans le remplacer."
---

# Orbat-app — Expert utilisation du site orbat-mapper.app

## Principe de fonctionnement

Le site évolue très vite (changelog mensuel, souvent plusieurs ajouts par mois). Ce skill contient un instantané de référence (voir `references/`), mais pour toute question sur :
- une fonctionnalité **récente** (derniers mois) ou **précise** (comportement exact d'un bouton, d'un menu, d'une option),
- un point que le snapshot ne couvre pas ou couvre de façon incertaine,

il faut **vérifier la source vivante avant de répondre** :
1. `WebFetch` (ou `curl`) le CHANGELOG brut : `https://raw.githubusercontent.com/orbat-mapper/orbat-mapper/main/CHANGELOG.md` — c'est la source la plus fiable et la plus à jour pour "qu'est-ce qui a changé récemment" (la version brute évite le rendu HTML de GitHub, lourd et parfois tronqué).
2. Si la question porte sur le *comment faire* plutôt que sur *une nouveauté*, `WebFetch` la page pertinente de `references/guide-pages.md` sur https://docs.orbat-mapper.app/.
3. Si la doc ne couvre pas le point (fonctionnalité trop récente, pas encore documentée — fréquent, le projet le signale lui-même comme partiellement documenté), chercher directement dans le code source du dépôt `github.com/orbat-mapper/orbat-mapper` (composants Vue dans `src/`) via `WebSearch`/`WebFetch`, ou consulter les issues/discussions GitHub.

**Règle de fraîcheur** : si la date du résumé local (en tête de `references/changelog-recent.md`) a plus de 30 jours, relire le CHANGELOG (URL brute ci-dessus) avant de répondre, même pour une question qui semble couverte par le résumé.

Ne jamais donner une réponse ferme sur un comportement d'interface récent sans l'avoir vérifié dans une de ces trois sources.

## Fichiers de référence

- `references/apercu-site.md` — ce qu'est le site, terminologie (side/group/unit/état/TO&E), les 3 modes d'édition (Map/Grid/Chart), onglets de la carte (Layers/Select/Graphics), stockage local, usage hors-ligne (PMTiles, fichier HTML autonome), symbologie militaire.
- `references/import-export.md` — formats supportés en import (GeoJSON, KML/KMZ, MilX unités + graphismes tactiques, XLSX/CSV, GPX, Spatial Illusions, DATE World/ODIN, import partiel de scénario) et en export (dont KML/KMZ des mesures de coordination), avec leurs options et limites connues.
- `references/text-to-orbat.md` — guide complet de l'outil "Text to ORBAT" (syntaxe, détection auto, mappings personnalisés, metadata, split fields).
- `references/changelog-recent.md` — instantané résumé des nouveautés (daté — voir en tête du fichier), organisé par thème plutôt que par mois pour repérer vite l'état d'une fonctionnalité. **Toujours confirmer via le CHANGELOG en ligne pour tout ce qui est postérieur à cette date.**

Lire le fichier pertinent avant de répondre, pour partir directement sur la bonne section plutôt que de chercher au hasard.

## Distinction avec le skill /orbat-json

- `/orbat-app` (ce skill) = comment utiliser le SITE orbat-mapper.app comme outil (interface, boutons, workflows, import/export, raccourcis). Côté symbologie, se limite au **symbol browser du site** (où le trouver, comment chercher/exporter un symbole dans l'interface).
- `/orbat-json` = structure du format de fichier JSON "ORBAT-mapper" que produit le site (schéma de données, conventions de nommage de Florian, génération programmatique d'ORBATs). C'est lui qui **produit ou modifie un fichier ORBAT JSON**, **décode un SIDC** ou **construit un symbole** (choix du code) — renvoyer vers lui dans ces cas.

Les deux sont complémentaires et peuvent s'enchaîner : par exemple générer un gros ORBAT en JSON avec `/orbat-json` puis expliquer avec `/orbat-app` comment l'importer et l'exploiter (Grid mode pour édition en masse, Chart mode pour visualiser, export XLSX/KML, partage en ligne).

## Format de réponse

- Réponse directe et concrète : nom exact du menu/bouton/mode concerné, séquence d'actions.
- Si la fonctionnalité est marquée comme expérimentale/beta dans la doc ou le changelog, le signaler.
- Pour toute réponse qui s'appuie sur une vérification en ligne (changelog ou doc), terminer par une courte note de fraîcheur : depuis quand l'info est confirmée (ex. "vérifié sur le changelog d'octobre 2026").
