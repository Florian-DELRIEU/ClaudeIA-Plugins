---
name: orbat-acronymize
description: "Convertit un ORBAT JSON entier (format orbat-mapper.app) des noms réels de matériel et de personnel vers les codes du système /acronyme (V4) : renomme les catalogues `equipment`/`personnel`, propage dans tout l'arbre et les timelines, pose les légendes. Déclencher IMPÉRATIVEMENT dès que Florian tape /orbat-acronymize, fournit un ORBAT JSON et demande de convertir, renommer ou remplacer les noms de véhicules/troupes par leurs acronymes, ou dit \"convertis cet ORBAT en acronymes v4\", \"acronymise ce fichier\", \"remplace les noms de matériel par leurs codes\", \"renomme les unités de ce JSON avec le système d'acronymes\". C'est ce skill, et non `acronyme` (qui identifie un code à la fois), qui traite la conversion d'un ORBAT entier ; il consulte `acronyme` (codes, lexiques) et `orbat-json` (format) avant toute conversion. Les noms d'unités (`name`/`shortName`) relèvent d'`orbat-json`.\n"
---

# Acronymisation d'un ORBAT existant

## Objectif

Prendre un fichier ORBAT JSON (format `orbat-mapper.app`, voir skill `orbat-json` /
`references/format.md`) et remplacer les **noms** des entrées des catalogues
`equipment` (véhicules/matériel) et `personnel` (troupes) par leur code du
système `/acronyme` V4, en propageant le changement partout où ces noms sont
référencés dans l'arbre d'unités.

Ce skill ne modifie **que les catalogues et leurs références** — pas les noms
des unités/formations (`Unit.name` / `Unit.shortName`), qui relèvent des
conventions du skill `orbat-json` (`references/naming.md`), sauf demande explicite
de Florian en ce sens (y compris les titres enrichis de l'étape 6, désactivés par
défaut).

> 🔴 **Aucun code n'entre au lexique sans Florian** (arbitrage du 2026-10-10,
> alignement sur `orbat-json/references/naming.md` §§ 7.1-7.2). Composer un code
> à partir d'éléments **déjà attestés** (Type, rôle, suffixes, gabarit, notation
> numérique documentés) reste permis. Mais **tout code absent de
> `lexique.json` / `lexique-40k.json` est signalé à Florian** comme tel, et
> n'est écrit dans un lexique **qu'après sa validation explicite**. Pas d'élément
> de vocabulaire nouveau, pas de code forgé via `METHODE.md` et appliqué sans
> validation, pas d'écriture automatique dans le lexique.

## Pipeline

1. **Localiser le fichier.** Si Florian n'a pas donné de chemin, demander le
   fichier ORBAT JSON à traiter.

2. **Lire les catalogues racine** `equipment` et `personnel` du fichier
   (liste de `{name, description}` — voir skill `orbat-json`, `references/format.md`,
   section "Enveloppe (racine)"). Ce sont les `name` de ces catalogues qu'il
   faut convertir — pas les noms d'unités. Ne jamais remettre dans le mapping une
   entrée qui porte déjà un code v4 valide (déjà acronymisée).

3. **Partir du brouillon automatique** :
   ```
   python3 scripts/draft_mapping.py <orbat.json> [-o mapping_brouillon.json] [--40k]
   ```
   Il propose un code pour chaque nom de catalogue **trouvé dans le lexique**
   (`lexique.json`, ou `lexique-40k.json` avec `--40k` pour un univers fictif) et
   range tous les autres dans `_a_valider` — il n'invente jamais de code.

