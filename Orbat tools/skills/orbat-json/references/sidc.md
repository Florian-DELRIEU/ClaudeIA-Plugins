# SIDC — code symbole APP-6D / MIL-STD-2525D (20 chiffres)

Le `sidc` encode le symbole militaire d'une unité. Structure **vérifiée** sur les
fichiers de Florian. Pour lire un symbole depuis une image, on identifie ces champs
visuellement puis on les recompose ; pour écrire, on assemble les 20 chiffres.

> 📖 **Ce fichier donne la grammaire du code. Pour le *sens* — comment un symbole se
> construit en couches, d'où viennent les formes, et surtout comment l'époque de la
> source change le symbole à choisir — lire `symbologie.md`.** Obligatoire avant
> d'attribuer des icônes à un ORBAT historique : « cavalerie » en 1914 et « cavalry »
> en 1975 ne prennent pas le même symbole.

## Positions

```
 1 2 | 3 | 4 | 5 6 | 7 | 8 | 9 10 | 11 12 13 14 15 16 | 17 18 | 19 20
 ver   ctx id   set  st  hq  éch.       entité (icône)     mod1    mod2
```

| Champ | Pos | Valeurs |
|-------|-----|---------|
| Version | 1-2 | `10` (2525D / APP-6D éd.1) |
| Contexte | 3 | `0` réalité · `1` exercice · `2` simulation |
| **Identité** | 4 | `0` pending · `1` inconnu · `2` ami présumé · **`3` ami** · `4` neutre · `5` suspect · `6` hostile |
| **Symbol set** | 5-6 | **`10` unité terrestre** · `11` civil terrestre · `15` équipement terrestre · `20` installation · `01` air · `30` mer surface · `35` sous-marin · `05` espace |
| Statut | 7 | `0` présent · `1` planifié/anticipé · `2` pleinement capable · `3` **endommagé** · `4` **détruit** · `5` plein à capacité |
| HQ/TF/Dummy | 8 | `0` aucun · `1` leurre · **`2` QG** · `3` QG leurre · `4` task force · `5` TF leurre · **`6` QG de task force** · `7` QG de TF leurre |
| **Échelon** | 9-10 | voir table ci-dessous |
| **Entité** | 11-16 | icône principale, 6 chiffres (entité·type·sous-type) |
| Modificateur 1 | 17-18 | **Secteur 1 — capacité** (blindé, tireurs d'élite, franchissement…), dessiné en **haut** du cadre. Ex. `56` mitrailleuse |
| Modificateur 2 | 19-20 | **Secteur 2 — mobilité** (roues, chenilles, aéroporté, montagne, amphibie…), dessiné en **bas** du cadre |

⚠️ **Ne pas confondre les deux secteurs** : « blindé » est une *capacité* (secteur 1),
« à roues » / « chenillé » est une *mobilité* (secteur 2). Les deux se combinent presque
toujours et vont dans deux champs distincts — détail et exemples dans `symbologie.md`.

## Table des échelons (pos 9-10) — vérifiée

| Code | Échelon (FR) | Note |
|------|--------------|------|
| `11` | Équipe / Crew | |
| `12` | Escouade / Groupe | |
| `13` | **Section** (`SEC`) | « grosse escouade » ~15+, élément d'un seul tenant |
| `14` | **Peloton** (`PLT`) | = *platoon* — conteneur, regroupe escouades/équipes/sections |
| `15` | **Compagnie** / Batterie / Escadron | |
| `16` | **Bataillon** | |
| `17` | **Régiment** / Groupement | |
| `18` | **Brigade** | |
| `21` | **Division** | |
| `22` | Corps | |
| `23` | Armée | |
| `24` | Groupe d'armées | |
| `26` | Commandement | |

⚠️ **Le champ 9-10 n'encode un échelon que si son 1er chiffre est `1` ou `2`.** Avec
`3`/`4`/`5`, il encode la **mobilité d'un matériel** (`33` chenillé, `35` tracté,
`37` animaux de bât…) — indispensable pour l'équipement hippomobile d'avant 1940.
Table complète dans `symbologie.md` § 1.

