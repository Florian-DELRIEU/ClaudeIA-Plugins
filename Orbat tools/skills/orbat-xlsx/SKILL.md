---
name: orbat-xlsx
description: >
  Lecture, écriture, analyse et conversion d'ORBAT (Order of Battle) au
  format tableur **xlsx ODIN / JTDS** (TRADOC G2) : classeur avec feuille
  `UNIT INFO` + feuilles template, équivalent tableur du XML JTDS OBSV4.2.
  Déclencher dès que Florian tape /orbat-xlsx, fournit un `.xlsx` contenant
  une feuille `UNIT INFO`, un XML **JTDS** (`OBSV4.2`), mentionne « ODIN »,
  « TRADOC », « JTDS » ou un « ORBAT en tableur / Excel », ou demande de :
  lire/analyser un ORBAT ODIN, compter le matériel ou le personnel d'une
  unité d'un classeur, créer ou éditer un ORBAT au format xlsx (ajout/
  suppression d'unité, feuille template), valider l'intégrité d'un classeur,
  ou convertir un ORBAT ODIN vers le format JSON orbat-mapper.app.
  Déclencher aussi pour des demandes courtes ("lis ce classeur ODIN",
  "combien de BMP 2 dans la 171 IFV BDE ?", "ajoute un bataillon à ce
  classeur", "convertis cet ORBAT ODIN pour orbat-mapper"). Pour un ORBAT
  déjà au format JSON `type: "ORBAT-mapper"`, c'est le skill `orbat-json`
  qu'il faut.
---

# ORBAT xlsx ODIN — lecture, écriture, édition, conversion (format ODIN/JTDS)

Scission (juillet 2026) de l'ancien skill unique `orbat_maker`, séparé en deux
skills : **`orbat-xlsx`** (ce skill — format tableur ODIN/JTDS) et **`orbat-json`**
(format JSON natif orbat-mapper.app de Florian). Si le fichier fourni est un
`.json` avec `type: "ORBAT-mapper"`, ce n'est pas ce skill — passer à
`orbat-json`.

## Avant tout : connaître le format

**Lire `references/xlsx_format.md` avant de toucher au fichier.** Tout passe par
`scripts/xlsx_orbat.py` — ne jamais parser le classeur à la main.

En une phrase :

> `UNIT INFO` = l'ossature (1 ligne par unité ; `T` = composition prise dans la
> feuille template nommée, `U` = conteneur dont les enfants sont d'autres lignes
> de `UNIT INFO`). Les feuilles template décrivent la composition avec 5 types de
> lignes : `U` unité, `E` plateforme, `W` remorqué, `M` emport, `P` personnel
> (rôle `C` équipage / `P` passager).

## Outil fourni (`scripts/`)

- **`xlsx_orbat.py`** — **format xlsx ODIN** : `read`, `tree`, `agg`, `validate`,
  `tojson`. En bibliothèque : `load`, `expand`, `save`, `add_unit`, `remove_unit`,
  `TemplateBuilder`, `validate`, `to_mapper_json`.
- **`orbat_lib.py`** — présent ici uniquement en support de la conversion
  `tojson` (validation du JSON de sortie via `validate.py`, qui l'utilise
  également). Pour tout travail sur un fichier déjà en JSON orbat-mapper une
  fois converti, basculer sur le skill `orbat-json`, plus complet sur ce format.
- **`validate.py`** — valide le JSON produit par `tojson` (0 erreur attendu).

### Deux pièges à erreurs silencieuses (détaillés dans `xlsx_format.md`)

1. **Les noms d'unités ne sont pas uniques dans une feuille.** La résolution est
   **séquentielle** : un nom désigne la définition `U` la plus récente. Indexer
   par nom fusionne les homonymes et sur-compte le matériel sans lever d'erreur.
   `xlsx_orbat.py` gère ça — c'est une raison de plus de ne pas parser à la main.
2. **`ECHELON` et l'échelon du code 2525C divergent volontairement.** Ne jamais
   « corriger » l'un d'après l'autre ; `ECHELON` fait autorité.

