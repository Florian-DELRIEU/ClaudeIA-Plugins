# Symbologie militaire — construction des icônes et contexte historique

Complément de `sidc.md`, qui donne la **grammaire du code** (les 20 chiffres).
Ce fichier-ci donne le **sens** : comment un symbole se construit, d'où viennent
les formes, et surtout **comment l'époque de la source change le symbole à
choisir** pour un même mot.

Établi en août 2026 après que Florian a constaté des erreurs récurrentes
d'attribution d'icônes sur les ORBAT qu'il fournit.

> 🔴 **Le mot ne détermine pas le symbole. Le mot + l'époque + le rôle réel le
> déterminent.** « Cavalerie » en 1914 et « Cavalry » en 1975 ne désignent pas la
> même chose et ne prennent pas la même icône. C'est l'erreur n°1 de ce domaine,
> et elle est invisible pour qui ne connaît pas la période.

---

## 1. Anatomie d'un symbole — les cinq couches

Un symbole d'unité n'est jamais un dessin unique : c'est un **empilement de
couches**, chacune codée par une position différente du SIDC. Les lire séparément
est la seule façon de ne pas se tromper.

| Couche | Ce qu'elle dit | Où elle est dessinée | Position SIDC |
|---|---|---|---|
| **Cadre** (*frame*) | identité + domaine + statut | le contour | 3-4 (identité), 5-6 (set), 7 (statut) |
| **Icône principale** | la **fonction** de l'unité (infanterie, artillerie, génie…) | centre du cadre | 11-16 |
| **Secteur 1** | une **capacité** (blindé, tireurs d'élite, franchissement…) | partie **haute** du cadre | 17-18 (mod 1) |
| **Secteur 2** | la **mobilité** (roues, chenilles, aéroporté, montagne, amphibie…) | partie **basse** du cadre | 19-20 (mod 2) |
| **Amplificateur d'échelon** | la taille de l'unité | **au-dessus** du cadre | 9-10 |

Deux couches supplémentaires, souvent oubliées :

- **Position 8 — QG / Task Force / Leurre.** Ce n'est pas une icône mais une
  altération du cadre (hampe de QG, crochets de task force, cadre pointillé pour
  un leurre) : `0` rien · `1` leurre · `2` **QG** · `3` QG leurre · `4` task force
  · `5` TF leurre · `6` **QG de task force** · `7` QG de TF leurre.
- **Position 7 — statut.** Plus riche que présent/planifié : `0` présent ·
  `1` planifié/anticipé · `2` présent pleinement capable · `3` **endommagé** ·
  `4` **détruit** · `5` plein à capacité. Utile pour un ORBAT de scénario avec
  pertes.

### Le champ 9-10 n'est pas toujours un échelon

Le même champ encode **soit** l'échelon d'une unité, **soit** la mobilité d'un
matériel (symbol set `15`, équipement terrestre). Le premier chiffre tranche :

| 1er chiffre | Signification du couple |
|---|---|
| `1` | échelon, brigade et en dessous (`11` équipe → `18` brigade) |
| `2` | échelon, division et au-dessus (`21` division → `26` commandement) |
| `3` | **mobilité terrestre** : `31` roues tout-chemin · `32` roues tout-terrain · `33` **chenillé** · `34` roues+chenilles · `35` **tracté** · `36` rail · `37` **animaux de bât** |
| `4` | mobilité sur neige : `41` engin sur neige · `42` traîneau |
| `5` | mobilité sur eau : `51` barge · `52` amphibie |
| `6` | antenne remorquée (naval) |

⚠️ `37` (animaux de bât) et `35` (tracté) sont les deux codes qui servent le plus
souvent pour du matériel **hippomobile** d'avant 1940 — voir § 3.

---

## 2. D'où viennent les formes — la logique de composition

Le système descend des symboles créés par l'**US Army Corps of Engineers en 1917**,
et les formes de base sont des **pictogrammes d'époque** dont le sens est resté :

| Brique | Forme | Origine | Fonction moderne |
|---|---|---|---|
| **Infanterie** | croix / sautoir (X dans le cadre) | les **bretelles croisées** du fantassin | infanterie |
| **Cavalerie** | **une seule barre diagonale** | la **bandoulière de sabre** du cavalier | cavalerie, puis reconnaissance |
| **Artillerie** | **point plein** (disque) | le **boulet de canon** | artillerie |
| **Blindé** | **ellipse / ovale** | la **chenille vue de profil** | tout ce qui est blindé/chenillé |

**Le principe qui fait tout le reste : on empile les briques.** Un symbole
complexe n'est pas un dessin nouveau, c'est une combinaison lisible :

| Unité | Composition | Lecture |
|---|---|---|
| Infanterie blindée / mécanisée | ovale **+** croix | des fantassins qui montent dans des engins blindés |
| Cavalerie blindée / reco blindée | ovale **+** barre diagonale | de la reconnaissance montée sur blindés |
| Artillerie automotrice | point **+** ovale | un canon sur châssis blindé |
| Chasseur de chars | brique antichar **+** ovale | de l'antichar sur châssis blindé |
| Infanterie portée | croix **+** brique de mobilité roues | des fantassins transportés par camions |

Corollaire pratique : devant une unité inconnue, **décomposer avant de chercher**.
« Que fait-elle ? » donne l'icône principale ; « avec quoi ? » donne le secteur 1 ;
« comment se déplace-t-elle ? » donne le secteur 2. Trois questions, trois couches.

---

## 3. Contexte historique — la source d'erreur principale

**Un ORBAT se date avant de se symboliser.** Le même mot change de sens au cours
du siècle, et le symbole doit suivre le **rôle réel**, jamais l'étiquette.

### 3.1 Le cas « cavalerie » — l'exemple canonique

| Période | Ce que « cavalerie » désigne réellement | Symbole attendu |
|---|---|---|
| XIXe s. → ~1914 | **des chevaux.** Choc, exploitation, reconnaissance montée | cavalerie montée (*horse cavalry*), mobilité animale |
| Entre-deux-guerres | **transition**, souvent mixte dans une même armée : régiments à cheval **et** premiers éléments motorisés/blindés | dépend de l'unité précise — ne jamais généraliser à l'armée entière |
| ~1940 → aujourd'hui | **des blindés.** Le nom « cavalerie » est conservé pour la tradition, la monture a disparu | reconnaissance blindée / *armored cavalry* |

Le standard OTAN conserve **les deux familles côte à côte** — *Horse Cavalry* et
*Horse Reconnaissance* d'un côté, *Armoured Cavalry / Armoured Reconnaissance*
(chenillé, à roues, avec ou sans canon) de l'autre — précisément parce que les
deux ont existé et existent encore. Le choix entre les deux **ne se déduit pas du
nom de l'unité**, seulement de sa date et de son équipement réel.

> Un « 2e Régiment de Hussards » de 1812, de 1914 et de 1985 sont **trois unités
> de nature différente** portant le même nom : cavalerie légère à cheval, cavalerie
> à cheval en voie d'obsolescence, régiment de reconnaissance blindé. Trois
> symboles différents.

### 3.1 bis — Consigne de Florian : la cavalerie, c'est la diagonale seule

*Actée le 2026-08-18, après qu'un ORBAT a été livré avec une icône composite.*

Une unité de cavalerie se symbolise par la **diagonale nue**, rien d'autre.

| Ce qu'il faut écrire | Entité | Icône | Quand |
|---|---|---|---|
| ✅ **Cavalerie / reconnaissance** | `121300` | **diagonale seule** | **cas par défaut de toute cavalerie**, quelle que soit l'époque |
| ⚠️ Reconnaissance blindée | `120501` | ellipse **+** diagonale | seulement si l'unité est **réellement montée sur blindés** |
| ❌ Blindés / chars | `120500` | **ellipse** | jamais pour une unité de cavalerie — c'est l'icône des chars |
| 🔎 Reconnaissance montée | `121303` | *(HM RECON)* | piste pour la cavalerie **à cheval** d'avant 1940 — **à confirmer par rendu** |

**La règle simple :** ne pas empiler de briques que la source ne justifie pas. Le nom
« cavalerie » à lui seul ne donne droit qu'à la diagonale ; l'ellipse ne s'ajoute que
si l'unité a réellement des blindés, et la mobilité (roues/chenilles) va au secteur 2,
pas dans l'icône principale.

> ⚠️ **Le dictionnaire porte le mauvais précédent.** Les Cuirassiers, Dragons,
> Chasseurs et Spahis y sont codés `120500` (blindés), le 3e Hussards `120501`. Ces
> entrées sont **antérieures à cette consigne et ne doivent pas être imitées**. Les
> bonnes entrées de référence sont en `121300` — *Peleton de reconnaissance*,
> *10e Bataillon de Hussards*. C'est un cas concret de la mise en garde générale :
> un SIDC repris d'un vieil ORBAT se relit, il ne se recopie pas.

### 3.2 Les autres pièges d'époque, même mécanique

| Terme | Piège | Ce qui tranche |
|---|---|---|
| Dragons, Hussards, Chasseurs, Uhlans, Cuirassiers | noms de cavalerie conservés bien après la disparition du cheval | la date + le matériel réel de l'ORBAT |
| **Artillerie** avant ~1940 | très majoritairement **tractée**, souvent **hippomobile** — pas automotrice | mobilité `35` tracté ou `37` animaux de bât, pas de brique blindée |
| **Infanterie « portée » / motorisée** | transportée par camions non blindés ≠ mécanisée (engins blindés) | présence ou non de blindage |
| **Panzergrenadier** (all.) | c'est de l'**infanterie mécanisée**, pas des blindés | rôle réel |
| **« Char » 1917-1918** | engin d'accompagnement d'infanterie, doctrine sans rapport avec un MBT | l'époque |
| **Train / colonnes** avant 1940 | logistique **hippomobile** | mobilité animale, pas roues |
| **Reconnaissance** avant 1914 | assurée par la cavalerie elle-même, pas par une arme distincte | ne pas créer une unité de reco moderne là où la source dit « cavalerie » |
| **Section** (source anglaise) | ~8-10 hommes = **escouade** | l'effectif, pas le mot — voir `sidc.md` |

### 3.3 La règle de conduite

1. **Dater la source d'abord.** Année, armée, théâtre. C'est le préalable à toute
   attribution de symbole, pas un détail de confort.
2. **Traduire le nom en rôle réel**, en s'appuyant sur l'équipement listé dans
   l'ORBAT quand il l'est — un régiment doté de chevaux n'est pas un régiment doté
   d'AMX-30, quel que soit son nom.
3. **En cas de doute sur l'époque ou le rôle : demander à Florian.** Ne jamais
   trancher au jugé — une erreur d'icône historique est indétectable pour qui n'a
   pas la période en tête, donc elle survit dans le fichier.
4. **Documenter le choix** en `description` quand il n'est pas évident
   (« régiment de tradition Hussards, équipé en reconnaissance blindée en 1985 »).

---

## 4. Erreurs constatées — à ne pas reproduire

Relevées par Florian sur des ORBAT livrés :

- **Traduire « cavalerie » par un symbole blindé sans regarder l'année.** L'erreur
  la plus fréquente et la plus coûteuse.
- **Alourdir l'icône de cavalerie.** Constaté le 2026-08-18 : symbole composite livré
  là où Florian attend la **diagonale seule** (`121300`). Ne pas ajouter l'ellipse des
  blindés à une unité dont seul le *nom* évoque la cavalerie — § 3.1 bis.
- **Coller une icône sur le nom plutôt que sur la fonction.** Un « Régiment de
  Dragons » n'est pas symbolisé « dragons » : il est symbolisé selon ce qu'il fait
  à la date de l'ORBAT.
- **Oublier que le secteur 2 existe.** Une infanterie de montagne, aéroportée ou
  amphibie a la **même icône principale** que l'infanterie ordinaire — c'est le
  secteur 2 qui les distingue. Omettre le modificateur produit un symbole qui n'est
  pas faux mais qui perd toute l'information.
- **Confondre capacité (secteur 1) et mobilité (secteur 2).** « Blindé » est une
  capacité, « à roues » / « chenillé » est une mobilité ; les deux se combinent
  presque toujours et vont dans deux champs différents.
- **Donner une entité propre à un état-major.** Un QG hérite de l'entité de son
  unité mère et se marque par la **position 8** (`2` = QG), pas par une icône
  spéciale — voir `sidc.md`.
- **Recopier un SIDC d'un ORBAT antérieur sans le relire.** Les codes des vieux
  fichiers de Florian contiennent des erreurs connues (échelons `13`/`14` confondus
  avant le 2026-08-09).

---

## 5. Procédure obligatoire d'attribution d'un symbole

À dérouler pour **chaque** unité, à l'écriture comme à la relecture :

1. **Dater la source** (§ 3.3) — une fois pour l'ORBAT entier, avant de commencer.
2. **Déterminer le rôle réel** de l'unité, pas son nom.
3. **Chercher le SIDC dans `sidc_dictionary.json`** (499 entrées extraites des
   ORBAT de Florian) avec `scripts/sidc_lookup.py "<terme>"` ou `--code <entité>` —
   c'est la source de vérité empirique, cohérente avec orbat-mapper.app. Un code déjà employé pour ce type d'unité se réutilise tel quel.
4. **Décomposer en couches** (§ 1) : icône principale, puis secteur 1 (capacité),
   puis secteur 2 (mobilité), puis échelon.
5. **Ne jamais inventer une entité.** Si aucun code du dictionnaire ne convient :
   partir de l'entité la plus proche et n'ajuster que les modificateurs, **en le
   signalant explicitement à Florian**. Une entité forgée à la volée est une erreur
   silencieuse — elle affiche un symbole plausible mais faux.
6. **Vérifier le rendu.** Un SIDC ne se valide pas sur le papier : il s'affiche.
   En cas de doute sur un code non attesté au dictionnaire, le dire dans le rapport
   de livraison (Règle 8, bloc 🔴) plutôt que de le présenter comme acquis.

> Historique des décisions de symbologie (icône cavalerie, construction des icônes) :
> `historique-decisions.md`.

> ⚠️ **Limite connue de ce fichier.** Les codes d'entité des familles historiques
> (cavalerie montée, artillerie hippomobile) ne sont pas attestés dans les sources
> ouvertes consultées en août 2026. **Une piste existe cependant dans
> `sidc_dictionary.json` : l'entité `121303`**, employée pour des unités notées
> *HM RECON / HM REC SQD / HM REC SEC* — « HM » se lisant très probablement
> *horse-mounted*. C'est un sous-type de `1213` (reconnaissance), donc cohérent avec
> la diagonale. **À confirmer par rendu avant de l'employer**, et à journaliser une
> fois validé par Florian.
> Tant qu'ils n'y sont pas, ils relèvent du point 5 : proposer, signaler, faire
> valider — jamais affirmer. Enrichir le dictionnaire à chaque code confirmé par
> Florian.

---

## Sources

- [SIDC identifiers in MIL-STD-2525D — Carmenta](https://docs.carmenta.com/pages/milstd2525d_tactical_sidc.html) — structure des 20 chiffres, tables identité/statut/QG/échelon-mobilité
- [Military Symbols Study Guide — MGRS Mapper](https://mgrs-mapper.com/blog/military_symbols_fundamentals/) — cadre, icônes principales, secteurs 1 et 2
- [NATO Map Symbols — Army.ca Wiki](https://army.ca/wiki/index.php/NATO_Map_Symbols) — familles cavalerie/reconnaissance, dont *Horse Cavalry* et *Horse Reconnaissance*
- [Armoured cavalry — Wikipedia](https://en.wikipedia.org/wiki/Armoured_cavalry) — remplacement du cheval par le blindé, conservation du nom
- [NATO Joint Military Symbology — Wikipedia](https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology) — origine 1917, US Army Corps of Engineers
- [Basic Military Map Symbols — US Army Center of Military History](https://www.history.army.mil/books/wwii/11-4/symbols.htm) — briques de base et composition
- [MIL-STD-2525D (document officiel)](http://www.mapsymbs.com/MilStd2525D.pdf) — référence normative
