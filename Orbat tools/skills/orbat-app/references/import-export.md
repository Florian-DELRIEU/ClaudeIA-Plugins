# Import et export — orbat-mapper.app

Source : https://docs.orbat-mapper.app/guide/import-data, /export-data, /sharing-scenarios + CHANGELOG (relu le 2026-10-10)

## Import

Menu **File > Import** (ou drop direct d'un fichier sur l'éditeur — plus besoin de passer par le menu depuis janv. 2023).

Formats/sources supportés :
- **Excel (.xlsx) / CSV** — écran de mappage de colonnes vers les propriétés d'unité (Name obligatoire ; Icon = code SIDC complet OU nom lisible type "Infantry" ; Echelon = "Platoon"/"Company" etc. — le générateur essaie de créer un SIDC valide à partir de Icon+Echelon). Options : inclure équipement des templates d'unité dans le TO&E, inclure personnel des templates dans le TO&E. Support import générique avec mapping de champs custom depuis fév. 2026.
- **MilX (.milxlyz / .milxly)** de map.army — unités ET, depuis oct. 2026, **graphismes tactiques** : chaque calque MilX devient un calque de mesures de coordination (control measures), identité et statut "planned" conservés, formes libres map.army importées comme graphismes génériques (couleurs et texte gardés), les graphismes sans équivalent sont **signalés** (donc pas importés). Les unités importées gardent leur direction et tous leurs amplificateurs texte, et on choisit où placer leurs positions : position initiale, heure courante du scénario, ou un événement du scénario. Piège connu qui subsiste : map.army utilise des codes SIDC alphabétiques MIL-STD 2525C/APP-6C ; le site convertit vers 2525D/APP-6D mais ça peut échouer pour certains symboles. (Correctif oct. 2026 : un `.milxly` simple n'est plus détecté à tort comme du TSV.)
- **Spatial Illusions ORBAT Builder** — export JSON simple, bien supporté (options d'aperçu enrichies).
- **Order of Battle Generator** (orbatgenerator.com).
- **DATE World / ODIN** (Decisive Action Training Environment, US Army) — format DRAGON (Agnostic). Pour importer : sur le site DATE World, chaque unité de la force structure a un bouton export en haut à droite → choisir le format DRAGON (Agnostic). ⚠️ Les force structures DATE sont énormes (potentiellement des milliers d'unités) — import massif à anticiper.
- **GeoJSON** — import direct de features, y compris **coller depuis le presse-papier** (Ctrl/Cmd+V dans le calque actif) depuis avril 2026 ; mesures de coordination incluses depuis août 2026.
- **KML/KMZ** — y compris sélection des dossiers à charger, chargement de plusieurs fichiers simultanément, clic sur une feature KML/KMZ ouvre une vue détails en lecture seule avec rendu HTML enrichi.
- **GPX** — support ajouté avril 2026 (conversion de tracks, association piste↔unité).
- **PMTiles** (juillet 2026) — pas un import de scénario mais un fond de carte : une archive `.pmtiles` glissée sur la carte (ou ouverte via Layers / menu contextuel) devient le fond de carte, ou des données d'élévation via "Use for terrain" (oct. 2026). Voir `apercu-site.md` § Usage hors-ligne.
- **Import partiel d'un scénario dans un autre** — choix des calques à importer (y compris calques de control measures, avec remappage sûr des ID — août 2026) ; depuis sept. 2026, possibilité de **remplacer** les calques de features/control measures existants (appariés par ID, aperçu ajouts/modifs/suppressions, annulable par Undo) au lieu de les importer en copies.

## Export

Menu **File > Export scenario**.

- **GeoJSON** — standard ouvert pour features géographiques + attributs (control measures incluses depuis août 2026).
- **KML/KMZ** — pour Google Earth et autres outils géospatiaux. Options : dossiers par côté (side), un dossier KML par événement de scénario (mode "multiple events"), tracé du contour du symbole, échelle icône/label ajustable, rendu des amplificateurs de symbole, dossiers imbriqués sides/groups, export des unités sélectionnées seulement, icônes custom embarquées dans le KMZ.
  - **Mesures de coordination (control measures)** exportées avec leur style depuis août 2026, labels et amplificateurs texte générés ; en KMZ, labels natifs ou **intégrés en images** (pour conserver orientation, échelle, ancrage et typographie).
  - Les unités **masquées sur la carte** (sept. 2026) sont exclues des exports GeoJSON/KML.
- **XLSX** — export unités vers Excel.
  - Option "one sheet per side" (une feuille par camp) vs tout sur une seule feuille.
  - Attributs sélectionnables : id, name, sidc, shortName, description, url, location, parent ID, side ID, side name.
  - Format de coordonnées au choix : JSON array [lon, lat] / Lat,Lon / Lon,Lat / MGRS / Degrés-Minutes-Secondes / Degrés décimaux.
- **CSV/TSV** — avec séparateur configurable (depuis fév. 2026).
- **MilX** — export expérimental vers map.army, mêmes limites de conversion 2525D→2525C que pour l'import.
- **Spatial Illusions ORBAT Builder** — export JSON compatible.
- **Copier comme GeoJSON** — dispo depuis le menu du calque de features, le menu d'une feature individuelle, et le panneau détails d'une feature (les cercles sont exportés en polygones).
- **Export image de la carte** (via panneau Tools) — viewfinder ajustable, presets de ratio d'aspect, guide de zone de sécurité, échelle de résolution de sortie, barre d'échelle/flèche du nord/attribution en overlay optionnels, bouton copier directement dans le presse-papier (juin 2026).
- **Export symboles** (symbol browser) : PNG ou SVG, taille et options d'affichage configurables.

## Partage de scénario

- **Share scenario online** / **Share scenario as URL** — génère un lien partageable (le site ne stocke rien côté serveur par défaut, mais ces fonctions permettent le partage en ligne / via URL).
- Scénarios **chiffrés et protégés par mot de passe** possibles à l'export/import/partage en ligne.
- Historique des scénarios partagés accessible via **File > Recently Shared**.
- Alternative "self-hosted" : héberger le fichier .json sur un dépôt GitHub public (ex. GitHub Pages) et charger via le paramètre d'URL `?loadScenarioURL=...` — cf. dépôt exemple `orbat-mapper/scenario-hosting-test`.
