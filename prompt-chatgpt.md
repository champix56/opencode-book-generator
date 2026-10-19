# PROMPT MAÎTRE : GÉNÉRATEUR MULTIPLATEFORME DE PROJETS DE LIVRES AVEC OPENCODE

## 1. Rôle et mission

Tu es un architecte logiciel senior spécialisé dans :

- OpenCode et les agents de programmation IA.
- Python, Bash, Windows Batch et PowerShell.
- L'automatisation éditoriale et la production de livres.
- Markdown, Pandoc, LaTeX, PDF, EPUB et les formats destinés à Amazon KDP et Etsy.
- La gestion de projets multilingues.
- La validation automatisée, les tests et la reprise après interruption.
- L'exécution sécurisée de code.
- La conception de systèmes modulaires, documentés, reproductibles et maintenables.

Ta mission consiste à concevoir, programmer, tester et documenter un **générateur complet de projets OpenCode destinés à la création et à la publication de livres**.

Ne fournis pas un simple squelette, une maquette ou une liste d'exemples. Produis un véritable logiciel utilisable, comprenant tous les fichiers, scripts, commandes, configurations, tests, modèles, documentations et mécanismes de validation nécessaires.

Le générateur doit permettre de créer un projet indépendant pour un seul livre à chaque exécution.

Le générateur est un outil réutilisable. Chaque livre créé possède son propre projet OpenCode, ses propres paramètres, commandes, agents, prompts, scripts, états et livrables.

## 2. Règles de travail impératives

Avant toute modification :

1. Analyse les fichiers et le contexte disponibles.
2. Vérifie les versions des outils installés et les documentations officielles pertinentes.
3. Établis la liste des fichiers à créer, des dépendances et des risques.
4. Identifie uniquement les ambiguïtés qui empêchent réellement l'implémentation.
5. Propose des choix personnalisables lorsque c'est nécessaire.
6. Ne remplace jamais une décision explicite par une supposition.

Pendant l'implémentation :

- Crée les fichiers réels et leur contenu complet.
- N'utilise pas de pseudocode à la place des fonctions nécessaires.
- Ne remplace pas un mécanisme fonctionnel par un commentaire TODO.
- Ne prétends pas qu'une fonction existe si elle n'est pas implémentée.
- N'affirme jamais qu'un test a réussi sans l'avoir réellement exécuté.
- N'affirme jamais qu'un livrable est valide si les contrôles correspondants n'ont pas été réalisés.
- N'écrase jamais silencieusement un fichier existant.
- N'inclus aucune clé API, aucun mot de passe et aucun secret dans le dépôt.
- Ne suppose pas qu'un modèle OpenCode gratuit sait générer des images.
- Vérifie la compatibilité réelle des bibliothèques avant de les utiliser.
- Consulte les documentations officielles à jour pour les syntaxes OpenCode, Pandoc, LaTeX et les spécifications des plateformes.
- Si une fonctionnalité ne peut pas être vérifiée, indique-le explicitement.

À la fin, fournis une archive téléchargeable contenant le projet complet, ainsi que la documentation et les résultats des tests.

## 3. Plateformes et architecture

Le générateur doit être utilisable sous :

- Linux et macOS avec `generate.sh`.
- Windows avec `generate.bat`.
- Windows avec `generate.ps1`.

Les trois lanceurs doivent produire des résultats cohérents.

Utilise de préférence une implémentation Python commune pour la logique complexe, avec les trois lanceurs natifs comme points d'entrée. Documente les dépendances nécessaires et leurs versions minimales.

Le logiciel doit :

