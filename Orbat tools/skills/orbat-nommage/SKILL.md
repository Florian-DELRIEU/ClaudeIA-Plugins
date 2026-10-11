---
name: orbat-nommage
description: >
  Conventions de NOMMAGE des formations militaires réelles (compagnie →
  régiment → division) : Allemagne, États-Unis, Royaume-Uni, URSS-Russie,
  France, du XIXᵉ siècle à aujourd'hui, plus la couche « organisation de
  mission » (Kampfgruppe, Task Force, Battlegroup, BTG, GTIA). Déclencher
  IMPÉRATIVEMENT dès que Florian tape /orbat-nommage ou /orbat-nom, ou
  demande : comment nommer/numéroter une unité ou une sous-unité et dans quel
  style d'armée, comment décoder une désignation (`3./IR 9`, `B/1-5 IN`,
  `II./AR 155`, `1st Guards msp`, `501e RCC`, `TEILE/PIONIER-REGIMENT 2`),
  pourquoi la lettre « J » est sautée, ce qu'est une « Abteilung », un
  « squadron » US vs UK, un « escadron » français, ou comment construire une
  nomenclature maison cohérente pour un ORBAT fictif. Différent de
  `orbat-tools:acronyme` (codes maison de Florian) et de
  `orbat-tools:orbat-historique` (structure et effectifs) : ici c'est le
  LIBELLÉ de l'unité qui est l'objet — les trois s'enchaînent.
---

# ORBAT Nommage — conventions de désignation des formations

Décrire, décoder et appliquer les **mécaniques de nommage** des unités
militaires (compagnie → régiment → division) de plusieurs armées et de
plusieurs époques, et en dériver une nomenclature maison cohérente.

Ce skill porte sur le **libellé** de l'unité, pas sur son contenu :

| Besoin | Skill |
|--------|-------|
| Comment s'appelle / se numérote l'unité | **ce skill** |
| Comment elle est structurée, ses effectifs | `orbat-tools:orbat-historique` |
| Code du système de nomenclature maison de Florian | `orbat-tools:acronyme` |
| Fichier ORBAT à lire/écrire | `orbat-tools:orbat-json` / `orbat-xlsx` |

## Cadre général — les 6 axes de décision

Toute nomenclature réelle se ramène à une poignée de choix. **C'est la grille
de lecture de tout le reste et la base de conception d'une règle maison** :
face à une demande de nommage, répondre d'abord aux 6 axes, puis décliner.

| # | Axe | Question posée |
|---|-----|----------------|
| A1 | **Codage de l'échelon** | Chaque niveau reçoit-il un numéro, une lettre, un nom propre, ou un titre d'honneur ? |
| A2 | **Continuité de la numérotation** | Les sous-unités repartent-elles de 1 à chaque échelon, ou la numérotation est-elle continue à travers l'unité mère ? |
| A3 | **Encodage de l'arme** | Le type d'arme est-il inscrit dans le nom ? Si oui, **avant ou après** le numéro ? |
| A4 | **Séparateur typographique** | `.` `/` `-` virgule, fraction… |
| A5 | **Élément de commandement** | Comment nomme-t-on l'état-major / la compagnie de commandement ? |
| A6 | **Couche organisation de mission** | Existe-t-il une désignation temporaire (task force / groupement) par-dessus la structure administrative fixe ? |

## Tableau de synthèse (6 axes × 5 nations)

| Axe | 🇩🇪 Allemagne | 🇺🇸 États-Unis | 🇬🇧 Royaume-Uni | 🇷🇺 URSS/Russie | 🇫🇷 France |
|-----|:---:|:---:|:---:|:---:|:---:|
| **A1** Bataillon | 🔢 romain | 🔢 arabe | 🔢 arabe | 🔢 arabe | 🔢 arabe |
| **A1** Compagnie | 🔢 arabe | 🔤 lettre (J sauté) | 🔤 lettre / 🏷️ nom | 🔢 arabe | 🔢 arabe |
| **A2** Numérotation cie | ➡️ continue (WWII/NVA) · 🔄 remise à 0 (RFA) | ➡️ continue | variable | 🔄 par unité | 🔄 remise à 0 · réserve continue |
| **A3** Arme dans le nom | ✍️ oui, **après** n° | ✍️ oui | 🏷️ identité régimentaire | ✍️ oui | ✍️ **sigle**, ordinal **devant** |
| **A4** Séparateur | `.` `/` | `-` `/` | virgule / « of » | virgule | fraction `/` · ordinal « e » |
| **A5** Commandement | Stabskompanie (SK) | HHC/HHT/HHB | HQ Company | — | Cie/escadron de commandement |
| **A6** Couche mission | Kampfgruppe | Task Force / Team | Battlegroup | OMG / BTG | GTIA / SGTIA |
| **Honneurs** | rare | surnoms d'unité | 🎖️ dans le nom | 🎖️ empilés dans le nom | 🎖️ sur le drapeau (hors nom) |

**Légende :** 🔢 numéro · 🔤 lettre · 🏷️ nom propre/tradition · ➡️ continue ·
🔄 remise à zéro · ✍️ arme encodée dans le libellé · 🎖️ titre d'honneur.

## Couche transverse — l'organisation de mission

Par-dessus la structure administrative fixe, toutes les armées plaquent des
**groupements temporaires** au nommage distinct. À traiter comme une
**surcouche**, jamais comme un remplacement de la désignation permanente : les
unités constitutives gardent leur nom.