⚠️ **Section et Peloton sont deux échelons distincts (décision du 2026-08-09).**
`SEC` = `13`, `PLT` = `14`. La différence est de **nature**, pas d'effectif : une
section est un élément terminal (un bloc d'hommes, sans sous-éléments), un peloton
est un conteneur qui regroupe plusieurs escouades / équipes / sections. Échelle
complète dans `../acronyme/identification/personnel.md`.

⚠️ **Piège FR/EN, version mécanique.** Une « Section » anglaise (Commonwealth) compte
~8-10 hommes → c'est une **escouade**, donc `SQ` / `12`, jamais `SEC` / `13` qui
commence vers 15. Le nombre tranche seul, sans avoir à connaître la convention.
« Compagnie » reste `15` dans les deux langues.

⚠️ **Fichiers antérieurs au 2026-08-09 :** des sections y ont pu être codées `14`
(les deux échelons étaient alors confondus). Elles se retrouvent au niveau peloton et
faussent toute condensation/agrégation par échelon. La règle vaut pour les **écritures
neuves** ; reprendre un ancien fichier est une opération explicite, à demander.

## Entité (pos 11-16)

6 chiffres = entité · type · sous-type. Pour les unités terrestres (`set=10`), les blocs
les plus courants chez Florian :

| Entité | Signification (d'après usage) |
|--------|-------------------------------|
| `121100` | Infanterie |
| `121000` | Infanterie blindée / mécanisée |
| `121105` | Infanterie mécanisée sur IFV (*MECH IFV DIV/BDE/BN*) |
| `121102` | Infanterie mécanisée sur APC/VAB |
| `120400` | Anti-char (ATGM) |
| `120500` | **Blindés / chars** — icône : **ellipse** (chenille de profil). *TANK BN/BDE, Peleton Char.* ⚠️ **Ne pas y mettre la cavalerie** — voir l'encadré ci-dessous |
| `120502` | Char léger (*152 TANK BN LT*) |
| `120501` | **Reconnaissance blindée** — icône : **ellipse + diagonale**. Réservé à de la reco réellement montée sur blindés |
| `121300` | **Reconnaissance / cavalerie — icône : DIAGONALE SEULE.** ✅ **Forme par défaut de toute cavalerie** (*RECON PLT/SQD/CO, Peleton de reconnaissance, 10e Bataillon de Hussards*) |
| `121303` | Reconnaissance **montée** (*HM RECON — horse-mounted*) — sous-type de `1213`. Piste sérieuse pour la cavalerie à cheval d'avant 1940, **à confirmer par rendu** |
| `120600` | Aviation / opérations aériennes |
| `110600` | Influence / Information |
| `107000` | Police / sécurité (POL) |
| `000000` | Quartier général / regroupement générique (*Comp. Commandement, Etat Majors des Armées de Terre*) |

> 🔴 **Cavalerie = la diagonale seule (`121300`). Consigne de Florian, août 2026.**
> Une unité de cavalerie se symbolise par la **diagonale nue**, sans rien y ajouter.
> Ne pas lui coller l'**ellipse** des blindés (`120500`), ni la forme composite
> **ellipse + diagonale** (`120501`) : cette dernière est réservée à de la
> reconnaissance **réellement montée sur blindés**, pas à une unité qui porte
> simplement un nom de cavalerie.
>
> ⚠️ **Le `sidc_dictionary.json` contient le mauvais précédent** : les régiments de
> Cuirassiers, Dragons, Chasseurs et Spahis y ont été codés `120500` (blindés), et le
> 3e Hussards `120501`. **Ne pas recopier ces entrées** — c'est exactement l'erreur que
> cette consigne corrige. Les entrées correctes à imiter sont celles en `121300`
> (*Peleton de reconnaissance*, *10e Bataillon de Hussards*).
>
> Raisonnement de fond et pièges d'époque : `symbologie.md` § 3.

⚠️ **Il n'existe pas d'entité « état-major » propre.** Un QG de compagnie de chars porte
l'entité de sa compagnie (`120500`), un QG de batterie d'artillerie porte `130300`, etc. :
la sous-unité de commandement **hérite de l'entité du parent**. C'est pourquoi les noms
génériques (`HQ`, `CMD SEC`, `STAFF SEC`, `1 PLT`) apparaissent sous presque toutes les
entités du dictionnaire et **ne doivent jamais servir à déduire une entité**. `000000` est
réservé aux regroupements sans arme dominante.

La liste complète des entités est vaste. **Le dictionnaire réel extrait des ORBAT de
Florian est dans `references/sidc_dictionary.json`** (499 entrées : `sidc` → échelon,
entité, exemples de noms). C'est la première source à consulter pour réutiliser un code
cohérent avec son univers. Pour un type non couvert, partir de l'entité la plus proche
et n'ajuster que les modificateurs, ou demander confirmation à Florian.

## Lire un SIDC

`10031000151211005600` :
`10`·`0`·`3`·`10`·`0`·`0`·`15`·`121100`·`56`·`00`
→ ami, unité terrestre, **compagnie** d'**infanterie**, modificateur **mitrailleuse**.

## Écrire un SIDC

Utiliser `scripts/new_orbat.py:build_sidc(echelon, entity, identity='3')`. Par défaut :
version `10`, contexte réalité, set terrestre `10`, statut présent. Ne renseigner que
l'échelon (nom ou code) et l'entité (6 chiffres), plus modificateurs si besoin.
