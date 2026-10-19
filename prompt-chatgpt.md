# PROMPT MAÎTRE : GÉNÉRATEUR COMPLET DE LIVRES AVEC OPENCODE

## 1. Rôle et mission

Tu es un ingénieur logiciel senior spécialisé dans OpenCode, les agents IA, l'automatisation documentaire, la génération de livres, les pipelines éditoriaux, la production PDF et EPUB, ainsi que la préparation de publications pour Amazon KDP et Etsy.

Ta mission est de créer ou de compléter un **générateur de projets de livres entièrement piloté par OpenCode**, configurable, modulaire, documenté, reprenable après interruption et utilisable sans dépendre d'un modèle IA payant.

Le système doit permettre de préparer, rédiger, vérifier, traduire, illustrer, assembler et exporter un livre complet à partir d'un questionnaire de configuration.

Il doit fonctionner sous Ubuntu/Linux, Windows et PowerShell, avec des scripts adaptés à chaque environnement.

Le projet ne doit pas être un simple squelette de fichiers Markdown. Il doit fournir un véritable workflow opérationnel, des commandes OpenCode fonctionnelles, des scripts de production, des validations, des modèles de documents et un processus d'assemblage final vérifiable.

## 2. Première règle : analyser l'existant

Avant toute modification :

1. Analyse l'intégralité du projet existant et de ses sous-dossiers.
2. Identifie les scripts, commandes OpenCode, agents, skills, fichiers de configuration, modèles, tests et documentations déjà présents.
3. Identifie les fonctionnalités opérationnelles, incomplètes, redondantes ou manquantes.
4. Vérifie la cohérence entre les commandes documentées et les fichiers réellement présents.
5. Préserve les fonctionnalités existantes qui sont correctes.
6. Corrige les incohérences et implémente les fonctionnalités manquantes.
7. N'écrase jamais silencieusement un fichier existant.
8. Avant toute opération destructive, demande confirmation, sauf si l'utilisateur a explicitement demandé cette opération.
9. Ne prétends jamais qu'une fonctionnalité fonctionne si elle n'a pas été vérifiée.

Ne crée pas une seconde architecture parallèle si une architecture exploitable existe déjà.

À la fin, fournis un bilan précis des modifications, des tests et des éventuelles limitations restantes.

## 3. Objectif général : un livre par exécution

Le générateur doit traiter **un seul livre par exécution du questionnaire de création**.

Le projet créé doit être autonome et contenir tous les éléments nécessaires à la production de ce livre.

Il doit permettre de reprendre le travail à tout moment sans perdre les décisions éditoriales, les validations, les contenus déjà produits ou l'état de fabrication.

Le système doit fonctionner de manière incrémentale : il ne doit pas régénérer inutilement les éléments déjà approuvés.

Il doit conserver un état explicite de chaque étape et de chaque élément du livre.

## 4. Questionnaire de configuration

Créer un questionnaire interactif au lancement du générateur.

Il doit recueillir les informations nécessaires à la création du livre, sans imposer de choix éditoriaux arbitraires.

Les réponses proposées peuvent contenir des exemples, mais toutes les valeurs importantes doivent être modifiables.

### 4.1 Informations générales

Recueillir :

- Titre du livre.
- Sous-titre éventuel.
- Nom d'auteur ou pseudonyme.
- Description du projet.
- Thématique principale.
- Sous-thématiques.
- Objectif du livre.
- Langue originale.
- Langues de publication supplémentaires.
- Public cible.
- Niveau de difficulté.
- Ton éditorial.
- Style rédactionnel.
- Longueur souhaitée.
- Nombre de chapitres souhaité.
- Présence ou non d'exercices, de corrigés, de quiz, d'études de cas, d'exemples, de tableaux et d'illustrations.

Permettre à l'utilisateur de définir une thématique, un public ou un type de livre personnalisé lorsqu'aucune proposition ne convient.

### 4.2 Types de livres et profils

Prévoir plusieurs profils éditoriaux combinables, sans limiter le système à une liste fermée.

Les profils peuvent notamment couvrir :

