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


## Brief éditorial détaillé obligatoire avant rédaction (version 1.1.0)
- Chaque langue dispose de `chapter-briefs/INDEX.md` et d’un fichier par chapitre.
- `/book-chapter-brief` prépare le contenu détaillé sans rédiger le chapitre final.
- `/book-chapter-brief-edit` prend en charge ajout, correction, remplacement, déplacement, suppression et validation explicite.
- Le brief couvre objectifs, prérequis, sous-sections, notions, explications, exemples, exercices avec énoncé complet, consignes, critères de réussite, corrigés attendus, illustrations, sources et transitions.
- Le chapitre ne peut être rédigé que si le brief porte `APPROVED`. Les commandes de plage et de livre entier doivent bloquer ou signaler les chapitres non approuvés.
- `scripts/chapter_briefs.py` permet l’initialisation d’un modèle, la liste des statuts et la validation structurelle; il refuse d’écraser un brief existant.
