# OpenCode Book Project Generator

**Version 1.2.0** · Générateur multiplateforme de projets éditoriaux OpenCode, un livre par exécution.

## Changements importants en 1.2.0

- Le brief est maintenant un **plan synthétique** : points à aborder, visuels avec légendes, exercices avec énoncé et objectif, sans rédaction finale ni correction.
- Le chapitre doit être un **contenu final substantiel** : explications complètes, exemples, transitions et pédagogie adaptée au public et à la langue.
- Les notions techniques/scientifiques peuvent inclure des analogies pertinentes, signalées par `💡 Explication imagée`.
- Le script de briefs propose `--action approve --chapter CH001 --confirm-approval`, avec contrôles préalables et mise à jour de l'index.
- Les projets générés contiennent des scripts d'installation et d'exécution Python pour Linux/macOS, Windows CMD et PowerShell.
- Le README de chaque projet généré comprend un tutoriel de bout en bout jusqu'à la compilation et au contrôle des livrables.

## Contenu du générateur

- `generate.sh` : lancement sous Linux/macOS.
- `generate.bat` : lancement sous Windows CMD.
- `generate.ps1` : lancement sous PowerShell.
- `generators/bookgen.py` : questionnaire, configuration et génération des projets.
- `tests/test_generator.py` : tests unitaires et d'intégration.
- `docs/CAHIER_DES_CHARGES.md` : périmètre fonctionnel.
- `docs/ARCHITECTURE.md` : architecture des projets générés.
- `docs/OPENCODE_COMPATIBILITY.md` : conventions de commandes OpenCode.
- `docs/TEST_PLAN.md` : plan de vérification.
- `CHANGELOG.md` : historique des versions.

## Prérequis

- Python 3.10 ou plus récent pour le générateur.
- OpenCode pour les tâches éditoriales assistées par IA.
- Pandoc pour les conversions PDF/EPUB.
- XeLaTeX ou une distribution LaTeX adaptée pour la sortie PDF.
- Git facultatif.

Le générateur lui-même n'a pas de dépendances Python externes. Les projets générés incluent néanmoins `scripts/requirements.txt` et les scripts de création/activation de l'environnement virtuel, pour installer proprement les dépendances Python futures. Pandoc et LaTeX sont des outils système, non des paquets pip.

## Lancer le questionnaire initial

Depuis le dossier du générateur :

Linux/macOS :
```sh
chmod +x generate.sh
./generate.sh
```

Windows CMD :
```bat
generate.bat
```

PowerShell :
```powershell
.\generate.ps1
```

Le questionnaire demande les informations éditoriales et techniques : titre, sous-titre, auteur, description, type de livre, public, langue, volume, niveaux, polices, contraintes, dispositifs pédagogiques, affichage du code, formats, dimensions, marges, mise en page, mode de recherche, workflow, validation, illustrations, Git et chemin du projet. Les suggestions ne sont pas des choix imposés : les champs libres et valeurs personnalisées restent disponibles.

Le générateur refuse un dossier cible non vide sans `--force`. `--force` autorise le remplacement des fichiers générés portant les mêmes chemins, sans effacer les autres fichiers. Sauvegarde avant toute utilisation.

Mode automatisé :
```sh
python3 generators/bookgen.py --non-interactive-config chemin/config.json --output /chemin/du/projet
```

## Réponses à fournir au questionnaire initial

Le questionnaire de `generate.sh`, `generate.bat` ou `generate.ps1` est interactif. Il n'existe pas de thème ou de contenu éditorial présélectionné. Prépare les informations suivantes avant de le lancer; les exemples ci-dessous sont illustratifs et doivent être adaptés à ton livre.