- Guide pratique.
- Livre pédagogique.
- Manuel technique.
- Livre de formation.
- Cahier d'exercices.
- Livre de développement personnel.
- Livre illustré.
- Livre de référence.
- Livre de coloriage.
- Livre spécialisé.
- Projet éditorial personnalisé.

Les profils doivent définir des paramètres et des recommandations de structure, et non imposer un contenu éditorial figé.

L'utilisateur doit pouvoir combiner plusieurs profils et en définir de nouveaux.

### 4.3 Formats de publication

Permettre de sélectionner plusieurs formats pour un même livre :

- PDF destiné à l'impression.
- PDF destiné à la lecture sur écran.
- Livre broché pour Amazon KDP.
- Livre numérique Kindle.
- EPUB.
- Documents numériques destinés à Etsy.
- Autres formats configurables si leur prise en charge est réellement implémentée.

Ne pas confondre un fichier EPUB avec un fichier Kindle prêt à publier : vérifier les exigences propres à chaque sortie.

### 4.4 Dimensions, marges et pagination

Pour les formats concernés, permettre :

- La sélection de dimensions prédéfinies.
- La saisie de dimensions personnalisées.
- Le choix des unités.
- La configuration des marges.
- La configuration des marges intérieures et extérieures.
- La prise en compte de la reliure et du fond perdu lorsqu'ils sont nécessaires.
- Le choix de l'orientation.
- Le format de pagination.
- La configuration des en-têtes et pieds de page.
- Le choix des polices et des tailles de caractères.
- La gestion des pages blanches, des pages liminaires et des pages de fin.

Les paramètres doivent être enregistrés dans la configuration du livre.

Ne jamais affirmer qu'un document est conforme à Amazon KDP ou à Etsy sans avoir effectué les contrôles correspondants. Les exigences doivent être vérifiées selon le format et le type de publication.

## 5. Architecture du projet généré

Créer une organisation cohérente, lisible et documentée.

Prévoir au minimum des espaces distincts pour :

- Configuration du livre.
- Documentation éditoriale.
- Plan général.
- Sommaire.
- Briefs détaillés des chapitres.
- Chapitres rédigés.
- Traductions.
- Catalogues d'illustrations.
- Prompts d'illustrations.
- Images sources.
- Images validées.
- Couvertures.
- Sources et références.
- Contrôles qualité.
- Fichiers temporaires.
- Journaux d'exécution.
- Livrables finaux.

Chaque langue doit disposer d'un espace propre pour ses textes et ses illustrations.

Les chemins doivent être déterministes, documentés et utilisés de manière cohérente par toutes les commandes.

Le système doit distinguer clairement les fichiers de travail des fichiers approuvés et des livrables finaux.

## 6. Mémoire et reprise des sessions

Le projet doit pouvoir être repris après une fermeture d'OpenCode, un arrêt de la machine ou une interruption de génération.

Créer et maintenir des fichiers de mémoire documentaire, par exemple :

- `CURRENT_STATE.md` : état actuel du projet.
- `NEXT_SESSION.md` : prochaines actions recommandées.
- `DECISIONS.md` : décisions prises et raisons.
- Un journal de production.
- Un état des validations.
- Un index des chapitres, briefs, traductions, illustrations et livrables.

À chaque étape importante, mettre à jour les informations pertinentes.

Au début d'une nouvelle session, l'agent doit lire les fichiers de reprise nécessaires, vérifier l'état réel des fichiers et reprendre le travail à partir de cet état.

Ne pas se fier uniquement à la mémoire conversationnelle.

Limiter les lectures inutiles et les répétitions de contexte afin de réduire la consommation de tokens, sans sacrifier la qualité ni la sécurité.

## 7. Workflow éditorial obligatoire

Le workflow doit séparer clairement la planification, la rédaction, la vérification et l'assemblage.

Ordre de référence :

