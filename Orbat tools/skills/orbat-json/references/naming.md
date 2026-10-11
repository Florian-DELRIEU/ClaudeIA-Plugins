# Conventions de nommage — `name` et `shortName`

Ces règles s'appliquent à **toute** unité créée ou modifiée dans un ORBAT (Tâche 4,
et toute réécriture de noms existants). Établies suite à la construction de l'ORBAT
France 1980.

> 🔴 **RÈGLE ABSOLUE — tout acronyme vient de `orbat-tools:acronyme`** (Florian,
> août 2026). Dès que la rédaction d'un `name`, d'un `shortName`, d'une ligne de TOE
> ou d'une `description` demande une forme abrégée, **invoquer le skill
> `orbat-tools:acronyme`** (outil `Skill`) et y prendre le code. Aucune autre source
> n'est admise : ni mémoire, ni codes vus plus haut dans la conversation, ni codes
> repris d'un ORBAT antérieur, ni table locale à ce skill. Si le code n'existe pas :
> Règle 7 § 7.2 (question à Florian), jamais une invention. Cette règle prime sur
> toute formulation plus ancienne des Règles 1 à 7 ci-dessous.

## Règle 1 — Jamais de parenthèses dans `name`

Aucune parenthèse dans le nom d'une unité, quelle que soit la raison :

- **Contexte de parenté** (le cas le plus fréquent en génération programmatique,
  ex. `"1er Régiment Blindé (1ère Division Blindée)"`) → **ne pas l'ajouter**. La
  position de l'unité dans l'arbre (`subUnits`) porte déjà ce contexte ; le répéter
  dans chaque nom alourdit la lecture sans ajouter d'information récupérable
  autrement. C'est aussi le style des documents sources eux-mêmes (les TO&E ne
  nomment généralement pas leurs sous-unités de façon unique — « Armoured
  Regiment » revient identique dans toutes les divisions).
- **Garnison / localisation** → utiliser un tiret cadratin dans le nom si utile
  (`"1ère Division Blindée — Allemagne de l'Ouest"`), jamais des parenthèses.
- **Précision d'équipement, incertitude de source, note méthodologique** → dans le
  champ `description` de l'unité, jamais dans `name`.

Des noms identiques entre unités-sœurs de branches différentes sont acceptables et
normaux (ex. chaque division a son "1er Régiment Blindé") : le contexte vient de la
position dans l'arbre, pas du texte du nom.

## Règle 2 — Toujours renseigner un `shortName`

Chaque unité doit porter un `shortName` cohérent avec son `name`, composé **avec les
codes de `orbat-tools:acronyme`** (jamais une troncature arbitraire du texte, ni une
abréviation dérivée de tête — voir la règle absolue en tête de fichier et § 7.5).
Conserver dans le `shortName` :
- les numéros d'ordre (1er/2e/1ère/3e…) ;
- une garnison éventuelle (même séparateur " — ") ;
- toute note conservée intentionnellement entre parenthèses dans un cas
  exceptionnel et justifié (très rare, cf. Règle 1).

Des `shortName` identiques entre unités-sœurs de branches différentes sont
acceptables, pour la même raison qu'en Règle 1.

### Où trouver les abréviations — **aucune table ici**

> **Principe de source unique (août 2026).** `orbat-json` ne stocke **aucune liste
> d'acronymes**. Toute abréviation d'échelon, de type de formation ou de rôle vient
> du skill **`orbat-tools:acronyme`**, et de lui seul. Une table recopiée ici
> deviendrait silencieusement fausse à la première décision prise dans `acronyme`.

| Ce qu'on cherche | Fichier — source de vérité |
|---|---|
| Échelon (Division, Régiment, Bataillon, Compagnie, Peloton, Escouade…) | `../acronyme/references/groupements.md` § **Échelons** |
| Type de formation (Infanterie, Blindés, Mécanisé, Artillerie, Génie, Reco…) | `../acronyme/references/groupements.md` § **Types d'unité** |
| Vérifier qu'un code existe | `../acronyme/references/INDEX.md` (index généré, un `grep` suffit) |
| Partir du nom réel d'un matériel | `../acronyme/identification/lexique.json` (ou `lexique-40k.json`) |

**Le réflexe est le renvoi, pas la recherche mentale.** Le besoin d'une abréviation
déclenche l'invocation du skill `orbat-tools:acronyme` — on ne dérive jamais un
`shortName` « par abréviation du rôle » de sa propre initiative, même quand la forme
paraît évidente (`Bat` pour bataillon, `Cie` pour compagnie…). C'est précisément
ainsi que sont nés les codes périmés listés plus bas.

