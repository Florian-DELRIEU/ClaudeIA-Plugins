# Châssis → Type (toutes nations, toutes époques)

On classe le **châssis** par archétype, ce qui fixe le **Type**. Les colonnes « exemples »
sont volontairement multi-nations pour montrer la généralité. Les rôles/armements viennent
ensuite en suffixes (voir `METHODE.md`).

> Ce fichier est **extensible** : on l'enrichit à chaque nouveau cas résolu. Les entrées
> marquées ⚑ sont des points d'idiolecte à confirmer par Florian (voir bas de page).

> **`IFV` n'est pas un code du système** — c'est un terme générique d'identification qui
> regroupe plusieurs codes existants selon le châssis : `VCI`, `VBCI`, `VTCI`, etc. Utile
> pour reconnaître rapidement la famille d'un véhicule réel avant de choisir le Type
> précis ci-dessous ; ne jamais l'écrire tel quel comme acronyme du système.

---

## Terrestres — chenillés

| Archétype de châssis | Discriminants | Type | Exemples (multi-nations) |
|----------------------|---------------|------|--------------------------|
| Char de bataille | tourelle, canon principal, protection lourde, doctrine MBT | `MBT` | Leclerc, AMX-30, Leopard 1/2, M1, T-72/80/90, Challenger, Merkava |
| Char léger/moyen (hist.) | chenillé, canon, blindage modéré | `TL` / `TM` / `TH` | AMX-13, M24 Chaffee, PT-76, M4 Sherman |
| IFV (transport + soutien) | chenillé, transport troupes **et** canon auto/appui | `VBCI` — *code atomique : combat d'infanterie chenillé* (confirmé) | AMX-10P, M2 Bradley, BMP-1/2/3, Marder, Warrior |
| APC pur | chenillé, transport, sans canon d'appui | `VBTT` | M113, AMX-VCI, FV432 |
| Char anti-char chenillé (tourelle) | chenillé, tourelle, canon AT, reste un char (blindage tous azimuts, mobilité) | `TAT` (+ gabarit `TLAT`/`TMAT`/`THAT`) | Sherman 76, Sherman SA50 |
| Canon AT automoteur chenillé (casemate) | chenillé, sans tourelle, canon AT, position/embuscade | `SPAT` | Jagdpanzer, Jagdtiger, ASU-57/85 |
| Chasseur de char générique (config variable) | chenillé, conçu/employé pour détruire des chars, tourelle ou non, mobilité de combat souvent limitée | `TD` (+ gabarit `TDL`/`TDM`/`TDH`) | M10, ELC bis — voir clarification détaillée plus bas |

## Terrestres — roues blindées

**Discriminant central : le niveau de l'armement ET de la protection, pas la présence
d'une tourelle.** `TV` = « char à roues » — un engin dont l'**armement principal** ET la
**protection** équivalent à ceux d'un **char léger** de son époque, la seule différence
étant les roues à la place des chenilles (mobilité tout-terrain moindre, mais gabarit
blindage/puissance de feu comparable). Tant que l'un des deux critères (armement ou
protection) reste en dessous de ce niveau — même avec tourelle et canon léger — l'engin
reste `V` (**voiture blindée à roues**). Le seuil s'apprécie **de la même façon, mais
séparément**, pour le pendant chenillé `VB` : `VB` est le châssis chenillé qui n'atteint pas
le niveau char (au-delà, on passe à `TL`/`TM`/`TH`/`MBT`). `V` et `VB` sont deux acronymes
atomiques distincts, jamais interchangeables. Catégorie **transversale aux époques** : elle
regroupe aussi bien les automitrailleuses lourdes de la Seconde Guerre mondiale que les
engins modernes.

| Archétype de châssis | Discriminants | Type | Exemples (toutes époques) |
|----------------------|---------------|------|----------------------------|
| Char à roues (armement + protection niveau char léger) | roues, armement principal ET blindage comparables à un char léger de son époque | `TV` | AMX-10RC (105mm), ERC-90 Sagaie, AML-90, EBR-90, Sd.Kfz. 234 Puma (all., 39-45), M8 Greyhound (US, 39-45), Rooikat, Centauro |
| Voiture blindée (armement et/ou protection sous le niveau char léger) | roues, blindage léger, armement léger/moyen (MG, canon léger, ATGM porté) même avec tourelle | `V` | VBL Panhard, Fennek, AML-60 (mortier 60mm), Ferret |
| APC/IFV à roues | roues, blindé, transport troupes | `VTT` (APC) / `VCI` (IFV léger à roues) — codes déclarés, pas des dérivés de `V` | VAB, Stryker, BTR-80, Pandur, Piranha |
| Camion/utilitaire | roues, non blindé ou très peu | `VU` / `VL` | voir section suivante |

