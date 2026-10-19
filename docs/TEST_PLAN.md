# Plan de tests et critères d'acceptation

1. Génération interactive sur Linux avec dossier cible absent.
2. Refus sans modification si le dossier cible contient déjà un fichier.
3. Mode non interactif avec fichier de configuration complet.
4. Valeurs éditoriales personnalisées conservées dans `config/generator-input.json`.
5. Présence de commandes natives et `scriptable-*` dans `.opencode/commands/`.
6. Création d'une nouvelle langue par commande sans contenu traduit automatiquement.
7. Catalogue propre à chaque langue et chemins image contenant le code langue.
8. Détection d'ID d'illustration dupliqué et de marqueur non résolu.
9. Assembleur refuse d'écraser un manuscrit déjà existant.
10. Construction signale clairement l'absence de Pandoc/XeLaTeX.
11. Exécuteur : refuse shell par défaut, timeout limité, erreur rapportée honnêtement.
12. Git facultatif; si demandé et disponible, initialisation et commit selon choix.
13. Wrappers Windows relaient code retour Python; tests de syntaxe PowerShell/CMD à exécuter sur Windows réel.
14. Les formats ebook/EPUB ne sont pas présentés comme une édition papier.
15. Le rapport ne promet pas l'acceptation KDP/Etsy.

Les tests automatisés présents couvrent les comportements testables dans l'environnement de construction. Les tests natifs Windows nécessitent une machine Windows; ils ne sont pas prétendus exécutés sous Linux.


## Tests ajoutés en 1.1.0 : briefs détaillés
- Vérifier que chaque langue possède `chapter-briefs/README.md` et `INDEX.md`.
- Vérifier que le modèle de brief couvre plan de contenu, exercices, énoncés, critères et corrigés attendus.
- Vérifier les commandes normales et `scriptable-` de création/modification de briefs.
- Vérifier que `/book-chapter`, `/book-range` et `/book-all` interdisent la rédaction sans brief APPROVED.
- Créer un brief avec `scripts/chapter_briefs.py --action init`, lister les statuts et valider la structure.
- Confirmer que l'initialisation refuse d'écraser un brief existant et inscrit le nouveau brief dans l'index.
- Créer un chapitre sans brief APPROVED et vérifier que le validateur signale un blocage.
- Tester la traduction des briefs individuels et en lot vers une langue distincte.