4. **Résoudre les noms de `_a_valider`** en suivant le skill `acronyme` (à invoquer) :
   - **Matériel réel ou univers fictif** (Warhammer 40,000, Cosmotter…) : consulter
     le lexique correspondant — `acronyme/identification/lexique.json` ou
     `lexique-40k.json` — et réutiliser un code existant si le même matériel/châssis
     y figure déjà (cohérence inter-fichiers, règle P5 de `METHODE.md`). Chercher dans
     le lexique **de l'univers de la source** : les deux lexiques sont un choix
     d'organisation (correspondances matériel réel ↔ code d'un côté, matériel fictif ↔
     code de l'autre), **pas** une différence de sens — un code signifie la même chose
     partout (règle cardinale n°4 de `acronyme/SKILL.md`, ex. `VB` = véhicule blindé
     chenillé dans les deux). Seule la doctrine d'emploi du matériel décrit peut faire
     choisir un Type plutôt qu'un autre (`chassis-types.md`, « VBCI vs VB — rôle
     combattant vs soutien »).
   - Sinon, le pipeline en 6 étapes de `acronyme/identification/METHODE.md`
     (châssis → Type via `identification/chassis-types.md`, rôle/armement →
     suffixes, gabarit, fusions, décisions établies) sert à **proposer** un code
     composé d'éléments attestés — jamais à l'adopter seul : le code est marqué
     « hors lexique, à valider » dans le tableau de l'étape 5.
   - **Châssis partagé combat/soutien** : quand plusieurs variantes partagent le même
     châssis (ex. plusieurs dérivés d'un même transport de troupes), vérifier
     laquelle combat réellement aux côtés d'une escouade (garde le Type de combat
     complet, ex. `VBCI`/`VBTT`) et lesquelles sont des variantes de soutien
     non-combattantes (sanitaire, dépannage, génie/logistique, artillerie, mortier,
     AA automoteur — dégradent vers `VB` générique, voir `chassis-types.md`). Ne
     jamais appliquer le Type de combat à une variante de soutien par simple réflexe
     de cohérence de châssis.
   - Personnel : `acronyme/identification/personnel.md` (échelon
     escouade/équipe/binôme + rôle dominant).
   - Ne jamais deviner sans consulter ces fichiers — le principe du châssis (une
     même plateforme garde le même Type à travers ses variantes) est fréquemment
     source d'erreur si on code « à l'oreille ».
   - Aucun code défendable → laisser le nom d'origine et le signaler (cas
     `naming.md` § 7.2), plutôt qu'approximer.

5. **Présenter le mapping complet** `{nom_original: code_v4}` à Florian sous forme
   de tableau (nom d'origine → code proposé → source : *lexique* / *hors lexique,
   composé* → brève justification) **avant d'écrire quoi que ce soit**. Signaler les
   cas ambigus (plusieurs codes défendables) plutôt que de trancher silencieusement.
   Florian valide, corrige ou écarte chaque ligne hors lexique.

