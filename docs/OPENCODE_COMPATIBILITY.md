# Compatibilité OpenCode

## Commandes personnalisées

Les commandes sont des fichiers Markdown dans `.opencode/commands/`, conformément à la documentation OpenCode consultée le 19 octobre 2026 : https://opencode.ai/docs/commands/ et https://opencode.ai/docs/config/.

Structure utilisée :

```markdown
---
description: Description courte
---

Prompt avec `$ARGUMENTS`.
```

Le nom du fichier devient le nom de commande. Les commandes `scriptable-*` sont également des commandes OpenCode, et non des scripts shell autonomes.

## Appels depuis un script

Le projet fournit des wrappers `scripts/platform/run-opencode.*` qui délèguent à `opencode run`. La syntaxe CLI et la disponibilité des modes d'exécution peuvent évoluer; le wrapper reste volontairement simple et transmet les arguments au CLI installé. Avant d'orchestrer une production non supervisée, exécuter `opencode --help` et `opencode run --help` avec la version installée et vérifier la syntaxe d'arguments. Ne pas supposer qu'une commande interactive est non interactive si elle pose des questions.

## Pas de modèle imposé

Aucun modèle ni fournisseur payant n'est inscrit dans la configuration. L'utilisateur choisit et configure ses fournisseurs/modèles OpenCode selon son environnement et ses contraintes de coût.
