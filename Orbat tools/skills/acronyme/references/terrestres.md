# Véhicules Terrestres & Hélicoptères

Format : `{Type}-{Rôle1}-{Rôle2}`, gabarit fusionné au Type par `.` : `{Type}.{Gabarit}-{Rôle1}.{Rôle2}` (jamais `{Type}-{Gabarit}` — `references/grammaire.md` § Gabarits)

---

## Types — Véhicules terrestres

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| Tk | | Tankette | Blindé très léger, mitrailleuse |
| T | | Tank | Véhicule chenillé et blindé |
| TL | | Tank léger | Variante atomique de `T` par gabarit |
| TM | | Tank moyen | Variante atomique de `T` par gabarit |
| TH | | Tank lourd | Variante atomique de `T` par gabarit |
| TSH | | Tank super-lourd | Variante atomique de `T` par gabarit |
| TV | | Tank à roue | Char léger à roues |
| VL | | Voiture légère | Non blindée ou très peu |
| VM | | Voiture moyenne | |
| VU | | Véhicule utilitaire | Camion (légèrement blindé) |
| VUL | | Véhicule utilitaire léger | Petit camion |
| VB | | Véhicule chenillé | **Acronyme atomique** : véhicule blindé chenillé générique. Aucun lien de dérivation avec `V` (voiture blindée, à roues) — les deux codes désignent des engins distincts et ne collisionnent pas |
| VH | | Véhicule semi-chenillé | Half-track |
| VC | | Véhicule de cavalerie | Très mobile, correctement armé |
| TCI | | Char combat d'infanterie | Lourd/lent, soutien rapproché |
| MBT | | Main Battle Tank | Protection + puissance + mobilité |
| VA | | Voiture amphibie | Capable de traverser des plans d'eau |
| TA | | Tank amphibie | Capable de traverser des plans d'eau. ⚠️ `TA` ici = **Type** (tank amphibie) ; désambiguïsation par position (`decisions.md` § 3, exception à la règle cardinale n°2) |
| SP | | Automoteur | Blindé sans tourelle (AT ou artillerie). Terme générique de sa famille (`SPAT`/`SPHE`/`SPC`/`SPART`/`SPG`/`SPAA`) — `decisions.md` § 4 |
| SPAA | | Automoteur anti-aérien | **Collectif** de tout véhicule automoteur à rôle AA principal, tout châssis. ⚠️ **Exception à `SP`** : tourelle admise (terme trop consacré). Sous-ensembles : `SPAAG` (canon) / `SPAAM` (missile). Voir `decisions.md` § 4 |
| VSP | | Voiture automoteur | Voiture sans tourelle |
| ST | | Position armes fixes | Trépied, déplaçable |
| FIX | | Armes fixes | Permanent (bunker, vissé) |
| REM | | Remorque | |
| CT | | Citerne | |
| RCT | | Citerne remorquée | |
| WM | | Moto | Wheeled Motorbike |
| WMS | | Moto avec sidecar | |
| WB | | Vélo | |
| TRN | | Train | |
| RV | | Rover | Piloté/automate, scientifique/exploration |
| CAV | | Cheval / monture individuelle (Type) | Véhicule rapide / reconnaissance. **Remplace l'ancien `C` = Cheval, retiré le 2026-08-03** (même décision que `C` = Cavalier dans `infanterie.md`) — `C` reste Croiseur (Type naval) et Canonnier (Rôle naval). ⚠️ Désambiguïser par position : `CAV` en Rôle/groupement = cavalerie (type d'unité) |

> ⚠️ **La famille `V*` n'a aucune règle de composition.** Chaque code (`V`, `VL`, `VM`, `VU`,
> `VB`, `VH`, `VTT`, `VBCI`…) est un **acronyme atomique déclaré individuellement** dans ce
> fichier : aucun n'est dérivable par analogie, aucun ne se décompose a posteriori.
> L'ancienne grammaire générative `V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}` a été
> **supprimée le 2026-08-09** (`decisions.md` § 1). Les seuls gabarits universels sont
> `.L` / `.M` / `.H` / `.SH` — ainsi une voiture blindée lourde s'écrit `V.H`, et **non** `VH`
> (qui reste le semi-chenillé).

