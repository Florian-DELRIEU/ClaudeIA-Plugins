# Infanterie & Personnages

Format : `{Grade}-{Type} {Arme}-{Munitions}` ou `{Grade}.{Type}-{Arme}.{Munitions}`

---

## Types de personnages / infanterie

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| PN | Personnage générique | **Officiel** (2026-08-03). `P` reste alternatif dans le bassin Type — bassin distinct de `P` = Chasseur (Rôle aérien), pas de conflit |
| PN+ / PN* | Personnage important / héroïque | Unique. `P+` / `P*` restent alternatifs, comme `P` |
| INF | Infanterie | Fantassins. **Officiel** (2026-08-04) — `I` collisionne avec Industriel, Incendiaire, Intercepteur. `I` reste alternatif en lecture (lu Infanterie par défaut en position Type) |
| SF | Forces spéciales | |
| OFF | Officier | |
| NCO | Sous-officier | |
| RNG | Rangers | |
| GRD | Gardes | |
| VOL | Voltigeurs | |
| PAR | Parachutiste | |
| POL | Politicien militaire | Commissaires |
| KN | Knights / Chevaliers | |
| ASN | Assassins | |
| AGT | Agent | |
| IM | Infanterie monstrueuse | |
| CRM | Créature monstrueuse | |
| DRG | Dragon | |
| IV | Infanterie volante | |
| IS | Infanterie de saut | |
| CRMV | Créature monstrueuse volante | |
| BT | Bêtes | |
| BTV | Bêtes volantes | |
| CR | Créature | |
| CRV | Créature de vol | |
| CRS | Créature de saut | |
| EX | Exo-armure | |
| Z | Zombie | ⚠️ **Alternatif informel** (2026-08-03) : l'officiel du code `Z` est **Zone générique** (`structures.md`). Lisible en lecture, ne plus produire en écriture |

### Cas documenté — `I-CAV` = Cavalier (personnage individuel monté)

Il n'existe **pas** de code de Type dédié au cavalier : c'est une **composition explicite**
`Infanterie + Cavalerie`, écrite `I-CAV` (Type `I` + Rôle `CAV`). L'ancien Type `C` = Cavalier
est retiré — `C` reste Croiseur (Type naval) et Canonnier (Rôle naval), et la monture
individuelle est portée par `CAV` en position Type (voir SKILL.md § Décisions établies).

- `I-CAV` — cavalier générique (fantassin monté)
- Cavalier à lance / archer à cheval → composition standard `CAV.LC` / `CAV.BW` (sur un Type, ex. `I-CAV.LC`). Les anciennes fusions atomiques `CLC` / `CBW` sont **supprimées** (2026-08-04)

---

## Fusions avec U (gabarit Drone/Unnamed)

| Acronyme | Décomposition | Description |
|----------|--------------|-------------|
| PU / PNU | `PN.U` | Personnage drone / robot. Décomposition alignée sur `PN` (2026-08-03) ; `PU` reste la forme courte usuelle |
| IU | I.U | Infanterie drone |
| BTU | BT.U | Bête robotique |

---

## Grades

| Grade | Acronyme | Commandement |
|-------|---------|-------------|
| Enrôlé | ENL | |
| Soldat 1e classe | 1eENL | |
| Caporal | CPL | Équipe |
| Caporal-chef | CPLc | |
| Sergent | SGT | Escouade / Mentor |
| Sergent-chef | SGTc | |
| Adjudant | ADJ | |
| Adjudant-chef | ADJc | |
| Major | MAJ | |
| Sous-lieutenant | sLT | |
| Lieutenant | LT | Section / Assistant |
| Capitaine | CPT | Compagnie |
| Commandant | CDT | Bataillon / officier exécutif |
| Lieutenant-colonel | LTCOL | |
| Colonel | COL | Régiment |
| Général | GEN# | # = nombre d'étoiles |
| Amiral | AML | |
| Maître (de chapitre) | MTR | |

---