6. **Appliquer le mapping validé** avec le script fourni :
   ```
   python3 scripts/apply_rename_map.py <orbat.json> <mapping.json>
   ```
   Écrire d'abord `mapping.json` (le mapping validé, sans la clé `_a_valider`) dans
   un fichier temporaire, puis lancer le script. Il :

   a. **Renomme les entrées de catalogue** (en conservant l'ancien nom en tête
      de leur `description`, naming.md Règle 5) et propage le renommage à toutes
      les références de l'arbre : `equipment[].name` / `personnel[].name` **et**
      les `update`/`diff` des timelines `state[]`.
      **Convergence gérée** : si plusieurs noms d'origine partent vers le même
      code (deux camions → `VU-LOG`), le script fusionne lui-même — une entrée
      de catalogue (`"Camion A / Camion B"`), une ligne par unité à quantité
      cumulée, timelines réexprimées en deltas pour que les quantités restent
      exactes à toute date. Il affiche la liste des codes fusionnés.

   b. **Annote la `description` de chaque échelon** avec la légende canonique
      (`**CODE : Désignation réelle**`, Équipement / Personnel séparés, module
      `orbat-json/scripts/legends.py`) des codes présents dans son sous-arbre.
      Un échelon ne cite que les désignations **réellement présentes** chez lui :
      un groupe qui n'a que des VAB affiche `**VBTT : VAB**`, même si `VBTT`
      couvre aussi des VBL ailleurs. La phrase de contexte déjà présente dans la
      `description` est conservée.

   c. **Titres enrichis — seulement avec `--titres`** (opt-in, sur demande de
      Florian ; désactivés par défaut depuis le 2026-10-10, cohérent avec
      `naming.md` § 7.6 qui réserve `name` au libellé lisible de l'unité). Si un
      échelon ne porte, EN PROPRE, qu'un seul type de véhicule (`equipment`,
      jamais `personnel`), son `name` est complété avec le nom réel du véhicule,
      ex. `"Escadron"` → `"Escadron de VAB"`. Sans effet sur un échelon mixte ou
      purement organisationnel. `--no-titles` reste accepté, sans effet.

   d. **Valide le résultat** (mêmes contrôles que `orbat-json/scripts/validate.py`)
      et affiche le rapport ; code de sortie 1 s'il reste une erreur.

   Comportement idempotent : relancer le script sur un fichier déjà traité ne
   duplique ni les légendes ni les suffixes de titre. Il importe les modules
   partagés du skill `orbat-json` (même plugin), localisés automatiquement ;
   `ORBAT_TOOLS_ROOT` = racine du plugin s'il a été copié ailleurs.

   **Le script écrase le fichier d'origine par défaut** (comportement voulu) —
   `--dry-run` pour un aperçu, `--output` pour une copie séparée, `--no-legend`
   pour ne pas poser les légendes. Détail : `--help`.

7. **Lexique — uniquement les codes validés.** Proposer à Florian les paires
   désignation réelle ↔ code v4 **qu'il a explicitement validées** à l'étape 5 et
   qui manquent au lexique ; ne les écrire dans `acronyme/identification/lexique.json`
   (matériel réel) ou `lexique-40k.json` (univers fictif) qu'après son accord, pour
   que les prochains ORBAT réutilisent les mêmes codes (règle P5). Rien n'est
   journalisé automatiquement.

8. **Lire le rapport de validation** affiché par le script (étape 6 d) : 0 erreur
   attendue. Toute retouche manuelle ultérieure se revalide avec
   `python3 ../orbat-json/scripts/validate.py <orbat.json>`.

   > 🔴 **La convergence de codes reste le piège n°1** (deux modèles de camion →
   > `VU-LOG`). `apply_rename_map.py` fusionne lui-même les lignes et le
   > catalogue ; mais une correction **à la main** après coup peut réintroduire
   > deux lignes du même code — `validate.py` le détecte. **Ne jamais livrer une
   > conversion sans rapport de validation à 0 erreur.**

9. **Résumer** à Florian : nombre d'entrées renommées, nombre de références
   propagées, codes hors lexique validés (et ceux laissés en attente ou écartés),
   ajouts au lexique effectués avec son accord, résultat de la validation.

## Points d'attention

- Un même `name` de catalogue peut être référencé par de nombreuses unités à
  travers l'arbre — c'est pour ça que le renommage passe toujours par le
  script plutôt qu'un remplacement manuel unité par unité.
- Ne jamais renommer une entrée de catalogue qui porte déjà un code v4
  valide — vérifier via un motif simple (présence de séparateurs `-`/`/`/`.`
  typiques du système) et, au besoin, `../acronyme/references/INDEX.md`.
- Si Florian veut aussi convertir les noms d'unités/formations (`Unit.name`,
  `shortName`), c'est hors du périmètre par défaut de ce skill : rediriger vers
  `orbat-json/references/naming.md` (Règle 4 pour les mots d'échelon, § 7.5 et
  `orbat-json/scripts/short_names.py` pour les `shortName`, § 7.6 pour `name`) et
  vers `orbat-nommage` pour le vocabulaire réel des échelons — c'est un renommage
  de nature différente (échelon d'organisation, pas matériel/personnel).
