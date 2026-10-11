# Groupements & Unités

Format : `{Échelon}-{Type Unité}` ou `{Échelon}-{Véhicule}` (ex. `BT-INF`, `BGE-IB`).

> Ce fichier code les échelons et types d'unité **de la nomenclature maison**. Les libellés et la numérotation des unités d'armées réelles (`3./IR 9`, `501e RCC`…) relèvent d'`orbat-nommage`, qui fait foi pour ce vocabulaire (2026-10-10).

---

## Échelons

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | ⚠️ Note |
|---|---|---|---|
| ARMY | | Armée | `ARMY` officiel (2026-10-10) — remplace l'ancien code de l'échelon Armée, rendu aux Blindés (type d'unité, plus bas) |
| CRP | | Corps d'armée | |
| DIV | D | Division | `DIV` officiel, `D` valide (2026-08-09) |
| BGE | B | Brigade | |
| REG | R | Régiment | |
| BT | BN | Bataillon | `BT` officiel, `BN` valide (2026-08-09). ⚠️ Distinct de `BAT` = Batterie |
| CIE | C | Compagnie | |
| PLT | P | Peloton | **Conteneur** : regroupe plusieurs éléments (escouades, équipes, sections…). Strictement **au-dessus** de `SEC` — la différence est de nature, pas d'effectif (2026-08-09) |
| SEC | E | Section | `SEC` officiel (2026-08-09). Ligne scindée de l'ancienne entrée fourre-tout `SEC / ESC / E`. **Élément terminal** (« grosse escouade », ~15+ hommes d'un seul tenant, sans sous-éléments) — strictement **sous** `PLT`. Échelle complète : `identification/personnel.md` |
| ESC | E | Escadron | `ESC` officiel (2026-08-09) — escadron (terrestre/maritime) / escadrille (aérien), double sens contextuel (decisions.md § 2) |
| GRP | | Groupe | |
| DET | | Détachement | Officiel = Détachement (2026-08-05) |
| BAT | BTE | Batterie | ⚠️ Distinct de `BT` = Bataillon (2026-08-09) |
| TF | | Task Force | |
| SQ | | Escouade | ~7-15. Échelle des petits éléments : `identification/personnel.md` |
| EQP | EQU, TE | Équipe | `EQP` officiel ; `EQU` et `TE` alternatifs. `TE` réhabilité le 2026-08-09 : un acronyme isolé se lit comme un **Type** (SKILL.md § 3), donc `TE` seul = Équipe ; en position Rôle, `TE` = Tireur élite. Effectifs : `identification/personnel.md` |
| BI | | Binôme | 2 hommes |
| GTIA | | Groupement Tactique Interarme | |
| LEG | | Légion | |
| CRZ | | Croisade | Renommé le 2026-10-10 : l'ancien code `CRS` reste Créature de saut (`infanterie.md`) |
| HRD | | Horde | |

---

## Types d'unité (formation)