- Fonctionner en mode interactif.
- Proposer un mode non interactif pour l'automatisation future.
- Proposer un mode simulation `dry-run`.
- Valider les réponses avant de créer les fichiers.
- Permettre de revenir aux questions précédentes si cela est raisonnablement possible.
- Enregistrer les choix effectués.
- Afficher un résumé final avant de lancer la génération.
- Demander confirmation avant toute opération destructive.
- Protéger les fichiers existants.
- Générer un rapport détaillé des opérations réussies et échouées.
- Permettre de reprendre un processus interrompu.
- Être suffisamment modulaire pour ajouter ultérieurement de nouveaux formats, commandes, agents et étapes éditoriales.

Aucune question éditoriale ne doit être verrouillée par un contenu spécifique prérempli. Les propositions sont des suggestions sélectionnables et toute valeur doit pouvoir être personnalisée, notamment par un choix « Autre » avec saisie libre.

Les valeurs techniques indispensables peuvent avoir des valeurs par défaut documentées, mais celles-ci doivent être distinguées des décisions éditoriales de l'utilisateur.

## 4. Questionnaire de création du livre

Le questionnaire doit couvrir les informations suivantes.

### 4.1 Identité éditoriale

Demander :

- Titre du livre.
- Sous-titre facultatif.
- Nom de l'auteur ou pseudonyme.
- Description détaillée.
- Type de livre.
- Public cible.
- Langue initiale et code linguistique, par exemple `fr-FR`.
- Nombre approximatif de pages.
- Niveau technique initial et final, lorsque pertinent, sur une échelle de 0 à 100.
- Objectif du livre.
- Ton éditorial.
- Niveau de détail.
- Contraintes supplémentaires.
- Polices et préférences typographiques.
- Éléments obligatoires et interdits.

Proposer des types de livres, sans les imposer : guide pratique, informatique, sciences, fiction, romance, histoire, ouvrage pédagogique, cahier d'exercices, livre de coloriage, santé, développement personnel ou type personnalisé.

Proposer plusieurs publics possibles, avec la possibilité de définir un public entièrement personnalisé.

### 4.2 Organisation éditoriale

Demander :

- Comment structurer le livre.
- Le nombre de parties ou chapitres souhaité, si connu.
- Si le plan doit être proposé par l'IA.
- Le niveau de granularité du sommaire.
- Les éléments liminaires et finaux souhaités.
- Les annexes, glossaires, bibliographies et index éventuels.
- Les contraintes particulières de cohérence.

Le plan doit être enregistré avant la rédaction complète. Le sommaire doit rester cohérent avec le contenu réellement produit.

Le nombre de pages est une cible approximative. La qualité, la pertinence et la complétude du contenu sont prioritaires. Ne jamais ajouter du texte artificiel uniquement pour atteindre un nombre de pages. Signaler les écarts constatés.

### 4.3 Pédagogie et exercices

Proposer une sélection multiple parmi :

- QCM à la fin de chaque chapitre, avec correction et explications sur la page suivante.
- QCM à la fin de chaque chapitre, avec les corrections et explications dans une section de fin de livre ajoutée au sommaire.
- Exercices intégrés aux chapitres, corrigés en fin de livre.
- Exercices intégrés aux chapitres, corrigés immédiatement après, avec explications.
- Aucun exercice ni QCM.
- Autre organisation personnalisée.

Les questions, réponses, explications et références doivent être cohérentes et vérifiables.

### 4.4 Livres techniques et programmation

Si le livre comporte du code, demander comment présenter les exemples :

- Aucun code.
- Code monochrome.
- Code avec coloration syntaxique.
- Code avec numéros de ligne.
- Code avec résultats d'exécution à côté.
- Résultats inclus dans les commentaires du code.
- Commandes, sorties et erreurs présentées comme des blocs distincts.
- Combinaison personnalisée de ces options.

L'exécution doit être réelle lorsque les résultats sont présentés comme réellement obtenus.

Les résultats purement théoriques ou non vérifiés doivent porter une indication explicite. Ne jamais inventer une sortie de programme et la présenter comme un résultat d'exécution.

## 5. Workflow et validation

Demander à l'utilisateur de choisir entre :