1. Questionnaire de configuration.
2. Création de la structure du livre.
3. Analyse éditoriale et définition des objectifs.
4. Création du sommaire.
5. Création des briefs détaillés de chaque chapitre.
6. Révision et approbation des briefs.
7. Rédaction des chapitres.
8. Révision des chapitres par rapport aux briefs.
9. Corrections éditoriales.
10. Préparation des illustrations.
11. Traductions éventuelles.
12. Contrôle de cohérence générale.
13. Assemblage du livre.
14. Production des formats demandés.
15. Contrôles techniques des fichiers.
16. Génération du rapport de validation.
17. Présentation du livrable final et de ses emplacements.

Une étape non validée ne doit pas être considérée automatiquement comme terminée.

Le workflow doit permettre de travailler sur un seul chapitre, une plage de chapitres ou l'ensemble du livre.

## 8. Brief détaillé obligatoire avant la rédaction de chaque chapitre

**Aucun chapitre ne doit être rédigé définitivement avant la création et l'approbation de son brief détaillé.**

Le sommaire seul ne suffit pas.

Chaque chapitre doit posséder un fichier de planification détaillée, avec un identifiant stable, par exemple `CH001.md`.

Le brief doit expliquer précisément ce que le chapitre doit contenir, dans quel ordre et avec quel niveau de détail.

### 8.1 Contenu minimal du brief

Chaque brief doit comprendre :

- Identifiant et titre du chapitre.
- Place du chapitre dans le livre.
- Objectifs pédagogiques ou éditoriaux.
- Connaissances préalables nécessaires.
- Résultats attendus pour le lecteur.
- Concepts à expliquer.
- Définitions à fournir.
- Sections et sous-sections prévues.
- Contenu détaillé de chaque section.
- Explications à développer.
- Exemples à fournir.
- Études de cas ou démonstrations éventuelles.
- Erreurs fréquentes à expliquer.
- Points délicats nécessitant une attention particulière.
- Sources à consulter et informations à vérifier.
- Illustrations prévues et rôle de chacune.
- Vocabulaire à employer.
- Liens avec les autres chapitres.
- Transition vers le chapitre suivant.
- Conclusion attendue.

### 8.2 Exercices, activités et corrigés

Si le livre contient des exercices, le brief doit prévoir chacun d'eux individuellement.

Pour chaque exercice, préciser :

- Identifiant et objectif.
- Niveau de difficulté.
- Compétence visée.
- Énoncé complet attendu.
- Consignes exactes données au lecteur.
- Données, documents ou matériel nécessaires.
- Contraintes à respecter.
- Étapes éventuelles.
- Critères d'évaluation.
- Solution ou corrigé attendu.
- Explication du raisonnement.
- Erreurs possibles et conseils de correction.

Ne pas se contenter de noter « prévoir un exercice ».

Le brief doit permettre à un autre agent de rédiger l'exercice sans avoir à inventer les éléments pédagogiques essentiels.

### 8.3 Gestion des briefs

Créer des commandes permettant :

- De créer le brief d'un chapitre.
- De générer les briefs à partir du sommaire.
- De régénérer un brief précis.
- D'ajouter une section.
- De modifier ou remplacer une section.
- De déplacer une section.
- De supprimer une section.
- D'ajouter, modifier, déplacer ou supprimer un exercice.
- De modifier les illustrations prévues.
- De contrôler la complétude du brief.
- De comparer un chapitre rédigé avec son brief.
- D'approuver explicitement le brief.
- De traduire un brief dans une autre langue.

Les opérations destructives doivent demander confirmation lorsqu'elles n'ont pas été explicitement demandées.

Un brief nouvellement créé ou modifié doit être marqué comme brouillon ou nécessiter une nouvelle approbation, selon la nature de la modification.

Seul un brief explicitement approuvé peut autoriser la rédaction du chapitre correspondant.

La génération d'un chapitre doit s'arrêter proprement si son brief manque ou n'est pas approuvé.

La génération d'une plage ou de tous les chapitres doit signaler les briefs manquants ou non approuvés et ne pas les contourner silencieusement.

## 9. Commandes OpenCode

Créer des commandes OpenCode distinctes, documentées et réellement exécutables.

Les noms ci-dessous sont des noms fonctionnels attendus. Si l'architecture actuelle utilise une convention différente, documenter la correspondance et maintenir une nomenclature cohérente.

