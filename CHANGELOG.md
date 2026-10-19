# Journal des modifications

## 1.1.0
- Ajout des briefs détaillés de chapitres, générés avant la rédaction finale.
- Ajout des commandes `/book-chapter-brief` et `/book-chapter-brief-edit` et de leurs variantes `scriptable-`.
- Les commandes de rédaction d’un chapitre, d’une plage et du livre entier exigent désormais des briefs marqués `APPROVED`.
- Ajout du modèle complet de brief et de `scripts/chapter_briefs.py` pour initialiser, lister et valider la structure sans écraser les fichiers existants.
- Ajout de tests d’intégration pour les briefs et leur protection contre l’écrasement.

# Changelog

## 1.0.0

- Générateur interactif multiplateforme SH/BAT/PS1 avec questionnaire sans réponses éditoriales présélectionnées.
- Projets OpenCode complets avec commandes, agents, skills, documentation et scripts.
- Préparation multilingue explicite, catalogue et chemins d'images distincts par langue.
- Scripts de validation, assemblage, compilation PDF/EPUB, suivi et préparation d'illustrations.
- Exécution de code fail-closed nécessitant Docker sans réseau ou bubblewrap Linux.
- Tests unitaires et tests d'intégration.
