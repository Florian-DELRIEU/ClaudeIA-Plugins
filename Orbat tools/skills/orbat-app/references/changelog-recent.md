# Instantané changelog — état au 28 juillet 2026

Source complète et toujours à jour : https://github.com/orbat-mapper/orbat-mapper/blob/main/CHANGELOG.md
⚠️ Ce fichier est un résumé thématique figé à la date ci-dessus. Pour toute question sur "la dernière nouveauté" ou un comportement très récent, refaire un `web_fetch` du changelog en ligne — il est mis à jour quasi tous les mois.

## Grandes tendances récentes (2026)

- **MapLibre devient le mode carte par défaut** (mai 2026), en remplacement progressif d'OpenLayers. Portage progressif des fonctionnalités : dessin/mesure/snapping, KML, sélection multiple, rotation des symboles, export image haute qualité avec viewfinder configurable, calques raster/image, globe 3D expérimental, terminateur jour/nuit avec zones de crépuscule, animation de la timeline compatible.
- **ORBAT en tant que sidebar redimensionnable** (plus un simple overlay carte) depuis mars 2026 — la carte se redimensionne physiquement.
- **Sauvegarde hybride** (mars 2026) : Save scenario = sauvegarde explicite ; autosave = brouillons de récupération ; alerte seulement sur changements non sauvegardés.
- **Support des ORBAT variant dans le temps** (time-varying ORBATs) — mars 2026.
- **Text to ORBAT** énormément enrichi entre fév.-mars 2026 (voir `text-to-orbat.md` — mappings custom, priorités, short names, split fields, presse-papier/drag&drop).
- **Import générique tableur (CSV/TSV)** avec mapping de champs custom — fév. 2026.
- **Symbol browser en page dédiée** `/symbol-browser` (avril 2026), export symboles PNG/SVG.
- **Recovery drafts** et actions "Revert to opened state"/"Revert to saved version" — avril 2026.

## Repères par mois (résumé, non exhaustif)

- **Juin 2026** : bouton copier-coller l'export carte MapLibre directement dans le presse-papier (PNG).
- **Mai 2026** : outil rectangle pour le dessin, toggle "ajout multiple" sur la toolbar de dessin, désactivation des trajets géodésiques en mode Mercator, KML expérimental en MapLibre, calques raster/image en MapLibre, export image carte haute qualité avec viewfinder — **MapLibre devient le mode par défaut**.
- **Avril 2026** : snapping en MapLibre, planification d'itinéraire avec obstacles, coller du GeoJSON depuis le presse-papier (Ctrl/Cmd+V), import GPX, dessin/modification de features en MapLibre, mesures en MapLibre, statistiques de géométrie, vue détails en lecture seule pour features KML/KMZ cliquées, contraintes de vue (étendue max, zoom min/max) sauvegardées dans le scénario, mode MapLibre expérimental avec globe, page symbol-browser dédiée, "Copy as GeoJSON", short name auto dans le formulaire d'unité, suppression multiple des scénarios stockés, tri asc/desc dans le navigateur de scénarios stockés, recovery drafts.
- **Mars 2026** : ORBATs variant dans le temps, recherche/filtrage dans le navigateur de scénarios, taille de symbole custom par unité, gros enrichissement Text to ORBAT (voir fichier dédié), panneau ORBAT passé en sidebar flex, drag-and-drop ORBAT corrigé (unité sélectionnée utilisable comme cible de drop).
- **Février 2026** : colonnes redimensionnables + virtualisation en Grid mode, drag-and-drop d'unités ORBAT entre onglets/fenêtres différents, icônes custom pour export KMZ, action "Collapse"/"Expand units"/"Collapse units" sur le menu contextuel des unités et side/side-group, panneau resizable mobile, section "Map Visibility" dans le panneau de filtres, rotation de symbole "timeline-aware", mode dessin freehand, UI pour définir la bounding box du scénario, import tableur générique CSV/TSV, section "Recently Shared" (File menu), bouton "Share Scenario" dans la toolbar, export CSV/TSV avec séparateur configurable, abréviations d'échelon concaténées en Text to ORBAT (`2bn`, `1bde`), action "Move up in hierarchy". Suppression du label "beta" de l'appli.
- **Janvier 2026** : "Paste scenario from clipboard" (page d'accueil + éditeur), pointes de flèche début/fin sur les lignes, scénarios chiffrés/protégés par mot de passe (export/import/partage en ligne), masquage de features individuelles, fuseaux horaires militaires.

## Fonctionnalités plus anciennes mais structurantes (2023-2025, toujours en place)

- Grid edit mode (tableur), Chart edit mode (organigramme) — les deux encore listés comme "fonctionnalité limitée / en développement" dans la doc officielle.
- Range rings (cercles de portée), groupés avec fusion si superposition.
- Symboles custom (icône + couleur de remplissage).
- Verrouillage (lock) de side/group/unit contre modifications accidentelles.
- Import DATE World (ODIN, US Army), Spatial Illusions ORBAT Builder (import + export), Order of Battle Generator.
- Export KML/KMZ, GeoJSON, XLSX, MilX (partiel), symboles PNG/SVG.
- Statuts d'unité, attribut disponible/en dotation (available/on hand) pour équipement et personnel.
- Timeline avec playback, raccourcis clavier dédiés (Alt+P ou K play/pause, `<`/`>` vitesse).
- Depuis sept. 2025 : les unités peuvent être ajoutées directement à un side, sans passer par un group.

## Pour aller plus loin

- Discussions GitHub (idées / retours des devs sur les choix de conception) : https://github.com/orbat-mapper/orbat-mapper/discussions
- Issues ouvertes (bugs connus / fonctionnalités en cours) : https://github.com/orbat-mapper/orbat-mapper/issues