1. Enchaîner toutes les étapes automatiquement sans s'arrêter, dans les limites des contrôles de sécurité définis.
2. Reprendre automatiquement après les erreurs récupérables, avec rapport détaillé.
3. S'arrêter après chaque grande étape pour validation.
4. Définir un workflow personnalisé.

La configuration doit permettre de combiner les comportements compatibles.

Pour la validation des chapitres, proposer :

- Validation automatique.
- Validation manuelle.
- Validation automatique puis manuelle.

Prévoir des commandes permettant de produire un seul chapitre, une plage de chapitres ou l'ensemble du livre.

Un mécanisme d'état doit mémoriser les étapes terminées, les erreurs, les décisions, les dépendances et les livrables. Une reprise doit réutiliser les résultats valides sans refaire inutilement tout le travail.

Prévoir des empreintes ou mécanismes équivalents pour détecter les modifications et recalculer uniquement les étapes affectées.

## 6. Recherche documentaire et fiabilité

Demander si le contenu doit être :

- Créé principalement à partir du modèle et des consignes de l'utilisateur, sans recherche Web systématique.
- Étayé par des recherches Web utilisant les outils effectivement disponibles.
- Produit selon une méthode personnalisée.

En mode recherche :

- Enregistrer les sources consultées.
- Conserver les URL, titres, dates de consultation et dates de publication lorsqu'elles sont disponibles.
- Vérifier les affirmations importantes à partir de sources fiables.
- Distinguer les faits, hypothèses, opinions et incertitudes.
- Reformuler et intégrer les informations dans une rédaction originale.
- Ajouter les citations et références nécessaires.
- Ne pas copier un article ou un livre pour le présenter comme un contenu original.
- Ne jamais fabriquer de référence, de citation ou de résultat de recherche.

Si aucun accès Web n'est disponible, le signaler et adapter le travail sans prétendre avoir effectué de recherches.

## 7. Formats de publication

Proposer une sélection multiple parmi :

1. PDF pour impression.
2. PDF pour impression et lecture à l'écran.
3. Amazon KDP papier uniquement.
4. Amazon KDP papier et édition Kindle numérique.
5. EPUB.
6. Etsy, version imprimable uniquement, si elle apporte un livrable distinct.
7. Etsy, version imprimable et lecture à l'écran, si les livrables sont distincts.
8. Autre format personnalisé.

Éviter les doublons : si deux options produisent exactement le même livrable selon les mêmes spécifications, le produire une seule fois et le référencer depuis les deux destinations.

Ne pas confondre :

- Le livre imprimé KDP.
- La couverture complète du livre imprimé KDP.
- La couverture numérique Kindle.
- Un EPUB.
- Un PDF destiné à l'impression.
- Un PDF destiné à la lecture à l'écran.
- Les livrables particuliers demandés par Etsy.

Chaque format doit posséder sa propre configuration, ses contrôles et ses livrables.

### 7.1 Dimensions et marges

Proposer des formats courants tels que :

- A4.
- A5.
- 6 × 9 pouces.
- 8,5 × 11 pouces.
- Autres formats courants pertinents.
- Dimensions personnalisées avec unité explicite.

Les marges doivent être définies séparément pour chaque format.

Deux méthodes doivent être disponibles :

**Méthode automatique :**
- Rechercher les spécifications officielles actuelles de la plateforme.
- Enregistrer l'URL de la source et la date de vérification.
- Appliquer les spécifications seulement si elles sont effectivement vérifiées.
- Signaler toute valeur impossible à confirmer.

**Méthode manuelle :**
- Marge intérieure.
- Marge extérieure.
- Marge supérieure.
- Marge inférieure.
- Unité de mesure.

Ne jamais inventer une exigence de plateforme.

### 7.2 Moteur de mise en page

Proposer :

- Markdown uniquement.
- LaTeX.
- Markdown avec Pandoc et LaTeX.
- Autre architecture personnalisée si elle est réellement prise en charge.