1. **Titre** : titre principal du livre, obligatoire.
2. **Sous-titre** : facultatif; appuie sur Entrée si tu n'en veux pas.
3. **Auteur/pseudonyme** : nom affiché dans le livre, obligatoire.
4. **Description détaillée** : but, sujets couverts, promesse éditoriale et contenu attendu.
5. **Type de livre** : choisis un profil proposé ou saisis une valeur personnalisée.
6. **Public cible** : niveau et lectorat visé; valeur personnalisée possible.
7. **Langue initiale** : code de langue, par exemple `fr-FR`, `en-US` ou `es-ES`.
8. **Nombre approximatif de pages** : estimation, pas une garantie de pagination.
9. **Niveau technique initial et final** : nombres de 0 à 100 qui indiquent la progression souhaitée.
10. **Polices** : famille(s) souhaitée(s), ou `choix automatique`.
11. **Contraintes éditoriales** : règles de ton, longueur, sujets à éviter, sources ou normes; écris `aucune` si tu n'en as pas.
12. **Dispositifs pédagogiques** : sélection multiple par numéros séparés par des virgules; `0` signifie aucun. Les options comprennent QCM, exercices et différents emplacements de corrections.
13. **Présentation du code** : demandé pour les livres techniques ou si tu réponds oui à la question sur le code; choisis les styles de code voulus.
14. **Formats de publication** : sélection multiple. Les formats imprimables demandent ensuite dimensions et marges pour chaque profil; choisis la recherche des spécifications officielles ou saisis des marges manuelles avec unités (`mm`, `cm`, `in` ou `pt`).
15. **Mise en page** : Markdown seul, LaTeX ou Markdown + Pandoc + LaTeX.
16. **Recherche documentaire** : mode autonome ou recherche Web avec sources et vérification.
17. **Mode de workflow** : enchaînement, reprise après erreur, arrêt par étape ou personnalisé.
18. **Validation des chapitres** : automatique, manuelle ou automatique puis manuelle.
19. **Illustrations** : sélectionne les types utiles ou `aucune`. Pour chaque type, choisis la préparation d'un prompt IA ou l'utilisation d'une image fournie. Le questionnaire ne lance pas de moteur d'images.
20. **Git** : indique si tu veux initialiser un dépôt, puis éventuellement un commit initial.
21. **Dossier parent et nom du projet** : chemin absolu de destination, puis nom du dossier. Le générateur refuse d'écraser un dossier non vide sans `--force`.

Pour les sélections multiples, saisis les numéros séparés par des virgules, par exemple `1,3`. Pour aucun choix, saisis `0`. Les valeurs personnalisées peuvent être saisies quand le questionnaire propose l'option personnalisée ou accepte du texte libre. Les réponses sont enregistrées dans `config/generator-input.json` du projet généré.

## Tutoriel d'usage complet pour un livre généré

Les commandes OpenCode se lancent dans la conversation OpenCode sous la forme `/nom-de-commande`. Les scripts Python se lancent dans le terminal depuis la racine du projet généré, de préférence via `scripts/run_python.*` pour activer le virtualenv.

### 1. Installer l'environnement du projet généré

Linux/macOS :
```sh
sh scripts/setup_venv.sh
sh scripts/install.sh
```
Windows CMD :
```bat
call scripts\setup_venv.bat
call scripts\install.bat
```
PowerShell :
```powershell
.\scripts\setup_venv.ps1
.\scripts\install.ps1
```

Les scripts créent `.venv`, activent l'environnement pendant l'installation, puis installent `scripts/requirements.txt`. Si une future dépendance est ajoutée, elle doit être déclarée dans ce fichier. Sur Windows, si PowerShell bloque les scripts, autorise-les pour la session courante uniquement avec `Set-ExecutionPolicy -Scope Process Bypass` puis relance la commande.

### 2. Démarrer OpenCode et planifier

Dans la racine du livre :
```sh
opencode
```

Puis dans OpenCode :
```text
/book-plan
/book-summary
```

Vérifie le plan, l'ordre, le nombre de chapitres, le public, le niveau et les objectifs. Les chapitres doivent avoir des identifiants stables comme `CH001`, `CH002`, etc.

### 3. Créer, modifier, valider et approuver les briefs

Pour chaque chapitre :
```text
/book-chapter-brief CH001
/book-chapter-brief-edit CH001 ajouter un point sur ...
/book-chapter-brief-validate CH001
```

Le brief est synthétique. Il liste les points à développer, les illustrations/schémas/tableaux utiles avec légendes, et les exercices avec énoncé, objectif et consignes. Il ne contient ni explications finales ni corrigés.

Contrôle technique des briefs :
```sh
sh scripts/run_python.sh scripts/chapter_briefs.py --root . --lang fr-FR --action list
sh scripts/run_python.sh scripts/chapter_briefs.py --root . --lang fr-FR --action validate
```

Créer un modèle si nécessaire :
```sh
sh scripts/run_python.sh scripts/chapter_briefs.py --root . --lang fr-FR --action init --chapter CH001
```

Après vérification humaine et accord explicite, l'approbation scriptable s'effectue ainsi :
```sh
sh scripts/run_python.sh scripts/chapter_briefs.py --root . --lang fr-FR --action approve --chapter CH001 --confirm-approval
```

Le script refuse l'approbation si les sections sont absentes, si des placeholders restent à renseigner ou si des cases de contrôle restent décochées. Il ne prouve pas la qualité éditoriale : cette décision doit être humaine. Sous Windows CMD, remplace la forme `sh scripts/run_python.sh` par `call scripts\run_python.bat` suivi des mêmes arguments. Sous PowerShell, utilise `./scripts/run_python.ps1` suivi des mêmes arguments.

### 4. Rédiger et relire les chapitres

Pour un chapitre :
```text
/book-chapter CH001
/book-review CH001
```

Pour une plage ou tous les chapitres :
```text
/book-range CH002-CH005
/book-all
/book-review-all
```

