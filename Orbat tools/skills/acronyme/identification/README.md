# identification/ — apprendre à trouver l'acronyme

Module d'aide à l'**identification** : produire l'acronyme v4 *le plus évident* pour tout
véhicule ou élément de personnel, toute nation, toute époque.

- `METHODE.md` — le raisonnement : principe du châssis, pipeline, arbitrage « plus évident ».
- `chassis-types.md` — table châssis → Type (multi-nations, extensible).
- `personnel.md` — codage des éléments de personnel.
- `lexique.json` — registre `désignation réelle ↔ code v4` pour le **matériel réel**
  (toutes nations/époques), amorcé depuis ORBAT 2023, enrichi à chaque cas résolu
  (garantit la cohérence inter-fichiers).
- `lexique-40k.json` — registre équivalent **dédié aux univers fictifs** (Warhammer
  40,000, Cosmotter…), où certains codes prennent un sens différent du monde réel.
  À consulter et enrichir en priorité dès que la source est un univers fictif.
- `entrainement.md` — protocole du mode d'entraînement (Florian donne un nom, on
  identifie l'acronyme avec raisonnement détaillé, il note sur 5, on journalise les cas
  validés dans `lexique.json`).

Consulter ce dossier dès qu'il faut **attribuer** ou **vérifier** un acronyme à partir
d'une désignation réelle. À l'inverse (décoder un code existant), les tables de
`references/` suffisent.

## Historique des audits de lexique

**Audit du 2026-07-29, appliqué le 2026-07-30.** Croisement des deux lexiques contre
toutes les tables de `references/` et `identification/`. Corrections appliquées :

| Ancien code | Nouveau | Raison |
|---|---|---|
| `ESC-INF` | `SQ-I` | `ESC` renommé `SQ` ; suffixe `INF` déprécié au profit de `I` (voir `personnel.md` § Historique) |
| `ESC-HW` / `ESC-ENG` / `ESC-MS` / `ESC-AT` | `SQ-HW` / `SQ-ENG` / `SQ-MS` / `SQ-AT` | `ESC` → `SQ` |
| `ESC-HQ` | `GRP-HQ` | Cas particulier acté : groupe de commandement à effectif réduit |
| `INF` / `SQ-INF` / `GRP-INF` (lexique-40k) | `I` / `SQ-I` / `GRP-I` | Suffixe `INF` déprécié au profit de `I` |
| `REM-SUP` | `REM-LOG` | `SUP` n'existait dans aucune table ; `LOG` est le rôle canonique (cohérent avec `VU-LOG`) |
| `CH-LATT` / `CH-LTT` | `CH.L-ATT` / `CH.L-TT` | Gabarit infixé sans séparateur interdit (collision `CHM`/`(CHM)`=Chimique) |
| `CH-T` | `CH-TT` | `T` n'est pas un rôle de transport (`T`=Tank en Type, `T`=Traçante en munitions) ; `TT` est le rôle canonique |

**Faux positifs écartés** (conventions valides, aucune action) : `VUTT` (= `VU`+`TT`,
concaténation de deux codes définis), `CA.20` / `MOR.80` / `VTT-MOR.80` (convention calibre
fusionnée par point — ces codes étaient écrits collés `CA20`/`MOR80` jusqu'au 2026-08-10, forme abandonnée depuis), `MK2` / `MK2-REC` (convention numéro collé).

> ⚠️ **Revirement du 2026-08-05 — le sens de conversion `INF`↔`I` est inversé.**
> L'audit de juillet ci-dessus dépréciait `INF` au profit de `I`. Cette décision a été
> **inversée le 2026-08-04** (`INF` redevient l'officiel, `I` collisionnant avec
> Industriel/Incendiaire/Intercepteur) et propagée le 2026-08-05. Les entrées converties
> en `*-I` doivent donc **repasser en `*-INF`** (`SQ-I`→`SQ-INF`, `GRP-I`→`GRP-INF`).
> Le tableau ci-dessus est conservé tel quel comme trace de l'état de juillet ; c'est
> `decisions.md` § 6 qui fait foi pour l'état courant.

**Méthode de re-audit** (reproductible) : pour chaque entrée de lexique, vérifier que
chaque élément de `parts` existe dans une table de `references/*.md` ou
`identification/*.md`, en tenant compte des conventions de concaténation (calibre,
numéro, gabarit fusionné). Tout composant non résolu est signalé à Florian plutôt que
supposé valide (cf. `SKILL.md` § Workflow de vérification, point 8).