### 9.1 Configuration et planification

Prévoir des commandes pour :

- Initialiser le projet.
- Lire et vérifier sa configuration.
- Modifier les paramètres du livre.
- Construire ou actualiser le sommaire.
- Générer le plan éditorial général.
- Vérifier la cohérence du plan.
- Afficher l'état du projet.
- Reprendre une session.

### 9.2 Briefs des chapitres

Prévoir notamment :

- `/book-chapter-brief` : créer ou mettre à jour le brief détaillé d'un chapitre.
- `/book-chapter-brief-edit` : ajouter, modifier, déplacer, supprimer ou corriger des éléments du brief.
- Une commande d'approbation explicite des briefs.
- Une commande de contrôle des briefs.
- `/book-translate-chapter-brief` : traduire un brief.
- `/book-translate-chapter-briefs` : traduire plusieurs briefs ou tous les briefs.

### 9.3 Rédaction et révision

Prévoir :

- `/book-chapter` : rédiger un chapitre à partir de son brief approuvé.
- `/book-range` : traiter une plage de chapitres.
- `/book-all` : traiter tous les chapitres admissibles.
- `/book-review` : vérifier un chapitre.
- `/book-review-all` : vérifier l'ensemble du livre.
- Des commandes de correction et de mise à jour ciblées.

La rédaction doit respecter les briefs approuvés et la configuration du livre.

La révision doit détecter les omissions, contradictions, répétitions inutiles, exercices incomplets, problèmes de structure et incohérences avec les autres chapitres.

### 9.4 Illustrations

Prévoir des commandes distinctes pour :

- Préparer le catalogue des illustrations.
- Générer les descriptions détaillées.
- Générer les prompts.
- Contrôler les répétitions.
- Vérifier la cohérence avec le thème et le chapitre.
- Préparer les images attendues.
- Contrôler les images existantes.
- Approuver les illustrations.

Le système doit pouvoir préparer les descriptions et les prompts sans démarrer automatiquement un moteur de génération d'images.

**Ne pas lancer automatiquement le moteur d'images.** Sa disponibilité, son démarrage et son arrêt restent sous le contrôle de l'utilisateur ou d'une procédure explicitement demandée.

Ne pas déclarer une illustration produite si seul son prompt existe.

### 9.5 Traductions

Prévoir des commandes indépendantes pour traduire :

- Le sommaire.
- Les briefs détaillés.
- Un chapitre.
- Une plage de chapitres.
- Tous les chapitres.
- La description commerciale.
- La quatrième de couverture.
- Les catalogues d'illustrations.
- Les prompts d'illustrations.
- Les autres éléments éditoriaux nécessaires.

Une commande globale de traduction doit orchestrer les tâches appropriées sans mélanger les contenus de langues différentes.

### 9.6 Assemblage et publication

Prévoir des commandes distinctes pour :

- Vérifier les prérequis à l'assemblage.
- Assembler le livre complet.
- Générer les PDF demandés.
- Générer l'EPUB demandé.
- Préparer les fichiers pour Kindle.
- Préparer les fichiers de publication KDP.
- Préparer les fichiers numériques pour Etsy.
- Générer les couvertures nécessaires.
- Contrôler les dimensions, marges, polices, pagination et éléments requis.
- Générer un rapport final.
- Lister tous les livrables créés et leur chemin.

La commande d'assemblage du livre doit être distincte des commandes de rédaction.

Elle doit assembler les chapitres dans le bon ordre, inclure les éléments liminaires et finaux prévus, respecter la configuration et vérifier que les fichiers nécessaires sont présents.

La commande de production finale doit créer les formats réellement demandés dans la configuration.

Ne jamais inventer le nom d'une commande : toute commande documentée doit correspondre à un fichier présent et à une fonctionnalité implémentée.

## 10. Commandes automatisables

Pour les opérations pouvant être exécutées sans interaction éditoriale, prévoir des variantes scriptables, par exemple avec le préfixe `scriptable-`.

Ces variantes doivent pouvoir être utilisées dans des scripts et des pipelines automatisés.

Elles doivent :