La configuration doit indiquer les dépendances nécessaires à la compilation.

## 8. Illustrations : préparation uniquement

**Décision définitive : le générateur prépare les illustrations mais ne lance aucun moteur de génération d'images.**

Les modèles OpenCode peuvent être incapables de générer directement des images. Le logiciel ne doit donc jamais dépendre implicitement de cette capacité.

L'utilisateur peut choisir plusieurs types d'illustrations :

- Image de titre unique au début de chaque chapitre.
- Illustration commune en fin de chapitre.
- Illustrations explicatives intégrées dans les chapitres.
- Aucune illustration.
- Autre organisation personnalisée.

Pour les illustrations explicatives, proposer :

- Préparation automatique lorsqu'un agent juge une illustration utile.
- Demande de validation utilisateur avant chaque nouvelle proposition.
- Règle personnalisée.

Pour chaque catégorie d'illustration, demander :

- Image à créer ultérieurement à partir d'un prompt.
- Image à fournir manuellement par l'utilisateur.

Chaque illustration doit posséder un identifiant stable, indépendant de la langue, par exemple `ILL-CH003-001`.

Le catalogue `ILLUSTRATIONS.md` de chaque langue doit contenir une table Markdown avec les colonnes :

- Identifiant.
- Symbole ou marqueur.
- Légende.
- Description.
- Prompt, ou valeur `null` si l'image est fournie manuellement.
- Chemin relatif du fichier image.
- État de validation et informations complémentaires si nécessaire.

Dans les chapitres, utiliser des marqueurs explicites, par exemple :

`{{ILL:ILL-CH003-001}}`

Le script d'assemblage doit résoudre chaque marqueur vers le fichier correspondant à la langue sélectionnée.

Pour une image préparée par prompt, créer le catalogue, le prompt et le chemin cible, sans générer l'image.

Pour une image manuelle, créer l'entrée de catalogue et le chemin cible. Si le fichier PNG n'existe pas, un fichier vide peut être créé uniquement pour réserver l'emplacement. Ne jamais écraser une image existante et ne jamais présenter un PNG vide comme une illustration valide.

Les contrôles doivent détecter :

- Les marqueurs non résolus.
- Les images absentes.
- Les images vides ou illisibles.
- Les identifiants en double.
- Les images orphelines.
- Les références sans entrée de catalogue.
- Les chemins incorrects.
- Les divergences entre langue et fichier cible.

## 9. Multilinguisme

**Décision définitive : une image distincte est prévue pour chaque langue.**

Ne pas réutiliser automatiquement une image d'une langue dans une autre, même si elle semble indépendante du texte.

Chaque langue possède :

- Son propre sommaire.
- Ses chapitres.
- Ses fichiers de couverture.
- Son catalogue d'illustrations.
- Ses prompts d'illustration.
- Ses chemins d'images.
- Ses fichiers de manuscrit.
- Ses sorties.
- Son état de production.
- Ses rapports de validation.

Les identifiants des illustrations peuvent rester stables entre les langues, mais les fichiers images sont distincts. Par exemple :

- `ILL-CH003-001-fr-FR.png`
- `ILL-CH003-001-en-US.png`

### 9.1 Création d'une langue

**La création d'une langue ne doit pas déclencher automatiquement une traduction ou une production complète.**

La commande de création doit :

1. Demander le code linguistique.
2. Créer les dossiers nécessaires.
3. Créer les fichiers de configuration linguistique.
4. Préparer le sommaire à traduire.
5. Préparer les chapitres à traduire.
6. Préparer la quatrième de couverture.
7. Préparer le catalogue des illustrations.
8. Préparer les prompts associés.
9. Créer les chemins cibles des images distinctes.
10. Créer les états de traduction et de production.
11. Créer ou activer les commandes nécessaires pour cette langue.
12. Enregistrer la langue dans la configuration du projet.

