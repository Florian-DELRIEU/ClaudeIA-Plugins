# Véhicules Maritimes & Spatiaux

Format : `{Catégorie}-{Rôle}`

**Principe fondamental : doctrine > taille**
Le type est déterminé par la doctrine et l'indépendance opérationnelle, pas le tonnage.

---

## Catégories navales

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| SS | S | Sous-marins | |
| SLE | | Sous-marin lanceur d'engins | |
| SSN | | Sous-marin nucléaire | |
| SNLE | | Sous-marin nucléaire lanceur d'engins | |
| K | | Corvette | |
| E | | Escort | Peu armé/blindé, ASW |
| F | PF | Frégate / Corvette polyvalente | ⚠️ PF = polyvalente, FF = trans-océanique. Texte d'origine `F / PF` conservé : deux codes distincts ou alias ? (`PFG` = « Frégate polyvalente gunship ») — `decisions.md` § 5 |
| FF | | Frégate (trans-océanique) | Ocean-capable, spécialisation niveau corvette. Distincte de PF |
| DD | | Destroyer | |
| DE | | Destroyer d'escorte | Trans-océanique, ASW |
| DDE | | DE amélioré | Armements/radars plus performants, escorte flotte principale |
| DL | | Destroyer leader | |
| C | | Croiseur | ⚠️ C = Croiseur en position Type (≠ Canon en position Rôle) |
| BC | | Croiseur de bataille | |
| BB | | Cuirassé | Tient la ligne, absorbe les dommages ⚠️ Distinct de CA |
| CA | | Croiseur lourd | Frappe et conserve capacité de désengagement ⚠️ Distinct de BB |
| CV | | Porte-avions | |
| LH | | Porte-hélicos | |
| LS | | Landing Ship | |
| LOG | | Navire cargo | |
| TT | | Transport | |
| PC | | Patrouille côtière | Léger et rapide |
| CS | | Capital ship | Vaisseau mère / navire principal |

---

## Fusions navales prédéfinies

<!-- bassin: types -->
| Officiel | Alternatifs | Décomposition | Description |
|---|---|---|---|
| FFLM | | FF + LM | Frégate lance-missile |
| FFR | | FF + R | Frégate radar / reconnaissance |
| FFAA | | FF + AA | Frégate anti-aérienne |
| KG | | K + G | Corvette gunship |
| PFG | | PF + G | Frégate polyvalente gunship |
| FFG | | FF + G | Frégate trans-océanique gunship |
| DDG | | DD + G | Destroyer gunship |
| CG | | C + G | Croiseur gunship |

---

## Rôles navals

<!-- bassin: roles -->
| Officiel | Alternatifs | Signification | Notes |
|---|---|---|---|
| C | | Canonnier | ⚠️ En position Rôle = canon (≠ Croiseur en position Type) |
| DN | | Dreadnought | Canon gros calibre exclusivement |
| AA | | Anti-aérien | |
| E | | Escort | |
| ASW | K, HK | Anti-sous-marins | `ASW` officiel (2026-08-04, terme OTAN consacré) — `K` collisionne avec Corvette |
| T | | Torpilleur | `T` **isolé**, attaché à un Type via `-` (ex. `K-T` = corvette-torpilleur). ⚠️ Distinct de `.T` en suffixe de munition = Traçante — voir `decisions.md` § 3 |
| REC | | Reconnaissance | ⚠️ **3 capacités distinctes, pas des notations d'un même rôle** (ancienne écriture `REC / RAD / SON` corrigée le 2026-08-02) |
| RAD | | Radar | Capacité radar. ⚠️ `RAD` a 3 sens désambiguïsés par position/contexte (voir `decisions.md` § 3) |
| SON | | Sonar | Capacité sonar |
| ML | M | Poseur de mines | ⚠️ Distinct de `MS` (dragueur), pas un alias — cohérent terrestres/infanterie (2026-08-02). `M` = alias court en lecture |
| MS | | Dragueur de mines | ⚠️ Distinct de `ML` (poseur) |
| CH | | Avec hélicoptère | |
| N | | Nucléaire (propulsion) | Motorisation nucléaire |
| NK | | Nucléaire (armement) | Armement nucléaire (nuke) ⚠️ Distinct de N (propulsion) |
| GM | | Missile guidé | |
| LE | | Lanceur d'engins | Générique. `BM` dissocié (2026-08-04) — voir `BM` = Missile balistique ci-dessous |
| BM | | Missile balistique | Dissocié de `LE` (2026-08-04), cohérent avec `.BM` (section Missiles, `infanterie.md`). ⚠️ Décrit « Type naval » par Florian dans le devlog — placement exact Type/Rôle à confirmer (`decisions.md` § 5) |
| L | | Leader | |
| MA | | Soutien amphibie | **Officiel** (2026-08-03) — remplace `SA`, code abandonné en Rôle naval (`SA` reste Space Plane/SSTO et Supériorité aérienne côté aérien, non affectés). Coexiste avec `-MA` = Marines (Type/groupement) : bassins différents, pas de collision |
| AN | | Anti-navire de surface | ⚠️ Redondant si armement implique déjà la fonction |
| TRD | COM | Commerce | `TRD` officiel — `COM` réservé à Communication (aérien) |

