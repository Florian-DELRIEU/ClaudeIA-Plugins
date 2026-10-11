# Orbat Tools

Plugin regroupant les outils ORBAT et nomenclature militaire de Florian.

## Skills inclus

- **orbat** — Lecture, écriture, analyse et agrégation d'ORBAT (Order of Battle),
  au format `orbat-mapper.app` (JSON) comme au format xlsx ODIN / JTDS (TRADOC G2).
  Créer/lire/modifier des ORBAT, décoder des symboles militaires (SIDC), sommer du
  matériel, convertir une image d'ORBAT en JSON.

- **orbat-historique** — Expert en organisation militaire historique réelle (ordres
  de bataille, organigrammes) du début du 19e siècle à aujourd'hui, toutes nations
  confondues.

- **acronyme** — Système de nomenclature militaire modulaire V4 : code tout
  véhicule, unité, navire, aéronef, structure ou personnage selon un format
  Type/Rôle/Armement. Inclut une méthode d'identification pour convertir du
  matériel réel en acronyme.

- **orbat-acronymize** — Skill dédié : prend un ORBAT JSON existant et remplace
  automatiquement les noms de véhicules (`equipment`) et de troupes (`personnel`)
  par leurs codes `/acronyme` V4, en propageant le changement dans tout l'arbre
  d'unités. S'appuie sur les deux skills ci-dessus. Écrase le fichier d'origine
  par défaut (option `--dry-run` / `--output` disponible pour un aperçu ou une
  copie séparée).

## Utilisation typique

1. Fournir un fichier ORBAT JSON (format `orbat-mapper.app`).
2. Demander : « convertis cet ORBAT en acronymes v4 » (ou taper
   `/orbat-acronymize`).
3. Le skill propose un tableau des correspondances nom → code avant d'écrire,
   applique le renommage, journalise les nouveaux codes dans le lexique
   `/acronyme`, puis valide le fichier résultant.