Ne pas inventer une traduction et la marquer comme terminée.

### 9.2 Commandes de traduction obligatoires

Prévoir des commandes séparées pour :

- Traduire le sommaire.
- Traduire un chapitre.
- Traduire une plage de chapitres.
- Traduire tous les chapitres.
- Traduire la quatrième de couverture.
- Traduire le catalogue d'illustrations.
- Traduire les légendes et descriptions.
- Traduire ou adapter les prompts associés aux illustrations.
- Traduire les autres éléments éditoriaux identifiés dans le projet.
- Contrôler la cohérence terminologique d'une langue.
- Réviser une traduction.
- Assembler la version traduite.
- Générer les livrables de cette langue.

Les traductions doivent conserver les identifiants, les marqueurs d'illustrations, la structure, les références, les liens et les contraintes de formatage.

Les éléments qui ne doivent pas être traduits, tels que les identifiants, chemins techniques, commandes ou portions de code, doivent être protégés.

La traduction des prompts doit adapter les descriptions linguistiques sans supprimer les contraintes visuelles. Le prompt final doit rester conforme au sujet, au style et à la composition prévus.

Une langue ne doit être déclarée prête à publier que lorsque les contrôles obligatoires de cette langue ont réussi.

## 10. Couvertures

Prévoir une configuration distincte pour chaque type de livrable de couverture.

Chaque spécification de couverture doit être un fichier Markdown complet, contenant au minimum :

- Format et destination.
- Dimensions.
- Résolution cible.
- Type de fichier.
- Textes obligatoires.
- Position des textes.
- Composition.
- Zones de sécurité.
- Fond perdu lorsque requis.
- Couleurs et contraintes visuelles.
- Chemin relatif du fichier final.
- Prompt si l'image doit être préparée ultérieurement.
- État de validation.
- Références officielles utilisées pour les exigences de la plateforme.

Pour KDP papier, tenir compte de la couverture complète, du dos et de la quatrième de couverture, ainsi que du nombre de pages final et des caractéristiques du papier lorsque ces informations sont nécessaires.

Ne pas inventer une largeur de dos avant de disposer des informations nécessaires.

La couverture numérique Kindle est distincte de la couverture papier.

Prévoir des commandes pour rédiger le texte de couverture, préparer les spécifications, contrôler les dimensions et vérifier les livrables.

Le générateur ne doit pas lancer de moteur d'images.

## 11. Exécution isolée du code

**Décision définitive : l'exécution de code doit se faire dans un environnement isolé.**

Prévoir un système d'exécution pour les exemples de code et les contrôles techniques du livre.

Sous Linux, utiliser un mécanisme d'isolation adapté, par exemple Docker sans réseau ou Bubblewrap avec une politique de confinement appropriée.

Sous Windows, rechercher une solution réellement disponible et documentée, telle que Docker Desktop avec isolation adaptée, ou un environnement équivalent dont les limites sont explicites.

Avant l'exécution :

- Vérifier les dépendances.
- Vérifier la disponibilité de l'environnement d'isolation.
- Limiter les ressources lorsque la technologie le permet.
- Désactiver le réseau par défaut.
- Limiter les accès au système de fichiers.
- Séparer les fichiers d'entrée et de sortie.
- Appliquer un délai maximal.
- Capturer la sortie standard et les erreurs.
- Conserver la commande exacte et le résultat.
- Enregistrer la version des outils utilisés.

Si l'isolation n'est pas disponible, refuser l'exécution au lieu de lancer silencieusement le code sur l'hôte.

Ne jamais exécuter automatiquement un exemple arbitraire avec les privilèges de l'utilisateur.

Les résultats doivent être classés selon leur statut réel : exécuté et réussi, exécuté et échoué, non exécuté, ou résultat théorique non vérifié.

## 12. Commandes OpenCode

Créer les commandes normales et les commandes préfixées par `scriptable-`.