Pour un terme non couvert par ces fichiers : **ne pas improviser une abréviation** —
c'est un cas Règle 7 § 7.2 (question à Florian), pas une décision d'auteur.

**⚠️ Tables France 1980 retirées (août 2026).** Ce paragraphe contenait jusqu'ici deux
tables (« Échelons/formations » et « Rôles/spécialités ») héritées de l'ORBAT France
1980. Elles étaient **antérieures à la normalisation v4 du 2026-08-04** et entraient
en conflit direct avec `groupements.md` :

| Ancienne table `naming.md` | `acronyme/references/groupements.md` aujourd'hui |
|---|---|
| Bataillon → `B` | `BN`/`BT` — et `B` = **Brigade** |
| Brigade → `Bde` | `BGE`/`B` (`Bde` n'existe pas) |
| Batterie → `B`/`Bat` | `BAT`/`BTE` |
| Blindé → `B` | `ARM` officiel (`-B` collisionne Bâtiment/Chenillé) |
| Infanterie → `I` | `INF` officiel (`I` collisionne Industriel/Incendiaire/Intercepteur) |
| Artillerie → `A` | `ART` officiel |
| Génie → `G` | `GEN` officiel |
| Parachutiste → `P` | `-PAR` (`P` libéré) |

C'est exactement le mode de panne que la source unique évite. Un ORBAT ancien qui
porte encore ces codes se relit avec l'ancienne table (ci-dessus, conservée à titre
d'archive) ; toute **écriture** neuve suit `groupements.md`.

## Règle 3 — Indicateur de TOE vide (symbole `Ø`)

Établie sur l'ORBAT « Altis Forces Rearmed » (juillet 2026). Quand une unité **et
tout son sous-arbre** ne portent ni `equipment` ni `personnel` nulle part (TOE non
détaillé par la source), on l'indique en suffixant `name` **et** `shortName` avec
`" Ø"` (espace + Ø, U+00D8 — choisi pour sa lisibilité universelle : Latin-1/UTF-8,
sans risque d'affichage contrairement à `∅` U+2205, et sans ambiguïté contrairement
à `0` ou des mots comme `(vide)`/`[VIDE]`).

**Condition stricte : le sous-arbre ENTIER doit être vide, pas seulement l'unité
elle-même.** Une compagnie sans equipment/personnel propre mais dont au moins une
sous-unité (peloton, section...) porte du contenu n'est **pas** marquée — seules
les sous-unités réellement vides le sont, individuellement. Concrètement : calcul
récursif post-ordre (voir `orbat_lib.mark_empty_subtrees`), une unité est marquée
seulement si elle n'a rien en propre ET que 100% de ses enfants (récursivement)
sont eux-mêmes marqués vides.

Exemple (Altis Forces Rearmed) : `Signals Company`, `Engineer Company` et
`Service Support Company` sont des feuilles sans composition détaillée dans le
PDF source → marquées `Signals CIE Ø` / `Sig CIE Ø` etc. La `Pathfinder Company`,
sœur de ces trois-là dans la même HQ Bn, n'est pas marquée (elle a du contenu) —
et sa présence empêche aussi le parent (HQ Bn) d'être marqué.

À utiliser en toute fin de construction (Tâche 4), après le nommage, juste avant
`validate.py` : `orbat_lib.mark_empty_subtrees(orbat)`.

## Règle 4 — Traduire les mots d'échelon d'une source anglaise vers `/nomenclature-v4`

Établie sur l'ORBAT « Altis Forces Rearmed » (source PDF en anglais, convention
britannique/OTAN). Quand Florian demande d'aligner les noms sur son système
`/nomenclature-v4` plutôt que de garder les abréviations anglo-saxonnes brutes du
document source, remplacer par mot entier (regex `\b...\b`, sur `name` **et**
`shortName`, pas seulement `shortName`) en s'appuyant sur la table Échelons de
`nomenclature-v4/references/groupements.md` :

**La table de correspondance ne vit pas ici.** Les cibles françaises
(`Battalion`→ ?, `Company`→ ?, `Battery`→ ?…) se lisent dans
`../acronyme/references/groupements.md` § **Échelons** au moment de la conversion.
Ce qui reste propre à `orbat-json`, c'est la cartographie des **formes sources
anglaises vers la notion d'échelon** — jamais le code final :

| Mot source (EN), formes pleines et abrégées | Échelon visé (→ code dans `groupements.md`) |
|---|---|
| `Battalion` / `Bn` | Bataillon |
| `Company` / `Coy` | Compagnie |
| `Platoon` / `Plt`, `Troop` / `Tp` | Peloton |
| `Section` / `Sect` | **Escouade** — ⚠️ voir le piège FR/EN ci-dessous |
| `Detachment` / `Det` | Détachement |
| `Battery` / `Bty` | Batterie |

