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


## Tests historiques de 1.1.0 (attentes remplacées en 1.2.0)
- Vérifier que chaque langue possède `chapter-briefs/README.md` et `INDEX.md`.
- Ancienne attente : le brief contenait le plan détaillé et les corrigés attendus. Remplacée en 1.2.0 par un brief synthétique sans corrections.
- Vérifier les commandes normales et `scriptable-` de création/modification de briefs.
- Vérifier que `/book-chapter`, `/book-range` et `/book-all` interdisent la rédaction sans brief APPROVED.
- Créer un brief avec `scripts/chapter_briefs.py --action init`, lister les statuts et valider la structure.
- Confirmer que l'initialisation refuse d'écraser un brief existant et inscrit le nouveau brief dans l'index.
- Créer un chapitre sans brief APPROVED et vérifier que le validateur signale un blocage.
- Tester la traduction des briefs individuels et en lot vers une langue distincte.

## Tests ajoutés en 1.2.0
- Le brief est synthétique et ne demande pas de corrigé d'exercice.
- Les commandes de rédaction exigent `APPROVED` et prescrivent un chapitre final développé, non une reprise des puces.
- Le script de briefs refuse l'approbation sans `--confirm-approval`, contrôle les placeholders et met à jour l'index.
- Le validateur signale les chapitres trop courts ou sans prose; l’assembleur bloque les chapitres uniquement constitués de titres/puces.
- Le projet généré embarque `setup_venv`, `install`, `run_python`, `requirements.txt` et les wrappers OpenCode en SH/BAT/PS1.
- Le README généré décrit le parcours jusqu'à l'assemblage, la compilation et le contrôle.
- Les scripts Python générés sont compilés avec `py_compile`; les scripts shell sont contrôlés avec `bash -n`. Les scripts Windows/macOS restent à exécuter nativement sur leurs plateformes respectives avant de déclarer ces plateformes testées.