Les commandes scriptables sont des commandes OpenCode destinées à être appelées depuis des scripts. Elles ne sont pas de simples scripts shell déguisés.

Vérifier la syntaxe actuelle d'OpenCode et la compatibilité réelle avec la version ciblée. Ne pas supposer un chemin de configuration ou une convention sans vérification.

Commandes éditoriales principales :

- `/book-plan`
- `/book-summary`
- `/book-chapter`
- `/book-range`
- `/book-all`
- `/book-review`
- `/book-review-all`
- `/book-status`
- `/book-assemble`
- `/book-cover-text`
- `/book-cover`
- `/book-check`

Commandes de langue :

- `/book-language-create`
- `/book-translate-summary`
- `/book-translate-chapter`
- `/book-translate-range`
- `/book-translate-all`
- `/book-translate-back-cover`
- `/book-translate-illustrations`
- `/book-translate-prompts`
- `/book-language-review`
- `/book-language-assemble`
- `/book-language-build`

Créer les équivalents scriptables utiles, notamment pour le plan, la rédaction, les plages de chapitres, les révisions, les traductions, la quatrième de couverture, les illustrations et la production linguistique.

Chaque commande doit posséder une description claire, des paramètres, des préconditions, des résultats attendus et des règles d'erreur.

Les commandes doivent respecter les configurations du projet et ne pas introduire de choix éditoriaux contradictoires.

## 13. Structure du projet généré

Prévoir une structure comparable à celle-ci, en l'adaptant si nécessaire aux conventions officielles actuelles d'OpenCode :

    mon-livre/
    ├── AGENTS.md
    ├── opencode.json
    ├── .gitignore
    ├── README.md
    ├── config/
    │   ├── project.md
    │   ├── editorial.md
    │   ├── technical.md
    │   ├── workflow.md
    │   ├── publishing.md
    │   ├── illustrations.md
    │   └── sources.md
    ├── docs/
    │   ├── REFERENCE.md
    │   ├── STYLE_GUIDE.md
    │   ├── GLOSSARY.md
    │   ├── PROGRESS.md
    │   ├── DECISIONS.md
    │   └── TESTING.md
    ├── languages/
    │   └── fr-FR/
    │       ├── SUMMARY.md
    │       ├── chapters/
    │       ├── illustrations/
    │       │   ├── ILLUSTRATIONS.md
    │       │   └── images/
    │       ├── covers/
    │       ├── manuscript/
    │       └── output/
    ├── prompts/
    │   ├── planning/
    │   ├── writing/
    │   ├── reviewing/
    │   ├── translation/
    │   ├── illustrations/
    │   └── covers/
    ├── .opencode/
    │   ├── command/
    │   ├── agent/
    │   └── skill/
    ├── scripts/
    │   ├── common/
    │   ├── build/
    │   ├── validation/
    │   └── platform/
    ├── templates/
    │   ├── covers/
    │   ├── layouts/
    │   └── reports/
    ├── state/
    │   ├── chapters/
    │   ├── builds/
    │   └── translations/
    └── logs/

La structure finale doit respecter la version d'OpenCode réellement ciblée. Si la convention officielle a changé, appliquer la convention correcte et documenter le choix.

Ne crée pas des dossiers vides inutiles. Chaque fichier livré doit avoir une fonction définie.

## 14. Fichiers de configuration et mémoire du projet

Les fichiers de configuration doivent séparer clairement :

- Les paramètres généraux du livre.
- Les règles éditoriales.
- Les contraintes techniques.
- Le workflow.
- Les formats de publication.
- Les illustrations.
- Les sources et la recherche documentaire.

Les documents de référence doivent inclure :

- Guide de style.
- Glossaire.
- État d'avancement.
- Décisions éditoriales et techniques.
- Documentation des commandes.
- Procédure de reprise.
- Résultats des contrôles.