Un brief `APPROVED` est une condition préalable, pas le contenu final. Chaque point doit être développé en paragraphes explicatifs substantiels dans la langue du livre. Ajouter des définitions, exemples et transitions. Pour les sujets techniques/scientifiques, les analogies utiles sont signalées par `💡 Explication imagée`. Insérer ou référencer les visuels prévus. Les exercices doivent inclure leur énoncé et leur but; les corrections suivent le dispositif pédagogique configuré et ne sont pas ajoutées arbitrairement au chapitre.

### 5. Préparer illustrations et couvertures

Dans OpenCode :
```text
/book-cover-text
/book-cover
```

Le moteur d'images est désactivé. Les prompts, descriptions et chemins ne sont pas des images générées. Il faut créer ou fournir les fichiers avec un outil externe, puis vérifier leurs chemins, légendes et dimensions. Les placeholders vides ne sont pas publiables.

### 6. Ajouter une langue (facultatif)

```text
/book-language-create es-ES
/book-translate-chapter-briefs vers es-ES
/book-language-all es-ES
/book-language-assemble es-ES
/book-language-build es-ES
```

La création de langue prépare uniquement les dossiers. Les traductions doivent être explicitement demandées, vérifiées et approuvées. Les images possèdent des fichiers distincts par langue.

### 7. Vérifier le projet avant assemblage

```sh
sh scripts/run_python.sh scripts/validate_project.py --root .
sh scripts/run_python.sh scripts/status.py --root .
```

Corrige les erreurs et examine les avertissements sur les images, placeholders, marqueurs non résolus et éléments manquants. `/book-check` peut également effectuer un contrôle éditorial assisté par IA.

### 8. Assembler le manuscrit

Linux/macOS :
```sh
sh scripts/run_python.sh scripts/assemble.py --root . --lang fr-FR
```

Windows CMD :
```bat
call scripts\run_python.bat scripts\assemble.py --root . --lang fr-FR
```

PowerShell :
```powershell
.\scripts\run_python.ps1 scripts\assemble.py --root . --lang fr-FR
```

Sortie attendue : `languages/fr-FR/manuscript/MANUSCRIPT.md`. L'assembleur refuse d'écraser un fichier existant et bloque les chapitres sans paragraphe de prose. Archive ou renomme le manuscrit avant un nouvel assemblage.

### 9. Compiler les formats

Tous les formats PDF/EPUB pris en charge et activés dans la configuration :
```sh
sh scripts/run_python.sh scripts/build.py --root . --lang fr-FR --format all
```

PDF uniquement : `--format pdf`. EPUB uniquement : `--format epub`. Pandoc est nécessaire; XeLaTeX est requis pour les PDF. Les spécifications de marges non résolues bloquent les profils correspondants. La couverture et les images ne sont pas créées par le compilateur.

### 10. Vérifier le livrable et préparer la publication

```sh
sh scripts/run_python.sh scripts/validate_project.py --root .
sh scripts/run_python.sh scripts/status.py --root .
```

Inspecte `languages/fr-FR/output/BUILD_REPORT.json`, les fichiers réellement créés, la pagination, les polices, les illustrations, les couvertures et les exigences officielles à jour de la plateforme. Une compilation réussie ne garantit pas l'acceptation KDP/Etsy.

## Inventaire des scripts du projet généré

- `scripts/chapter_briefs.py` : initialisation, liste, validation structurelle et approbation explicite des briefs.
- `scripts/validate_project.py` : validation de la structure, des briefs et du catalogue d'illustrations.
- `scripts/status.py` : état factuel du projet.
- `scripts/assemble.py` : assemblage du manuscrit et résolution des marqueurs d'illustration.
- `scripts/build.py` : compilation PDF/EPUB et rapport `BUILD_REPORT.json`.
- `scripts/prepare_illustration.py` : entrée de catalogue et chemin cible, sans génération d'image.
- `scripts/invoke_command.py` : appel des commandes OpenCode `scriptable-*`, avec `--dry-run`.
- `scripts/safe_exec.py` : exécution de code contrôlée si un runtime d'isolation est disponible.
- `scripts/setup_venv.sh`, `.bat`, `.ps1` : création de l'environnement virtuel.
- `scripts/install.sh`, `.bat`, `.ps1` : installation des dépendances Python.
- `scripts/run_python.sh`, `.bat`, `.ps1` : activation de l'environnement et exécution d'un script Python.
- `scripts/platform/run-opencode.sh`, `.bat`, `.ps1` : appel à `opencode run`.

## Tests du générateur

Depuis la racine de l'archive du générateur :
```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile generators/bookgen.py tests/test_generator.py
bash -n generate.sh
```

## Limites

Les images ne sont pas générées automatiquement. Pandoc/XeLaTeX sont des dépendances système. Les scripts Windows/macOS doivent être testés sur leurs systèmes natifs avant de déclarer une validation multiplateforme complète. Les exigences officielles de publication doivent être vérifiées au moment de la production.
