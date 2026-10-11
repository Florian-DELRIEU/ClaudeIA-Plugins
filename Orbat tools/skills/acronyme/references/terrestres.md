# Véhicules Terrestres & Hélicoptères

Format : `{Type}-{Gabarit} {Rôle1}-{Rôle2}` ou `{Type}.{Gabarit}-{Rôle1}.{Rôle2}`

---

## Types — Véhicules terrestres

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| Tk | Tankette | Blindé très léger, mitrailleuse |
| T | Tank | Véhicule chenillé et blindé |
| TL / TM / TH / TSH | Tank L/M/H/SH | Variantes par gabarit |
| TV | Tank à roue | Char léger à roues |
| VL | Voiture légère | Non blindée ou très peu |
| VM | Voiture moyenne | |
| VU | Véhicule utilitaire | Camion (légèrement blindé) |
| VUL | Véhicule utilitaire léger | Petit camion |
| VB | Véhicule chenillé | **Acronyme atomique** : véhicule blindé chenillé générique. Aucun lien de dérivation avec `V` (voiture blindée, à roues) — les deux codes désignent des engins distincts et ne collisionnent pas |
| VH | Véhicule semi-chenillé | Half-track |
| VC | Véhicule de cavalerie | Très mobile, correctement armé |
| TCI | Char combat d'infanterie | Lourd/lent, soutien rapproché |
| MBT | Main Battle Tank | Protection + puissance + mobilité |
| VA / TA | Voiture/Tank amphibie | Capable de traverser des plans d'eau. ⚠️ `TA` ici = **Type** (tank amphibie) ; désambiguïsation par position (voir SKILL.md § Décisions établies) |
| SP | Automoteur | Blindé sans tourelle (AT ou artillerie). Collectif Tier 1 de sa famille (`SPAT`/`SPHE`/`SPC`/`SPART`/`SPG`/`SPAA`) |
| SPAA | Automoteur anti-aérien | **Collectif** de tout véhicule automoteur à rôle AA principal, tout châssis. ⚠️ **Exception à `SP`** : tourelle admise (terme trop consacré). Sous-ensembles : `SPAAG` (canon) / `SPAAM` (missile). Voir SKILL.md § Acronymes collectifs |
| VSP | Voiture automoteur | Voiture sans tourelle |
| ST | Position armes fixes | Trépied, déplaçable |
| FIX | Armes fixes | Permanent (bunker, vissé) |
| REM | Remorque | |
| CT | Citerne | |
| RCT | Citerne remorquée | |
| WM | Moto | Wheeled Motorbike |
| WMS | Moto avec sidecar | |
| WB | Vélo | |
| TRN | Train | |
| RV | Rover | Piloté/automate, scientifique/exploration |
| CAV | Cheval / monture individuelle (Type) | Véhicule rapide / reconnaissance. **Remplace l'ancien `C` = Cheval, retiré le 2026-08-03** (même décision que `C` = Cavalier dans `infanterie.md`) — `C` reste Croiseur (Type naval) et Canonnier (Rôle naval). ⚠️ Désambiguïser par position : `CAV` en Rôle/groupement = cavalerie (type d'unité) |

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
> de cette liste n'est dérivable par analogie (cf. `SKILL.md` § « Une fusion n'existe que si
> explicitement déclarée »). Pour ajouter un code, le déclarer ici — pas le composer à la volée.

