# OpenCode Book Project Generator

**Version 1.0.0** · Générateur interactif multiplateforme pour créer un projet éditorial OpenCode complet, un livre par exécution.

## Ce que le générateur produit

- Configuration éditoriale et technique, décisions, glossaire, références, suivi de progression et prompts de travail.
- Commandes OpenCode natives dans `.opencode/commands/` et versions `scriptable-` prévues pour être appelées par `opencode run`.
- Scripts déterministes de validation, assemblage, état et compilation, ainsi qu'un exécuteur de code contrôlé.
- Arborescence dédiée à chaque langue, catalogue d'illustrations et spécifications de couverture par format.
- Options de publication, formats et dimensions configurables, marges officielles à vérifier ou marges manuelles.
- Git optionnel, avec commit initial optionnel.

## Prérequis

- Python 3.10+ recommandé, sans dépendance Python externe pour générer le projet.
- OpenCode pour utiliser les commandes IA.
- Pour construire des livrables : Pandoc et les moteurs nécessaires (par exemple XeLaTeX pour PDF). Ces outils sont optionnels tant que vous ne lancez pas la compilation.
- Git facultatif.

## Lancer le questionnaire

Linux/macOS :

```sh
chmod +x generate.sh
./generate.sh
```

Windows CMD :

```bat
generate.bat
```

Windows PowerShell :

```powershell
.\generate.ps1
```

Le questionnaire demande tous les paramètres éditoriaux. Les propositions sont des options de confort, jamais des réponses imposées. Pour les choix multiples, utilisez des numéros séparés par des virgules; `0` signifie aucun et `texte:ma valeur` ajoute une option personnalisée. Les champs libres acceptent les valeurs définies par l'utilisateur.

Le générateur refuse un dossier cible non vide. `--force` autorise l'écriture des fichiers portant les mêmes chemins, sans effacer les autres fichiers; utilisez-le seulement après sauvegarde.

## Mode automatisé

Pour les tests et les chaînes d'automatisation, fournissez un JSON complet au format attendu :

```sh
python3 generators/bookgen.py --non-interactive-config chemin/config.json --output /chemin/du/projet
```

La configuration peut être exportée depuis un projet généré : `config/generator-input.json`. Pour un nouvel appel non interactif, ajustez `project_parent` et `project_name` dans la copie fournie.

## Workflow du livre

1. `opencode` dans le dossier du livre.
2. `/book-plan`, puis `/book-summary`.
3. `/book-chapter CH001`, `/book-review CH001`, puis `/book-range CH002-CH005` ou `/book-all`.
4. `/book-review-all`, `/book-assemble fr-FR`, `/book-cover-text`, `/book-cover`, `/book-check`.
5. Scripts déterministes : `python scripts/validate_project.py --root .`, `python scripts/status.py --root .`, `python scripts/assemble.py --root . --lang fr-FR`, `python scripts/build.py --root . --lang fr-FR --format all`.

## Nouvelle langue : préparation puis traduction explicite

`/book-language-create es-ES` prépare tous les dossiers et fichiers pour la langue cible, mais ne traduit ni ne génère le livre. Ensuite, au choix :

- `/book-translate SUMMARY.md vers es-ES`
- `/book-language-chapter CH001 vers es-ES`
- `/book-language-range CH001-CH005 vers es-ES`
- `/book-language-all es-ES`
- `/book-translate-all es-ES` pour sommaire, chapitres, quatrième, catalogue, descriptions et prompts
- `/book-language-assemble es-ES`
- `/book-language-build es-ES`

Chaque langue a son catalogue et ses propres images. Les IDs d'illustration restent stables, mais les fichiers images portent le code langue. Le moteur d'images est volontairement inactif : prompts et chemins sont préparés, rien n'est présenté comme généré.

## Commandes OpenCode et compatibilité

Les commandes personnalisées Markdown sont placées dans `.opencode/commands/`, chemin reconnu par la documentation OpenCode. Les commandes utilisent le frontmatter `description` et le corps du fichier comme prompt; `$ARGUMENTS` est l'espace réservé des arguments. Vérifiez la version installée avant d'automatiser les appels CLI. Voir `docs/OPENCODE_COMPATIBILITY.md`.

## Exécution de code : avertissement de sécurité

`scripts/safe_exec.py` exige Docker avec réseau désactivé et limites de ressources, ou bubblewrap sous Linux. Si aucun runtime d'isolation n'est disponible, il refuse d'exécuter le code. Le shell est désactivé par défaut. Pour du code réellement hostile, privilégier une VM/conteneur administré, sans secrets et sans réseau.

## Limites de publication

La compilation locale ne garantit pas l'acceptation Amazon KDP ou Etsy. Les spécifications de marges, fonds perdus, dos, résolution et couverture doivent être vérifiées sur les pages officielles au moment de la production. Si la vérification échoue, le rapport doit afficher « non vérifié » plutôt que d'inventer des exigences.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

### Préparer une entrée d'illustration manuellement

Pour enregistrer une image fournie par l'utilisateur sans écraser un fichier existant :

```sh
python scripts/prepare_illustration.py --root . --lang fr-FR --id ILL-CH001-001 --filename ILL-CH001-001-fr-FR.png --mode user_provided --caption "Légende" --description "Description"
```

Cette commande ajoute une ligne au catalogue. Si le PNG n'existe pas, elle crée un fichier vide explicitement marqué `PLACEHOLDER_EMPTY`; ce n'est pas une image publiable. Un ID déjà présent est refusé. Pour préparer un prompt IA, utilisez `--mode ai_prompt --prompt "description du prompt"`, sans lancer de moteur d'image.

### Appeler une commande depuis un script

```sh
python scripts/invoke_command.py scriptable-book-plan --root . --args "plan initial"
```

Le script lit le prompt Markdown de la commande et le transmet à `opencode run`. `--dry-run` affiche le prompt sans appel au modèle. Les appels automatisés doivent être supervisés et testés avec la version OpenCode installée.