> ⚠️ **Divergence assumée avec les désignations réelles.** Ce système est un idiolecte : le
> code ne reprend pas le nom du véhicule réel. Ex. : le vrai VBCI français (Nexter) est un 8×8
> à roues, il se note ici `VCI` ou `V8CI` — `VBCI` désigne un engin **chenillé** (ex. AMX-10P).
> Idem le VBL Panhard (léger, 4×4) → `VL` ou `V4L`. **Ne jamais déduire un code du nom réel
> d'un véhicule**, ni l'inverse.

---

## Acronymes combinés (fusions prédéfinies)

> **Liste figée d'acronymes déclarés individuellement.** La colonne *Décomposition* n'est
> qu'un **rappel d'origine historique**, jamais une règle de composition : aucun code absent
> de cette liste n'est dérivable par analogie (cf. `references/grammaire.md` § Règles de composition des fusions,
> « Une fusion n'existe que si explicitement déclarée »). Pour ajouter un code, le déclarer ici — pas le composer à la volée.

<!-- bassin: types -->
| Officiel | Alternatifs | Décomposition | Description |
|---|---|---|---|
| VTT | | code déclaré (V + TT) | Transport de troupes, roues. Palier lourd : `VTT.H` (gabarit universel). Pour un châssis chenillé ou semi-chenillé, employer `VBTT` / `VHTT` et leurs variantes |
| VLTT | IMV | code déclaré (V + TT, léger) | Transport de troupes léger, roues. Alias reconnu : `IMV` |
| VMTT | MRAP | code déclaré (V + TT, moyen) | Transport de troupes moyen, roues. Alias reconnu : `MRAP` (protection anti-mine/anti-embuscade) |
| VBTT | | code déclaré (VB + TT) | Transport de troupes, chenillé. Palier lourd : `VBTT.H` |
| VBLTT | | code déclaré (VB + TT, léger) | Transport de troupes léger, chenillé |
| VBMTT | | code déclaré (VB + TT, moyen) | Transport de troupes moyen, chenillé |
| VHTT | | code déclaré (VH + TT) | Transport de troupes, semi-chenillé. Palier lourd : `VHTT.H` |
| VHLTT | | code déclaré (VH + TT, léger) | Transport de troupes léger, semi-chenillé |
| VHMTT | | code déclaré (VH + TT, moyen) | Transport de troupes moyen, semi-chenillé |
| VCI | | code déclaré (V + CI) | Combat d'infanterie, roues. Palier lourd : `VCI.H` |
| VLCI | | code déclaré (V + CI, léger) | Combat d'infanterie léger, roues |
| VMCI | | code déclaré (V + CI, moyen) | Combat d'infanterie moyen, roues |
| VBCI | | code déclaré (VB + CI) | Combat d'infanterie, chenillé. Palier lourd : `VBCI.H` |
| VBLCI | | code déclaré (VB + CI, léger) | Combat d'infanterie léger, chenillé |
| VBMCI | | code déclaré (VB + CI, moyen) | Combat d'infanterie moyen, chenillé |
| VHCI | | code déclaré (VH + CI) | Combat d'infanterie, semi-chenillé. Palier lourd : `VHCI.H` |
| VHLCI | | code déclaré (VH + CI, léger) | Combat d'infanterie léger, semi-chenillé |
| VHMCI | | code déclaré (VH + CI, moyen) | Combat d'infanterie moyen, semi-chenillé |
| V4L | | code déclaré (V + 4 roues + L) | **Voiture légère à 4 roues.** Redéclaré le 2026-08-09 comme acronyme atomique (il n'existait auparavant que comme exemple de la grammaire supprimée) |
| V8CI | | code déclaré (V + 8 roues + CI) | **Véhicule de combat d'infanterie à 8 roues.** Redéclaré le 2026-08-09 comme acronyme atomique (il n'existait auparavant que comme exemple de la grammaire supprimée) |
| APC | | collectif, rôle `TT`, tout châssis | **Type collectif** (2026-08-04) : tout véhicule à rôle `TT`, quel que soit le châssis (`VTT`/`VBTT`/`VHTT`/`VU-TT`). `VUTT` = alias compact de `VU-TT`. Voir `decisions.md` § 4 |
| IFV | | collectif, rôle `CI`, famille `V` | **Type collectif** (2026-08-04) : tout véhicule à rôle `CI` de la **famille `V` uniquement**. `TCI`/`TVCI` exclus (char, pas véhicule `V`). Voir `decisions.md` § 4 |
| TCI | | T + CI | Char de combat d'infanterie (pas de transport) |
| TLCI | | TL + CI | Char léger de combat d'infanterie |
| TMCI | | TM + CI | Char moyen de combat d'infanterie |
| THCI | | TH + CI | Char lourd de combat d'infanterie |
| TVCI | | TV + CI | Tank à roues de combat d'infanterie |
| VUB | | VU + B | Camion chenillé |
| IG | STIG | ST + IG | Canon infanterie statique. `IG` officiel même en contexte statique (2026-08-04) ; `STIG` variante explicite conservée |
| AA | STAA | ST + AA | **Type collectif** (2026-08-04) : batterie AA déployable, sans châssis. `AA` officiel (équivalent conceptuel de `STAA`, gardé en variante). Pendant véhiculé = `SPAA`. Voir `decisions.md` § 4 |
| ART | START | ST + ART | **Type collectif** (2026-08-04) : pièce d'artillerie déployable, sans châssis. `ART` officiel (équivalent conceptuel de `START`, gardé en variante). Pendant véhiculé = `SPART`. Voir `decisions.md` § 4 |
| MG | STMG | ST + MG | Mitrailleuse statique. `MG` officiel ; `STMG` variante explicite |
| STC | | ST + C | Canon statique moderne en position fixe |
| STG | | ST + G | Obusier statique |
| SPHE | | SP + HE | Canon HE automoteur *(⚠️ chevauchement possible avec `SPG` — à clarifier si besoin, `decisions.md` § 5 : SPHE = canon HE automoteur générique, SPG = soutien-feu direct à l'obusier)* |
| TLAT | | TL + AT | Char léger anti-char — variante de `TAT` ci-dessous |
| TMAT | | TM + AT | Char moyen anti-char — variante de `TAT` ci-dessous |
| THAT | | TH + AT | Char lourd anti-char — variante de `TAT` ci-dessous |
| TAT | | T + AT | **Char anti-char.** Reste sémantiquement un char (blindage tous azimuts, MG coaxiale/annexes, mobilité, va au contact) — l'armement est simplement orienté anti-char plutôt que HE générique. *Ex. : Sherman 76, Sherman SA50.* |
| SPAT | | SP + AT | **Canon anti-char automoteur.** Armement en casemate (pas de tourelle rotative), blindage souvent privilégié à l'avant. Évite le contact et les grandes manœuvres ; rôle = tenir une position, bloquer un axe, embuscade. *Ex. : Jagdpanzer, Jagdtiger, ASU-57/85.* |
| SPG | | SP + G | **Obusier/canon d'assaut automoteur — soutien-feu DIRECT.** Armement = obusier employé en appui rapproché direct, pas en tir indirect longue portée. *Ex. : StuH, SU-152, M44.* **⚠️ Exclut le rôle `ART` (`references/grammaire.md` § Règles de duplication) : pour du tir indirect longue portée, utiliser `SP-ART`/`SPART`.** *Ex. de notation : M44 = `SPG-C.155/MG`.* |
| SPC | | SP + C | **Canon automoteur générique.** Ni exclusivement AT ni exclusivement HE. *Ex. : StuG.* Frontière SPAT/SPC parfois floue et subjective — **le rôle voulu prévaut** : un canon automoteur employé en rôle anti-char se classe `SPAT` même si l'armement paraît « faiblard » pour ce rôle. |
| SPART | | SP + ART | Artillerie automotrice (obusier/canon d'artillerie, tir indirect longue portée). Gabarit universel : `SPART.L` / `SPART.M` / `SPART.H`. Pas de confusion réelle avec SPAT malgré la ressemblance orthographique. *Ex. : Hummel.* |
| SPAAG | | SP + AA + G | **Automoteur AA à canon** (intersection des collectifs `SPAA` et `AAG`). Tout châssis. *Ex. : Gepard = `VB-2AACA`, Tunguska (partie canon) = `VB-2AARTG`, TPK 6.41 = `VU-2AACA.20`.* Voir `decisions.md` § 4 |
| SPAAM | | SP + AA + M | **Automoteur AA à missile** (pendant missile de `SPAAG`). Tout châssis. Guidage porté par la notation du missile embarqué, pas par `SPAAM`. *Ex. : Roland = `VB-AAGM`.* Voir `decisions.md` § 4 |
| TDL | | TD + L | Tank Destroyer léger — variante de `TD` ci-dessous |
| TDM | | TD + M | Tank Destroyer moyen — variante de `TD` ci-dessous |
| TDH | | TD + H | Tank Destroyer lourd — variante de `TD` ci-dessous |
| TD | | Tank Destroyer (+ variantes `TDL`/`TDM`/`TDH` optionnelles) | **Catégorie générique** regroupant tout véhicule spécifiquement conçu et employé pour détruire des chars, qu'il ait une tourelle ou non. Un `SPAT` est toujours un `TD`, mais un `TD` n'est pas forcément un `SPAT` — ex. le M10 : tourelle rotative, "comme un char", mais blindage réduit et rotation de tourelle lente le rendent inadapté au combat blindé intense ; son rôle reste similaire à un SPAT. À utiliser pour les cas qui ne rentrent proprement ni dans `TAT` (pas assez "char" : blindage/mobilité insuffisants pour aller au contact) ni dans `SPAT` (a une tourelle). Le gabarit `L/M/H` est optionnel, à ajouter seulement si la distinction de poids importe dans le contexte. **⚠️ Rôle `AT` implicite : ne pas écrire `TD-AT`.** *Ex. de notation : M10 = `TD-C.90/MG`.* |
| VTL | | VT + L | VTOL léger |
| VTM | | VT + M | VTOL moyen |
| VTH | | VT + H | VTOL lourd |

---

## Hélicoptères

<!-- bassin: types -->
| Officiel | Alternatifs | Décomposition | Description |
|---|---|---|---|
| CH | | Chopper | Hélicoptère générique |
| CHG | | CH + G | Gunship (AH-64 type) |
| CHTT | | CH + TT | Transport de troupes |
| CHATT | | CH + ATT | Hélico d'attaque |
| CHMED | CHSAN | CH + MED/SAN | Évacuation sanitaire. `CHMED` officiel (cohérent avec `MED`) ; `CHSAN` variante |
| CH.L | | CH + L (fusion `.`) | Hélicoptère léger, combinable avec un rôle : `CH.L-TT`, `CH.L-ATT`. Infixe `CHL` interdit — règle dans `references/grammaire.md` § 1 |
| CH.M | | CH + M (fusion `.`) | Hélicoptère moyen (`CHM` interdit : collision avec `(CHM)` = Chimique) |
| CH.H | | CH + H (fusion `.`) | Hélicoptère lourd (`CHH` interdit) |

*Les hélicoptères peuvent utiliser des rôles aériens.*

---

## Marcheurs & véhicules antigrav

> Regroupement thématique, sans restriction d'usage (SKILL.md § Règles cardinales n°4) — introduit à l'occasion du projet Cosmotter, utilisable dans n'importe quel contexte.

<!-- bassin: types -->
| Officiel | Alternatifs | Description |
|---|---|---|
| MK# | | Marcheur/Mecha (# = nombre de pattes, ex. `MK2`) |
| MKL | | Marcheur/Mecha léger |
| MKM | | Marcheur/Mecha moyen |
| MKH | | Marcheur/Mecha lourd |
| TTN | | Titan |
| VG | | Véhicule antigrav |
| TG | | Char antigrav |

---

## Armes de siège

<!-- bassin: types -->
| Officiel | Alternatifs | Description |
|---|---|---|
| BST | | Baliste |
| CAP | | Catapulte |
| TBC | | Trébuchet |
| BLR | | Bélier |
| TDS | | Tour de siège |

---

## Canon ancien (semi-statique)

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| CN | | Canon napoléonien / pré-industriel | Canon à âme lisse ou rayée de la période pré-industrielle. Semi-statique par nature. Notation : `CN.L/M/H` (gabarit) ou `CN.#` (calibre en mm ou livres) |

> `CN` remplace l'ancien raccourci `STC/CN`. `STC` reste l'acronyme pour un canon statique moderne en position fixe.

---

## Rôles terrestres

<!-- bassin: roles -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| HE | | High Explosives | Destruction d'objectifs non blindés |
| AA | | Anti-aérien | |
| AAGM | | AA Missile | **Registre court** du missile anti-aérien sur un porteur (miroir de `ATGM`) ; sa forme longue est `SAM` (tir sol-air), voir section Missiles de `references/infanterie.md` |
| AACA | | AA Canon automatique | Canon automatique anti-aérien (membre du collectif `AAG`) |
| AAC | | AA Canon | Canon anti-aérien (membre du collectif `AAG`) |
| AAG | | AA à canon (collectif) | **Collectif** de tout armement AA **à canon** : `AAC` / `AACA` / `AA-RTG`. ⚠️ **Exclut** `AAGM` (missile). `G` = « canon » générique (sens contextuel à sa racine). Voir `decisions.md` § 4 |
| ART | | Artillerie | Bombardements longue portée. **Officiel** du code `ART`. `ART` = Artistes (`structures.md`) est désormais `ARTS` (résolu 2026-08-04) |
| RART | | Artillerie lance-roquette | |
| HQ | Cmdt | Commandement | Centre mobile, radio. `HQ` officiel (2026-08-04, unique et cohérent) ; `Cmdt` hors gabarit typographique, conservé en lecture |
| TR | | Transport | Matériel générique, non blindé |
| TT | | Transport de troupes | Non blindé |
| TRK | | Tracteur / remorquage | |
| TRM | | Transport munitions | |
| TRML | | Transport munitions léger | |
| TRMH | | Transport munitions lourd | |
| MUN | | Munitions (cargaison) | ⚠️ **Sens désambiguïsés par le Type porteur** (2026-08-10, exception à la règle cardinale n°2) — `MUN` sur un véhicule = cargaison de munitions (ici) ; `MUN` en rôle dominant d'un élément de personnel = fonction d'approvisionnement en munitions (`identification/personnel.md`). `AM` = assistant munitions individuel (`infanterie.md`), code distinct |
| MUNL | | Munitions, chargement léger | |
| MUNM | | Munitions, chargement moyen | |
| MUNH | | Munitions, chargement lourd | |
| TRV | | Transport de véhicule | |
| REC | | Reconnaissance | |
| TA | | Observation artillerie | ⚠️ `TA` = 3 sens désambiguïsés par position (`decisions.md` § 3) : ici Rôle = observation artillerie |
| ENG | | Ingénieur | |
| MED | SAN, MEDEVAC | Médical / Sanitaire | ⚠️ `MED` **officiel**, `MEDEVAC` **déprécié** (conservé en lecture, ne plus produire — décision actée alignée le 2026-08-02). Cohérent avec `references/infanterie.md` (rôle `MED`) |
| SIG | | Signal / Transmission | Équipé radio |
| EW | | Guerre électronique | |
| MAIN | | Maintenance | |
| LOG | | Logistique | Porteur/remorque de ravitaillement (munitions, vivres, rechanges). ⚠️ `SUP` n'est **pas** un code valide (erreur fréquente) — décision du 2026-07-30 (`REM-SUP` → `REM-LOG`) |
| SPT | | Support | Appui/soutien générique (même sens que `-SPT`, `groupements.md`) |
| CT | | Citerne et transport de fluide | |
| MLRS | | Lance-roquettes multiple | M270 type |
| TTNK | | Armes tueuses de titans | |
| NBC | | Protection NBC | |
| CI | | Combat d'infanterie | Soutien rapproché |
| BDZ | | Bulldozer | |
| ML | | Poseur de mines | Minelayer. ⚠️ Distinct de `MS`, pas un alias (cohérent avec `maritimes.md` et `infanterie.md`, 2026-08-02) |
| MS | | Démineur | Dragueur/démineur (minesweeper). ⚠️ Distinct de `ML` |
| SD | | Furtif (silence/discrétion) | ⚠️ Distinct de STH |
| STH | | Stealth | Furtivité visuelle/radar ⚠️ Distinct de SD |
| ATT | | Attaque / Assaut | Rupture de position |
| DEF | | Défense | Tenue de position |
| MNV | | Maneuvre | Spécialisé maniabilité, esquive, agilité |
| BRH | | Breacher | Rupture de défense/obstacle/front |
| UAV | | Drone | |
| NV | | Nocturne | Vision nocturne (rôle) ⚠️ NVG = équipement spécifique (jumelles) |

---

## Armement terrestre

<!-- bassin: roles -->
| Officiel | Alternatifs | Signification | Notes |
|---|---|---|---|
| C | | Canon | Rechargé **obus par obus** après chaque tir (critère `C` vs `CA` : `references/grammaire.md` § 2). Gabarit : `C.L` / `C.M` / `C.H` (gabarit universel), ou calibre `C.105`. Les anciennes formes `LC`/`MC`/`HC` sont supprimées (2026-10-10, « le canon cède ») : `LC` = Lance, `HC` = Hache. ⚠️ **`C` et `G` sont deux armes distinctes, pas des alias** (2026-08-02) |
| G | HWZ | Obusier | **`G` officiel**, `HWZ` alternatif de lecture uniquement (2026-10-10, lignes `G` et `HWZ / G` fusionnées). ⚠️ Distinct du canon `C`. `G` = Gunship (rôle aérien) : même code, Type porteur différent (exception à la règle cardinale n°2) |
| RK | R, RKT | Roquette non guidée | `RK` officiel (2026-08-04) — `R` collisionne avec Reconnaissance (groupement) et Roquette |
| MG | | Mitrailleuse | |
| AT | | Anti-tank / chasseur de char | |
| ATGM | | AT + GM (missile guidé anti-char) | **Registre court** : à employer sur un *porteur* (véhicule/unité), portée et guidage non spécifiés. Miroir de `AAGM` (AA + GM). Pour spécifier portée/guidage, basculer sur la forme longue de la section Missiles (`references/infanterie.md`) — jamais de portée ni de guidage sur un porteur. Section Missiles refondue le 2026-07-30 (deux registres articulés). |
| GMG | | Grenade Machine Gun | Lance-grenade automatique |
| GL | | Lance-grenade | |
| CA | | Canon automatique | Alimentation par **magasin/bande** + tir auto/rafale (`references/grammaire.md` § 2) |
| LCA | | Canon automatique léger | Variante atomique de `CA` |
| MCA | | Canon automatique moyen | Variante atomique de `CA` |
| HCA | | Canon automatique lourd | Variante atomique de `CA` |
| CAA | | Canon automatique Anti-Aérien | Fusion `CA` + `AA` |
| LCAA | | Canon automatique Anti-Aérien léger | Fusion par gabarit |
| MCAA | | Canon automatique Anti-Aérien moyen | Fusion prédéfinie (usage AA permanent ; `MCA.AA` = rôle AA circonstanciel) |
| HCAA | | Canon automatique Anti-Aérien lourd | Fusion par gabarit |
| LM | | Lance-missile générique | |
| IG | | Canon infanterie | |
| MOR | | Mortier | Calibre : `MOR.81` (convention calibre) |
| LMOR | | Mortier léger | |
| MMOR | | Mortier moyen | |
| HMOR | | Mortier lourd | |

> **Règles de construction associées** — critère mécanique `C` vs `CA`, convention `MCA.AA` vs `MCAA`, convention calibre `C.90`/`CA.20` (forme collée `C90` abandonnée le 2026-08-10) : **`references/grammaire.md` § 2 à § 4** (source unique, non recopiée ici).