Fonction prête à l'emploi : `orbat_lib.apply_word_substitutions(orbat,
orbat_lib.build_echelon_word_subst())`. `build_echelon_word_subst()` **relit
`../acronyme/references/groupements.md` à chaque appel** et échoue bruyamment si le
skill `acronyme` est introuvable — c'est voulu : mieux vaut une erreur qu'un ORBAT
entier renommé avec des codes périmés. (L'ancienne constante figée
`ECHELON_WORD_SUBST_EN_TO_NOMV4` a été retirée en août 2026 : elle codait
`Battery → BTE` alors que `groupements.md` donne `BAT` en forme officielle.)
À exécuter **avant**
`mark_empty_subtrees` (Règle 3), pour que le tag `Ø` s'accroche aux noms déjà
convertis.

**⚠️ Piège FR/EN sur « Section » (déjà signalé dans `sidc.md`) :** en anglais/
Commonwealth, une « Section » d'infanterie compte ~8-10 hommes — c'est un échelon
**escouade** (`SQ`, `échelon=12`). La `Section` du système `/acronyme` (`SEC`,
`échelon=13`) est une « grosse escouade » de ~15+ hommes. Ne jamais convertir
mécaniquement `Section`→`SEC` : la bonne cible est `SQ`.

Depuis le 2026-08-09 le piège se désamorce tout seul par les effectifs — 8-10 tombe
dans `SQ` (~7-15), pas dans `SEC` (~15+). Voir l'échelle complète dans
`../acronyme/identification/personnel.md`.

**⚠️ Corollaire — `SEC` n'est plus l'équivalent de `PLT`.** Ce paragraphe affirmait
jusqu'ici que « la Section `/nomenclature-v4` désigne l'échelon peloton, comme
`PLT` ». C'est **faux** : `PLT` est un échelon strictement supérieur, un conteneur
qui regroupe plusieurs escouades/équipes/sections, alors que `SEC` est un élément
terminal. Ne pas les traiter comme interchangeables.

**`Team`, `Pair`, `Group`, `Crew` (échelon équipe) :** ces mots sources n'ont pas de
correspondance univoque évidente. Ne pas trancher de tête — **consulter
`orbat-tools:acronyme`** (`references/groupements.md` § Échelons et
`identification/personnel.md` § Échelons d'élément, qui donnent `EQP`, `BI`, `GRP`,
`SQ` avec leurs effectifs indicatifs) et retenir le code correspondant à la **nature
réelle** de l'élément. Si aucun ne convient, cas Règle 7 § 7.2 → question à Florian.
Laisser le terme anglais brut n'est acceptable que sur décision explicite de Florian.

**Cas des sigles déjà établis par la source — ne plus les reprendre par défaut.**
Un sigle du document source (ex. `HHC` = *Headquarters and Headquarters Company*)
n'est **pas** un acronyme du système : l'écrire en `shortName` introduit un
vocabulaire concurrent. Le `shortName` se compose donc avec les codes de
`orbat-tools:acronyme` (ici `CIE-HQ`, à vérifier dans
`../acronyme/references/groupements.md` au moment de l'écriture), et le sigle source
est conservé **en `description`** pour la traçabilité (« désignée `HHC` dans la
source »). Garder le sigle verbatim en `shortName` reste possible, mais seulement
**sur demande explicite de Florian** pour un fichier donné.

## Règle 5 — Description de catalogue : toujours nommer le matériel réel

Établie suite au retour de Florian sur l'ORBAT CSAT (juillet 2026, ORBAT codé
directement en acronymes `/nomenclature-v4` sans jamais donner le nom réel du
véhicule à l'échelle de l'unité, seulement dans le catalogue racine — pas assez
pour qu'il sache "de quel véhicule/matériel exact on parle").

Toute entrée des catalogues racine `equipment`/`personnel` doit avoir une
`description` qui **commence par la désignation réelle** du matériel ou du
véhicule (nom de plateforme réelle ou du jeu), éventuellement suivie de
`" — "` puis d'un contexte additionnel (rôle, variante, état du parc...) :

```
"MSE-3 Marid — variante commandement (transmissions renforcées)"
"T-100 Varsuk — char de bataille principal CSAT, canon lisse 125mm"
```

Une description qui ne mentionne pas le matériel réel (ex. juste un
commentaire de contexte, ou vide) casse la traçabilité acronyme → matériel et
empêche `scripts/add_legends.py` (Tâche 4 point 6) de générer
la légende par échelon — toujours vérifier que le nom réel est identifiable en
tête de `description` avant de livrer un ORBAT.

**Format de restitution :** dès que cette information ressort dans une
`description` d'unité (légende par échelon), elle s'écrit dans la forme canonique
`**CODE : Désignation réelle**` — voir Règle 7 § 7.3. L'ancien format `* CODE = ...`
peut subsister dans de vieux fichiers : relancer un script de légende le remplace.

### ⚠️ Piège confirmé — codes partagés entre plusieurs camps du même fichier

Établi suite à l'ORBAT « Arma 3 - Altis » (juillet 2026, scénario multi-camps :
France / FIA / AAF / CSAT dans un seul fichier). Le catalogue racine
`equipment`/`personnel` est **global par nom de code, pas cloisonné par camp** :
si deux camps réutilisent le même acronyme `/nomenclature-v4` (ex. `MBT` pour
le char de bataille générique), il n'existe **qu'une seule entrée catalogue**
pour ce code, partagée par tous les camps qui l'utilisent.

**Avant d'écrire une désignation réelle dans le catalogue racine pour un code
utilisé par un camp précis, toujours vérifier si d'autres camps utilisent le
même code** :

```python
from collections import defaultdict
users = defaultdict(set)
for u, path in orbat_lib.iter_units(orbat, with_path=True):
    for e in (u.get("equipment") or []) + (u.get("personnel") or []):
        users[e["name"]].add(path[0])   # path[0] = nom du side