- Accepter des paramètres explicites.
- Vérifier les prérequis.
- Fournir un code de sortie exploitable.
- Produire des messages de diagnostic clairs.
- Éviter les questions interactives non nécessaires.
- Ne pas contourner les validations éditoriales.
- Ne pas approuver automatiquement un contenu nécessitant une décision humaine.
- Ne jamais écraser silencieusement des fichiers existants.

Les commandes interactives et les commandes scriptables doivent partager les mêmes règles métier.

## 11. Gestion multilingue

Chaque langue doit avoir son propre espace de travail, ses textes, ses briefs et ses illustrations.

Lorsqu'une nouvelle langue est ajoutée :

1. Créer l'arborescence complète de cette langue.
2. Créer les fichiers de configuration nécessaires.
3. Créer les index, modèles et espaces de stockage.
4. Préparer les emplacements pour les sommaires, briefs, chapitres, prompts et illustrations.
5. Documenter les étapes nécessaires pour rendre la langue opérationnelle.

**La création d'une langue ne doit déclencher aucune traduction ni génération de contenu automatiquement.**

Elle doit seulement préparer les espaces et les outils nécessaires.

L'utilisateur choisit ensuite explicitement les commandes de traduction ou de création à exécuter.

Les traductions doivent préserver le sens, la structure, les exercices, les exemples et les références. Les unités, exemples culturels et conventions locales doivent être adaptés lorsque nécessaire, sans altérer le sens du contenu.

Les illustrations doivent être distinctes pour chaque langue. Ne pas simplement réutiliser automatiquement les images d'une autre langue comme si elles étaient localisées.

Les images peuvent partager une intention visuelle commune, mais chaque langue doit posséder ses propres fichiers et son propre processus de validation.

## 12. Images et couvertures

Prévoir un système de catalogue et de suivi des illustrations.

Chaque illustration doit disposer d'un identifiant stable, d'une description, d'un emplacement prévu, d'un prompt et d'un statut.

Le système doit détecter les illustrations manquantes et les répétitions potentielles.

Les couvertures doivent être préparées selon le format de publication choisi.

Pour une couverture brochée, prendre en compte les dimensions du livre, le nombre de pages, le dos, le fond perdu et les contraintes techniques applicables.

La quatrième de couverture doit posséder un espace et un contenu éditorial distincts.

Ne jamais déclarer une couverture techniquement prête si les paramètres nécessaires sont absents ou non vérifiés.

## 13. Modèles IA gratuits et compatibilité

Le projet doit être conçu pour fonctionner avec des modèles gratuits ou locaux.

Ne pas imposer Claude, une API payante, un abonnement ou une clé API payante.

Ne pas supposer qu'un modèle gratuit est disponible sans quota : documenter les limites connues et les prérequis de chaque fournisseur.

Séparer la configuration du modèle utilisé par OpenCode des scripts de production documentaire.

Permettre de modifier le fournisseur et le modèle sans réécrire le workflow éditorial.

Lorsque le modèle est local, tenir compte des ressources disponibles et des limites matérielles.

Ne jamais inscrire de secrets, de clés API ou de mots de passe dans le dépôt, les documents de mémoire ou les fichiers livrables.

## 14. Exécution isolée et sécurité

Les scripts doivent fonctionner dans un environnement contrôlé.

Toute exécution de code ou de commandes doit être limitée aux actions nécessaires au projet.

Éviter les suppressions globales, les modifications du système, les installations non sollicitées et les commandes dangereuses.

Vérifier les chemins et les paramètres avant d'exécuter une opération.

Utiliser des environnements virtuels ou des mécanismes d'isolation appropriés lorsque cela est nécessaire et disponible.

Ne pas exécuter automatiquement un script ou du code provenant d'une source non vérifiée.

Les erreurs doivent être remontées clairement et ne doivent pas conduire à annoncer un succès fictif.

## 15. Scripts multiplateformes

Fournir des scripts équivalents pour :

- Linux et Ubuntu : `.sh`.
- Windows : `.bat`.
- PowerShell : `.ps1`.

Les trois versions doivent permettre d'effectuer les opérations principales du générateur.