---

## Rôles vaisseaux (missions spécialisées)

> Regroupement thématique, sans restriction d'usage (SKILL.md § Règles cardinales n°4) — introduit à l'occasion du projet Cosmotter, utilisable dans n'importe quel contexte.

<!-- bassin: roles -->
| Officiel | Alternatifs | Signification |
|---|---|---|
| MIN | | Mineur |
| CONS | | Constructeur |
| MAIN | | Réparateur |
| EXP | | Explorateur (grande autonomie) |
| SF | | Chantier naval |
| COL | | Colonisation |
| SCI | | Scientifique |

---

## Échelons navals

<!-- bassin: types -->
| Officiel | Alternatifs | Signification |
|---|---|---|
| ESC.N | | Escadrille |
| FLT.N | | Flotte |
| FLTL.N | | Flottille |
| GRP.N | | Groupe |

---

## Types de flottes

> Codes écrits sans le tiret de liaison : `-L` (`FLT.N-L`) est le code `L` (format du 2026-10-10).
>
> ⚠️ Ces types s'écrivent en **2e position** (`FLT.N-L`, `FLT.N-T`) mais sont classés dans le bassin Types, comme les types d'unité. `L` / `M` / `H` y recoupent les gabarits universels `.L` / `.M` / `.H`, et `T` (Torpilleurs) recoupe `T` = Tank — points ouverts (`decisions.md` § 5).

<!-- bassin: types -->
| Officiel | Alternatifs | Signification |
|---|---|---|
| L | | Flotte légère |
| M | | Flotte moyenne |
| H | | Flotte lourde |
| CV | | Groupe porte-avion |
| MA | | Soutien invasion — casse normalisée le 2026-08-03 (était `Ma`) |
| ART | | Bombardement côtier |
| AA | | Anti-aérienne |
| REC | | Reconnaissance |
| T | | Torpilleurs |
| ASW | | Anti-sous-marins |
| SSA | | Meute de sous-marins d'attaque |
| SLE | | Meute de sous-marins lanceurs d'engins |
| LRG | | Longue portée |
| XLRG | | Très longue portée |
| ML | | Poseur de mines |
| MS | | Dragueur de mines |
| E | | Escorte (ex-doublon de la ligne `AA / REC / T / E`, fusionné le 2026-10-10) |
| HKC | | Chasse de convoi (Hunt-Kill Convoy) |
| QRF | | Intervention rapide |
| CD | | Défense de convoi |
| DC | | Défense côtière |
| RES | | Réserves |

---

## Notes Cosmotter (Sci-Fi)

> Notes de transposition doctrinale, pas des acronymes. Reformulation/déplacement en attente (`decisions.md` § 5).

- ✅ Logique sous-marin → vaisseau furtif (se transfère)
- ✅ Hiérarchie d'escorte (se transfère)
- ❌ Géographie côtière (ne se transfère pas)
- ❌ Menaces en environnement 2D (ne se transfèrent pas)