> ⚠️ Le nom réel ne suffit jamais à trancher seul — deux véhicules de la même famille
> peuvent tomber de part et d'autre du seuil selon leur armement/protection (ex. AML-60
> mortier, blindage léger → `V` ; AML-90 canon 90mm, blindage renforcé → `TV`). Toujours
> vérifier armement **et** protection, pas le nom de plateforme.

## Terrestres — roues souples / utilitaires

| Archétype | Discriminants | Type | Exemples |
|-----------|---------------|------|----------|
| Camion | roues, non blindé, logistique/porteur | `VU` (`VUL` léger) | Berliet, TRM-2000/4000, Kamaz, Ural, M35 |
| 4×4 léger | roues, non blindé, léger | `VL` | Jeep, Hotchkiss M201, HMMWV (souple) |
| Moto | — | `WM` (`WMS` sidecar) | — |
| Remorque | tractée | `REM` | citernes, munitions |

## Chasseurs de char, canons AT et artillerie automotrice — clarification

Quatre familles se ressemblent visuellement (châssis automoteur, canon proéminent) mais
répondent à des logiques différentes. **Le rôle voulu/employé prévaut sur l'armement
exact** quand la frontière est floue (cas `SPAT` vs `SPC`).

| Code | Nature | Tourelle | Doctrine | Exemples |
|------|--------|----------|----------|----------|
| `TAT` / `T{L/M/H}AT` | **Char anti-char** — reste un char à part entière (blindage tous azimuts, MG, mobilité, va au contact), armement orienté AT | ✅ | Combat blindé mobile, cherche l'affrontement | Sherman 76, Sherman SA50 |
| `SPAT` | **Canon AT automoteur** — armement en casemate, blindage souvent renforcé à l'avant | ❌ | Évite le contact/manœuvre ; tient une position, embuscade, bloque un axe | Jagdpanzer, Jagdtiger, ASU-57/85 |
| `SPG` | **Obusier automoteur** — armement HE/tir indirect, pas un canon AT | ❌ (généralement) | Appui-feu, destruction d'objectifs non blindés | StuH, SU-152 |
| `SPC` | **Canon automoteur générique** — ni exclusivement AT ni exclusivement HE | ❌ | Polyvalent | StuG |
| `SPART` | Artillerie automotrice — tir indirect longue portée | Variable | Appui-feu longue portée | Hummel |
| **`TD` / `TDL` / `TDM` / `TDH`** | **Tank Destroyer — catégorie générique.** Regroupe tout véhicule conçu/employé pour détruire des chars, tourelle ou non. `SPAT` ⊂ `TD`, mais `TD` ⊄ `SPAT`. À utiliser pour les cas qui ne rentrent proprement ni dans `TAT` (blindage/mobilité insuffisants pour aller au contact) ni dans `SPAT` (a une tourelle). Gabarit `L/M/H` optionnel. | Variable | Destruction de chars, quelle que soit la config | M10 (tourelle mais rôle et mobilité de combat proches d'un SPAT), ELC bis |

**Règle d'arbitrage SPAT vs SPC** : quand la frontière semble subjective, catégoriser en
`SPAT` dès que le véhicule est **conçu ou employé** en rôle anti-char, même avec un canon
« faiblard » pour ce rôle. Le rôle prévaut sur la puissance nominale de l'armement.

**Cas d'école ELC bis** : petit char léger chenillé, canon 90mm, aucune mitrailleuse,
équipage 2. Sa doctrine (infiltration, destruction de chars, pas de combat rapproché
infanterie) en fait un chasseur de char, pas un char léger polyvalent — d'où `TD` (ou
`TAT` si on veut souligner qu'il conserve tourelle + mobilité proche d'un char).

---

## Artillerie & AA (le châssis tranche, cf. cas d'école)

| Archétype | Type | Exemples |
|-----------|------|----------|
| Canon sur camion | `VU-ART` | CAESAR |
| Automoteur à tourelle dédié | `SPART` / `SPG` / `SPC` | GCT/AUF1, M109, PzH2000 |
| Mortier (porté ou tracté) | `MOR.M` / `MOR.H` (ou `VTT-MOR` si porté VAB) | MO-81, MO-120-RT |
| AA automoteur dédié | `SP-AACA` / `SP-AAGM` | Guépard, ZSU-23-4 Shilka, Gepard |
| AA tracté | `START` + rôle AA / `AA` | Tarasque 20 mm |
| SAM sur châssis | `V-AAGM` (léger) / châssis dédié + `AAGM` | VBL Mistral, Roland, Crotale (`V-RAD.AA`) |

