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


## Séparation du sommaire, du brief et du chapitre
Le plan de haut niveau (`languages/<lang>/SUMMARY.md`) est distinct des briefs (`languages/<lang>/chapter-briefs/CHxxx.md`), eux-mêmes distincts du chapitre final (`languages/<lang>/chapters/CHxxx.md`). Le brief doit être explicitement approuvé avant rédaction. La commande IA gère le contenu éditorial et les opérations d’édition; `scripts/chapter_briefs.py` crée les modèles, liste les statuts, vérifie la structure et effectue une approbation CLI explicite.

## Version 1.2.0 : séparation brief/chapitre
Le brief est un plan synthétique et ne contient ni prose finale ni corrections d'exercices. Il référence les visuels prévus avec légendes et les exercices avec énoncé et but. La rédaction doit développer chaque point en texte substantiel dans la langue du projet. Le repère `💡 Explication imagée` signale les analogies pédagogiques utiles. Le script `chapter_briefs.py` distingue l'initialisation, la liste, la validation structurelle et l'approbation explicitement confirmée.

Chaque projet généré embarque `setup_venv`, `install` et `run_python` en SH/BAT/PS1. Les scripts d'exécution activent le virtualenv avant de lancer Python. `requirements.txt` liste les dépendances Python; Pandoc et XeLaTeX restent des dépendances système.