| Acronyme | Décomposition | Description |
|----------|--------------|-------------|
| VTT / VLTT / VMTT / VTT.H | codes déclarés (V + TT) | Transport de troupes, roues — gabarit optionnel. Alias reconnus : `IMV` = `VLTT`, `MRAP` = `VMTT` (protection anti-mine/anti-embuscade). Pour un châssis chenillé ou semi-chenillé, employer les codes déclarés des deux lignes suivantes (`VBMTT`, `VHMTT`…) |
| VBTT / VBLTT / VBMTT / VBTT.H | codes déclarés (VB + TT) | Transport de troupes, chenillé — gabarit optionnel |
| VHTT / VHLTT / VHMTT / VHTT.H | codes déclarés (VH + TT) | Transport de troupes, semi-chenillé — gabarit optionnel |
| VCI / VLCI / VMCI / VCI.H | codes déclarés (V + CI) | Combat d'infanterie, roues — gabarit optionnel |
| VBCI / VBLCI / VBMCI / VBCI.H | codes déclarés (VB + CI) | Combat d'infanterie, chenillé — gabarit optionnel |
| VHCI / VHLCI / VHMCI / VHCI.H | codes déclarés (VH + CI) | Combat d'infanterie, semi-chenillé — gabarit optionnel |
| V4L | code déclaré (V + 4 roues + L) | **Voiture légère à 4 roues.** Redéclaré le 2026-08-09 comme acronyme atomique (il n'existait auparavant que comme exemple de la grammaire supprimée) |
| V8CI | code déclaré (V + 8 roues + CI) | **Véhicule de combat d'infanterie à 8 roues.** Redéclaré le 2026-08-09 comme acronyme atomique (il n'existait auparavant que comme exemple de la grammaire supprimée) |
| APC | collectif, rôle `TT`, tout châssis | **Type collectif** (2026-08-04) : tout véhicule à rôle `TT`, quel que soit le châssis (`VTT`/`VBTT`/`VHTT`/`VU-TT`). `VUTT` = alias compact de `VU-TT`. Voir SKILL.md § Acronymes collectifs |
| IFV | collectif, rôle `CI`, famille `V` | **Type collectif** (2026-08-04) : tout véhicule à rôle `CI` de la **famille `V` uniquement**. `TCI`/`TVCI` exclus (char, pas véhicule `V`). Voir SKILL.md § Acronymes collectifs |
| TCI / TLCI / TMCI / THCI | T/TL/TM/TH + CI | Char de combat d'infanterie (pas de transport) |
| TVCI | TV + CI | Tank à roues de combat d'infanterie |
| VUB | VU + B | Camion chenillé |
| IG / STIG | ST + IG | Canon infanterie statique. `IG` officiel même en contexte statique (2026-08-04) ; `STIG` variante explicite conservée |
| AA / STAA | ST + AA | **Type collectif** (2026-08-04) : batterie AA déployable, sans châssis. `AA` officiel (équivalent conceptuel de `STAA`, gardé en variante). Pendant véhiculé = `SPAA`. Voir SKILL.md § Acronymes collectifs |
| ART / START | ST + ART | **Type collectif** (2026-08-04) : pièce d'artillerie déployable, sans châssis. `ART` officiel (équivalent conceptuel de `START`, gardé en variante). Pendant véhiculé = `SPART`. Voir SKILL.md § Acronymes collectifs |
| MG / STMG | ST + MG | Mitrailleuse statique. `MG` officiel ; `STMG` variante explicite |
| STC | ST + C | Canon statique moderne en position fixe |
| STG | ST + G | Obusier statique |
| SPHE | SP + HE | Canon HE automoteur *(⚠️ chevauchement possible avec `SPG` — à clarifier si besoin : SPHE = obus HE générique, SPG = obusier dédié tir indirect)* |
| TAT / TLAT / TMAT / THAT | T/TL/TM/TH + AT | **Char anti-char.** Reste sémantiquement un char (blindage tous azimuts, MG coaxiale/annexes, mobilité, va au contact) — l'armement est simplement orienté anti-char plutôt que HE générique. *Ex. : Sherman 76, Sherman SA50.* |
| SPAT | SP + AT | **Canon anti-char automoteur.** Armement en casemate (pas de tourelle rotative), blindage souvent privilégié à l'avant. Évite le contact et les grandes manœuvres ; rôle = tenir une position, bloquer un axe, embuscade. *Ex. : Jagdpanzer, Jagdtiger, ASU-57/85.* |
| SPG | SP + G | **Obusier/canon d'assaut automoteur — soutien-feu DIRECT.** Armement = obusier employé en appui rapproché direct, pas en tir indirect longue portée. *Ex. : StuH, SU-152, M44.* **⚠️ Exclut le rôle `ART` (voir SKILL.md) : pour du tir indirect longue portée, utiliser `SP-ART`/`SPART`.** *Ex. de notation : M44 = `SPG-C.155/MG`.* |
| SPC | SP + C | **Canon automoteur générique.** Ni exclusivement AT ni exclusivement HE. *Ex. : StuG.* Frontière SPAT/SPC parfois floue et subjective — **le rôle voulu prévaut** : un canon automoteur employé en rôle anti-char se classe `SPAT` même si l'armement paraît « faiblard » pour ce rôle. |
| SPART / SPART.L/M/H | SP + ART | Artillerie automotrice (obusier/canon d'artillerie, tir indirect longue portée). Pas de confusion réelle avec SPAT malgré la ressemblance orthographique. *Ex. : Hummel.* |
| SPAAG | SP + AA + G | **Automoteur AA à canon** (intersection des collectifs `SPAA` et `AAG`). Tout châssis. *Ex. : Gepard = `VB-2AACA`, Tunguska (partie canon) = `VB-2AARTG`, TPK 6.41 = `VU-2AACA.20`.* Voir SKILL.md § Acronymes collectifs |
| SPAAM | SP + AA + M | **Automoteur AA à missile** (pendant missile de `SPAAG`). Tout châssis. Guidage porté par la notation du missile embarqué, pas par `SPAAM`. *Ex. : Roland = `VB-AAGM`.* Voir SKILL.md § Acronymes collectifs |
| **TD** / **TDL / TDM / TDH** *(nouveau)* | Tank Destroyer (+ gabarit optionnel L/M/H) | **Catégorie générique** regroupant tout véhicule spécifiquement conçu et employé pour détruire des chars, qu'il ait une tourelle ou non. Un `SPAT` est toujours un `TD`, mais un `TD` n'est pas forcément un `SPAT` — ex. le M10 : tourelle rotative, "comme un char", mais blindage réduit et rotation de tourelle lente le rendent inadapté au combat blindé intense ; son rôle reste similaire à un SPAT. À utiliser pour les cas qui ne rentrent proprement ni dans `TAT` (pas assez "char" : blindage/mobilité insuffisants pour aller au contact) ni dans `SPAT` (a une tourelle). Le gabarit `L/M/H` est optionnel, à ajouter seulement si la distinction de poids importe dans le contexte. **⚠️ Rôle `AT` implicite : ne pas écrire `TD-AT`.** *Ex. de notation : M10 = `TD-C.90/MG`.* |
| VTL / VTM / VTH | VT + L/M/H | VTOL L/M/H |

---

## Hélicoptères

| Acronyme | Décomposition | Description |
|----------|--------------|-------------|
| CH | Chopper | Hélicoptère générique |
| CHG | CH + G | Gunship (AH-64 type) |
| CHTT | CH + TT | Transport de troupes |
| CHATT | CH + ATT | Hélico d'attaque |
| CHMED / CHSAN | CH + MED/SAN | Évacuation sanitaire. `CHMED` officiel (cohérent avec `MED`) ; `CHSAN` variante |
| CH.L / CH.M / CH.H | CH + gabarit (fusion `.`) | Gabarit de l'appareil (léger/moyen/lourd), combinable avec un rôle en suffixe : `CH.L-TT` (hélico léger de transport), `CH.L-ATT` (hélico léger d'attaque). **Fusion `.` obligatoire, jamais infixe direct** (`CHL`/`CHM`/`CHH` interdits) : `CHM` collide avec `(CHM)`=Chimique (propulsion, `aeriens.md`) et avec le préfixe de `CHMED`. Décision actée le 2026-07-30 : pour rester cohérent, la règle `.` s'applique uniformément aux trois gabarits (pas de traitement différencié par lettre). |

