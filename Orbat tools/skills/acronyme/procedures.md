# Procédures de validation

Ces procédures s'appliquent **au moment où Florian valide une décision de nomenclature** (ajout, modification, retrait d'un code). Elles sont la mise en œuvre concrète de « Autorité de validation — Florian seul » : Claude vérifie et propose, Florian tranche, puis ces étapes garantissent que la décision est répercutée sans introduire d'incohérence.

> À dérouler avant d'écrire quoi que ce soit dans une table de référence, un lexique, l'état `decisions.md` ou la `chronologie.md`. Toute décision actée s'écrit aux deux endroits : son effet dans `decisions.md` (état courant), son entrée datée dans `chronologie.md` (ancien → nouveau code, motif, fichiers touchés), puis `scripts/build_index.py` régénère l'INDEX.

---

## P1 — Vérifier la présence dans tous les fichiers, pas seulement les lexiques

**Outil obligatoire** : après toute modification du skill, régénérer l'index (`python scripts/build_index.py`) puis lancer `python scripts/check.py` — 0 erreur exigée ; examiner les avertissements nouveaux.

Après toute modification, contrôler la cohérence dans **l'ensemble** des fichiers, pas juste les deux lexiques : `identification/lexique.json`, `identification/lexique-40k.json`, `identification/chassis-types.md`, `identification/personnel.md`, les tables `references/` (et `grammaire.md`), `decisions.md`, et le corps du `SKILL.md`. La `chronologie.md` est historique : on y ajoute une entrée, on ne réécrit pas les anciennes.

*Pourquoi* : le cas `I`/`INF` a divergé précisément parce que le lexique avait été mis à jour mais pas les autres fichiers — vérifier un seul emplacement laisse les autres mentir.

## P2 — Vérifier conflits et surutilisation AVANT de modifier (contrôle asymétrique)

**Outil obligatoire** : avant de proposer ou d'officialiser un code `X`, lancer `python scripts/check.py --code X` — il liste tous les sens de `X` (officiel/alternatif, bassin, fichier:ligne), ses collisions, son statut d'exception et les lexiques qui l'emploient. Un code absent partout est libre.

**Collisions connues** : `check.py` ne tolère une collision entre officiels d'un même bassin que pour les couples (code, sens) enregistrés dans `scripts/collisions_connues.json` (exception de la règle 2, cas confirmé § 2, ou point ouvert § 5 — ce dernier reste un avertissement). Tout sens nouveau sur un code déjà en collision, même un code de la liste d'exceptions, est une ERREUR. Ce fichier ne se régénère (`python scripts/check.py --accepter-collisions`) qu'**après arbitrage de Florian** consigné dans `decisions.md` (§ 2, § 5 ou liste d'exceptions) — jamais pour faire taire une erreur.

Avant d'officialiser un code, vérifier qu'il n'entre pas en collision dans son bassin. Le contrôle est **asymétrique** (règle cardinale 2) :
- un **officiel** doit être strictement unique dans son bassin (Types ou Rôles/Armements) ;
- une **alternative** a le droit de collisionner, gérée par le contexte.

Ne signaler donc que les collisions entre deux **officiels**, hors liste fermée des exceptions de la règle 2 (`SKILL.md`, commentaire `exceptions-regle-2`). Lister chaque collision d'alternatives comme un problème produit des faux positifs en masse (`C` Camp/Croiseur, `V` Ville/Véhicule, `F` Forteresse/Frégate/Fusilier…) et noie les vrais.

## P3 — Détecter les revirements

Avant d'acter une décision sur un code, chercher dans `decisions.md` (état) **et** dans `chronologie.md` (par recherche texte sur le code), ainsi que dans les fichiers concernés, toute décision antérieure datée le concernant. Si la nouvelle **inverse** une ancienne, l'écrire explicitement comme un revirement (« remplace la décision du JJ/MM »), et propager l'inversion partout — pas seulement à l'endroit où on la formule.

*Pourquoi* : la décision `INF` du 2026-08-04 inversait une décision de juillet restée écrite ailleurs, sans que le revirement soit signalé ni propagé.

## P4 — Enregistrer tout point ouvert dans le registre central

Toute mention « à confirmer / provisoire / à clarifier » écrite dans un fichier de référence est, **dans le même geste**, ajoutée au § 5 « Codes encore non résolus » de `decisions.md`.

*Pourquoi* : le registre ne sert de rien s'il annonce un seul point ouvert alors que quatre autres traînent, dispersés dans les tables.

## P5 — Faire le bilan libération / occupation d'un code

- Un code **libéré** (ex. `P`, `I`, `A`, `COM` lors de décisions récentes) : vérifier que rien ne le réclame déjà silencieusement ailleurs avant de le considérer disponible.
- Un code **occupé** par un nouveau sens : lister ce qu'il déloge et indiquer où ce sens migre.

*Pourquoi* : les décisions arrivent souvent en cascade ; c'est là que se créent les orphelins (un sens qui perd son code sans remplaçant — cf. Détention/`DET` le 2026-08-05).

## P6 — Contrôler les sens survivants lors d'un retrait

Quand un code est retiré ou renommé dans un fichier, vérifier ses **autres sens** dans les autres fichiers et statuer sur chacun (conservé ? renommé ? confirmé sans conflit ?).

*Pourquoi* : `ESC` a été retiré comme Escouade (→ `SQ`) mais restait vivant comme Escadron et Escadrille sans que ce soit documenté — trou comblé seulement à l'audit.

## P7 — Contrôler la forme

Deux règles de forme déjà actées, à vérifier systématiquement à l'écriture plutôt qu'a posteriori :
- **Casse** : tous les codes en majuscules (des rattrapages ont été nécessaires sur `-Mi`, `Mo`, `Ma`, `Gén`).
- **Format des tables (2026-10-10)** : `| Officiel | Alternatifs | Signification | … |` — une ligne = un code officiel et ses alias de lecture (séparés par `, `), jamais deux codes distincts (variantes de gabarit comprises). Chaque table porte au-dessus sa balise `<!-- bassin: types -->` / `roles` / `precisions` / `aucun`. L'ancienne notation `X / Y` en 1re colonne n'est plus écrite.

## P8 — Signaler l'impact hors skill

Toute modification d'un code **officiel** signale si les skills consommateurs sont concernés : `/orbat-acronymize`, `/orbat-json`, `/nomenclature-planets`. La divergence, sinon, se découvre à l'usage sur un fichier réel.