Déclencheur doctrinal (🇺🇸, FM 3-90.2) : un bataillon devient *task force* dès
qu'il reçoit une unité de la taille d'une compagnie **d'une autre arme**, ou
qu'il part en mission semi-indépendante ; une compagnie ainsi renforcée devient
un *Team*. C'est la seule des cinq écoles à poser un critère explicite.

| Nation / cadre | Nom du groupement | Logique de nommage |
|----------------|-------------------|--------------------|
| 🇩🇪 2ᵉ GM | Kampfgruppe | nom du **chef** (KG Peiper) |
| 🇺🇸 | Task Force (bataillon) / Team (compagnie) | **désignation du noyau conservée** (`TF 1-41 IN`, `Team B`) ou nom de code (`TF Smith`) |
| 🇬🇧 / Commonwealth | Battlegroup | d'après l'unité noyau |
| 🇷🇺 Guerre froide / moderne | OMG / BTG | d'après la brigade/bataillon mère |
| 🇫🇷 | GTIA / SGTIA | d'après le **régiment noyau** |
| OTAN (interarmées/multinational) | JTF / CTF / CJTF | Joint (multi-services), Combined (multinational) |

Note OTAN : la symbologie APP-6 / MIL-STD-2525 prévoit un **champ « task
force »** distinct sur le symbole d'unité, et un champ « échelon » pour la
taille — voir `orbat-tools:orbat-json` (références sidc) pour l'encodage.

## Fichiers de référence

Lire le fichier pertinent **avant de répondre**, plutôt que de citer de mémoire :

- `references/nations.md` — vocabulaire des échelons (table d'équivalence par
  arme), **règles typographiques transverses** (TR-1…TR-6 : forme du numéro
  selon l'échelon, place de l'arme, termes non traduits) et **règles codées par
  nation** (DE-1…DE-16, US-1…US-13, UK-1…UK-7, RU-1…RU-9, FR-1…FR-14), avec
  exemples canoniques.
- `references/pieges.md` — pièges, faux amis et collisions à connaître
  (« squadron » US ≠ UK, « troop » US ≠ UK, « Gruppe » à trois sens, « escadron »
  avant/après 1815, « Abteilung », lettre « J », numérotation continue allemande,
  renumérotations françaises), les **points où les sources divergent**, et deux
  annexes de décodage d'exemples réels (dont les cas d'école WARNO).
- `references/sources.md` — sources classées par nation et par fiabilité
  (🥇 institutionnel · 🥈 encyclopédique · 🥉 communautaire), avec la note de
  fiabilité à respecter avant d'affirmer un « pourquoi », le marquage des sources
  effectivement lues, et les **pistes non couvertes**.

**Périmètre :** formations **terrestres**. Seule exception traitée, la Luftwaffe
(règle DE-15, qui partage la notation à slash allemande). Ne pas extrapoler aux
marines ni aux forces aériennes modernes.

## Procédures

### Décoder une désignation existante

1. Repérer l'**école** au séparateur et au type de chiffre : `./` + romain →
   🇩🇪 ; lettre de compagnie → 🇺🇸/🇬🇧 ; ordinal devant + sigle → 🇫🇷 ; empilement
   d'honneurs ou `v/ch` → 🇷🇺.
2. Ouvrir `references/nations.md` à la section correspondante et appliquer les
   règles dans l'ordre A1 → A6.
3. Vérifier systématiquement `references/pieges.md` avant de conclure — la
   plupart des erreurs de lecture viennent de là (7ᵉ compagnie ≠ 7ᵉ bataillon,
   squadron US ≠ UK…).
4. Restituer : échelon, arme, unité mère, et ce que le libellé **ne dit pas**.

### Nommer une unité « à la manière de » X

1. Fixer la nation et l'époque (les règles varient : Wehrmacht ≠ Bundeswehr,
   France d'avant 1815 ≠ après).
2. Dérouler les 6 axes depuis le tableau de synthèse, puis appliquer les règles
   détaillées de la nation.
3. Produire le nom **long officiel** et la **contraction d'usage** quand
   l'école en a une (`3./IR 9`, `B/1-5 IN`, `18/1`).
4. Signaler toute collision créée (numéro déjà pris, lettre interdite).

### Construire une nomenclature maison (ORBAT fictif)

1. Faire choisir explicitement une valeur pour chacun des 6 axes — proposer
   une école existante comme base plutôt que d'inventer à vide.
2. Vérifier la **cohérence interne** : un choix A2 « continue » impose de
   figer le nombre de sous-unités par échelon ; un choix A3 « arme après le
   numéro » interdit l'ordinal en tête.
3. Écrire la règle sous forme de codes numérotés réutilisables (même format
   que `references/nations.md`) et donner 3 exemples déclinés du haut en bas
   de la hiérarchie.
4. Si le projet de Florian utilise déjà le système de codes maison, croiser
   avec `orbat-tools:acronyme` avant de figer quoi que ce soit — ce skill
   donne la *forme* du libellé, `acronyme` donne les *codes*.

## Règles de rigueur

- Ne jamais affirmer une règle nationale de mémoire seule quand un détail
  précis est en jeu : ouvrir `references/nations.md`.
- **La mécanique** de chaque système est concordante entre toutes les sources ;
  les *justifications historiques* le sont beaucoup moins. Distinguer les deux
  et signaler quand une explication relève du folklore (cas type : le « J »
  sauté aux États-Unis).
- Une désignation n'est valable qu'à une **date** donnée : toujours situer
  l'époque avant de trancher.