Elles doivent vérifier les dépendances, les paramètres, les chemins et les erreurs.

Les différences entre plateformes doivent être documentées.

Ne pas annoncer que les scripts Windows ont été testés sur Windows si les tests ont été effectués uniquement sous Linux.

Fournir des instructions précises d'installation, de lancement, de configuration et de dépannage.

## 16. Construction et assemblage du livrable complet

C'est une fonctionnalité essentielle.

Le projet doit posséder une commande identifiable et documentée pour **assembler le livre complet et produire les livrables finaux**.

Le processus doit distinguer au minimum :

1. La génération du contenu.
2. L'approbation et la validation du contenu.
3. L'assemblage des sources.
4. La génération des formats demandés.
5. Le contrôle technique des fichiers.
6. La publication des résultats dans le répertoire final.

La commande d'assemblage doit vérifier :

- Que le sommaire est présent.
- Que les chapitres nécessaires existent.
- Que les briefs correspondants sont approuvés.
- Que les chapitres ont été contrôlés.
- Que les traductions requises sont présentes.
- Que les illustrations obligatoires existent ou que leur absence est explicitement acceptée.
- Que les couvertures requises sont présentes ou que leur production est demandée.
- Que les paramètres de sortie sont valides.
- Que les dépendances de conversion sont disponibles.

Si un prérequis manque, la commande doit afficher précisément les éléments bloquants et les commandes à exécuter pour les résoudre.

Elle ne doit ni supprimer le travail existant ni produire silencieusement un livrable incomplet présenté comme définitif.

Après assemblage, créer un répertoire de sortie organisé par langue et par format.

Générer un manifeste recensant chaque fichier, son type, son chemin, sa date de création et son statut de validation.

Créer également un rapport de production précisant :

- Les fichiers générés.
- Les formats produits.
- Les contrôles effectués.
- Les contrôles réussis.
- Les avertissements.
- Les erreurs.
- Les éléments restant à produire.
- Les limites de conformité éventuelles.

Prévoir une commande de contrôle permettant de vérifier que tous les livrables attendus sont réellement présents.

La documentation doit indiquer explicitement **la commande exacte à lancer après la rédaction pour assembler et construire le livrable complet**, puis la commande exacte de vérification finale.

Ces commandes doivent exister dans le projet et être testées. Ne pas se contenter de les mentionner dans un README.

## 17. Qualité, tests et cohérence

Créer des tests automatisés couvrant les fonctions importantes.

Vérifier notamment :

- La création d'un nouveau projet.
- Le questionnaire et l'enregistrement de la configuration.
- La création de l'arborescence.
- La création des briefs.
- Le blocage de la rédaction si un brief n'est pas approuvé.
- La modification des briefs.
- La gestion des exercices.
- La création d'une nouvelle langue.
- L'absence de traduction automatique à la création d'une langue.
- Les commandes de traduction.
- La génération des chapitres.
- La vérification du contenu.
- L'assemblage.
- La génération des formats.
- La détection des fichiers manquants.
- La gestion des erreurs.
- La protection contre l'écrasement de fichiers.
- Les scripts et les commandes réellement disponibles.

Tester les fonctions de manière reproductible.

Ne pas remplacer les tests par une simple inspection visuelle des fichiers.

Ne pas déclarer un test réussi s'il n'a pas été exécuté.

## 18. Documentation obligatoire

Fournir une documentation complète, claire et compréhensible.

Elle doit expliquer :

- L'architecture du générateur.
- L'installation des dépendances.
- Le lancement sous chaque plateforme.
- Le fonctionnement du questionnaire.
- La configuration d'un livre.
- L'utilisation des commandes OpenCode.
- La création et l'approbation des briefs.
- La rédaction et la révision des chapitres.
- La création des langues.
- La traduction.
- La préparation des illustrations.
- L'assemblage.
- La génération des formats.
- Le contrôle des livrables.
- La reprise après interruption.
- Le dépannage.
- Les limitations connues.

Inclure une table récapitulative des commandes réellement disponibles, avec leur fonction, leurs paramètres, leurs prérequis et un exemple d'utilisation.

