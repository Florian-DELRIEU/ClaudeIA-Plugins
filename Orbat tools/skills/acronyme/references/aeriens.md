# Véhicules Aériens

Format : `{Gabarit}-({Propulsion-Vitesse}) {Rôle1}-{Rôle2}`

---

## Types / Catégories aériennes

<!-- bassin: types -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| A | | Airframe | Avion |
| AH | | Hydravion | |
| AE | | Carrier Airframe | Équipé porte-avions |
| AV | | Avion VTOL | Décollage vertical |
| AS | | Drop ship | VTOL avec capacité transport troupes/matériel, atterrissage tous terrains |
| BL | | Ballon | Aérostat générique, plus léger que l'air, sans propulsion propre. Décliné en `BLC`/`BLB`/`BLM`. `MGF` (Montgolfière) conservé en lecture, pointe vers `BLM` |
| BLC | | Ballon captif | Amarré au sol par un câble/treuil — observation, ancien usage d'artillerie |
| BLB | | Ballon de barrage | Fixe, déployé comme obstacle aérien passif |
| BLM | MGF | Ballon mobile | Vol libre, dérive au vent — ne présume pas du type d'enveloppe (air chaud, hélium…) |
| DR | ZEP | Dirigeable | Aérostat propulsé et dirigeable. Pas de sous-type structurel pour l'instant (rigide/souple/semi-rigide non codé — voir `decisions.md`). `ZEP` (Zeppelin) conservé en lecture, pointe vers `DR` |
| SR | | Fusée (Space Rocket) | Générique |
| SRS | | Fusée suborbital | |
| SRO | | Fusée orbite basse | |
| SRI | | Fusée orbite moyenne | |
| SRG | | Fusée haute / géostationnaire | |
| SRX | | Fusée extraplanétaire | |
| SA | | Space Plane / SSTO | Vol atmosphérique / spatial |
| SV | | Space Vessel | Vaisseau spatial durable, mission diverse, équipage qq années max |
| PSV | | Planetary Space Vessel | SV restant dans l'influence d'une même planète |
| SSV | | Stellar Space Vessel | SV pour missions au sein d'un système solaire (production requise, habitat long terme 1–10 ans) |
| ISV | SVI | Interstellar Space Vessel | SV destiné à sortir du système solaire (équipage permanent, gravité artificielle, cryo) |
| U | UAV | Drone | `U` officiel — `UAV` collisionne avec Technicien drone (`infanterie.md`) |
| UE | | Drone embarqué | |
| UH | | Drone hydravion | |
| UV | | Drone VTOL | |
| SAU | | SSTO drone | |
| SVU | | Space Vessel drone | |
| SRU | | Fusée drone | |
| VT | | VTOL | Avion capable de VTOL |
| SAT | | Satellites | |
| DP | | Drop Pods | |
| LAN | | Lander | |
| RV | | Rover | |
| SVT | | Étage de voyage | Charge utile + manœuvres orbitales |
| ORB | | Orbiteur | Manœuvres orbitales, grande autonomie, missions diverses |
| KSAT | | Kill satellites | Satellites de combat |
| CSAT | | Sat de communication | |
| GSAT | | Sat GPS | |
| SSAT | | Sat de scan | |
| DPTT | | Drop Pods TT | DP + TT |

---

## Propulsion (entre parenthèses)

<!-- bassin: precisions -->
| Officiel | Alternatifs | Signification |
|---|---|---|
| (J) | | Jet |
| (R/F) | | Moteur fusée |
| (H) | | Hélice |
| (N) | | Nucléaire |
| (S) | | Stato-réacteur |
| (CHM) | | Chimique |
| (ION) | | Ionique |
| (ELC) | | Électrique |
| (SLR) | | Solaire / Voile solaire |

---

## Vitesse (entre parenthèses, combinable avec propulsion)

