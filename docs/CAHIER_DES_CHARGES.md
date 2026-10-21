# Cahier des charges définitif

## Objet
Générateur interactif, réutilisable et multiplateforme qui crée un projet OpenCode complet pour **un seul livre par exécution**. Il génère les fichiers de projet et ne rédige pas automatiquement le livre lors de l'initialisation.

## Plateformes
- `generate.sh` : Linux/macOS.
- `generate.bat` : Windows CMD.
- `generate.ps1` : Windows PowerShell.
- Logique métier commune en Python pour éviter trois implémentations divergentes.

## Questionnaire éditorial
- Titre, sous-titre facultatif, auteur/pseudonyme, description détaillée.
- Type de livre avec suggestions et valeur personnalisée.
- Public cible avec suggestions et valeur personnalisée.
- Langue initiale, nombre approximatif de pages, niveau initial/final, polices, contraintes.
- Dispositifs pédagogiques multi-sélection : QCM et corrections, exercices et corrections, aucun.
- Affichage du code : aucun, monochrome, coloration, numéros de ligne, sorties, commentaires de résultats, commandes/sorties/erreurs.
- Recherche autonome ou recherche Web avec registre de sources et vérification factuelle.
- Mode de workflow : enchaînement, reprise après erreur, arrêt par étape, personnalisé.
- Validation de chapitre : automatique, manuelle ou automatique puis manuelle.
- Formats de publication et mise en page.
- Dimensions par format physique; marges recherchées dans les sources officielles ou saisies manuellement.
- Types d'illustrations et mode de préparation IA (prompt uniquement) ou image fournie par l'utilisateur.
- Initialisation Git et commit initial optionnels.
- Nom et dossier du projet.
- Tous les champs éditoriaux sont posés à chaque exécution; les suggestions ne sont pas des choix imposés.

## Formats
PDF impression, PDF écran, KDP broché, KDP broché + Kindle numérique, EPUB, Etsy impression, Etsy impression + écran. Les sorties identiques peuvent être dédupliquées si leurs spécifications concordent. Kindle numérique et EPUB sont traités comme formats distincts. La couverture est spécifiée séparément par format.

## Langues et illustrations
- Chaque langue possède `SUMMARY.md`, chapitres, manuscrit assemblé, couverture, quatrième, sorties et catalogue d'illustrations.
- Création de langue : préparation uniquement, sans traduction ni production automatique.
- Commandes distinctes pour traduire sommaire, chapitre unique, plage, tous les chapitres, quatrième de couverture, catalogue et prompts; commande globale facultative pour tous les éléments.
- Commandes distinctes pour assembler puis construire les livrables de la langue.
- Une image distincte par langue, ID stable entre les langues, fichier et chemin propres à chaque langue.
- Marqueurs `{{ILL:ILL-CH003-001}}`; catalogue Markdown avec ID, symbole, légende, description, prompt, chemin, mode et statut.
- Si un utilisateur fournit une image, ne jamais l'écraser. Ne créer un PNG vide que si le fichier n'existe pas et le marquer explicitement comme vide.
- Moteur d'images désactivé : préparation de catalogue, prompt et chemin uniquement.

## Exécution du code
Exécution isolée contrôlée avec délai, sortie plafonnée, répertoire temporaire et environnement réduit. Résultats présentés comme réels uniquement si le processus a effectivement été exécuté. L'exécuteur standard n'est pas une sandbox forte; le code non fiable requiert VM/conteneur sans réseau et sans secrets.

## Protection des données
- Refus d'écrire dans un dossier cible non vide sans confirmation explicite/option `--force`.
- Aucun effacement récursif du dossier cible.
- Les fichiers existants ne sont jamais écrasés par défaut.
- Pas de secrets ou clés API dans les fichiers générés.
- État de progression, journaux, décisions et rapports vérifiables.

## Qualité et limites
- Le volume de pages est indicatif; aucune génération de remplissage pour atteindre le nombre exact.
- Contrôles de fichiers, marqueurs, catalogues, images manquantes, langues, formats, métadonnées et dépendances.
- Recherche des spécifications officielles au moment du contrôle; date et URL consignées.
- Ne jamais prétendre à une acceptation de plateforme ou à une vérification non effectuée.


## Brief éditorial avant rédaction (historique 1.1.0, remplacé en 1.2.0)
Dans la version 1.1.0, le brief contenait à tort des explications détaillées et des corrigés attendus. Cette conception est remplacée en 1.2.0 : le brief est synthétique, le chapitre est le contenu final et les corrigés ne figurent pas dans le brief.

## Corrections éditoriales et multiplateformes (version 1.2.0)
- Le brief est un plan synthétique intermédiaire : points à aborder sans paragraphes finaux; visuels nécessaires selon la configuration avec identifiants et légendes; exercices avec énoncé, objectif et consignes, sans correction ni solution.
- Le chapitre est le contenu final rédigé dans la langue prévue; chaque point est développé en explications substantielles, exemples, transitions et structure éditoriale adaptée.
- Pour les sujets techniques/scientifiques, ajouter si cela aide une explication imagée ou une analogie liée au point, signalée par `💡 Explication imagée`.
- Une commande IA de validation et une action CLI d'approbation explicite contrôlent le brief avant rédaction; le script ne doit pas approuver automatiquement.
- Le validateur signale les chapitres trop courts et ceux sans paragraphes de prose afin de détecter un plan déguisé en chapitre.
- Chaque projet généré embarque les scripts de virtualenv, d'installation et d'exécution Python SH/BAT/PS1, `requirements.txt`, et des scripts d'appel OpenCode.
- Le README du projet généré décrit le questionnaire, les commandes OpenCode, les scripts et les étapes de production jusqu'au contrôle de publication.
