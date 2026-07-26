---
name: wt-notes
description: >
  Système de notation d'avions War Thunder (RB) construit avec Florian : grille de critères
  hiérarchique (catégories → notes → sous-notes), barèmes, notation objectif+subjectif,
  et implémentation dans le fichier Google Drive « Notes avions WT » (feuille « note »).
  Déclencher IMPÉRATIVEMENT dès que Florian tape /wt-notes, ou mentionne « ma grille de
  notation avions », « le fichier Notes avions WT », la feuille « note », ou demande de :
  noter/évaluer un avion, ajouter un avion à la grille, discuter/modifier un barème ou un
  critère, ajouter une catégorie, calculer une note de rôle, ou éditer le fichier Excel
  associé. Déclencher aussi pour des demandes courtes ("note-moi tel avion", "quel barème
  pour X ?", "ajoute cet avion à la grille", "pourquoi Avionique est à part ?"). Contient
  aussi les pièges Excel/LibreOffice rencontrés en construisant le fichier — les relire
  avant toute édition programmatique de ce classeur.
---

# Système de notation d'avions War Thunder

Grille de notation personnelle de Florian pour comparer les avions de War Thunder (Realistic
Battle), catégorie par catégorie plutôt qu'avec un score global unique.

## Principes de conception (ne pas s'en écarter sans validation de Florian)

- **Comparaison strictement intra-BR.** Tous les avions d'un même Battle Rating sont notés
  sur les mêmes critères, quel que soit leur type (chasseur, bombardier, CAS...). Un
  bombardier aura donc naturellement une Maniabilité faible — c'est voulu, ça fait ressortir
  les rôles à travers les stats. **On ne compare jamais deux avions de BR différents** :
  une note se lit "pour ce BR", pas en absolu (ex. "le plus rapide des BR 2.0").
- **Pas de score global unique.** Florian juge les avions trop complexes pour être réduits à
  un seul chiffre, et un score composite ne dirait rien du comportement réel. Chaque
  catégorie reste lisible séparément.
- **Avionique est une catégorie à part**, jamais resommée avec les autres. Elle donne une
  lecture "qualité générale des systèmes de bord" indépendante du combat. Trois de ses notes
  (Pas d'Hélice, MEC, Radiateur et Refroidissement) sont **dupliquées** dans Moteur et
  Énergie, lues sous un angle différent (rendement propulsif / puissance exploitable / tenue
  de la puissance en WEP). Le doublon est volontaire et sans risque tant qu'aucun score
  global n'est construit à partir des deux.
- **Notes de rôle séparées**, un cran au-dessus des catégories : moyenne pondérée des
  catégories (poids propre à chaque rôle, ex. Maniabilité forte en Dogfight/quasi nulle en
  Boom & Zoom) + subjectif ample. Elles ne sont pas encore calculées — la table de poids
  rôle × catégorie reste à définir avec Florian avant de brancher les formules.

## Notation objectif + subjectif

Chaque note élémentaire se tape dans **une seule cellule**, sous la forme texte :

```
<objectif>+<subjectif>   ex. 5+2
<objectif>-<subjectif>   ex. 4-1
<objectif>                ex. 6      (aucun ajustement)
(vide)                     si le critère ne s'applique pas à l'avion
```

- L'objectif vient de valeurs mesurables/comparables entre avions du même BR.
- Le subjectif est un bonus/malus d'appréciation (réactivité moteur non chiffrable, plage de
  fonctionnement, etc.), **borné ±2** pour les notes élémentaires, **±4** pour les notes de
  rôle (qui synthétisent beaucoup plus de paramètres).
- Ne jamais taper directement `=5+2` (Excel calcule et efface la trace de l'ajustement) —
  toujours le texte brut `5+2`.

## Hiérarchie complète et barèmes

`◆` = note calculée (moyenne pondérée) — jamais saisie à la main. Les autres lignes sont des
notes élémentaires saisies au format objectif+subjectif ci-dessus. ⁽ᵈ⁾ = dupliquée depuis
Avionique. ⁽ᵖ⁾ = proposition non encore validée par Florian (voir dernière section).

### Avionique — qualité générale des systèmes de bord (autonome, jamais resommée)
| Note | Barème objectif | Coef |
|---|---|---|
| Volets — nb de crans (aucun/atterrissage seul/tous) | /3 (0 + 1 par cran) | 3 |
| Pas d'Hélice — fixe/variable/vitesse constante | /2 | 3 |
| MEC — gain de puissance selon qualité de gestion moteur | /4 | 4 |
| Trim — précision/amplitude en croisière | /3 | 1 |
| Radiateur et Refroidissement — tenue de la température | /10 | 3 |

### Maniabilité — comportement en combat rapproché
| Note | Barème objectif | Coef |
|---|---|---|
| Virage à Plat | /10 | 4 |
| Roulis | /10 | 4 |
| Efficacité des Volets (réactivité/envergure/résistance à vitesse en manœuvre) | /10 | 3 |
| Conservation d'Énergie en virage | /10 | 3 |
| Performance verticale ⁽ᵖ⁾ — ressourcer/manœuvrer en montée | /10 | 3 |

### Moteur et Énergie
| Note | Barème objectif | Coef |
|---|---|---|
| Puissance du Moteur — **spécifique** (rapportée au poids), pas brute | /10 | 5 |
| Taux de Montée | /10 | 5 |
| Vitesse Max. Palier | /10 | 4 |
| Vitesse Max. Piqué | /10 | 4 |
| Pas d'Hélice ⁽ᵈ⁾ | /4 | 2 |
| MEC ⁽ᵈ⁾ | /6 | 2 |
| Radiateur & Refroidissement ⁽ᵈ⁾ | /12 | 2 |
| Altitude critique ⁽ᵖ⁾ — tenue de puissance en altitude, nb d'étages de compresseur | /10 | 3 |

### Résilience
| Note | Barème objectif | Coef |
|---|---|---|
| Blindage de l'Équipage — nb de plaques | /4 | 4 |
| Protection de la cellule (structure + surfaces de contrôle) | /10 | 3 |
| Protection modules (dont résistance des radiateurs) | /10 | 4 |
| Résistance du Bloc Moteur | /10 | 3 |
| Risque Incendie ⁽ᵖ⁾ — probabilité qu'un impact déclenche un feu | /10 | 2 |

### Armement Offensif
Agrégation à deux étages : Puissance de Feu et Quantité de munitions sont elles-mêmes des
◆ notes calculées à partir de leurs 3 armes, avant d'entrer dans le calcul global de la
catégorie aux côtés de Diversité, Précision et Position des armes.

| Note | Barème objectif | Coef |
|---|---|---|
| ◆ Puissance de Feu | dérivée | 5 |
| — Armes 1 / Armes 2 / Armes 3 ou Pods | /10 chacune | 1 chacune |
| Diversité de l'Armement (variété de calibres/effets) | /2 | 2 |
| Précision (dispersion/stabilité de tir) | /10 | 4 |
| ◆ Quantité de munitions | dérivée | 4 |
| — Munitions 1 / 2 / 3 ou Pods | /10 chacune | 1 chacune |
| Position des armes ⁽ᵖ⁾ — éloignement de l'axe, position basse ou non | /3 | 2 |

### Armement Suspendu
| Note | Barème objectif | Coef |
|---|---|---|
| Charge Utile Maximale | /10 | 1 |
| Flexibilité de l'Armement (nb de configurations vs BR) | /10 | 1 |

### Armement Défensif
| Note | Barème objectif | Coef |
|---|---|---|
| Puissance des Armes Défensives | /10 | 1 |
| Angle de Tir (couverture angulaire) | /10 | 2 |

### Notes de rôle (à part, pas encore calculées)
Chasseur Dogfight, Boom & Zoom, Intercepteur, Bombardier en piqué, Attaqueur au sol,
Bombardier tactique, Bombardier Stratégique. Formule prévue : moyenne pondérée des
catégories ci-dessus (poids propre à chaque rôle — table à définir) + subjectif ±4.

## Ressources associées à ce skill

- **`scripts/build_note_sheet.py`** — reconstruit la feuille "note" à l'identique
  (en-têtes, couleurs, coefficients, formules, colonnes masquées de parsing
  obj+subj, mises en forme Texte, gel des volets). Ne construit QUE la feuille
  "note", n'écrit aucune donnée d'avion (grille vierge de 40 lignes). Usage :
  `python build_note_sheet.py <classeur.xlsx> [sortie.xlsx]`. Après exécution,
  penser au recalcul LibreOffice (voir "Pièges" plus bas) avant de livrer le
  fichier. Relire ce script avant toute reconstruction ou modification
  structurelle de la feuille "note", plutôt que de la recoder de mémoire.
- **`references/notes-avions.csv`** — snapshot des notes de tous les avions
  actuellement dans la grille (colonnes fixes + les 36 notes manuelles, une
  colonne par note, préfixées par leur catégorie). Les valeurs conservent le
  format texte brut tel que saisi dans Excel (`5+2`, `4-1`, ou nombre seul),
  cases vides laissées vides. Ne contient PAS les colonnes ◆ Note (calculées,
  pas des données sources) ni les notes de rôle (pas encore actives). À
  relire pour connaître l'état actuel des données sans rouvrir le classeur, et
  à régénérer après tout ajout/modification d'avion si Florian veut garder le
  skill synchronisé.

## Emplacement et structure du fichier

- Google Drive, classeur **« Notes avions WT »** (xlsx).
- Feuille **« note »** = la grille active (celle décrite ci-dessus). Colonnes fixes à gauche :
  Avion, Nation, BR, Rang, **Type** (ne jamais remplir cette colonne — c'est à Florian de le
  faire). Une colonne ◆ Note par catégorie, en-tête arborescent en couleur (une teinte par
  catégorie, plus clair = plus profond dans la hiérarchie).
- Feuille **« Claude »** = documentation lisible de tout le système (barèmes, descriptions) —
  à tenir synchronisée avec ce skill si la grille évolue.
- **Feuil2** (ancien système, pré-refonte) reste en place pour historique ; 7 avions y ont été
  migrés vers « note » (BB1, Br.693 AB2, P-40E-1, Ki-43-II, Typhoon mk Ia, D 520, P-51D-5).
  Ne pas resupprimer Feuil2 sans demande explicite.
- **Feuil1** et **Feuil3** = brouillons/tentatives antérieures, non maintenus.

## Pièges Excel/LibreOffice rencontrés (relire avant toute édition programmatique)

> ⚠️ Ces points ont chacun cassé le fichier au moins une fois pendant la construction.

1. **Parsing du texte `obj+subj`** : une colonne masquée par note (repliée, `outlineLevel=1`,
   `hidden=True`) extrait objectif et subjectif via
   `IF(cell="",0,IFERROR(VALUE(LEFT(cell,FIND("+",cell)-1))+VALUE(MID(...)),IFERROR(<idem
   avec "-">,VALUE(cell))))` — renvoie **0** (pas `""`) pour une cellule vide.
2. **La moyenne pondérée d'une catégorie ne doit contenir AUCUN appel de fonction à
   l'intérieur du `SUMPRODUCT`** (ni `N()`, ni `IF()` sur une plage). Ces deux ont chacun
   provoqué un bug d'intersection implicite dans Excel (seule la 1ʳᵉ cellule de la plage est
   prise en compte, silencieusement, pas d'erreur). Utiliser uniquement de l'arithmétique
   pure : `SUMPRODUCT(coef_range*(visible_range<>"")*helper_range) /
   SUMPRODUCT(coef_range*(visible_range<>""))`, avec `helper_range` déjà 100% numérique
   (jamais de `""`).
3. **Format des cellules de saisie = Texte (`@`)**, sinon Excel réinterprète des entrées comme
   `4-1` comme une date. Appliquer sur tout leaf/note manuel, pas sur les colonnes ◆ Note
   (formules) ni Avion/Nation/BR/Rang.
4. **`openpyxl` n'exécute jamais les formules** — il faut recalculer via LibreOffice headless
   (`ThisComponent.calculateAll(); ThisComponent.store()`) pour que les valeurs mises en cache
   soient présentes à l'ouverture. **Mais LibreOffice efface `fullCalcOnLoad`** à chaque
   sauvegarde : le réinjecter après coup par édition directe du zip
   (`xl/workbook.xml`, élément `<calcPr fullCalcOnLoad="1" forceFullCalc="1" .../>`), jamais
   via un rechargement `openpyxl` (qui, lui, efface les valeurs mises en cache des formules).
5. **La table `Tableau3` de Feuil2 est fragile** : si LibreOffice réenregistre un `autoFilter`
   sans condition active, il peut y écrire un `customFilter operator="**none**"` invalide, que
   `openpyxl` refuse ensuite de relire (`ValueError` sur les worksheets). Si ça se reproduit,
   remplacer dans `xl/tables/table4.xml` le bloc `<autoFilter ...><filterColumn>...
   </filterColumn></autoFilter>` par un simple `<autoFilter ref="..."/>`.
6. Après toute édition, vérifier via un vrai parseur XML (`xml.etree.ElementTree`), pas des
   regex sur le XML brut — une regex non-gourmande peut sauter d'une cellule à une autre et
   donner un faux résultat.

## Décisions encore ouvertes

- 4 critères **(proposition)** pas encore validés par Florian : Performance verticale
  (Maniabilité), Altitude critique (Moteur et Énergie), Risque Incendie (Résilience),
  Position des armes (Armement Offensif). Ne pas les traiter comme acquis dans une
  discussion — les rappeler comme propositions si le sujet revient.
- Table de poids **rôle × catégorie** non définie — nécessaire avant de brancher les formules
  des notes de rôle.
- Le doublon Moteur et Énergie / Avionique (Pas d'Hélice, MEC, Radiateur) est assumé tel
  quel ; ne pas le "corriger" sans que Florian le redemande.