## Rôles d'infanterie

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| F / FUS | Fusilier | Arme de base |
| FM | Fusilier mitrailleur | |
| TPF | TP Fusilier | Arme F + lunette adaptée |
| TP | Tireur précision | Arme plus adaptée (longue etc.) |
| TE | Tireur élite | Fusil de précision |
| TEH | Tireur élite gros calibre | TE avec fusil gros calibre |
| TEL | Tireur élite calibre léger | TE avec fusil calibre léger |
| TEA | Assistant TE | Spotteur |
| TES | TE + STH | Sniper camouflage avancé (fusion atomique) |
| TEAT | TE + AT | TE avec fusil antichar (fusion atomique) |
| MED | Médecin | |
| GEN | Génie | |
| VOL | Voltigeur | Infanterie légère (souvent 1800s) |
| MS | Démineur | |
| NV | Nocturne | Vision nocturne (rôle/capacité) |
| NVG | Vision nocturne (équipement) | Jumelles / lunettes spécifiques ⚠️ Distinct de NV (rôle) |
| UAV | Technicien drone | |
| BRH | Breacher | Ouvreur de portes/obstacles (générique) |
| BRHE | Breacher explosif | BRH + E (charges explosives) |
| BRHP | Breacher porte | BRH + P (destruction de porte) |
| BRHG | Breacher grillage | BRH + G (ouverture grillage) |
| BRHT | Breacher tôle | BRH + T (ouverture tôle) |
| BLR | Breacher bélier | L'outil implique le rôle — pas besoin de BRH |
| CSL | Breacher cisailles | L'outil implique le rôle — pas besoin de BRH |
| SD | Furtif | Équipement silencieux ⚠️ Distinct de STH |
| STH | Stealth | Camouflage avancé / invisibilité ⚠️ Distinct de SD |
| DEM | Démolition | |
| GL | Grenadier | |
| HW | Armes lourdes | Escouade soutien feu. Décrit l'**unité**, pas le servant : tout l'effectif ne porte pas d'arme lourde, l'organisation s'articule autour de leur emploi. ⚠️ Un servant de mortier ou de MG est `GUN` (2026-08-10) |
| MG | Mitrailleurs | Spécialiste mitrailleuse |
| AA | Spécialiste AA | |
| AT | Spécialiste antichar | Unité d'infanterie spécialisée antichar, armes **portables** (bazooka, PIAT, fusil AT) ; l'arme est embarquée dans l'élément. ⚠️ N'est **pas** un servant de canon antichar → `GUN` (2026-08-10) |
| REC | Reconnaissance | |
| SL / TL | Chef d'équipe/escouade | |
| GUN | Artilleurs (au sens large) | Quiconque **met en œuvre un système d'armes** — un tireur de MG est un « artilleur MG ». Reclarifié le 2026-08-03 en reprise d'une partie des usages de l'ancien `SPT`. **Les servants seuls, sans leur pièce** — celle-ci vit sur la ligne `equipment` de l'unité. Forme à privilégier pour tout équipage de pièce. ⚠️ Distinct de `AT` (fantassins antichar) et de `HW` (unité articulée autour d'armes lourdes) (2026-08-10). ⚠️ Distinct de `ART` (Artillerie = capacité/rôle véhicule) |
| JTAC / CAS | Officier CAS/ART | Au sein d'une escouade. `JTAC` officiel (2026-08-04) — `CAS` collisionne avec Close Air Support (rôle aérien) |
| AM | Assistant munitions | **Officiel** (2026-08-03, confirmé le 2026-08-10). Rôle **individuel au sein d'un élément** : porte les munitions et accompagne le ou les servants. Ne produit jamais de code d'élément — se mentionne en `description`. ⚠️ **`MUN` n'en est pas un alternatif** (mention retirée le 2026-08-10) : `MUN` est le rôle dominant d'un élément entier chargé d'approvisionner en munitions, ex. `SQ-MUN`. ⚠️ Sans rapport non plus avec `MUN` = cargaison munitions (`terrestres.md`), troisième bassin. Résout le doublon avec l'ancienne entrée `MUN` de la table Types, supprimée |
| GN | Gendarmes | |
| CRW | Equipage véhicule | |
| EVA | Equipage EVA | Spécialisé sortie extra-véhiculaire |
| (UDC) | Sous couverture | |

---

## Armes personnelles

| Acronyme | Signification | ⚠️ Note |
|---|---|---|
| W | Armes personnelles | |
| WSD | Armes silencieuses | |
| F / FUS | Fusil | FV = verrou, FA = auto, FS = semi-auto |
| FM / FMA / FAM / FMG | Fusil mitrailleur (variantes) | |
| FTE | Fusil de sniper | |
| FTP | Fusil à lunette | |
| FG | Fusil avec lance-grenade | |
| FAT | Fusil antichar | |
| SMG | Pistolet-mitrailleur favorisant cadence | |
| MG / LMG / MMG / HMG | Mitrailleuse L/M/H | |
| GMG | Lance-grenade automatique | |
| GL | Lance-grenade unique | |
| GF | Grenade à fusil | |
| GH | Grenade à main (Grenade Hand) | Officiel (2026-08-03), remplace `G` — reste commun à Gunship (aérien) et Canon/Obusier (terrestre) sans conflit |
| GE / GF | Grenade explosive / frag | |
| GFU / GFB | Grenade fumigène / flash | |
| GGZ / GGS | Grenade gaz léthal / non-léthal | |
| SG / SGA | Shotgun / automatique | |
| P / PS / PA | Pistolet / semi-auto / auto | |
| PM | Pistolet-mitrailleur | |
| PR | Revolver | |
| RK / R / RKT | Roquette / Lance-roquette | |
| MOR | Mortier | |
| LF | Lance-flamme | |
| SD | Silencieux | |
| GM | Missile guidé (tout guidage continu) | |
| FFM | Missile fire-and-forget | |
| BLR | Bélier (pour porte) | |
| CSL | Cisailles | |
| OPT | Optiques | |
| FLR | Contre-mesure (flare) | |
| NLT | Non létal | |
| BMB | Bombe (normale/non guidée) | |
| BMBG | Bombe guidée | `BMB` + variante `G` |
| BMBP | Bombe planante | `BMB` + variante `P` |
| RTG / RTM | Canon rotatif / Minigun | |
| RLG | Recoiless Gun | |
| RNG | Combats à distance divers | |

---

## Armes de corps-à-corps et de tir non guidées

> Regroupement thématique, sans restriction d'usage (SKILL.md § Règles cardinales n°4).

| Acronyme | Arme |
|----------|------|
| CAC | Corps à corps divers |
| SW | Épée |
| HC | Hache |
| MSS | Masse / contondant |
| (MRT) | Marteau |
| LCN | Lance / vouge |
| JT | Pilum / arme de jet |
| DG | Dague |
| BW | Arc |
| MSK | Mousquet |
| XBW | Arbalète |
| FL | Fléau |
| HLB | Hallebarde |
| RP | Rapière |
| SLG | Fronde |
| PK | Pique |
| SHD | Bouclier |
| LC | Lance |

---

## Armes à énergie et exotiques

> Regroupement thématique, sans restriction d'usage (SKILL.md § Règles cardinales n°4).

| Acronyme | Signification |
|----------|--------------|
| LZ | Laser continu |
| LZA | Laser automatique (rafale) |
| PL | Plasma |
| NTR | Neutron |
| MLT | Fuseur / Fusion |
| CG | Coilgun |
| RG | Railgun |
| PW | Energétique |

---

## Munitions et effets

| Acronyme | Signification |
|----------|--------------|
| FMJ | Balle classique |
| T | Traçante — **uniquement en suffixe fusionné** `.T` (`AP.T`, `HE.T`, `FMJ.T`). `T` isolé en position Rôle = Torpilleur, voir SKILL.md § Désambiguïsation positionnelle |
| HP | Pointe creuse |
| SUB | Subsonique |
| HE | Explosif |
| HEAT | Charge creuse |
| HESH | HE Squash Head |
| AP | Perforant |
| APC | AP Capped |
| APCBC | AP Capped Ballistic Capped |
| APCR | AP Composite Rigid |
| APCNR | AP Composite non Rigid |
| APDS | AP Discarding Sabot |
| APFSDS | Obus flèche |
| I | Incendiaire (libéré par `IND` = Industriel ; distinct de `I` = Infanterie, position Type) |
| NK | Nucléaire |
| FZD | Fuze Delay (munition à retard) — **officiel** (2026-08-03), remplace `FUS` qui reste l'alternatif de `F` = Fusil / Fusilier |
| PRX | Proximity |
| CHEM | Chimique |
| CLUS | Cluster / sous-munitions (`(SMN)` retiré 2026-08-04) |
| FRG / FRAG | Fragmentation (`FRG` officiel, plus compact) |
| NPLM | Napalm |
| THBR | Thermobarique |
| FU | Fumigène |
| FUC | Fumigène à couleur |
| WP | White Phosphore |
| FB | Flashbang |
| LUX | Éclairante |
| LUXIR | Éclairante IR — remplace `LUX-IR` (2026-08-04). Forme courte munition `IR` retirée ; `(IR)` guidage missile non affecté |
| GZ / GS | Gaz léthal / non-léthal |

### Effets génériques

| Acronyme | Signification |
|----------|--------------|
| THR | Thermique (dégâts contre boucliers) |
| KTQ | Cinétique (contre coques) |
| INC | Incapacitante |
| FLSH | Flash |
| EMP | Électro-magnétique |
| PWD | Energétique |

---

## Missiles

*Section retravaillée le 2026-07-30 (refonte de fond, cf. TODO dédié). Les deux
registres qui coexistaient sans hiérarchie sont désormais articulés explicitement,
tous les exemples fusionnés sont décomposés, et les collisions de lettres sont
traitées.*

### Deux registres, désambiguïsés par la POSITION

Le système missile a deux niveaux de précision. Ils ne s'opposent pas : **le registre
court est le registre long réduit à son seul Domaine.** Comme partout ailleurs dans le
système, c'est la **position** dans l'acronyme qui dit lequel on lit.

| Registre | Position | Ce qu'il décrit | Forme | Exemple |
|---|---|---|---|---|
| **Court** (fusion établie) | Armement/Rôle, **sur un porteur** (véhicule, unité, structure) | *Ce que le porteur emporte*, à gros grain | un seul code atomique | `V-ATGM` · `VBCI-CA30/ATGM` · `V-AAGM` |
| **Long** (spécification) | **Sur la munition elle-même** (catalogue de munitions, fiche d'armement) | *Le missile en tant qu'objet*, précisément | `(Portée).Domaine.(Guidage)[.Type]` | `MRG.ATGM.(L)` · `LRG.SSM.(GPS).CM` |

**Règle de choix — la question à se poser :**

```
"Je code un PORTEUR ou la MUNITION ?"
├─ Un porteur (véhicule/unité qui emporte le missile) → registre COURT
│    → `ATGM`, `AAGM`, `SAM`… en position Armement
└─ La munition elle-même (que je veux spécifier)      → registre LONG
     → `(Portée).Domaine.(Guidage)[.Type]`
```

Corollaire : **ne jamais mettre une portée ni un guidage sur un porteur.** Un char
n'est pas « à guidage laser » — c'est son missile qui l'est. Si le guidage doit
apparaître sur la fiche du véhicule, il va dans la description, pas dans l'acronyme du
véhicule.

**Lien formel entre les deux :** `ATGM` (court) ≡ `ATGM` en Domaine avec portée et
guidage **non spécifiés**. Dès qu'on veut préciser l'un des deux, on bascule sur la
forme longue — on ne bricole pas la forme courte.

### Portée

`SRG` Court · `MRG` Moyen · `LRG` Long · `SLRG` Super-long · `XRG` Extrême

> ⚠️ **Changement acté le 2026-07-30.** L'ancienne notation à lettre unique
> (`S` / `M` / `L` / `X`) est **abandonnée** : elle collisionnait frontalement avec
> le reste du système — `L` = Léger et `M` = Moyen (gabarits, omniprésents), `M` =
> Missile standard **dans cette section même** (table Type ci-dessous), `L` = Leader
> (maritimes), `S` = Sous-marin (maritimes), `X` = Spécial (structures). La portée
> utilise donc l'échelle canonique déjà définie dans `SKILL.md` (§ Portée), commune à
> tout le système. Conséquence sur les exemples existants : `S.ANRM` → `SRG.ANRM`.

### Domaine (codes atomiques pré-établis)

`AAM` Air-to-Air · `SAM` Surface-to-Air · `UAM` Underwater-to-Air · `ASM` Air-to-Surface ·
`SSM` Surface-to-Surface · `USM` Underwater-to-Surface · `AUM` Air-to-Underwater ·
`SUM` Surface-to-Underwater · `ATGM` Anti-tank · `ICBM` Intercontinental ·
`IRBM` Intermédiaire · `GLCM` Cruise sol-lancé

Ces codes sont **atomiques** : on les emploie tels quels, sans les redécomposer (règle
générale des fusions, `SKILL.md` § Règles de composition des fusions).

### Cibles (briques de composition)

`AN` Anti-navire · `AA` Anti-aérien · `AT` Antichar · `G` Ground (coordonnées)

> ⚠️ **`ATGM` (Domaine) vs `AT` (Cibles) — ce ne sont pas des doublons**, malgré
> l'apparence (incohérence signalée par Florian, tranchée ici) :
> - `ATGM` est un **code Domaine atomique** : la forme canonique d'un missile
>   antichar. C'est lui qu'on écrit, en court comme en long.
> - `AT` est une **brique de composition** (table Cibles) : elle ne sert qu'à
>   *expliquer l'étymologie* d'une fusion (`ATGM` = `AT` + `GM`) ou à composer une
>   fusion historique de la liste fermée ci-dessous. En position Armement sur un
>   porteur, `AT` seul garde son sens de `references/terrestres.md` : **capacité
>   antichar, vecteur non précisé** (canon ou missile) — c'est donc plus large que
>   `ATGM`, pas un synonyme.
>
> En pratique : missile antichar → `ATGM`. Capacité antichar sans préciser si c'est un
> canon ou un missile → `AT`. Ne jamais écrire `AT-ATGM` (redondance).

### Guidage — parenthèses OBLIGATOIRES

`(FF)`/`(F)` Fire-and-forget · `(G)` Guidé continu · `(IR)` Infrarouge · `(R)`/`(RAD)` Radar ·
`(RA)` Radar actif · `(RSA)` Radar semi-actif · `(SEAD)` Anti-radar · `(D)` Télécommandé ·
`(L)` Laser · `(EO)` Électro-optique · `(GPS)` GPS

> ⚠️ **Les parenthèses ne sont pas décoratives : elles SONT le désambiguïsateur.**
> Sans elles, chaque code de guidage collisionne avec un code existant ailleurs :
> `(R)` radar vs `R` roquette non guidée · `(G)` guidé vs `G` obusier/gunship/grenade ·
> `(F)` fire-and-forget vs `F` fusilier/chasseur/carburant · `(L)` laser vs `L` léger ·
> `(D)` télécommandé vs `D` division. Un guidage s'écrit **toujours** entre
> parenthèses dans la forme longue. C'est aussi la raison de la liste fermée
> ci-dessous : les fusions historiques qui omettent les parenthèses sont ambiguës par
> construction.

### Type

`M` Missile standard · `BM` Ballistic missile · `CM` Cruise missile

Optionnel : ne l'écrire que s'il apporte une information (`.CM` sur un missile de
croisière, `.BM` sur un balistique). `.M` est implicite et généralement omis — le
Domaine dit déjà qu'on parle d'un missile.

### Fusions historiques — liste FERMÉE, décomposées

Ces formes viennent de l'usage antérieur de Florian et sont conservées telles quelles
pour ne pas casser les fichiers existants. **Elles omettent les parenthèses de guidage
et sont donc ambiguës par construction : aucune nouvelle fusion de ce type ne doit être
créée.** Pour tout cas nouveau → forme longue.

| Fusion | Décomposition lettre par lettre | Sens | Forme longue équivalente |
|---|---|---|---|
| `ATGM` | `AT` (antichar) + `GM` (missile guidé) | Missile guidé antichar, guidage non précisé | `ATGM` — *déjà un code Domaine, pas une fusion ad hoc : le seul de cette liste à rester pleinement recommandé* |
| `AAGM` | `AA` (anti-aérien) + `GM` (missile guidé) | Missile guidé anti-aérien, guidage non précisé | `SAM` si tiré du sol (miroir exact de `ATGM`, cf. `references/terrestres.md` § Rôles terrestres) |
| `ANRM` | `AN` (anti-navire) + `R` (radar) + `M` (missile) | Missile anti-navire à guidage radar | `ASM.(R)` ou `SSM.(R)` selon la plateforme de tir |
| `AAIRM` | `AA` (anti-aérien) + `IR` (infrarouge) + `M` (missile) | Missile anti-aérien à guidage infrarouge | `AAM.(IR)` (air-air) ou `SAM.(IR)` (sol-air) |
| `SRG.ANRM` | `SRG` (courte portée) + `ANRM` | Missile anti-navire radar de courte portée | `SRG.ASM.(R)` — *ancienne écriture `S.ANRM`, cf. changement de portée ci-dessus* |
| `GGCM` | `G` (Ground, cibles sur coordonnées) + `G` (guidé continu) + `CM` (cruise missile) | Missile de croisière guidé, tir sur coordonnées sol | `GLCM.(G)` si lancé du sol, sinon `SSM.(G).CM` |

> 🔴 **`GGCM` est le cas le plus problématique de la liste** : deux `G` adjacents
> portant deux sens différents (Cibles « Ground » puis Guidage « Guidé continu »),
> illisibles sans la glose. **Écriture déconseillée** — préférer `GLCM.(G)` (ou
> `SSM.(G).CM`). `GGCM` n'est conservé ici que pour pouvoir relire les fichiers
> antérieurs.

### Exemples complets (forme longue recommandée)

| Code | Lecture |
|---|---|
| `MRG.ATGM.(L)` | Missile antichar de portée moyenne, guidage laser |
| `SRG.SAM.(IR)` | Missile sol-air de courte portée, guidage infrarouge |
| `LRG.SSM.(GPS).CM` | Missile de croisière sol-sol de longue portée, guidage GPS |
| `XRG.ICBM.(GPS).BM` | Missile balistique intercontinental, guidage GPS |
| `MRG.ASM.(RSA)` | Missile air-sol de portée moyenne, radar semi-actif |
| `V-ATGM` | *Porteur* : véhicule blindé léger emportant un missile antichar (registre court — pas de portée ni de guidage sur un porteur) |