### Lire / analyser

```bash
python3 scripts/xlsx_orbat.py read     F.xlsx            # compteurs après expansion
python3 scripts/xlsx_orbat.py tree     F.xlsx --depth 3
python3 scripts/xlsx_orbat.py agg      F.xlsx --unit "171 IFV BDE" --what equipment
```

### Créer / éditer

> 🔴 **Tout acronyme vient de `orbat-tools:acronyme`** (Florian, août 2026). Dès qu'un
> nom d'unité, une abréviation d'échelon ou un code de matériel doit être écrit,
> invoquer le skill `orbat-tools:acronyme` (outil `Skill`) et y prendre le code — ni
> mémoire, ni code repris d'un classeur antérieur, ni sigle forgé. Code inexistant →
> ne rien inventer, soumettre le cas à Florian (même procédure que `orbat-json`,
> `references/naming.md` Règle 7 § 7.2).

`new_workbook()`, `add_unit()`, `remove_unit(cascade=True)` pour l'ossature ;
`TemplateBuilder` pour une feuille template (il gère la numérotation séquentielle
des IDs, partagée entre `E`/`W`/`M`/`P`). **Toujours finir par `validate`**
(0 problème attendu) puis `save`.

> 🔴 **Contrôle de conformité à la source avant livraison — obligatoire.** `validate`
> ne contrôle que la structure du classeur, jamais les chiffres. Dès qu'un travail est
> réputé terminé, confronter le classeur à la source : totaux (`xlsx_orbat.py read` /
> `agg`), effectifs et matériel des unités feuilles, complétude structurelle, échelons.
> **Corriger d'office** les écarts trouvés, rejouer le contrôle, puis livrer avec
> `present_files` **accompagné du rapport en 3 blocs** — ✅ vérifié / ⚠️ corrigé /
> 🔴 non résolu (procédure complète : `../orbat-json/references/naming.md` Règle 8).
> Un silence sur un point non vérifié vaut affirmation de conformité : tout ce qui n'a
> pas pu être contrôlé va dans le bloc 🔴.

### Convertir vers orbat-mapper

```bash
python3 scripts/xlsx_orbat.py tojson F.xlsx OUT.json --side "NOM"
python3 scripts/validate.py OUT.json          # doit donner 0 erreur
```

La conversion est **lossy par construction** : le rôle équipage/passager et les
liens porteur→remorque ne sont pas représentables en orbat-mapper (le reste —
UIC, unit class, 2525C, échelon ODIN — part en `description`). `tojson` **liste
les function ID 2525C qu'il n'a pas su mapper** (entité générique `000000`) : les
signaler à Florian plutôt que de les passer sous silence, et compléter
`FUNCTION_MAP` s'il donne le code. Sur le fichier de référence, la couverture est
complète (56/56).

Une fois la conversion faite et validée, tout travail ultérieur sur le JSON
résultant (agrégation, restructuration, timeline, légendes...) relève du skill
`orbat-json`, pas de celui-ci.

## Persistance des éditions du skill

Comme pour ses autres skills, les modifications de ce dossier ne survivent pas entre
sessions sans le cycle `/maj` → zip → ré-upload. Ne repackager le skill que sur demande
explicite de Florian.

## Exemples de déclenchement

- « Lis ce classeur ODIN » / xlsx avec feuille `UNIT INFO` fourni → `xlsx_orbat.py read`.
- « Combien de BMP 2 dans la 171 IFV BDE ? » (xlsx) → `agg --unit`.
- « Convertis cet ORBAT ODIN pour orbat-mapper » → `tojson` + `validate.py`.
- « Ajoute un bataillon à ce classeur » / « fais-moi un ORBAT ODIN en xlsx » →
  `add_unit`/`TemplateBuilder` + `validate`.
- Un `.json` avec `type: "ORBAT-mapper"` → **ce n'est pas ce skill** — passer à
  `orbat-json`.