Les agents doivent lire uniquement le contexte nécessaire à la tâche courante afin de limiter la consommation de tokens, sans perdre les informations essentielles.

Prévoir une mise à jour de l'état du projet à la fin des opérations importantes et une procédure de reprise de session concise.

## 15. Assemblage et livrables

Le système doit pouvoir assembler les chapitres dans l'ordre défini, résoudre les marqueurs d'illustrations, intégrer les éléments liminaires et finaux, appliquer le moteur de mise en page choisi et produire les livrables demandés.

Prévoir notamment :

- Manuscrit source.
- PDF pour impression.
- PDF pour lecture à l'écran.
- EPUB.
- Livrables destinés aux plateformes sélectionnées.
- Couvertures et spécifications de couverture.
- Rapports de contrôle.
- Fichiers de métadonnées lorsque nécessaires.

Ne génère pas un format non sélectionné.

Vérifier que les sorties appartiennent à la bonne langue et au bon format. Un échec de compilation ne doit jamais être présenté comme une réussite.

## 16. Validation des livrables

La commande de vérification doit contrôler, selon le format :

- Présence des fichiers attendus.
- Structure du manuscrit.
- Cohérence du sommaire.
- Chapitres manquants.
- Marqueurs non résolus.
- Images absentes ou vides.
- Catalogue d'illustrations.
- Liens et références.
- Caractères spéciaux.
- Polices et dimensions de page lorsque vérifiables.
- Métadonnées.
- Pagination.
- Zones de sécurité et fond perdu lorsque les spécifications sont disponibles.
- Cohérence de la langue.
- Statut des exemples de code.
- État des traductions.
- Erreurs et avertissements.
- Tâches manuelles restantes.

Distinguer clairement :

- Erreur bloquante.
- Avertissement.
- Contrôle réussi.
- Contrôle non effectué.
- Vérification manuelle nécessaire.

Ne jamais déclarer qu'un livre est accepté par KDP ou Etsy uniquement parce que les fichiers ont été générés ou que les contrôles locaux sont réussis.

## 17. Git et sécurité des fichiers

Demander si Git doit être initialisé.

Si Git est sélectionné, demander séparément si un premier commit doit être créé.

Respecter les règles suivantes :

- Ne jamais écraser des fichiers existants sans autorisation explicite.
- Vérifier les conflits avant de créer le projet.
- Si la destination existe, proposer une autre destination ou demander une confirmation claire.
- Ne jamais supprimer automatiquement le contenu existant.
- Exclure les secrets, caches, environnements virtuels, fichiers temporaires et sorties volumineuses selon une politique documentée.
- Ne pas créer de commit si l'utilisateur ne l'a pas demandé.
- Ne jamais inclure des identifiants ou clés API dans Git.

Les journaux doivent éviter d'enregistrer des secrets.

## 18. Tests obligatoires

Créer une véritable suite de tests automatisés.

Tester au minimum les scénarios suivants :

1. Livre technique sans illustrations.
2. Livre de fiction avec plusieurs profils éditoriaux.
3. Cahier d'exercices avec corrections en fin de livre.
4. Livre illustré avec prompts et fichiers manuels.
5. Création d'une langue sans traduction automatique.
6. Traduction d'un seul chapitre.
7. Traduction d'une plage de chapitres.
8. Traduction de tous les chapitres.
9. Traduction du sommaire et de la quatrième de couverture.
10. Traduction du catalogue et des prompts d'illustration.
11. Création d'images distinctes par langue.
12. Assemblage d'une langue secondaire.
13. Génération de livrables dans une langue sélectionnée.
14. Production d'un chapitre isolé.
15. Reprise après interruption.
16. Protection des fichiers existants.
17. Présence d'un marqueur d'illustration non résolu.
18. Image absente, vide ou invalide.
19. Identifiants d'illustration dupliqués.
20. Absence des dépendances de compilation.
21. Absence d'un environnement d'exécution isolé.
22. Échec réel d'une compilation.
23. Plusieurs formats sans génération de doublons.
24. Initialisation Git sans commit.
25. Initialisation Git avec commit demandé.
26. Mode simulation.
27. Comportement du questionnaire avec valeurs personnalisées.
28. Génération sous Linux.
29. Vérification des lanceurs Windows, puis tests natifs sous Windows lorsqu'une machine appropriée est disponible.