Chaque commande documentée doit correspondre à une implémentation existante.

## 19. Livrables attendus du développement du générateur

Le résultat de ce travail doit inclure :

- Le code complet du générateur.
- Les scripts `.sh`, `.bat` et `.ps1`.
- Les commandes OpenCode.
- Les agents et skills nécessaires.
- Les modèles de fichiers.
- Les scripts de validation et d'assemblage.
- Les tests automatisés.
- Les documentations.
- Un exemple de configuration.
- Une procédure de création d'un livre de démonstration.
- Une procédure de construction du livrable final.
- Un rapport des tests effectués.
- Une archive ZIP complète du projet.
- Une archive TAR.GZ si possible.
- Une somme SHA-256 des archives.

Les archives doivent contenir les fichiers réellement présents dans le projet. Ne pas créer de liens de téléchargement fictifs.

## 20. Méthode de travail imposée

Travaille par étapes cohérentes :

1. Analyse de l'existant.
2. Diagnostic des fonctionnalités manquantes.
3. Proposition ou mise à jour de l'architecture.
4. Implémentation des fonctionnalités.
5. Création des commandes et scripts.
6. Ajout des tests.
7. Exécution des tests.
8. Correction des erreurs.
9. Génération d'un projet de démonstration.
10. Vérification du workflow complet.
11. Construction des archives.
12. Rapport final.

N'arrête pas le travail après avoir créé les fichiers de documentation ou les commandes Markdown.

Vérifie que les scripts référencés existent et que leurs paramètres correspondent à la documentation.

Lorsque c'est possible, réalise un test d'intégration allant de la configuration initiale jusqu'à l'assemblage d'un livrable.

Si un test nécessite un modèle IA, un moteur d'images ou un outil externe indisponible, distingue clairement ce qui a été testé automatiquement de ce qui reste à tester.

## 21. Critères d'acceptation finaux

Le projet sera considéré comme terminé lorsque :

- Le générateur crée un projet autonome pour un seul livre.
- Le questionnaire permet de définir les paramètres éditoriaux et techniques.
- Le workflow est reprenable.
- Chaque chapitre doit disposer d'un brief détaillé approuvé avant sa rédaction.
- Les briefs peuvent être modifiés et complétés.
- Les exercices possèdent des énoncés, des consignes et des corrections planifiés.
- Les commandes de traduction sont explicites.
- L'ajout d'une langue ne déclenche pas de génération automatique.
- Chaque langue possède ses propres espaces d'illustrations.
- Le moteur d'images n'est pas démarré automatiquement.
- Les commandes documentées correspondent aux commandes réellement disponibles.
- Le livre peut être assemblé et exporté dans les formats demandés.
- Les livrables sont contrôlés avant d'être déclarés terminés.
- Les scripts multiplateformes sont présents.
- Les tests exécutés et leurs résultats sont documentés.
- Les archives finales sont créées et vérifiables.

## 22. Consigne finale

Commence par analyser les fichiers présents.

Ensuite, implémente les fonctionnalités manquantes et corrige les incohérences.

Ne me fournis pas seulement des exemples de code ou des instructions pour réaliser moi-même les modifications : effectue les modifications dans le projet lorsque l'environnement le permet.

À la fin, donne-moi :

1. Le résumé des modifications.
2. Les commandes exactes pour créer un projet de livre.
3. Les commandes exactes pour créer, modifier et approuver les briefs.
4. Les commandes exactes pour rédiger et vérifier les chapitres.
5. Les commandes exactes pour traduire le contenu.
6. **La commande exacte pour assembler le livre complet après la rédaction.**
7. La commande exacte pour générer les livrables finaux.
8. La commande exacte pour vérifier ces livrables.
9. Les résultats réels des tests.
10. Les liens vers les archives créées et leurs sommes de contrôle.

Ne suppose pas qu'une commande existe parce que son nom paraît logique. Vérifie sa présence, son implémentation et son fonctionnement avant de me la communiquer.

Ne déclare pas le projet terminé si des fonctionnalités obligatoires sont absentes ou si le workflow de production final n'a pas été vérifié.