## Hélicoptères

| Archétype | Type | Exemples |
|-----------|------|----------|
| Hélico d'attaque lourd | `CHG` | Tigre, AH-64 Apache, Mi-24/28 |
| Hélico d'attaque léger | `CH.L-ATT` | Gazelle/HOT, OH-58D armé |
| Reco léger | `CH-REC` | Gazelle-obs, Alouette III, OH-58 |
| Transport léger | `CH.L-TT` | Alouette, Colibri |
| Transport moyen/manœuvre | `CH-TT.MR` / `CH-T` | NH90, Puma/Super Puma, UH-60 |

## Aériens (voilure fixe) — renvoi

Voir `references/aeriens.md` (Type = `A`/`AH`/`AV`… + rôle). Même logique : la cellule
fixe le Type, la mission donne le rôle.

---

## Décisions actées (idiolecte Florian)

- **`TV` vs `V` (roues blindées) :** le seuil est **armement ET protection** ensemble, pas la
  silhouette. `TV` = équivalent d'un char léger (armement + blindage), simplement à roues au
  lieu de chenilles ; `V` = tout le reste **à roues**, y compris avec tourelle, dès qu'un des
  deux critères reste en dessous. Catégorie transversale à toutes les époques (cf. tableau
  ci-dessus, exemples 39-45 → moderne).
- **Pendant chenillé :** le même seuil s'applique **indépendamment** au chenillé — en dessous
  du niveau char, `VB` ; au-dessus, `TL`/`TM`/`TH`/`MBT`. Ne jamais traiter `V` et `VB` comme
  un seul et même seuil : ce sont deux familles de châssis distinctes (2026-08-09).
- **`VBCI`** = **acronyme atomique** signifiant « véhicule de combat d'infanterie chenillé »
  (transport + appui rapproché sur chenilles). Ce n'est **pas** une composée de `VCI` ni de
  `VB` + `CI` : le code est déclaré tel quel dans `terrestres.md` (2026-08-09). À distinguer
  du VBCI réel français, qui est à roues et se note ici `VCI` ou `V8CI` — ne pas confondre le
  nom du code avec le nom du véhicule réel homonyme.
- **`VBCI` (ou tout Type de combat) vs `VB` sur variantes de même châssis — rôle
  combattant vs soutien.** Établie sur la famille Chimera (Astra Militarum, ORBAT
  « 114th Cadian Regiment »). Quand un châssis donne naissance à plusieurs variantes,
  **seule celle qui combat réellement aux côtés d'une escouade** (transport de troupes
  avec tourelle d'appui, engage l'ennemi en ligne) garde le Type de combat complet
  (`VBCI`, `VBTT`, etc.). Les variantes qui **ne combattent pas au contact** — sanitaire
  (`MED`), dépannage/récupération (`MAIN`), génie/logistique (`GEN`/`LOG`), artillerie
  automotrice (`ART`/`SPART`), mortier automoteur (`MOR`), AA automoteur (`AACA`) —
  **dégradent le Type vers `VB`** (véhicule blindé chenillé générique, non-combattant),
  même si le châssis physique est strictement identique au véhicule de combat.
  Raisonnement : le Type doit refléter la **doctrine d'emploi réelle**, pas seulement
  la plateforme — un véhicule sanitaire ou de dépannage n'est jamais engagé comme un
  véhicule de combat, quel que soit son blindage.
  - Exemple (famille Chimera) : `Chimera` (transport + tourelle, combat) → `VBCI` ·
    `Griffon` (mortier automoteur, même châssis) → `VB-MOR` · `Hydra` (AA automoteur) →
    `VB-AACA` · `Samaritan` (sanitaire) → `VB-MED` · `Atlas` (dépannage) → `VB-MAIN` ·
    `Trojan` (génie + ravitaillement) → `VB-GEN/LOG`.
  - ℹ️ **Pas de collision `V` / `VB`** (acté le 2026-08-09) : `V` = voiture blindée **à roues**,
    `VB` = véhicule blindé **chenillé**. Deux acronymes atomiques distincts, sans lien de
    dérivation — l'ancienne note de collision reposait sur une lecture erronée de la grammaire
    générative supprimée. Aucune mitigation particulière n'est nécessaire : les deux codes
    peuvent cohabiter dans un même ORBAT et dans le même lexique.