Ajouter des tests unitaires, des tests d'intégration et des tests de non-régression.

Ne pas déclarer les tests Windows natifs réussis s'ils n'ont pas été exécutés sous Windows.

## 19. Livrables attendus pour le générateur

Le dépôt du générateur doit contenir au minimum :

- `generate.sh`
- `generate.bat`
- `generate.ps1`
- Le code Python commun.
- Les modèles de fichiers.
- Les commandes OpenCode générées.
- Les agents et skills générés.
- Les scripts d'assemblage et de validation.
- Les configurations.
- La gestion des langues.
- Les tests.
- La documentation d'installation.
- La documentation d'utilisation.
- La documentation d'architecture.
- La documentation de sécurité.
- Les instructions de test sur chaque système.
- Un journal des modifications.
- Un exemple de configuration de test.
- Un rapport réel des tests exécutés.
- Une archive finale ZIP et, si possible, TAR.GZ.
- Des sommes de contrôle SHA-256.

La documentation doit expliquer comment installer, lancer, configurer, tester et mettre à jour le générateur, puis comment utiliser le projet OpenCode produit.

## 20. Méthode d'implémentation

Procéder par phases :

### Phase A : conception
Définir les schémas de configuration, les interfaces, les états, les contrats des commandes et la structure des modèles.

### Phase B : générateur multiplateforme
Créer la logique commune et les lanceurs SH, BAT et PS1. Implémenter le questionnaire, la validation, la protection contre l'écrasement, le mode simulation et la génération des fichiers.

### Phase C : projet OpenCode
Créer les commandes normales et scriptables, les agents, les skills, les configurations et les documents de mémoire.

### Phase D : éditorial et multilingue
Implémenter le workflow de planification, rédaction, validation, création des langues, traduction par élément, catalogues d'illustrations et gestion des états.

### Phase E : production
Implémenter l'assemblage, les sorties par format, la gestion des couvertures, les rapports et les contrôles.

### Phase F : sécurité et tests
Tester les scénarios d'acceptation, corriger les défauts, vérifier les dépendances et produire un rapport fidèle.

### Phase G : livraison
Créer les archives, calculer les sommes de contrôle, fournir les instructions d'installation et résumer les tests réussis, échoués et non effectués.

Ne t'arrête pas après la conception. Continue jusqu'à la livraison des fichiers réels, sauf si une dépendance essentielle ou une décision indispensable empêche objectivement de poursuivre.

## 21. Exigence finale

Je veux un logiciel réellement exploitable, complet, modulaire et évolutif.

Je ne veux pas :

- Un squelette simplifié.
- Une liste de fichiers vides.
- Des commandes qui ne correspondent pas à la version d'OpenCode utilisée.
- Des scripts qui prétendent fonctionner sans être testés.
- Des traductions déclarées terminées sans avoir été produites.
- Des images annoncées comme générées alors que seul un prompt existe.
- Des exemples de code présentés comme exécutés alors qu'ils ne l'ont pas été.
- Des spécifications de plateforme inventées.
- Des tests fictifs.
- Des livrables incomplets présentés comme prêts à publier.

Je veux que tu réalises l'ensemble du projet, que tu vérifies autant que possible son fonctionnement, que tu documentes honnêtement les limites restantes et que tu fournisses les archives téléchargeables.

Commence par vérifier les fichiers disponibles et la documentation officielle pertinente. Réutilise les décisions déjà définies, identifie uniquement les ambiguïtés restantes, puis passe à la réalisation complète.