*Les hélicoptères peuvent utiliser des rôles aériens.*

---

## Marcheurs & véhicules antigrav

> Regroupement thématique, sans restriction d'usage (SKILL.md § Règles cardinales n°4) — introduit à l'occasion du projet Cosmotter, utilisable dans n'importe quel contexte.

| Acronyme | Description |
|----------|-------------|
| MK# / MKL/M/H | Marcheur/Mecha (# pattes) |
| TTN | Titan |
| VG | Véhicule antigrav |
| TG | Char antigrav |

---

## Armes de siège

| Acronyme | Description |
|----------|-------------|
| BST | Baliste |
| CAP | Catapulte |
| TBC | Trébuchet |
| BLR | Bélier |
| TDS | Tour de siège |

---

## Canon ancien (semi-statique)

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| CN | Canon napoléonien / pré-industriel | Canon à âme lisse ou rayée de la période pré-industrielle. Semi-statique par nature. Notation : `CN.L/M/H` (gabarit) ou `CN.#` (calibre en mm ou livres) |

> `CN` remplace l'ancien raccourci `STC/CN`. `STC` reste l'acronyme pour un canon statique moderne en position fixe.

---

## Rôles terrestres

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| HE | High Explosives | Destruction d'objectifs non blindés |
| AA | Anti-aérien | |
| AAGM / AACA / AAC | AA Missile / Canon Auto / Canon | `AAGM` = **registre court** du missile anti-aérien sur un porteur (miroir de `ATGM`) ; sa forme longue est `SAM` (tir sol-air), voir section Missiles de `references/infanterie.md`. |
| AAG | AA à canon (collectif) | **Collectif Tier 2** de tout armement AA **à canon** : `AAC` / `AACA` / `AA-RTG`. ⚠️ **Exclut** `AAGM` (missile). `G` = « canon » générique (sens contextuel à sa racine). Voir SKILL.md § Acronymes collectifs |
| ART | Artillerie | Bombardements longue portée. **Officiel** du code `ART`. `ART` = Artistes (`structures.md`) est désormais `ARTS` (résolu 2026-08-04) |
| RART | Artillerie lance-roquette | |
| HQ / Cmdt | Commandement | Centre mobile, radio. `HQ` officiel (2026-08-04, unique et cohérent) ; `Cmdt` hors gabarit typographique, conservé en lecture |
| TR / TT | Transport / Transport de troupes | Non blindé |
| TRK | Tracteur / remorquage | |
| TRM / TRML / TRMH | Transport munitions L/M/H | |
| MUN / MUNL / MUNM / MUNH | Munitions L/M/H | ⚠️ **Trois sens désambiguïsés par la position** (2026-08-10) — `MUN` sur un véhicule = cargaison de munitions (ici) ; `MUN` en rôle dominant d'un élément de personnel = fonction d'approvisionnement en munitions (`identification/personnel.md`) ; `AM` = assistant munitions individuel (`infanterie.md`) |
| TRV | Transport de véhicule | |
| REC / TA | Reconnaissance / Observation artillerie | ⚠️ `TA` = 3 sens désambiguïsés par position (voir SKILL.md § Décisions établies) : ici Rôle = observation artillerie |
| ENG | Ingénieur | |
| MED / SAN | Médical / Sanitaire | ⚠️ `MED` **officiel**, `MEDEVAC` **déprécié** (conservé en lecture, ne plus produire — décision actée alignée le 2026-08-02). Cohérent avec `references/infanterie.md` (rôle `MED`) |
| SIG | Signal / Transmission | Équipé radio |
| EW | Guerre électronique | |
| MAIN | Maintenance | |
| LOG / SPT | Logistique / Support | ⚠️ `SUP` n'est **pas** un code valide (erreur fréquente) : utiliser `LOG` pour un porteur/remorque de ravitaillement (munitions, vivres, rechanges), `SPT` pour un appui/soutien générique. Décision actée le 2026-07-30 lors de l'audit des lexiques (`REM-SUP` → `REM-LOG`). |
| CT | Citerne et transport de fluide | |
| MLRS | Lance-roquettes multiple | M270 type |
| TTNK | Armes tueuses de titans | |
| NBC | Protection NBC | |
| CI | Combat d'infanterie | Soutien rapproché |
| BDZ | Bulldozer | |
| ML / MS | Poseur de mines / Démineur | ⚠️ **Deux rôles distincts, pas des alias** : `ML` = poseur (minelayer), `MS` = dragueur/démineur (minesweeper). Cohérent avec `maritimes.md` et `infanterie.md` (incohérence tranchée le 2026-08-02) |
| SD | Furtif (silence/discrétion) | ⚠️ Distinct de STH |
| STH | Stealth | Furtivité visuelle/radar ⚠️ Distinct de SD |
| ATT | Attaque / Assaut | Rupture de position |
| DEF | Défense | Tenue de position |
| MNV | Maneuvre | Spécialisé maniabilité, esquive, agilité |
| BRH | Breacher | Rupture de défense/obstacle/front |
| UAV | Drone | |
| NV | Nocturne | Vision nocturne (rôle) ⚠️ NVG = équipement spécifique (jumelles) |