<!-- bassin: precisions -->
| Officiel | Alternatifs | Signification | Détail |
|---|---|---|---|
| (SB) | | Subsonique | < Mach 0.8 |
| (TS) | | Transsonique | Mach 0.8–1.2 |
| (SS) | | Supersonique | > Mach 1.2 |
| (HS) | | Hypersonique | > Mach 3 |

---

## Rôles aériens

<!-- bassin: roles -->
| Officiel | Alternatifs | Signification | Description |
|---|---|---|---|
| CAS | | Close Air Support | Attaque cibles au sol, soutien troupes |
| ATT | | Avion d'attaque | Appui canon / roquette |
| DB | | Bombardier en piqué | Largage de bombes |
| G | CN | Canonière / Gunship | **`G` officiel** (2026-08-04). Canon latéraux/gros calibre (AC-130). `G` est commun à Gunship (aérien) et Canon/Obusier (terrestre) — pas un conflit, même concept décliné par le Type porteur (voir `decisions.md` § 2) |
| TB | | Bombardier tactique | Frappes ciblées |
| SB | | Bombardier stratégique | Longue distance |
| NB | | Bombardier naval | Cibles maritimes |
| SA | | Supériorité aérienne | Domination aérienne |
| FC | P, F | Chasseur | **Officiel** (2026-08-04), remplace `P` (libéré) — `F` collisionne avec Fusil/Fusilier (`infanterie.md`). `P`/`F` restent alternatifs en lecture. Rapide et maniable |
| FCH | FH, HF | Chasseur lourd | **Officiel** (2026-08-30), remplace `FH` (libéré au profit de `FH` = Fusil de calibre supérieur, `infanterie.md` — collision réelle dans le bassin Rôles/Armements). Fusion atomique déclarée, sans rapport avec le gabarit universel `.H` : un chasseur au gabarit lourd s'écrirait `FC.H`. Plus grand, meilleure autonomie. `FH` et `HF` conservés en lecture |
| FI | | Intercepteur | **Officiel** (2026-08-04), suit `FC`/`FCH`. Abattre bombardiers rapidement. `I` reste lu Infanterie par défaut (position Type) |
| MR | | Multirôle | Chasse + bombardement léger + etc. |
| REC | | Reconnaissance | Surveillance / collecte info |
| TR | | Transport | Matériel générique |
| TT | | Transport troupes | |
| NP | | Patrouille maritime | Reco maritime + ASW |
| GM | | Missile guidé | Frappes précises |
| KKZ | | Kamikaze Strike Craft | Mission suicide |
| AW | W | AWACS | Radar longue portée |
| EW | | Guerre électronique | |
| ASW | | Anti-sous-marins | |
| FUEL | | Ravitailleur / Citerne | |
| COM | | Communication | |
| SPY | | Espionnage | |
| N | | Nucléaire (propulsion) | |
| MNV | | Maneuvre | Spécialisé maniabilité, esquive, agilité — expert en dogfight |
| BZ | | Boom & Zoom | Maintient un maximum d'énergie, attaques rapides et brutales |

---

## Échelons aériens

<!-- bassin: types -->
| Officiel | Alternatifs | Signification |
|---|---|---|
| ESC.A | | Escadrille |
| SQ.A | | Squadron |
| GRP.A | | Groupe |

---

## Types de groupes aériens

<!-- bassin: types -->
| Officiel | Alternatifs | Signification |
|---|---|---|
| SA | | Supériorité aérienne |
| CAS | | Attaque au sol |
| FC | P, F | Chasseurs |
| RES | | Réserves |
| LOG | | Train aérien |
| W | | Reconnaissance / AWACS |
| TB | | Bombardement tactique |
| SB | | Bombardement stratégique |
| MR | | Multi-rôle |
| FI | | Interceptions |
| PAR | | Soutien parachutage |
| DC | MA | Surveillance des côtes — `MA` : casse normalisée le 2026-10-10 (était `Ma`, même correction que `maritimes.md` le 2026-08-03) |
| GAE | | Groupe embarqué |
| G | | Groupe de canoniers |
| ATT | | Groupe de raid |
