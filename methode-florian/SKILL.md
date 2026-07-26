---
name: methode-florian
description: Catalogue la méthode de travail et les préférences de collaboration de Florian avec Claude Code, synthétisée à partir de sessions réelles (notamment le mod HOI4 ImprovedDesigner). À consulter pour calibrer le style de collaboration — cadence, niveau de détail, quand proposer vs quand exécuter directement.
---

# Méthode de travail — Florian

Ce fichier catalogue des patterns de collaboration observés, pas des règles absolues à appliquer aveuglément. Il évoluera au fil des sessions — Florian peut dicter des ajouts directement.

## 1. Proposer avant d'implémenter, sur les décisions à fort impact

Sur tout changement qui touche à de l'équilibrage/design (valeurs de jeu, architecture, choix structurants), Florian veut voir une **proposition concrète et chiffrée** avant que ça parte en édition — pas juste une direction qualitative. Il valide, ajuste parfois un détail ("plutôt +4 que +6"), puis dit explicitement d'appliquer.

**Ne pas faire :** enchaîner directement sur l'implémentation dès qu'une idée semble bonne, même si le raisonnement est solide.
**Faire :** présenter un tableau/calcul, poser une question ouverte du type "je valide ces valeurs ou tu veux ajuster ?", attendre le feu vert explicite avant d'éditer les fichiers.

Exception : les corrections mécaniques évidentes (fautes de frappe, renommage sans ambiguïté, bugs de syntaxe confirmés) peuvent être faites directement sans repasser par ce cycle — surtout si Florian a déjà dit "corrige ça" ou équivalent.

## 2. Calculs réels, pas d'approximations à la louche

Quand un chiffre a du sens, il veut le vrai calcul posé explicitement (formule → valeurs → résultat), pas un ordre de grandeur vague. Ça vaut pour l'équilibrage de jeu comme pour tout domaine technique/quantitatif. S'appuyer sur les skills spécialisés pertinents (ex: `/aero` pour la cohérence aéronautique) plutôt que de répondre de mémoire sur un sujet qui a un skill dédié.

## 3. Une chose à la fois, en profondeur

Florian recadre activement quand la conversation part dans plusieurs directions à la fois ("on va rester concentré sur X, pas nous éparpiller"). Préférer creuser un sujet jusqu'au bout (avec calculs, tableaux, vérifications) plutôt que de couvrir plusieurs sujets superficiellement. Il segmente lui-même son travail en étapes séquentielles explicites et attend qu'on finisse une étape avant de passer à la suivante.

## 4. Vérification systématique après édition

Après une série de modifications de code/contenu, il demande régulièrement une **repasse de vérification** explicite (syntaxe, cohérence avec le reste du système — technologies qui débloquent, images/assets référencés existent, pas de régression). Anticiper ce réflexe : after une série d'édits non-triviaux, proposer spontanément cette vérification plutôt que d'attendre qu'il la demande.

## 5. Hygiène git — diffs propres

Sensible à la propreté des diffs de commit. Un exemple concret rencontré : un `sed` via Git Bash a silencieusement converti les fins de ligne d'un fichier de CRLF vers LF, gonflant un diff de 4 lignes réelles à 10 678 lignes changées. Toujours vérifier qu'un diff ne contient que les changements de contenu réels avant de commit — `git diff --ignore-space-at-eol` est un bon test rapide de sanity check après des édits via des outils shell (sed/awk) plutôt que l'outil Edit natif.

Florian gère parfois lui-même le push/la PR (ne pas supposer qu'il faut systématiquement pousser après un commit — demander ou attendre l'instruction).

## 6. Contexte historique/physique pour la cohérence de design

Sur son mod HOI4, il veut que les valeurs de jeu (vitesse, agilité, stats moteur) restent **crédibles par rapport à la vraie physique/histoire**, tout en gardant un gameplay satisfaisant — pas du réalisme pur qui rendrait les choix ennuyeux, mais pas non plus des nombres arbitraires. Quand un choix de design a une justification historique/physique claire, la citer explicitement (ex: pourquoi un moteur radial protège mieux le pilote qu'un moteur en ligne).

## 7. Workflow assets visuels

Pattern observé : Florian génère des images lui-même via un outil externe (ChatGPT) à partir d'un prompt qu'on lui fournit, les colle dans la conversation, Claude les récupère depuis son dossier Downloads et les intègre au projet (renommage, placement, mise à jour des références). Ne pas essayer de générer les images soi-même — fournir un prompt calibré sur le style déjà établi dans le projet (analyser les assets existants avant de rédiger le prompt).

## 8. Mémoire et règles impératives

Pour les règles que Florian formule comme non-négociables ("impérativement", "toujours"), les enregistrer en mémoire immédiatement et vérifier leur application à chaque occasion pertinente — pas seulement au moment où elles sont formulées. Une règle en mémoire mais non appliquée en pratique est pire que pas de mémoire du tout.
