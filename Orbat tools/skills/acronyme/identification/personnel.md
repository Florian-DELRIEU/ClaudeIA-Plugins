# Personnel → code (éléments, pas individus)

Dans les ORBAT de Florian, le catalogue `personnel` code un **élément** (escouade,
groupe, équipe, binôme), pas un soldat isolé. L'identification suit donc :

**`{Échelon d'élément}-{Rôle dominant}`**

## Échelons d'élément

**Échelle de référence (2026-08-09) — source unique des tailles d'élément.**
Les effectifs sont **indicatifs, jamais normatifs** : ils décrivent l'usage courant,
ils ne l'imposent pas.

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | Effectif indicatif |
|---|---|---|---|
| SEC | | Section — « grosse escouade », élément d'un seul tenant | ~15 et + |
| SQ | | Escouade | ~7-15 |
| GRP | | Groupe (demi-escouade, détachement réduit — y compris un groupe de commandement officier + escorte) | ~4-6 |
| EQP | EQU, TE | Équipe (fonction spécialisée distincte, pas une escouade réduite) — `EQU` et `TE` en alternatifs lisibles | ~3-4 |
| BI | | Binôme | 2 |

> ⚠️ **Le chiffre ne tranche jamais, la nature si.** Les fourchettes se recoupent
> volontairement (4 hommes = `EQP` ou `GRP` selon le cas) et il est parfaitement
> acceptable de nommer `GRP` un élément de 7 hommes si l'intention est bien « une
> fraction d'escouade ». Discriminants, dans cet ordre :
> - `GRP` = **fraction ou variante réduite d'une escouade** du même rôle
>   (demi-escouade, détachement de commandement) ;
> - `EQP` = **fonction à part entière**, non dérivée d'une escouade, typiquement
>   rattachée à une arme ou à un poste (équipe de reconnaissance, équipe drone,
>   servants d'une pièce) ;
> - `SEC` = **élément terminal**, pas un regroupement : un seul bloc d'hommes,
>   sans sous-éléments.

> ⚠️ **`SEC` est le dernier élément ; `PLT` change de catégorie.** `BI` → `EQP` →
> `GRP` → `SQ` → `SEC` sont des tailles croissantes du *même objet* (un bloc
> d'hommes). `PLT` (peloton) n'est pas la case au-dessus de `SEC` sur la même
> échelle : c'est un **conteneur**, qui regroupe plusieurs escouades, équipes ou
> sections. Un peloton se modélise donc en **unité avec `subUnits`**, jamais en
> ligne de catalogue `personnel`. Au-delà de ~15 hommes non structurés, on écrit
> `SEC-*` ; dès qu'il y a des sous-éléments, c'est un `PLT` et plus un élément.

> ⚠️ **Le préfixe encode la TAILLE réelle de l'élément, pas le rôle.** Le choix
> `SQ` / `GRP` / `EQP` / `BI` dépend uniquement de l'effectif concret que l'on
> veut représenter, jamais du rôle porté en suffixe. En particulier, `HQ`
> (commandement) n'impose aucun préfixe : `GRP-HQ` est simplement la forme la
> plus **fréquente** parce qu'un groupe de commandement est généralement réduit
> (~4-6 hommes, gabarit `GRP`) — mais **`SQ-HQ` est parfaitement valide** si on
> veut représenter une escouade de commandement pleine (~8-12 hommes) plutôt
> qu'un groupe réduit. De même `EQP-HQ` ou `BI-HQ` sont possibles selon
> l'effectif. Choisir le préfixe d'après la taille réelle, puis le suffixe
> d'après le rôle, indépendamment l'un de l'autre.

## Rôle dominant (exemples établis dans `ORBAT 2023`)

<!-- bassin: aucun -->
| Code | Élément |
|------|---------|
| `SQ-INF` | Escouade d'infanterie classique |
| `SQ-GUN` | **Servants d'une pièce lourde, nus** — la pièce est sur la ligne `equipment` de l'unité |
| `EQP-GUN` | **Servants d'une pièce légère, nus** — idem |
| `SQ-AT` | Escouade antichar d'**infanterie** — bazooka, PIAT, fusil AT portés par les hommes |
| `SQ-HW` | Escouade **articulée autour** de l'emploi d'armes lourdes |
| `EQP-MOR` | Équipe de mortier **pièce comprise** — équivaut à `MOR` + `EQP-GUN` |
| `SQ-ENG` | Escouade du génie |
| `SQ-MS` | Escouade démineur |
| `SQ-MUN` | Escouade d'approvisionnement en **munitions**, élément distinct des servants qu'elle dessert |
| `SQ-LOG` | Escouade d'approvisionnement **générique** — vivres, rechanges, munitions mélangées |
| `GRP-INF` | Groupe/demi-escouade d'infanterie (fire team) |
| `GRP-HQ` | Groupe de commandement (officier + escorte, effectif réduit) |
| `BI-TE` | Binôme tireur d'élite |
| `BI-AT` | Binôme antichar — le lance-roquettes est embarqué, pas de ligne d'équipement |
| `EQP-REC` | Équipe de reconnaissance |
| `EQP-UAV.R` | Équipe drone de reconnaissance |

### Doctrine `GUN` / `AT` / `HW` — où se trouve l'arme (2026-08-10)

Trois rôles voisins, séparés par un critère unique :

<!-- bassin: aucun -->
| Rôle | Ce que c'est | Où est l'arme |
|---|---|---|
| `GUN` | **Les servants, nus.** Artilleurs au sens large — quiconque met en œuvre un système d'armes, y compris un tireur de mitrailleuse. | Sur la ligne `equipment` de l'unité, **pas** dans l'élément |
| `AT` | Unité d'**infanterie** spécialisée dans la destruction de chars, armes portables : bazooka, PIAT, fusil antichar. Caractère fantassin conservé. | **Dans** l'élément — indissociable de l'homme |
| `HW` | Unité **articulée autour de l'emploi** d'armes lourdes : MG, lance-roquettes, lance-grenades, lance-missiles selon l'époque. Tout l'effectif n'en porte pas. | Variable — `HW` décrit une unité, pas un servant |

> ⚠️ **`GUN` est la forme à privilégier pour tout servant de pièce.** Un servant
> de canon antichar n'est pas `SQ-AT` : `AT` désignerait des fantassins au
> bazooka. Un servant de mortier n'est pas `SQ-HW` : `HW` désigne l'unité qui
> s'articule autour de l'arme, pas l'équipe qui la sert.

**L'exception — les rôles qui embarquent la pièce.** Certains rôles incluent
l'arme dans l'effectif de l'élément :

```
EQP-MOR  ≡  MOR    +  EQP-GUN
SQ-C.AT  ≡  C.AT   +  SQ-GUN
```

Ils sont valides, mais **font perdre le compte des pièces** dès qu'on remonte
au-dessus de l'élément. La forme éclatée est plus précise :

<!-- bassin: aucun -->
| Moins précis | Plus précis |
|---|---|
| `PLT-MOR` avec `3× EQP-MOR` | `PLT-GUN` avec `MOR ×3` en équipement et `3× EQP-GUN` en personnel |

> 🔴 **Règle de non-double-comptage.** Une unité porte **soit** la pièce en
> `equipment` + des servants en `*-GUN`, **soit** un élément en `*-MOR` /
> `*-C.AT` qui l'embarque — **jamais les deux**, sinon la pièce est comptée deux
> fois. C'est le piège principal de cette doctrine et il est silencieux : aucun
> validateur ne le détecte aujourd'hui.

**Portée sur les échelons supérieurs.** Les échelons au-dessus de l'élément
gardent leur mission ; seuls les éléments de personnel passent en `GUN` :

```
CIE-AT                      ← mission antichar de la compagnie : conservée
└─ PLT-AT                   ← mission antichar du peloton : conservée
   ├─ equipment : ST-C.57 ×2
   └─ personnel : SQ-GUN ×2 ← les servants, nus
```

La mission est un fait d'unité, pas de servant : `CIE-GUN` effacerait l'antichar
de l'organigramme sans rien apporter.

**Frontière `GUN` / `CRW`** — non tranché formellement : un servant de pièce
tractée ou en position est `GUN` ; l'équipage d'un automoteur, qui conduit *et*
sert la pièce, relève de `CRW`. À confirmer dès qu'un ORBAT contiendra des blindés
(point ouvert, `decisions.md` § 5).

> ⚠️ **`AM` (assistant munitions) est un rôle *individuel*** : il qualifie la
> composition d'un élément en `description`, il ne crée pas de ligne de
> catalogue. Ne pas cumuler `AM` et un `SQ-MUN` distinct pour les mêmes hommes —
> même logique de non-double-comptage que ci-dessus. Les porteurs sont **dans**
> l'équipe de servants → `EQP-GUN` seul, `AM` en `description` ; ils forment un
> **élément distinct** → `EQP-GUN` **et** `SQ-MUN`, deux lignes.

## Méthode pour une nouvelle armée

1. Déterminer la **taille de l'élément** (escouade / groupe / équipe / binôme) →
   préfixe, d'après l'effectif réel uniquement (pas d'après le rôle). Un groupe
   de commandement est le plus souvent `GRP` (effectif réduit), mais `SQ-HQ`
   reste valide pour une escouade de commandement pleine — voir l'encadré
   ci-dessus.
2. Déterminer le **rôle dominant** (INF, ENG, MS, AT, HW, TE, REC, UAV, HQ, MED…) →
   suffixe, en réutilisant les rôles de `references/infanterie.md`. Pour
   l'infanterie, le suffixe canonique est `INF` (`I` alternatif — voir Historique).
3. Réutiliser un code existant si l'élément est équivalent (P5 — cohérence lexique).

> Les grades/armes individuels (`references/infanterie.md`) ne servent ici qu'à *qualifier*
> le rôle dominant de l'élément, pas à créer un code par soldat.

## Historique

- V4 utilisait initialement `ESC` (Escouade/groupe confondus, ~6-12). Décision
  actée : `ESC` renommé `SQ` pour l'escouade pleine, et `GRP` introduit comme
  préfixe distinct pour toute fraction réduite d'escouade (demi-escouade,
  groupe de commandement). Mettre à jour tout code `ESC-*` préexistant vers
  `SQ-*` (sauf `ESC-HQ`, qui devient `GRP-HQ`).
- Suffixe Infanterie : **`INF` est la forme canonique** (officialisé le
  2026-08-04, confirmé le 2026-08-05). Une décision de juillet 2026 avait
  d'abord retenu `I` (plus compact) et déprécié `INF` ; ce choix a été
  **inversé** le 2026-08-04 car `I` collisionne avec Industriel / Incendiaire /
  Intercepteur. Mettre à jour tout code `*-I` d'infanterie vers `*-INF`
  (ex. `GRP-I` → `GRP-INF`, `SQ-I` → `SQ-INF`). `I` reste lu Infanterie par
  défaut en position Type mais ne doit plus être produit.
- Échelon Équipe : **`EQP` est l'officiel** (2026-08-05, inchangé) ; `EQU` reste
  alternatif lisible. **`TE` est redevenu un alternatif d'Équipe le 2026-08-09** :
  un acronyme isolé se lit comme un Type (`SKILL.md` § 3), donc `TE` seul = Équipe,
  sans ambiguïté avec `TE` = Tireur élite qui n'apparaît qu'en position Rôle
  (`BI-TE`, `SQ-TE`). Ceci annule la réserve inscrite ici le 2026-08-05.
- Règle `HQ` clarifiée (juillet 2026) : le préfixe encode la taille, pas le
  rôle — `SQ-HQ` est valide pour une escouade de commandement pleine, `GRP-HQ`
  n'est que la forme la plus fréquente (voir encadré en tête de fichier).