---

## Armement terrestre

| Acronyme | Signification | Notes |
|----------|--------------|-------|
| C (LC/MC/HC = Léger/Moyen/Lourd) | Canon | Rechargé **obus par obus** après chaque tir (voir note C vs CA). ⚠️ **`C` et `G` sont deux armes distinctes, pas des alias** (l'ancienne écriture `C / G` laissait croire à une équivalence — corrigé le 2026-08-02) |
| G | Obusier | Voir aussi `HWZ / G` plus bas (même arme). ⚠️ Distinct du canon `C` |
| RK / R / RKT | Roquette non guidée | `RK` officiel (2026-08-04) — `R` collisionne avec Reconnaissance (groupement) et Roquette |
| MG | Mitrailleuse | |
| AT | Anti-tank / chasseur de char | |
| ATGM | AT + GM (missile guidé anti-char) | **Registre court** : à employer sur un *porteur* (véhicule/unité), portée et guidage non spécifiés. Miroir de `AAGM` (AA + GM). Pour spécifier portée/guidage, basculer sur la forme longue de la section Missiles (`references/infanterie.md`) — jamais de portée ni de guidage sur un porteur. Section Missiles refondue le 2026-07-30 (deux registres articulés). |
| GMG / GL | Grenade Machine Gun / Lance-grenade | |
| CA / LCA / MCA / HCA | Canon automatique L/M/H | Alimentation par **magasin/bande** + tir auto/rafale (voir note C vs CA) |
| CAA / LCAA / MCAA / HCAA | Canon automatique Anti-Aérien L/M/H | Fusion CA + AA par gabarit |
| LM | Lance-missile générique | |
| IG | Canon infanterie | |
| HWZ / G | Obusier | |
| MOR / LMOR / MMOR / HMOR | Mortier L/M/H | |

> **Convention MCA.AA vs MCAA :** `MCA.AA` note un canon auto moyen en *rôle AA circonstanciel*. `MCAA` est la fusion prédéfinie pour un usage AA permanent. Même logique pour LCAA et HCAA.

> **`C` vs `CA` — critère mécanique, pas de calibre :**
> - **`CA`** (canon automatique) = alimentation par **magasin ou bande** + capacité de **tir automatique / rafale** (ex. tourelle 20mm d'un VBCI, canon d'un CV90).
> - **`C`** (canon) = pièce rechargée **obus par obus après chaque tir**, y compris avec une **aide au chargement / autoloader** (ex. Leclerc, M10, canon de 90mm d'un EBR). Un chargeur automatique n'en fait **pas** un `CA` : il faut toujours engager un nouvel obus dans la culasse entre deux tirs.
> - La distinction est **mécanique** (mode d'alimentation), indépendante du calibre.

> **Convention calibre (préférée au gabarit) :** quand le calibre est connu, l'ajouter en suffixe **fusionné par un point** plutôt que d'utiliser `L/M/H` : `C.90` (canon 90 mm), `CA.20` (canon auto 20 mm), `C.105`, `C.155`, `MOR.81`. Le gabarit `L/M/H` reste le repli quand le calibre est inconnu ou non pertinent. Exemples : `TD-C.90/MG`, `VBCI-CA.20/MG`, `SPG-C.155/MG`.
> ⚠️ **La forme collée (`C90`, `CA20`) est abandonnée le 2026-08-10** : elle contredisait `SKILL.md` § Notation numérique, où `ACR#` désigne un **nombre physique** (roues, pattes) — `C90` s'y lirait « 90 roues ». Conservée en lecture pour les fichiers antérieurs, ne plus produire.

> **Règles de construction associées** — critère mécanique `C` vs `CA`, convention `MCA.AA` vs `MCAA`, convention calibre `C.90`/`CA.20` : voir aussi **`references/grammaire.md` § 2-4**.
