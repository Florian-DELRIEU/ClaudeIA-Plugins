# Text to ORBAT

Source : https://docs.orbat-mapper.app/guide/text-to-orbat
Accès direct : https://orbat-mapper.app/text-to-orbat (aussi accessible depuis la page d'accueil)

Outil pour construire un ORBAT rapidement à partir de texte indenté — détecte automatiquement type d'unité + échelon par mots-clés, et génère les symboles militaires correspondants.

## Syntaxe de base

Une ligne = une unité. Indentation (2 espaces ou tab) = relation parent-enfant. Lignes vides ignorées. Lignes commençant par `#` = commentaires ignorés.

```
1st Infantry Division
  1st Brigade
    1st Battalion
    2nd Battalion
  2nd Brigade
    3rd Battalion
  Artillery Regiment
```

## Détection automatique

- **Mots-clés d'échelon** : Division, Brigade, Battalion, Company, Platoon, Squad, Team, Corps, Army (+ abréviations : div, bde, bn, co, plt, sqd). Abréviation collée au numéro acceptée : `2bn` = "2nd Battalion".
- **Mots-clés de type d'unité** : Infantry, Armor, Artillery, Engineer, Reconnaissance, Medical, Airborne, etc.
- Si aucun mot-clé trouvé dans le nom, l'unité hérite de l'échelon ET de l'icône du parent.
- Support des abréviations d'échelon concaténées (`2bn`, `1bde`, `Aco`) depuis fév. 2026.

## Mappings personnalisés (bouton "Patterns" dans la toolbar)

- Modal pour ajouter/retirer/modifier les mots-clés utilisés par le parser (icône ↔ mot-clé, échelon ↔ mot-clé).
- ⚠️ L'ordre compte : le parser examine les entrées de haut en bas et prend la première qui correspond → mettre les patterns spécifiques avant les généraux (ex. "airborne infantry" avant "infantry"). Réordonnable par drag des poignées.
- Export/import des mappings vers/depuis Excel pour modifier plusieurs entrées à la fois.
- Numéros de priorité + réordonnancement par drag-handle (fév. 2026), édition inline + suppression directe des entrées, sélecteur de symbole visuel pour choisir l'icône d'un mapping.
- Persistance en localStorage avec undo/redo.

### Syntaxe des alias (texte simple → regex flexible)

| Syntaxe | Exemple | Correspond à | Règle |
|---|---|---|---|
| `(texte)` | `marine(s)` | marine, Marines, MARINES | parenthèses = segment optionnel |
| plusieurs `()` | `armo(u)r(ed)` | armor, Armour, ARMORED, armoured | plusieurs segments optionnels cumulables |
| `.` | `R.A.` | RA, R.A., r.a., R.A | chaque point est optionnel |
| espace | `anti tank` | anti tank, Anti-Tank, ANTITANK, anti.tank | l'espace correspond à n'importe quel séparateur (espace/tiret/point) ou aucun |

- Le parser utilise des limites de mot (`inf` correspond à "2nd inf" mais pas à "information").
- Insensible à la casse ET aux accents ("blindé" correspond à l'alias "blinde").

### Regex brute

Pour les cas non couvrables par les alias (abréviations à casse fixe type `AT`, `RM`, patterns avec chiffres type `BM-21`) → champ **Patterns**, expression régulière brute utilisée telle quelle.

## Syntaxe metadata (donnée d'aide à la détection, n'apparaît pas dans le nom affiché)

- **Pipe** : `1st | tank bn` → affiche "1st", utilise "tank bn" pour trouver le symbole (ici : bataillon blindé).
- **Double-slash** (alternative au pipe) : `1st // tank bn` — tout ce qui suit `//` est traité comme metadata.
- **Crochets** : `2nd Art [bty]` → affiche "2nd Art", utilise "bty" (battery) pour l'échelon. Plusieurs paires de crochets possibles.
- Le parser regarde d'abord la metadata pour l'échelon/l'icône ; s'il ne trouve rien, il se rabat sur le nom affiché.

## Réglages (bouton "Settings")

- **Autocomplete** on/off (suggestions pendant la frappe).
- **Match input case** — les suggestions respectent la casse tapée.
- **Split fields** — voir ci-dessous.
- **Starting echelon** — échelon par défaut du niveau racine si aucun mot-clé détecté (défaut : Brigade). Les unités filles descendent progressivement en échelon.

## Split fields (séparateur virgule pour nom court + description)

Activable dans Settings. Choix de l'ordre des champs :

| Ordre | Format |
|---|---|
| name, short name, description | `Alpha Company, A, Main assault element` |
| short name, name, description | `A, Alpha Company, Main assault element` |

- Une seule valeur (pas de virgule) → utilisée comme nom.
- Deux valeurs → les deux premiers champs de la séquence choisie.
- Texte après la 3e virgule → mis dans la description.
- Avec split fields actif, TOUTE la ligne (tous les champs) sert à la détection auto d'échelon/icône.
- Combinable avec la syntaxe metadata : `A, Alpha Company | infantry bn`.

## Fonctions de l'éditeur

- **Autocomplete** pendant la frappe (si activé), avec aperçu des symboles.
- **Patterns** — modal listant tous les mappings pattern→icône et pattern→échelon avec leur priorité.
- **Icons** — modal de navigation dans tous les codes d'icône disponibles et leurs alias.
- **Debug info** (dans le panneau de sortie) — affiche l'échelon et le code icône détectés pour chaque unité de l'arbre. Très utile pour diagnostiquer une mauvaise détection.
- Presse-papier + drag-and-drop supportés directement dans l'éditeur (mars 2026), scratch pad avec undo/redo, coloration syntaxique.
- Un bouton "Generate short names" et des réglages dédiés aux noms courts (longueur max, majuscules, espaces, longueur forcée).

## Sortie / résultat

Panneau droit = aperçu en direct, arbre hiérarchique avec symboles militaires.

- **Copy** — copie l'ORBAT en JSON dans le presse-papier (à coller ensuite dans l'éditeur de scénario).
- **Drag and drop** — chaque icône d'unité dans l'arbre est une poignée de glisser-déposer : on peut glisser directement les unités dans l'arbre ORBAT de l'éditeur de scénario.
- **Open** — charge l'ORBAT complet comme nouveau scénario dans l'éditeur.
- **Export** — télécharge en :
  - **Battle Staff Tools JSON** (format Spatial Illusions)
  - **ORBAT Mapper Scenario** (fichier scénario complet, chargeable dans le site)