> Codes écrits **sans le tiret de liaison** : `-INF` dans un acronyme (`BT-INF`) est le code `INF` (format du 2026-10-10, sens inchangés).

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| ARM | B | Blindés | Force principale = chars de combat. `ARM` officiel (2026-08-04 ; seul sens de `ARM` depuis que l'échelon Armée est `ARMY`, 2026-10-10) — `-B` collisionne avec Bâtiment/Chenillé. ⚠️ Distinct de -MEC |
| INF | I | Infanterie | Infanterie à pied. **Officiel** `INF` (2026-08-04) — `I` collisionne (Industriel/Incendiaire/Intercepteur), conservé en lecture. Intercepteur (aérien) désormais `FI` |
| MOT | M | Motorisé | Infanterie avec transport assigné. `MOT` officiel — `-M` collisionne (Grande ville/Militaire/Poseur de mines) |
| MEC | | Mécanisé | Infanterie transportée par VBTT/véhicules blindés. ⚠️ Distinct de -B : pas de chars comme force principale |
| IB | | Infanterie blindée | Avec IFV |
| IBH | | Infanterie blindée lourde | Avec VBCI |
| IL | ILEG | Infanterie légère | Terrain difficile. `-IL` officiel (plus compact) |
| ART | A | Artillerie | `ART` officiel (par ricochet : `AGR` libère `A`, `ART` déjà officiel Artillerie) |
| GEN | G | Génie | `GEN` officiel (casse normalisée, était `Gén`) — `-G` collisionne (Grenade/Canon-Obusier/Gunship) |
| PNT | GEN.P | Génie pontonnier | |
| | GEN.F | Génie franchissement | Pas de code officiel : `GEN.F` est la seule forme attestée (ancienne cellule `/ GEN.F`) — point ouvert (`decisions.md` § 5) |
| DEF | GEN.D | Génie fortification | ⚠️ `DEF` est aussi officiel pour Défense (plus bas) : collision ouverte (`decisions.md` § 5) |
| | GEN.A | Génie assaut | Pas de code officiel : `GEN.A` est la seule forme attestée (ancienne cellule `/ GEN.A`) — point ouvert (`decisions.md` § 5) |
| ML | MS, GEN.M | Génie minage | |
| SAN | EVASAN | Sanitaire / évacuation | |
| RAD | SIG | Transmission / Signal | |
| PAR | | Parachutistes | `P` libéré (2026-08-04) |
| ABN | | Aéroportée / Airborne | Hélico/avion mais sans parachute |
| LOG | | Logistique | |
| CH | H | Hélicoptère | Groupement d'hélicos |
| CMB | | Armes combinées | Mélange sans dominance |
| ACQ | TA | Acquisition | Acquisition cible pour soutien |
| RES | | Réserves | |
| QRF | | Intervention rapide | Quick Response Force |
| SD | | Infiltration | |
| ADM | | Administratif | |
| MAT | | Matériel | Entretien et mécaniciens |
| MA | | Marines | Casse normalisée le 2026-08-03 (était `-Ma`). Coexiste avec `MA` = Soutien amphibie (Rôle naval) : bassins différents |
| MO | MTN, ALP | Montagne | `MO` officiel, casse normalisée (`Mo`→`MO`) |
| SOF | SF | Forces spéciales | `SOF` officiel — `-SF` collisionne avec Chantier naval |
| TRANS | T | Transport | Logistique et ravitaillement. `TRANS` officiel — `-T` collisionne (Tank/Torpilleur/Traçante) |
| TT | | Transport troupes | |
| MI | | Milice | Normalisé en majuscules le 2026-07-30 (était `-Mi`, seul code du système en casse mixte — cohérence avec `SQ-MI` employé dans les ORBAT). |
| GUE | | Partisans | Civils armés |
| REC | R | Reconnaissance | |
| MP | | Police militaire | |
| GN | | Gendarmes | |
| CAV | | Cavalerie | |
| MAIN | | Maintenance | |
| HOS | | Hôpital | |
| MED | | Médical | |
| UAV | | Drone | |
| FOR | | Forteresse | |
| JNGL | | Jungle | |
| ARTQ | | Arctique | |
| DSR | | Désert | |
| SPT | | Support | Soutien divers. **Officiel** du code `SPT` (2026-08-03) — l'ancien `SPT` = Assistant tireur (`infanterie.md`) a été supprimé, voir les remplaçants `AM` / `GUN` / `TEA` |
| URB | | Urbain | |
| ASS | | Assaut | Ligne unique depuis le 2026-10-10 : le doublon identique de § Types d'unités (petites unités) y est fusionné. ⚠️ Absent de `infanterie.md` — point ouvert (`decisions.md` § 5) |
| DEF | | Défense | ⚠️ Voir `DEF / GEN.D` (Génie fortification) : collision ouverte (`decisions.md` § 5) |
| BRH | | Rupture | Briser les lignes ennemies |
| EXC | | Extraction | Évacuation VIP / civils |

---

## Types d'unités (petites unités)

> **Source unique : `references/infanterie.md`.** Ces codes appartiennent au bassin
> des rôles d'infanterie et y sont définis en détail ; la table ci-dessous n'est
> qu'un **rappel d'aiguillage**, pas une définition concurrente. En cas d'écart,
> `infanterie.md` fait foi. Aligné le 2026-08-10, après constat que les deux tables
> avaient divergé.

<!-- bassin: roles -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| TP | | Tireur précision | Arme plus adaptée (longue etc.) — voir `infanterie.md` |
| TE | | Tireur élite | Fusil de précision. ⚠️ **Position Rôle uniquement** — `TE` isolé (position Type) se lit **Équipe**, alternatif de `EQP` (2026-08-09) |
| F | FUS | Fusilier | `F` officiel, `FUS` alternatif. Arme de base — voir `infanterie.md` (⚠️ `F / FUS` y a aussi un second sens dans le bassin Armement : `F` = Fusil, `FV`/`FA`/`FS` selon le mécanisme, `FH` = Fusil de calibre supérieur) |
| INF | I | Infanterie | `INF` officiel (2026-08-04), `I` alternatif — `I` collisionne avec Industriel / Incendiaire / Intercepteur. Voir `infanterie.md` |
| MS | | Démineur | Voir `infanterie.md` |
| UAV | | Drone | ⚠️ **Divergence non tranchée (2026-08-10)** : `infanterie.md` lit `UAV` comme « **Technicien drone** » (l'opérateur), cette table comme « Drone » (l'engin). Les deux lectures sont défendables selon le bassin ; à arbitrer par Florian — voir `decisions.md` § 5 |
| HW | | Armes lourdes | Décrit l'**unité** articulée autour de l'emploi d'armes lourdes, pas le servant — un servant de mortier ou de MG est `GUN`. Définition de référence : `infanterie.md` § Rôles d'infanterie (2026-08-10) |
