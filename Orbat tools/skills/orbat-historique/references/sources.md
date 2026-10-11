# Pistes de recherche et types de sources

Ce skill s'appuie principalement sur la **recherche web** (`web_search` /
`web_fetch`, ou leurs équivalents selon l'environnement) plutôt que sur des
données mémorisées en dur. Quelques pistes
pour des recherches efficaces.

## Formuler la recherche

Inclure systématiquement, quand c'est connu : **nation + année (ou
fourchette) + échelon + arme**. Exemples de requêtes efficaces :

- "division d'infanterie française 1914 composition organisation"
- "Wehrmacht panzer division 1943 order of battle"
- "ordre de bataille corps d'armée russe Borodino 1812"
- "British infantry division organisation 1944 establishment"
- "division motorisée soviétique 1985 organisation OTAN"

En anglais, le terme consacré est **"order of battle"** ou **"table of
organization and equipment" (TO&E / TOE)** — souvent plus productif que la
traduction littérale française pour des recherches précises, surtout pour
les nations non francophones.

## Types de sources généralement fiables

Marqueurs de consultation (octobre 2026) :
**✅ lue** = fetchée et exploitée dans les fichiers de ce skill ·
**🌐 répond** = page d'accueil vérifiée accessible, contenu non exploité ·
**⛔** = refusée à l'outil de lecture automatique (robots.txt / autorisation) mais
existence confirmée par une source tierce — à ouvrir manuellement ·
(sans marqueur) = non revérifiée.

- **Wikipedia** (et ses équivalents en langue d'origine — souvent plus
  détaillés que la version française pour un sujet national donné, ex.
  Wikipedia allemand pour la Wehrmacht, Wikipedia russe pour l'Armée
  rouge). Bon point de départ, à recouper si possible.
- **Sites spécialisés en ordres de bataille** (TO&E, OOB) :
  - ⛔ **Niehorster** — *World War II Armed Forces: Orders of Battle and
    Organizations* (L. Niehorster ; TO&E et OOB de toutes les nations
    belligérantes, séries organisationnelles allemandes en PDF) :
    https://www.niehorster.org/ (existence et contenu confirmés par
    https://generalstab.org/news/world-war-ii-armed-forces-niehorster-org/)
  - 🌐 **Lexikon der Wehrmacht** (unités, structures et notices de la
    Wehrmacht, en allemand) : https://www.lexikon-der-wehrmacht.de/
  - 🌐 **Bayonet Strength** (G. Kennedy ; évolution du bataillon d'infanterie
    britannique, allemand, soviétique et américain 1939-45, avec PDF tirés de
    documents d'époque) : https://www.bayonetstrength.uk/
  - Pour d'autres conflits, rechercher "[nation] [conflit] order of battle"
    pour trouver les références reconnues par les passionnés/historiens
    amateurs sérieux du domaine.
- **Services historiques officiels / archives nationales** :
  - 🌐 **US Army Center of Military History (CMH)** — lignées et honneurs,
    histoire de la structure des forces, collection *Army Lineage Series* :
    https://history.army.mil/
  - 🌐 **Service historique de la Défense (SHD)** — inventaires en ligne,
    archives numérisées (site parfois en maintenance) :
    https://www.servicehistorique.sga.defense.gouv.fr/
  - **Mémoire des hommes** (ministère des Armées ; journaux des marches et
    opérations des unités 1914-18, registres) :
    https://www.memoiredeshommes.sga.defense.gouv.fr/
  - **Bundesarchiv** (archives fédérales allemandes) :
    https://www.bundesarchiv.de/
  Plus rigoureux mais parfois moins faciles d'accès en ligne.
- **Études institutionnelles accessibles en ligne** :
  - ✅ McGrath, J. J., *The Brigade: A History, Its Organization and
    Employment in the US Army*, Combat Studies Institute Press, 2004, ch. 6
    (brigade et réforme ROAD) :
    https://www.vietnam.ttu.edu/exhibits/helicopter/other/Brigade-AHistory_clip.pdf
  - ✅ Modern War Institute (West Point), « The Right Division for the
    Fight: Force Design and Force Structure Lessons from the Cold War » :
    https://mwi.westpoint.edu/the-right-division-for-the-fight-force-design-and-force-structure-lessons-from-the-cold-war/
  - ✅ Ministère des Armées, *Chemins de mémoire* — A. Crépin, « Vers une
    nouvelle triade République-Nation-Armée » (lois de 1872, 1873, 1875) :
    https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/ressources-historiques/1870-1871-guerre-franco-prussienne/nouvelle-triade
  - ✅ Wikipedia — *Pentomic* (contexte de l'abandon de la brigade puis de
    ROAD) : https://en.wikipedia.org/wiki/Pentomic
- **Ouvrages de référence type "Osprey Publishing"** (collections Men-at-Arms,
  Battle Orders, Elite) : souvent cités/résumés en ligne, bonne base
  vulgarisée mais sourcée.
- **Forums spécialisés d'histoire militaire** (type forums de
  wargamers/reenactors sérieux) : à utiliser avec prudence, mais souvent
  de bonnes synthèses avec sources citées — vérifier la qualité des
  échanges et préférer les messages qui citent leurs sources.
- **Vocabulaire des échelons** (noms dans chaque langue, variantes par arme) :
  ne pas chercher ici — la table de référence et ses sources sont dans
  `orbat-tools:orbat-nommage` (`references/nations.md` §1 et
  `references/sources.md`).

## Prudence

- Les chiffres d'effectifs et de matériel circulant en ligne varient
  beaucoup d'une source à l'autre (méthodologies différentes : effectifs
  théoriques vs réels, date précise différente, inclusion ou non des
  services/soutien). **Toujours indiquer que c'est un ordre de grandeur**
  sauf si la source est clairement primaire/officielle et univoque.
- Se méfier des organigrammes "génériques" trouvés en image sans date
  précise — vérifier la date associée avant de la présenter comme valable
  pour l'année demandée par Florian.
- Pour les nations/conflits moins documentés en ligne (théâtres
  secondaires, petites nations, conflits coloniaux...), le dire
  explicitement si la recherche ne donne rien de solide plutôt que de
  combler par extrapolation non signalée.
