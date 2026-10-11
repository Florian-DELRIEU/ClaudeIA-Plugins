# Aperçu du site orbat-mapper.app

Sources : https://docs.orbat-mapper.app/guide/about-orbat-mapper, /terminology, /military-symbology, /editing-modes, /storage, /map-edit-mode, /offline-use + CHANGELOG (relu le 2026-10-10)
Dépôt : https://github.com/orbat-mapper/orbat-mapper (projet perso/hobbyiste, PAS un outil C2IS/simulation/planification militaire pro)

## Ce que c'est

Application web **100% côté client** (aucun serveur, tout est stocké sur l'ordinateur de l'utilisateur, dans l'IndexedDB du navigateur par défaut). Permet de :
- construire des ordres de bataille (ORBAT) avec drag-and-drop,
- visualiser les hiérarchies d'unités en organigramme (Chart mode),
- positionner les unités sur une carte et animer leurs déplacements dans le temps (dimension temporelle = fonctionnalité phare, différenciante),
- chercher/prévisualiser/exporter des symboles militaires (PNG/SVG),
- parser du texte en hiérarchie d'unités automatiquement (Text to ORBAT),
- éditer en mode tableur (Grid mode),
- dessiner des entités cartographiques et mesurer distances/surfaces,
- dessiner des **mesures de coordination** (control measures / graphismes tactiques : flèches d'attaque, limites, zones, tâches… — depuis août 2026, onglet **Graphics** depuis oct. 2026),
- importer/exporter GeoJSON, KML/KMZ, MilX, XLSX, CSV.

Moteur de carte : **MapLibre uniquement** depuis septembre 2026 (l'ancien mode OpenLayers a été supprimé ; les anciens liens ouvrent la vue MapLibre). Globe, relief 3D/ombrage, grilles MGRS et lat/long disponibles.

L'interface n'est pas optimisée mobile (préconisé : ordinateur/laptop).

## Terminologie clé

- **Scenario** : le fichier de travail (.json), contient des unités organisées en **sides**.
- **Side** : typiquement une nation/coalition. Possède une **standard identity / affiliation** (friend/neutral/hostile/couleur custom) qui détermine couleur+forme des symboles.
- **Group** : sous-organisation à l'intérieur d'un side, purement pour ranger les unités (un side peut avoir des unités directement, sans groupe, depuis sept. 2025).
- **Unit** : l'élément de base, composé de personnel + équipement = **TO&E** (Table of Organization and Equipment). Support basique du TO&E côté données.
- **State (état)** : valeurs courantes des attributs d'une unité (position, statut...) qui évoluent dans le temps — c'est ce qui alimente la timeline/playback.
- **Map / layers** : la carte a plusieurs couches ; la couche de base est dessinée en premier.
- Modèle de données inspiré (de loin) du **MSDL** (Military Scenario Definition Language).

## Symbologie militaire

- Basée sur **MIL-STD 2525D** et **NATO APP-6D** (rendu via la librairie Milsymbol), au choix entre les deux standards à la création du scénario.
- SIDC (Symbol Identification Code) = code à 20 chiffres. Pas besoin de le manipuler à la main en usage normal.
- Support de la conversion des anciens **codes SIDC alphabétiques** (2525C/APP-6C) vers le numérique (2525D/APP-6D) via la lib `convert-symbology`.
- APP-6D a un jeu de symboles supplémentaire pour l'individu débarqué (dismounted individual) absent en 2525D.
- Symboles personnalisés possibles (icônes custom, couleurs de remplissage custom) si les symboles standards ne suffisent pas.
- Page dédiée : **symbol browser** à `/symbol-browser` (recherche, aperçu, export PNG/SVG avec options de taille/affichage).

## Les 3 modes d'édition (à changer selon la tâche)

Accessible via le sélecteur de mode dans la barre de navigation (menu déroulant sur mobile).

1. **Map mode** — mode principal, focalisé sur la position des unités sur la carte. Contient : barre de navigation, panneau ORBAT (sidebar redimensionnable, plus un simple overlay — a été déplacé en flex sidebar en 2026), la carte, panneau de détails, barre d'outils carte (dessin : mesures de coordination épinglées, formes, options), timeline (avec panneau **Unit changes** depuis oct. 2026, bouton Changes ou touche `h`). Onglets de la sidebar d'outils notamment **Layers**, **Select** (ex-**Filters**, renommé en sept. 2026 : sélection d'unités par catégorie, mode Add/Narrow, Hide/Show), **Graphics** (catalogue des control measures, oct. 2026) et **Settings** — ordre et contenu à vérifier dans le changelog si la question est précise.
2. **Grid mode** — édition façon tableur, rapide pour éditer beaucoup d'unités/équipement d'un coup (colonnes redimensionnables, virtualisation pour les gros ORBATs, filtrage, navigation clavier). Fonctionnalité encore limitée/en développement.
3. **Chart mode** — visualisation en organigramme hiérarchique, zoom/pan, sélection de l'unité racine par recherche, export en plusieurs formats papier. Fonctionnalité encore limitée/en développement.

## Barre de navigation (Map mode)

Contient : menu File (sauvegarde/chargement/import/export), nom du scénario, menu playback, aide+recherche, sélecteur de mode d'édition, undo/redo, raccourcis clavier, menu paramètres (hamburger).

## Panneau de détails — onglet Transform

Le panneau de détails d'une unité/feature contient plusieurs onglets (State, TO&E/S, Map display, Properties, **Transform**, Debug). L'onglet **Transform** applique des transformations géométriques à l'élément sélectionné, avec choix **New feature** (créer une nouvelle entité) ou **Update existing** (remplacer la géométrie existante), et un toggle **Show preview**.

Avec **plusieurs unités sélectionnées** (depuis oct. 2026), le panneau de détails édite toutes les unités à la fois (statut, symbole, retrait de la carte, amplificateurs texte, vitesses, verrouillage, TO&E) ; les champs divergents affichent "Mixed" et les unités verrouillées sont ignorées. Le bouton de **masquage de l'unité sur la carte** (sept. 2026) se trouve dans la barre d'outils du panneau de détails.

Transformations disponibles : **Buffer** (zone tampon — Radius + Units + Steps pour le nombre de segments), **Convex Hull**, **Concave Hull** (avec un paramètre de lissage), **Union**, **Explode**, **Centroid**, **Center (absolute)**, **Center of mass**, **Smooth**, **Bounding box**. Chaînage de plusieurs transformations possible (bouton "+ Add"). Panneau Transform disponible aussi bien pour les scenario features que pour les unités (depuis 2025). Non documenté dans le guide officiel — vérifié par observation directe de l'interface.

## Sauvegarde / stockage

- **Pas de stockage en ligne côté site** : tout est local (IndexedDB du navigateur par défaut), + possibilité de télécharger le scénario en fichier `.json`.
- ⚠️ Le stockage navigateur n'est **pas un backup fiable** (peut être vidé/purgé automatiquement). Télécharger régulièrement les scénarios en local.
- Modèle de sauvegarde hybride (depuis 2026) : "Save scenario" met à jour le scénario stocké ; l'autosave écrit des brouillons de récupération ; à la fermeture/rechargement, seuls les changements non explicitement sauvegardés déclenchent un avertissement.
- Chargement : drag-and-drop du .json sur la fenêtre, ou File > Open scenario.
- Un scénario peut aussi être chargé depuis une URL (`loadScenarioURL`) — utile pour héberger des scénarios sur GitHub Pages par ex.
- Fonctionnalités de partage en ligne : "Share scenario online" / "Share scenario as URL", historique des liens partagés via "Recently Shared", scénarios chiffrés/protégés par mot de passe possibles.

## Usage hors-ligne

Possible depuis juillet 2026 (doc : https://docs.orbat-mapper.app/guide/offline-use). Par défaut, le site utilise des fonds de carte, des données d'élévation (Mapterhorn) et une recherche de lieux (Photon) hébergés en ligne. Trois niveaux de déploiement (le numéro indique l'infrastructure supprimée, pas la connexion requise) :

1. **Self-hosted** — l'appli (zip `orbat-mapper-<version>.zip` / dossier `dist`) servie par un serveur web du réseau, avec un serveur de tuiles local (`config/maplibreConfig.json` ou Layers > "Add map server…").
2. **Local map file** — fond de carte en **archive PMTiles** sur le disque, sans serveur de tuiles : clic droit sur la carte > Map base layer > "Open PMTiles archive…", bouton du panneau Layers (Base layers) ou glisser-déposer. Les archives vectorielles sans style reçoivent un style généré (variantes light/dark/white/black/grayscale). Chrome/Edge/Brave peuvent rouvrir l'archive à la session suivante (pas en glisser-déposer, ni sous Firefox/Safari).
3. **Standalone file** — tout le site en **un seul fichier HTML** (`orbat-mapper-standalone-<version>.html`, ~8 Mo, attaché à chaque release GitHub) ouvert en `file://`, sans aucun serveur, + archive PMTiles. Fonctionnent : édition, stockage navigateur (propre à l'emplacement du fichier), chargement/sauvegarde, import/export, terrain via archive d'élévation. Absents : scénarios de démo, recherche de lieux, lecture de `maplibreConfig.json`. Mise à jour = retélécharger le fichier.

- **Relief 3D hors-ligne** (oct. 2026) : archive PMTiles d'élévation (ex. extrait de Mapterhorn) via clic droit > Terrain > "Open elevation archive…", ou glisser-déposer puis "Use for terrain". Hors-ligne sans archive, le bouton terrain passe en ambre et la carte reste plate.
- **Seule limite restante : la recherche de lieux (géocodage)** n'a aucune solution hors-ligne, quel que soit le niveau.
