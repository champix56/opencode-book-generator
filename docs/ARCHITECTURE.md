# Architecture du générateur

## Séparation des responsabilités

- `generators/bookgen.py` : questionnaire et création déterministe du projet.
- `generate.sh`, `generate.bat`, `generate.ps1` : points d'entrée natifs; toute la logique est partagée par Python.
- `.opencode/commands/` dans le projet généré : prompts éditoriaux exécutés par OpenCode.
- `scriptable-*` : prompts dédiés à l'automatisation; `scripts/invoke_command.py` les transmet à `opencode run` et propose un `--dry-run`.
- `scripts/validate_project.py` : contrôles statiques, catalogues et marqueurs.
- `scripts/prepare_illustration.py` : enregistrement d'une illustration et création éventuelle d'un fichier vide explicitement signalé.
- `scripts/assemble.py` : assemblage de chapitres et résolution des marqueurs sans masquer les images absentes.
- `scripts/build.py` : compilation PDF/EPUB avec Pandoc, profils de format dédupliqués quand taille et marges sont identiques; refuse les spécifications non résolues et les écrasements.
- `scripts/safe_exec.py` : exécution de code uniquement dans Docker sans réseau ou bubblewrap Linux; échec fermé si aucune isolation n'est disponible.
- `tests/` : tests unitaires du générateur et tests d'intégration de la structure générée.

## État et reprise

Les décisions sont conservées dans `docs/DECISIONS.md`, l'état dans `docs/PROGRESS.md`, et les fichiers JSON sous `state/` peuvent être enrichis par les commandes IA. Les scripts déterministes ne prétendent pas qu'une étape éditoriale est achevée uniquement parce qu'un fichier existe.

## Limites

Le générateur ne crée pas le contenu complet du livre à l'initialisation. OpenCode réalise les tâches éditoriales sur commande. Les images ne sont jamais générées. Les builds ne valident pas l'acceptation des plateformes. Les tests Windows nécessitent une exécution native Windows.


## Planification détaillée des chapitres
Le plan de haut niveau (`SUMMARY.md`) est distinct des briefs de chapitre (`languages/<lang>/chapter-briefs/CHxxx.md`), eux-mêmes distincts du texte final (`chapters/CHxxx.md`). Le brief doit être explicitement approuvé avant rédaction. La commande IA gère le contenu éditorial et les opérations d’édition; `scripts/chapter_briefs.py` réalise les opérations déterministes de création de modèle, de liste et de contrôle structurel.