```

- Si le code n'est utilisé **que par un seul camp** → Règle 5 s'applique normalement,
  la désignation réelle va dans la `description` du catalogue.
- Si le code est **partagé par plusieurs camps** → ne jamais mettre de désignation
  réelle spécifique à un camp dans le catalogue racine (elle s'appliquerait aussi
  aux autres camps, ex. écrire "T-55" sur `MBT` contaminerait aussi le Leclerc
  français qui utilise le même code). Utiliser à la place la **légende locale par
  unité** (Règle 6 ci-dessous), qui porte l'information au niveau de chaque
  échelon plutôt qu'au niveau du catalogue global.

## Règle 6 — Légende locale par unité (codes partagés, comptes, hétérogénéité)

Établie sur l'ORBAT « Arma 3 - Altis » (juillet 2026) en complément de la Règle 5
et de `add_legends.py`. `add_legends.py` reste l'outil par défaut (Tâche 4 point 6)
quand un code catalogue a une désignation réelle univoque dans tout le fichier.
Il ne suffit plus dès que l'une de ces conditions s'applique :

1. **Code partagé entre plusieurs camps** (voir piège ci-dessus) — le nom réel
   diffère selon le camp, donc il ne peut pas vivre dans le catalogue global.
2. **Florian veut le compte par ligne** — cas devenu rare depuis la Règle 7 § 7.3
   qui fixe le format **sans quantité** (`**MBT : T-55**`) ; ne l'activer que sur
   demande explicite (`add_local_legends.py --avec-quantites`).
3. *(Caduc depuis octobre 2026 : `add_legends.py` sépare lui aussi Équipement et
   Personnel en deux blocs.)*
4. **Hétérogénéité locale à représenter** : un même code recouvre plusieurs modèles
   réels différents *au sein d'une même unité* (ex. `**VTT-LMG : BTR-60PB / OT-64
   SKOT**`) — impossible à exprimer avec une désignation catalogue unique.

Dans ces cas, utiliser `scripts/add_local_legends.py` à la place d'`add_legends.py` :
il construit, **par unité feuille** (pas par sous-arbre agrégé), une description au
format :

```
Équipement :
* **CODE : Désignation réelle**

Personnel :
* **CODE : Désignation réelle**
```

(Format canonique fixé par la Règle 7 § 7.3 — sans quantité. L'ancienne forme
`* CODE = Nx Désignation` est abandonnée ; tous les scripts produisent le format
canonique via `scripts/legends.py` et conservent la prose déjà présente.)

à partir d'une table de correspondance fournie (`{code: "désignation réelle"}`,
propre au camp traité) et d'overrides ponctuels par chemin d'unité pour
l'hétérogénéité locale. Voir `scripts/add_local_legends.py --help` et l'exemple
dans sa docstring. Contrairement à `add_legends.py`, il **n'agrège pas le
sous-arbre** : chaque unité listée doit porter directement son `equipment`/
`personnel` propre (feuilles), pas un total remonté depuis ses enfants — cohérent
avec le fait qu'il sert justement à distinguer des feuilles hétérogènes entre elles.

## Règle 7 — Procédure par défaut de génération (août 2026)

Établie explicitement par Florian (août 2026) comme **comportement par défaut de
toute génération d'ORBAT JSON** (Tâche 4 du SKILL.md), sans qu'il ait à la
redemander. Elle prime sur les habitudes de génération antérieures ; les Règles 1
à 6 restent valables et s'appliquent en complément.

### 7.1 — TOE/S exclusivement à partir d'acronymes existants

Les TOE/S (composition `equipment` / `personnel` d'une unité) se construisent
**uniquement avec des acronymes du système `/acronyme` (v4)** déjà établis.

> **Interdiction absolue d'inventer un acronyme.** Pas de code « plausible », pas
> d'extrapolation par analogie, pas de code forgé à la volée pour boucher un trou.

**Comment charger le système — étape obligatoire, pas déductible du contexte.**
Invoquer le skill **`orbat-tools:acronyme`** avec l'outil `Skill` *avant* d'écrire la
moindre ligne de TOE. Il vit dans le **même plugin** que `orbat-json`, donc ses
fichiers sont à `../acronyme/` depuis ce dossier. Ne jamais se contenter de « je
connais le système » ou des codes vus plus haut dans la conversation : c'est
exactement la situation où un acronyme s'invente tout seul.

**Ordre de recherche d'un code** (du moins coûteux au plus coûteux) :

1. `../acronyme/references/INDEX.md` — index alphabétique généré, **691 codes**, chacun
   pointant vers le(s) fichier(s) qui le définissent. C'est l'entrée par défaut : un
   `grep` sur le code suffit à savoir s'il existe.
2. `../acronyme/identification/lexique.json` (matériel réel) ou `lexique-40k.json`
   (univers fictifs : 40K, Cosmotter) — registre `désignation réelle ↔ code v4`. À
   consulter en premier quand on part du **nom du matériel** plutôt que du code.
3. Les tables thématiques `../acronyme/references/` : `terrestres.md`, `aeriens.md`,
   `maritimes.md`, `infanterie.md`, `structures.md`, `groupements.md`, `materiaux.md`
   (+ `grammaire.md` pour l'assemblage).
4. Si rien ne sort : `../acronyme/identification/METHODE.md` (pipeline châssis → Type,
   puis rôle/armement → suffixes) pour construire un code **à partir d'éléments
   attestés**. Si même ça ne donne rien, c'est un cas § 7.2 → question à Florian.

**Ce qui est une invention et ce qui n'en est pas une.** La combinaison d'éléments
attestés selon la grammaire documentée (suffixes de rôle/armement, notation numérique)
**n'est pas une invention** — c'est l'usage normal du système. Ce qui est interdit,
c'est de créer un **élément de vocabulaire** nouveau (un Type, un rôle, un suffixe) qui
n'existe nulle part. En revanche, un code composé à la volée mais absent des lexiques
**doit être signalé comme tel** à Florian (`acronyme/SKILL.md` point 8 : « `X-Y` n'existe
pas encore au lexique : composé à la volée, à journaliser si tu valides ») — il ne
s'ajoute jamais aux lexiques sans sa validation.

### 7.2 — Matériel sans acronyme correspondant : passe d'identification préalable, bloquante

Quand un matériel de la source ne correspond à aucun acronyme existant :

1. **Ne rien mettre.** Ne pas approximer avec le code « le plus proche », ne pas
   forger un code. L'entrée reste vide.
2. **Faire l'identification AVANT de construire.** La génération d'un ORBAT commence
   toujours par une **passe d'identification du matériel** : lister tout le matériel
   et le personnel de la source, résoudre chaque ligne vers son acronyme via la
   méthode `acronyme/identification/METHODE.md`, et isoler les cas non résolus.
3. **Soumettre les cas litigieux à Florian et attendre son arbitrage.** Présenter une
   liste : matériel source → ce qui a été cherché → codes candidats éventuels →
   pourquoi aucun ne convient. Florian tranche (choix d'un code existant, création
   d'un nouveau code de son côté, ou abandon de la ligne).
4. **Seulement ensuite, générer le JSON.** Pas de construction spéculative « quitte à
   corriger après » : c'est un choix explicite de Florian, motivé par le coût de
   reprise d'un ORBAT déjà bâti sur de mauvais codes.

Si Florian tranche « laisse tomber cette ligne », l'unité concernée est construite
sans cette entrée, et la lacune est mentionnée dans sa `description` (§ 7.4).

### 7.3 — Format canonique des descriptions : `**Acronyme : Nom du Modèle**`

Toute restitution d'un code vers son matériel réel, **dans une `description`
d'unité, à quelque échelon que ce soit**, s'écrit :

```
**CODE : Désignation réelle**
```

- **Sans quantité.** Le nombre est déjà porté par le champ `equipment`/`personnel`
  de l'unité ; le répéter dans la légende crée deux sources de vérité qui divergent
  dès la première édition.
- **Une ligne par code**, en liste, dans les blocs `Équipement :` / `Personnel :`
  quand les deux catégories coexistent (Règle 6).
- Hétérogénéité locale (un code, plusieurs modèles réels dans la même unité) :
  `**VTT-LMG : BTR-60PB / OT-64 SKOT**`.
- L'ancienne forme `* CODE = Nx Désignation réelle` est **abandonnée**. Les scripts
  `add_legends.py`, `add_local_legends.py` et `apply_rename_map.py` produisent le format
  canonique (module unique `scripts/legends.py`, octobre 2026) et remplacent toute
  légende à l'ancien format en conservant la phrase de contexte.

Cette forme ne dispense pas de la Règle 5 : le catalogue racine doit toujours
porter la désignation réelle en tête de sa propre `description`.

### 7.4 — Phrase de contexte obligatoire, surtout aux bas échelons

Chaque unité reçoit, **avant** le bloc de légende et séparée par une ligne vide,
**une à deux phrases** décrivant ce que la lecture de l'ORBAT ne montre pas.
Généralise la « directive description narrative » de la Tâche 4 point 6, qui était
jusqu'ici appliquée sur demande — elle est désormais le défaut.

**Priorité aux échelons les plus bas** (escouade, groupe, section, compagnie) :
ce sont eux qui n'ont pas de sous-échelons, donc leur composition interne n'est
lisible nulle part dans l'arbre. Y indiquer typiquement :

- la **composition en rôles** de l'escouade / de l'équipe (chef, tireur d'appui,
  servant, opérateur radio…), les grades quand la source les donne ;
- l'**articulation interne** d'une compagnie qui n'a pas de sous-unités déclarées
  (« trois sections de tir identiques + une section d'appui ») ;
- une **particularité de service** : réservistes, unité non complétée en temps de
  paix, matériel hétérogène, unité d'apparat, mise sur pied à la mobilisation.

Aux échelons supérieurs, une phrase de synthèse ou une exception notable
(« bataillon mixte chars / infanterie blindée », « seule unité de la division dotée
de X ») — rien si la formation n'a aucune particularité connue. **Ne jamais inventer
de contexte** : pas de phrase creuse générée pour remplir le champ, l'information
vient de la source ou de Florian.

Mentionner ici, le cas échéant, les lignes de TOE laissées vides faute d'acronyme
(§ 7.2), pour que le trou reste visible dans le fichier livré.

### 7.5 — `shortName` : acronymes en priorité, numéro d'unité inclus

Le `shortName` est **la forme acronymique** de l'unité, et il porte son numéro ou
sa lettre d'ordre. Il remplace l'abréviation « par abréviation du rôle » de la
Règle 2 quand un code `/acronyme` existe pour la formation.

Structure : `{numéro ou lettre} {ÉCHELON}-{TYPE}`

| Exemple | Lecture |
|---|---|
| `23e CIE-INF` | 23e compagnie d'infanterie |
| `"A" BT-INF` | bataillon d'infanterie « A » |
| `"B" BT-ARM` | bataillon blindé « B » |

- Numéro ordinal en français (`1ère`, `2e`, `23e`), lettre de désignation entre
  guillemets droits (`"A"`), conformément aux exemples fournis par Florian.
- Type de formation accolé à l'échelon par un tiret. **Le code exact se lit dans
  `../acronyme/references/groupements.md` § Types d'unité au moment de l'écriture** —
  ne pas se fier à une liste mémorisée ni aux codes vus dans un ORBAT antérieur.
- Une garnison éventuelle reste séparée par `" — "` (Règle 2).
- Le suffixe `Ø` de la Règle 3 s'ajoute en fin, après tout le reste.

⚠️ **Piège `BT` / `BAT` — tranché le 2026-08-09.** `BT` = **Bataillon** (forme
officielle, `BN` valide en lecture) ; `BAT` = **Batterie** (`BTE` valide). Les
premiers exemples fournis pour cette règle écrivaient `BAT-INF` pour un bataillon
d'infanterie — c'était une erreur, corrigée ci-dessus. Ne jamais écrire `BAT` pour
un bataillon. Voir `../acronyme/decisions.md` § 6, entrée 2026-08-09.

⚠️ **Ne pas non plus recopier les codes de type depuis un vieil ORBAT :** `-B` pour
blindé est déprécié (`ARM` officiel depuis le 2026-08-04, `-B` collisionne avec
Bâtiment/Chenillé), d'où `BT-ARM` et non `BT-B` dans la table ci-dessus. Relire
`../acronyme/references/groupements.md` § Types d'unité à chaque écriture.

### 7.6 — `name` : français lisible, sans vocabulaire d'abréviations maison

Le nom long reste **en français lisible** — c'est ce qui le distingue du `shortName`,
qui est la forme codée. Il doit rester compréhensible sans décodeur.

> 🔴 **Table d'abréviations de prose supprimée (août 2026).** Ce paragraphe portait
> jusqu'ici une liste d'abréviations françaises propres à ce skill (`Cie`, `Bat`,
> `Rgt`, `Div`, `Bde`, `EM`, `Esc`, `Bie`, `Plt`, `Sect`, `Inf`, `Bld`, `Méca`, `Art`,
> `Rec`, `Gén`, `Trans`), présentées comme « pas des acronymes v4 » et donc exemptées
> de la source unique. **Florian a supprimé cette dérogation** : elle constituait un
> second vocabulaire concurrent, entretenu nulle part, et c'est exactement le mode de
> panne que la source unique existe pour empêcher (cf. les codes périmés de la
> Règle 2). Ne jamais la réintroduire, même partiellement.

**Deux écritures admises pour `name`, et deux seulement :**

1. **Mots français entiers** — `"23e Compagnie d'Infanterie"`, `"État-Major"`,
   `"1er Bataillon Blindé"`, `"Section d'Appui"`. C'est la forme par défaut : le
   `name` n'a pas vocation à être compact, le `shortName` est là pour ça.
2. **Code officiel de `orbat-tools:acronyme`**, si Florian veut une forme codée dans
   `name` aussi — invoquer le skill et prendre le code tel quel (`CIE`, `BT`, `REG`,
   `DIV`, `BGE`, `INF`, `ARM`, `ART`, `GEN`…, à lire dans
   `../acronyme/references/groupements.md` au moment de l'écriture).

**Jamais de troisième voie.** Pas de forme intermédiaire inventée à la volée parce
qu'un nom paraît long. Si la formulation complète gêne vraiment et qu'aucun code
n'existe pour l'abréger, c'est un cas Règle 7 § 7.2 → question à Florian.

Rester cohérent à l'intérieur d'un même ORBAT : ne pas mélanger les deux écritures
d'une unité à l'autre.

### 7.7 — Jamais répéter le nom de la formation mère

Prolonge la Règle 1 (pas de parenthèses de parenté) en interdisant aussi la
répétition **hors parenthèses**. La position dans l'arbre porte déjà l'appartenance.

❌ À ne pas faire :
```
DBA
├─ État Major DBA
├─ 1ère Cie DBA
└─ 2e Cie DBA
```

✅ À faire :
```
DBA
├─ EM
├─ 1ère Cie
└─ 2e Cie
```

Vaut pour `name` **et** `shortName`, à tous les niveaux (une section sous la 1ère
compagnie ne reprend ni « 1ère Cie » ni « DBA »). Seule exception : si la source
elle-même désigne officiellement l'unité par un nom composé indissociable, le
garder verbatim et expliquer pourquoi en `description`.

## Règle 8 — Contrôle de conformité à la source, avant toute livraison

Établie par Florian (août 2026) comme **comportement par défaut**, sans qu'il ait à la
redemander. Elle s'ajoute à `validate.py`, qui ne contrôle que la **structure** du
fichier (schéma, références de catalogue, sidc) et ne sait rien de la **source**. Un
ORBAT peut être structurellement parfait et faux sur tous les effectifs.

> 🔴 **Aucun ORBAT n'est livré sans cette passe.** « J'ai fini de construire » n'est pas
> un état livrable : c'est le moment où le contrôle commence. Livrer sans l'avoir fait,
> ou en le mentionnant sans l'avoir réellement déroulé, est la faute la plus grave de
> ce skill — Florian ne peut pas la détecter sans refaire le travail lui-même.

### 8.1 — Quand

À chaque fois qu'un travail de génération ou de modification est réputé **terminé**, et
avant `present_files` :

- création d'un ORBAT complet (Tâche 4) ;
- ajout, suppression ou remaniement d'unités dans un ORBAT existant ;
- restructuration (`condense_orbat.py`, `group_units.py`, agrégation d'échelons) ;
- toute édition de masse des `count` (`equipment`, `personnel`, `supplies`).

Après une correction issue du contrôle, **le contrôle se rejoue** : une correction
peut en casser une autre (typiquement un total parent recalculé).

### 8.2 — Quoi vérifier — table de réconciliation source ↔ fichier

Reprendre la **source** (document, PDF, tableau, message de Florian) et confronter
ligne à ligne. Ne jamais contrôler le fichier « de mémoire » de ce qu'on croit avoir
écrit : relire le JSON produit.

| # | Contrôle | Méthode |
|---|---|---|
| 1 | **Totaux généraux** — effectifs et matériel de l'ensemble | `python3 scripts/aggregate.py <fichier.json> --kind all`, comparer aux totaux de la source quand elle en donne |
| 2 | **Totaux par grande formation** | `aggregate.py <fichier.json> --unit "<nom>" --kind all` sur chaque unité majeure, comparé au TOE de la source |
| 3 | **Effectifs/quantités des feuilles** | chaque unité terminale relue contre sa ligne de source (c'est là que les erreurs de saisie se logent) |
| 4 | **Complétude structurelle** | nombre de sous-unités à chaque échelon = celui de la source ; aucune unité oubliée, aucune inventée |
| 5 | **Échelons** | l'échelon attribué correspond à celui de la source (⚠️ piège FR/EN « Section », Règle 4) |
| 6 | **Codes attestés** | tout code de `equipment`/`personnel` existe dans `orbat-tools:acronyme` (Règle 7 § 7.1) et dans le catalogue racine du fichier |
| 7 | **Catalogues** | toute entrée de catalogue est réellement utilisée, et toute entrée utilisée est déclarée ; description commençant par la désignation réelle (Règle 5) |
| 8 | **Nommage** | pas de parenthèses dans `name` (Règle 1), `shortName` présent partout (Règle 2), pas de répétition de la formation mère (§ 7.7) |
| 9 | **Lacunes assumées** | les lignes laissées vides faute d'acronyme (§ 7.2) sont bien mentionnées en `description` (§ 7.4) |
| 10 | **Symboles (`sidc`)** | icône cohérente avec le **rôle réel** et l'**époque** de la source (`symbologie.md`) ; échelon du sidc = échelon de l'unité ; codes non attestés au `sidc_dictionary.json` signalés |
| 11 | **Structure** | `python3 scripts/validate.py <fichier.json>` → 0 erreur |

Quand la source **ne donne pas** un chiffre (TOE non détaillé, document partiel), ce
n'est pas un écart : c'est une **lacune de source**, à distinguer explicitement d'une
erreur dans le rapport (§ 8.4). Ne jamais combler une lacune de source par une
estimation silencieuse.

### 8.3 — Corriger

Tout écart constaté se corrige **avant** la livraison, sans demander l'autorisation :
c'est une erreur de construction, pas une décision de conception. Puis rejouer le
contrôle (§ 8.1).

Deux cas seulement ne se corrigent pas d'office, parce qu'ils engagent un choix :

- **la source est ambiguë ou se contredit** (deux chiffres différents pour la même
  unité, effectif « théorique » vs « réel ») → ne pas trancher seul, remonter à Florian ;
- **corriger impliquerait d'inventer un acronyme** → cas Règle 7 § 7.2.

### 8.4 — Rapport de contrôle à la livraison — obligatoire

La livraison s'accompagne **toujours** d'un compte rendu court, même quand tout est
conforme. Trois blocs, dans cet ordre, et on n'en omet aucun :

```
Contrôle de conformité à la source
✅ Vérifié : <ce qui a été confronté et concorde — totaux, effectifs, structure>
⚠️ Corrigé : <écarts trouvés ET corrigés, avec la valeur avant → après>
🔴 Non résolu : <écarts subsistants, lacunes de source, cas en attente d'arbitrage>
```

- Le bloc `⚠️ Corrigé` est **une information due à Florian**, pas un aveu à masquer :
  il lui dit où la source et la première lecture divergeaient.
- Le bloc `🔴 Non résolu` est **la raison d'être de la règle**. Tout ce qui n'a pas pu
  être vérifié ou corrigé y figure explicitement — y compris « la source ne donne pas
  les effectifs de telle compagnie ». Un silence sur ce point vaut affirmation de
  conformité.
- Si un bloc est vide, l'écrire quand même avec « néant » : l'absence de bloc est
  ambiguë, « néant » ne l'est pas.

## Implémentation type

Pour une génération programmatique (Python), dériver `shortName` en une passe
finale sur l'arbre entier plutôt qu'en argument séparé à chaque appel de
`make_unit` : une liste ordonnée de règles `(motif du nom complet → abrégé)`,
appliquée du motif le plus spécifique au plus générique, avec extraction/
réinjection préalable d'un éventuel suffixe " — garnison". Voir l'exemple
`make_shortname()` / `apply_shortnames()` développé pour l'ORBAT France 1980
(script `build_france_1980.py` et bibliothèque `templates_1980.py` de Florian).
