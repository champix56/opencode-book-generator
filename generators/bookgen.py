#!/usr/bin/env python3
"""Interactive, cross-platform generator for one complete OpenCode book project."""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys, textwrap, unicodedata
from pathlib import Path
from datetime import datetime, timezone

VERSION = "1.1.0"
FORMATS = [
    ("pdf_print", "PDF impression uniquement"), ("pdf_print_screen", "PDF impression + écran"),
    ("kdp_print", "Amazon KDP broché uniquement"), ("kdp_ebook", "Amazon KDP broché + Kindle numérique"),
    ("epub", "EPUB"), ("etsy_print", "Etsy impression (si différent des formats déjà générés)"),
    ("etsy_both", "Etsy impression + écran (si différent des formats déjà générés)")]
LEARN = [
    ("qcm_chapter_next", "QCM en fin de chapitre, corrections expliquées à la page suivante"),
    ("qcm_book_end", "QCM en fin de chapitre, corrections expliquées dans une section finale ajoutée au sommaire"),
    ("exercises_end", "Exercices dans les chapitres, corrections en fin de livre"),
    ("exercises_inline", "Exercices dans les chapitres, corrections expliquées juste après"),
    ("none", "Aucun")]
ILLUSTRATIONS = [
    ("chapter_opening", "Une image de titre distincte au début de chaque chapitre"),
    ("chapter_ending", "Un dessin commun à la fin de chaque chapitre"),
    ("explanatory_auto", "Illustrations explicatives proposées automatiquement par l'IA"),
    ("explanatory_ask", "Illustrations explicatives proposées par l'IA, avec validation utilisateur à chaque fois"),
    ("none", "Aucune illustration")]
BOOK_TYPES = ["Technique / informatique", "Scientifique", "Roman", "Romance", "Fantasy / science-fiction", "Histoire", "Guide pratique", "Cahier d'exercices", "Cuisine", "Santé / bien-être", "Jeunesse", "Coloriage", "Essai"]
AUDIENCES = ["Débutant", "Intermédiaire", "Avancé", "Grand public", "Enfants", "Adolescents", "Adultes", "Professionnels", "Universitaire"]

class UserAbort(Exception): pass

def ask(label, default=None, required=False):
    suffix = f" [{default}]" if default not in (None, "") else ""
    while True:
        v = input(f"{label}{suffix} : ").strip()
        if not v and default is not None: v = str(default)
        if v or not required: return v
        print("Cette valeur est obligatoire.")

def ask_yes_no(label):
    while True:
        v = input(f"{label} (o/n) : ").strip().lower()
        if v in ("o", "oui", "y", "yes"): return True
        if v in ("n", "non", "no"): return False
        print("Répondez par oui ou non.")

def ask_int(label, low=1, high=100000):
    while True:
        raw=ask(label, required=True)
        try: v=int(raw)
        except ValueError: print("Entrez un nombre entier."); continue
        if low <= v <= high: return v
        print(f"La valeur doit être comprise entre {low} et {high}.")

def ask_choice(label, options, allow_custom=True):
    print(f"\n{label}")
    for i, op in enumerate(options, 1): print(f"  {i}. {op}")
    if allow_custom: print(f"  {len(options)+1}. Personnalisé")
    while True:
        raw=ask("Choix", required=True)
        if raw.isdigit() and 1 <= int(raw) <= len(options): return options[int(raw)-1]
        if allow_custom and raw.isdigit() and int(raw)==len(options)+1: return ask("Valeur personnalisée", required=True)
        if allow_custom and not raw.isdigit() and raw: return raw
        print("Choix invalide.")

def ask_multi(label, options, allow_custom=True):
    print(f"\n{label}")
    for i, op in enumerate(options, 1): print(f"  {i}. {op}")
    print("Saisissez les numéros séparés par des virgules. 0 = aucun." + (" Ajoutez une valeur libre en fin de liste avec le préfixe texte:." if allow_custom else ""))
    while True:
        raw=input("Sélection : ").strip()
        if not raw: print("Une sélection est nécessaire (0 = aucun)."); continue
        if raw == "0": return []
        out=[]; valid=True
        for token in raw.split(","):
            token=token.strip()
            if allow_custom and token.lower().startswith("texte:"):
                value=token[6:].strip()
                if value: out.append(value)
                continue
            if not token.isdigit() or not 1 <= int(token) <= len(options): valid=False; break
            value=options[int(token)-1]
            if value not in out: out.append(value)
        if valid: return out
        print("Sélection invalide.")
def slugify(s):
    s=unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    s=re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "mon-livre"

def lang_code(s):
    s=s.strip().replace("_","-")
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", s): raise ValueError("Code langue invalide, exemple fr-FR ou en-US.")
    return s

def gather_config(args):
    print("\n=== Générateur de projet livre OpenCode ===\nChaque exécution crée un projet indépendant. Aucun thème ni contenu éditorial n'est présélectionné. Les exemples sont des suggestions : saisissez vos propres valeurs quand nécessaire.\n")
    title=ask("Titre du livre", required=True)
    subtitle=ask("Sous-titre (facultatif)")
    author=ask("Auteur / pseudonyme", required=True)
    description=ask("Description détaillée du livre", required=True)
    book_type=ask_choice("Type de livre", BOOK_TYPES)
    audience=ask_choice("Public cible", AUDIENCES)
    lang=lang_code(ask("Langue initiale (code BCP-47, ex. fr-FR)", required=True))
    pages=ask_int("Nombre approximatif de pages", 1, 10000)
    start_level=ask_int("Niveau technique initial (0-100)", 0, 100)
    end_level=ask_int("Niveau technique final visé (0-100)", 0, 100)
    fonts=ask("Polices souhaitées (famille(s), ou écrire explicitement 'choix automatique')", required=True)
    constraints=ask("Contraintes éditoriales supplémentaires (ou écrire explicitement 'aucune')", required=True)
    learning=ask_multi("Dispositifs pédagogiques (plusieurs choix possibles)", [x[1] for x in LEARN])
    if len(learning)>1 and LEARN[4][1] in learning: learning.remove(LEARN[4][1])
    code_display=[]
    if any(k in book_type.lower() for k in ("technique", "informatique", "scientifique", "programm")) or ask_yes_no("Le livre contient-il du code informatique ?"):
        code_display=ask_multi("Présentation du code", ["Aucun code affiché", "Code monochrome", "Coloration syntaxique", "Numéros de ligne", "Résultats d'exécution à côté du code", "Résultats en commentaires dans le code", "Commandes, sorties et erreurs"])
        if len(code_display)>1 and "Aucun code affiché" in code_display: code_display.remove("Aucun code affiché")
    formats=ask_multi("Formats de publication souhaités", [x[1] for x in FORMATS])
    format_ids=[k for k,label in FORMATS if label in formats]
    size_options=["A4", "A5", "6 × 9 pouces", "8,5 × 11 pouces", "7 × 10 pouces", "Format personnalisé"]
    format_specs={}
    for fid in format_ids:
        if fid == "epub": continue
        print(f"\nFormat physique/visuel : {dict(FORMATS)[fid]}")
        size=ask_choice("Dimensions du PDF imprimable", size_options, False)
        if size == "Format personnalisé": size=ask("Dimensions et unités (ex. 152 × 229 mm)", required=True)
        margin_mode=ask_choice("Marges", ["Recherche des spécifications officielles à jour lors du contrôle", "Valeurs définies manuellement"], False)
        margins={"mode":"official_lookup" if margin_mode.startswith("Recherche") else "manual"}
        if margins["mode"]=="manual":
            margins={"mode":"manual","inner":ask("Marge intérieure + unité", required=True),"outer":ask("Marge extérieure + unité", required=True),"top":ask("Marge haute + unité", required=True),"bottom":ask("Marge basse + unité", required=True)}
        spec={"label":dict(FORMATS)[fid],"size":size,"margins":margins}
        if fid in ("pdf_print_screen", "etsy_both"):
            screen_size=ask_choice("Dimensions du PDF écran", ["A4", "A5", "6 × 9 pouces", "8,5 × 11 pouces", "Format personnalisé"], False)
            if screen_size == "Format personnalisé": screen_size=ask("Dimensions écran et unités", required=True)
            spec["screen"]={"size":screen_size,"margins":{"mode":"not_applicable"}}
        format_specs[fid]=spec
    layout=ask_choice("Mode de mise en page", ["Markdown uniquement", "LaTeX", "Markdown + Pandoc + LaTeX"], False)
    research=ask_choice("Recherche documentaire", ["Autonome : le modèle maîtrise le contenu sans recherche Web", "Recherche Web : sources, vérification et citations si nécessaires"], False)
    workflow=ask_choice("Mode de déroulement", ["Enchaîner toutes les étapes sans arrêt", "Reprise automatique après erreur avec rapport détaillé", "Arrêt après chaque grande étape", "Personnalisé"], False)
    if workflow=="Personnalisé": workflow=ask("Décrivez les règles d'arrêt/reprise", required=True)
    validation=ask_choice("Validation de chaque chapitre", ["Automatique", "Manuelle", "Automatique puis manuelle"], False)
    illustrations=ask_multi("Types d'illustrations (plusieurs choix possibles)", [x[1] for x in ILLUSTRATIONS])
    if len(illustrations)>1 and ILLUSTRATIONS[4][1] in illustrations: illustrations.remove(ILLUSTRATIONS[4][1])
    illustration_specs=[]
    for label in illustrations:
        if label==ILLUSTRATIONS[4][1]: illustration_specs.append({"type":"none","label":label}); continue
        mode=ask_choice(f"Mode pour « {label} »", ["IA : préparer catalogue + prompt + chemin cible", "Fichier fourni par l'utilisateur : catalogue + chemin cible"], False)
        illustration_specs.append({"type":next((k for k,v in ILLUSTRATIONS if v==label),"custom"),"label":label,"mode":"ai_prompt" if mode.startswith("IA") else "user_provided"})
    git=ask_yes_no("Initialiser Git dans le projet généré ?")
    commit=git and ask_yes_no("Créer aussi un commit initial ?")
    project_dir=Path(ask("Dossier parent où créer le projet (chemin absolu)", required=True)).expanduser().resolve()
    project_name=slugify(ask("Nom du dossier de projet", required=True))
    return {"schema_version":1,"generator_version":VERSION,"created_at_utc":datetime.now(timezone.utc).isoformat(),"title":title,"subtitle":subtitle,"author":author,"description":description,"book_type":book_type,"audience":audience,"initial_language":lang,"target_pages_approx":pages,"technical_level":{"initial":start_level,"final":end_level},"fonts":fonts,"constraints":constraints,"learning_features":learning,"code_display":code_display,"publishing":{"formats":format_ids,"format_specs":format_specs,"layout":layout},"research_mode":"web" if research.startswith("Recherche Web") else "standalone","workflow_mode":workflow,"chapter_validation":validation,"illustrations":illustration_specs,"illustration_policy":"distinct_image_per_language","image_engine":"preparation_only","code_execution":"isolated_controlled","language_creation":"prepare_only","git":{"enabled":git,"initial_commit":commit},"project_parent":str(project_dir),"project_name":project_name}
def write_file(root, rel, content, force=False):
    path=root/rel
    if path.exists() and not force: raise FileExistsError(str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content.rstrip()+"\n", encoding="utf-8")

def json_dump(data): return json.dumps(data,ensure_ascii=False,indent=2)+"\n"

def command_body(name, description, task, lang):
    return f"---\ndescription: {description}\n---\n\nTu travailles dans un projet de livre OpenCode. Langue de travail du projet : `{lang}`.\n\nRègles non négociables :\n- Lis `AGENTS.md`, `config/project.md`, `config/editorial.md`, `config/workflow.md`, `docs/PROGRESS.md` et `docs/DECISIONS.md` avant d'agir.\n- Respecte les choix du projet, les commandes disponibles et les fichiers existants.\n- N'invente pas de sources, de résultats d'exécution, de validation de plateforme ou d'images déjà créées.\n- Ne remplace jamais un contenu existant sans proposer un diff et obtenir une confirmation explicite.\n- Mets à jour l'état et les rapports après chaque tâche.\n\nTâche : {task}\n\nArguments utilisateur : `$ARGUMENTS`\n\nSi une information indispensable manque, pose une question précise. Termine par : fichiers modifiés, validations effectuées, limites/avertissements, prochaine étape recommandée.\n"

COMMANDS={
"book-plan":("Planifier le livre", "Établis le plan complet, les objectifs, le public, la progression, les chapitres et l'estimation de volume. Mets à jour SUMMARY.md et l'état du projet. Ne rédige pas encore les chapitres."),
"book-summary":("Créer ou réviser le sommaire", "Crée ou révise le sommaire détaillé, attribue un ID stable à chaque chapitre (CH001, CH002…), définit objectifs, dépendances, activités pédagogiques et annexes. Ne rédige pas les chapitres. Étape suivante obligatoire : produire et faire valider les briefs détaillés via /book-chapter-brief avant toute rédaction."),
"book-chapter-brief":("Décrire en détail le contenu d'un chapitre avant rédaction", "Crée ou complète languages/<lang>/chapter-briefs/CHxxx.md sans rédiger le chapitre final. Décris objectifs, prérequis, concepts et sous-sections, explications attendues, exemples, pièges, sources à vérifier, transitions, illustrations et exercices avec énoncé complet, consignes, données, niveau, critères de réussite et corrigé attendu. Le statut initial est DRAFT; ne passe à APPROVED qu'après demande explicite de l'utilisateur. Mets à jour l'index et l'état."),
"book-chapter-brief-edit":("Modifier les descriptions détaillées d'un chapitre", "Modifie le brief du chapitre ciblé. L'argument précise l'ID et l'opération : ajouter, corriger, remplacer, déplacer, supprimer un élément ou exercice, ou valider. Avant suppression ou remplacement substantiel, présente les éléments concernés et demande confirmation si l'utilisateur n'a pas explicitement autorisé l'opération. Mets à jour index, statut et décisions. Ne rédige pas le chapitre final."),
"book-chapter":("Rédiger un chapitre", "Avant rédaction, vérifie que languages/<lang>/chapter-briefs/CHxxx.md existe et porte le statut APPROVED. Sinon, arrête-toi et demande /book-chapter-brief puis /book-chapter-brief-edit. Rédige uniquement à partir du brief approuvé, sans omettre concepts, exemples, exercices, énoncés ni corrections attendues. Vérifie prérequis, progression, faits, style et marqueurs d'illustration. Ne prétends pas avoir exécuté du code sans rapport d'exécution."),
"book-range":("Rédiger une plage de chapitres", "Traite uniquement la plage indiquée. Avant rédaction, vérifie que chaque chapitre possède un brief détaillé APPROVED; liste les briefs manquants/non approuvés et arrête la plage plutôt que de rédiger sans plan validé. Respecte les dépendances et validations. N'écrase rien sans confirmation."),
"book-all":("Produire tous les chapitres", "Exécute le workflow défini dans config/workflow.md. Étape préalable obligatoire : créer les briefs détaillés avec /book-chapter-brief et obtenir leur approbation. Ne rédige aucun chapitre sans brief APPROVED; liste les blocages. Suis le mode d'arrêt/reprise et consigne les résultats."),
"book-review":("Relire un chapitre", "Relis le chapitre indiqué par rapport à son brief APPROVED et au sommaire : vérifie que chaque section, exemple, exercice, énoncé et correction attendue a été traité, en plus de l'exactitude, du style, des références, du code et des illustrations. Fournis un rapport actionnable et corrige uniquement si le mode de validation l'autorise."),
"book-review-all":("Relire le livre entier", "Relis sommaire, briefs approuvés et chapitres ensemble. Détecte briefs absents, éléments prévus mais non rédigés, exercices/corrigés manquants, contradictions, répétitions, incohérences de niveau, termes non définis et références manquantes. Produit un rapport global."),
"book-status":("Afficher l'état du projet", "Inspecte l'état réel des fichiers, chapitres, validations, illustrations, traductions et livrables. Mets à jour docs/PROGRESS.md sans déclarer achevée une tâche non vérifiée."),
"book-assemble":("Assembler le manuscrit", "Assemble les éléments validés dans languages/<lang>/manuscript/ en respectant SUMMARY.md, les marqueurs d'illustration et les options de mise en page. Signale les éléments manquants sans les masquer."),
"book-cover-text":("Préparer les textes de couverture", "Rédige et vérifie le texte de première, quatrième de couverture et tranche si pertinente, selon le public, le format et les limites fournies. Ne prétends pas calculer la tranche sans pagination/papier/spécifications vérifiés."),
"book-cover":("Préparer la couverture", "Prépare une spécification Markdown complète par format de couverture : dimensions, résolution, fonds perdus, zones de sécurité, textes, placement, chemin cible, prompt si pertinent et état. Le moteur d'images reste désactivé : ne crée pas de faux fichier final."),
"book-check":("Contrôler les livrables", "Exécute les validations disponibles : chapitres, sommaire, marqueurs, illustrations, métadonnées, polices, caractères, liens, dimensions, couverture et exigences des plateformes. Distingue erreur, avertissement et contrôle manuel. Ne garantis jamais l'acceptation KDP/Etsy."),
"book-language-create":("Préparer une nouvelle langue", "Crée l'arborescence complète de la langue demandée, les fichiers de sommaire/chapitres/briefs détaillés/manuscrit/couvertures/sorties et un catalogue d'illustrations dédié. Ne traduis rien et ne lance aucune génération de contenu. Pour chaque illustration de la langue source, prépare une entrée dans le catalogue cible en conservant l'ID stable, réserve un chemin image distinct contenant le code langue cible et marque la traduction de légende/description/prompt comme à faire. Si une entrée est en mode image utilisateur, crée un PNG vide uniquement si le chemin cible n'existe pas et marque-le PLACEHOLDER_EMPTY. Aucun moteur d'images ne doit être lancé."),
"book-translate":("Traduire un élément", "Traduis uniquement l'élément indiqué dans la langue cible. Respecte le glossaire, la voix, les références et les marqueurs. Pour les illustrations, traduis légendes, descriptions et prompts associés; conserve les ID stables mais réserve une image distincte pour la langue cible."),
"book-translate-all":("Traduire tous les éléments", "Traduis tous les éléments existants vers la langue cible : sommaire, briefs détaillés des chapitres, chapitres, quatrième de couverture, catalogue d'illustrations, légendes, descriptions et prompts. Conserve les IDs d'illustration stables, mais utilise des chemins image propres à la langue cible; ne réutilise jamais l'image d'une autre langue. Vérifie l'exhaustivité et consigne chaque élément traduit/non traduit."),
"book-translate-chapter-brief":("Traduire le brief détaillé d’un chapitre", "Traduis le fichier languages/<langue_source>/chapter-briefs/CHxxx.md vers la langue cible dans son dossier chapter-briefs. Conserve toutes les sections, IDs d’exercices, critères de réussite, corrigés attendus et marqueurs; adapte les exemples et références culturelles si nécessaire. Le statut de traduction reste IN_REVIEW jusqu’à validation."),
"book-translate-chapter-briefs":("Traduire les briefs détaillés d’une plage ou de tous les chapitres", "Selon les arguments, traduis une plage de briefs ou tous les briefs existants vers la langue cible. Préserve la structure, les IDs, les exercices et les corrigés attendus. Ne rédige pas les chapitres finaux et ne marque pas les briefs comme APPROVED sans validation explicite."),
"book-language-chapter":("Traduire un chapitre", "Traduis le chapitre indiqué vers la langue cible en conservant la structure, le sens, le niveau, les références, le code et les marqueurs d'illustration. Mets à jour l'état de traduction."),
"book-language-range":("Traduire une plage de chapitres", "Traduis uniquement la plage de chapitres indiquée vers la langue cible. Préserve terminologie et cohérence inter-chapitres et consigne les erreurs."),
"book-language-all":("Traduire les chapitres d'une langue", "Traduis les chapitres disponibles vers la langue cible selon le mode demandé. N'omets aucun chapitre; marque explicitement les éléments non traduits."),
"book-language-assemble":("Assembler une version linguistique", "Assemble le manuscrit de la langue cible après vérification de l'exhaustivité des traductions et des images propres à cette langue. Ne comble pas les manques silencieusement."),
"book-language-build":("Produire les livrables d'une langue", "Lance les étapes de compilation et de validation autorisées pour la langue cible. Produis les formats configurés, les rapports et la liste des contrôles manuels. Ne déclare pas un livrable créé si un outil requis manque."),
}

def build_project(config, target, overwrite=False):
    target.mkdir(parents=True,exist_ok=True)
    lang=config['initial_language']; pname=config['project_name']
    files={}
    files['AGENTS.md']=f"""# Règles du projet OpenCode

Tu es l'assistant éditorial et technique du livre **{config['title']}** de {config['author']}.

## Priorités
1. Suivre `config/` et `docs/` comme source de vérité.
2. Maintenir cohérence, exactitude, originalité et progression éditoriale.
3. Ne jamais inventer sources, résultats d'exécution, fichiers d'images ou contrôles de conformité.
4. Protéger les fichiers existants : proposer un diff et attendre confirmation avant remplacement destructif.
5. Pour le code, utiliser uniquement l'exécuteur isolé `scripts/safe_exec.py`, qui impose un répertoire temporaire, un délai et une liste de langages autorisés. Si les contrôles d'isolation ne sont pas disponibles, ne pas exécuter.
6. Les illustrations sont en préparation uniquement. Créer catalogues/prompts/chemins, jamais prétendre avoir généré une image.
7. Chaque langue a ses propres images, fichiers et catalogue. Ne pas réutiliser une image d'une autre langue.
8. Avant de rédiger un chapitre, vérifier `languages/<lang>/chapter-briefs/CHxxx.md`. Il doit exister et porter le statut `APPROVED`. Sinon, créer ou compléter le brief avec `/book-chapter-brief`, le faire corriger/valider avec `/book-chapter-brief-edit` et ne pas rédiger le chapitre avant approbation explicite.
9. En mode recherche Web, enregistrer les sources dans `config/sources.md`, vérifier les faits importants, reformuler originalement et citer quand nécessaire.
10. La qualité et l'exhaustivité priment sur le nombre exact de pages. Signaler l'écart au lieu de gonfler artificiellement le texte.

## Reprise
Avant chaque tâche, lire `docs/PROGRESS.md`, `docs/DECISIONS.md` et l'état sous `state/`. Après chaque tâche, mettre à jour ces fichiers.
"""
    files['opencode.json']=json_dump({"$schema":"https://opencode.ai/config.json"})
    files['.opencode/agents/editorial-reviewer.md'] = """---
description: Relecture éditoriale et cohérence globale
mode: subagent
---

Tu es réviseur éditorial. Vérifie exactitude, structure, répétitions, progression, niveau de lecture, terminologie, cohérence avec le sommaire et qualité des explications. Distingue erreurs certaines, risques et recommandations. Ne réécris pas un fichier sans consigne explicite.
"""
    files['.opencode/agents/technical-reviewer.md'] = """---
description: Vérification technique, exemples et code
mode: subagent
---

Tu es réviseur technique. Vérifie la logique des exemples et du code. Ne prétends jamais qu'un code a été exécuté sans résultat du script `scripts/safe_exec.py`. Si l'isolation est indisponible, marque le résultat non vérifié. Signale les prérequis, versions, limites et risques.
"""
    files['.opencode/agents/researcher.md'] = """---
description: Recherche et traçabilité des sources
mode: subagent
---

Tu es documentaliste. En mode recherche Web, utilise des sources fiables et actuelles, vérifie les affirmations importantes, enregistre URL et date dans `config/sources.md`, et reformule avec originalité. N'invente jamais de référence. Signale les informations incertaines ou contradictoires.
"""
    files['.opencode/agents/translator.md'] = """---
description: Traduction éditoriale et cohérence multilingue
mode: subagent
---

Tu traduis uniquement les éléments demandés. Respecte le glossaire, le guide de style, les unités, les références et les marqueurs d'illustration. Chaque langue possède son propre catalogue et ses propres fichiers images. Signale les segments ambigus et ne déclare jamais une langue complète si des éléments manquent.
"""
    files['.opencode/skills/book-editorial/SKILL.md'] = """---
name: book-editorial
description: Règles éditoriales pour planifier, rédiger et relire un livre
---

Avant de rédiger, lire `config/project.md`, `config/editorial.md`, `docs/STYLE_GUIDE.md`, `docs/GLOSSARY.md` et le sommaire de la langue active. Exiger un brief `languages/<lang>/chapter-briefs/CHxxx.md` avec statut `APPROVED` avant la rédaction du chapitre; ne jamais contourner cette étape. Préserver l'originalité, la progression, la précision et la cohérence. Les pages cibles sont indicatives. Les sources doivent être réelles et traçables.
"""
    files['.opencode/skills/book-production/SKILL.md'] = """---
name: book-production
description: Assemblage, compilation et contrôles de livrables
---

Assembler seulement les chapitres attendus. Résoudre les marqueurs à partir du catalogue de la langue active. Exécuter les scripts de validation avant compilation. Refuser les écrasements sans confirmation. Consigner dépendances absentes, erreurs, avertissements et contrôles manuels. Une compilation réussie n'est pas une garantie d'acceptation de plateforme.
"""
    files['.opencode/skills/book-multilingual/SKILL.md'] = """---
name: book-multilingual
description: Création explicite, traduction et validation des versions linguistiques
---

La commande de création de langue prépare les fichiers uniquement. Aucune traduction ou génération de livre ne doit démarrer sans commande explicite. Traduire le sommaire, les chapitres, la quatrième de couverture, les légendes, descriptions et prompts. Chaque langue possède des images distinctes, un catalogue et un état de traduction indépendant.
"""
    files['.opencode/skills/illustration-catalog/SKILL.md'] = """---
name: illustration-catalog
description: Préparation de catalogues, prompts et chemins d'illustrations
---

Le moteur d'images est désactivé. Préparer des descriptions et prompts concrets, diversifiés et adaptés à l'usage, sans déclarer de fichier image généré. Utiliser des ID stables et un chemin par langue. Les PNG vides sont des marqueurs de remplacement, jamais des images finales.
"""
    files['.gitignore']="""# Build outputs et fichiers temporaires
__pycache__/
*.pyc
*.tmp
*.log
.venv/
.cache/
# Les images non validées restent dans les dossiers prévus; ne pas ignorer les sources par défaut.
"""
    files['README.md']=f"""# {config['title']}

Projet éditorial OpenCode autonome généré le {config['created_at_utc']}.

## Démarrage
1. Ouvrir un terminal dans ce dossier et lancer `opencode`.
2. Exécuter `/book-plan`, puis `/book-summary`.
3. Détailler le contenu avec `/book-chapter-brief CH001`; modifier avec `/book-chapter-brief-edit CH001 ...`, puis marquer explicitement le brief `APPROVED`.
4. Rédiger seulement ensuite avec `/book-chapter CH001`, puis valider avec `/book-review CH001`.
4. Suivre `docs/PROGRESS.md`; contrôler avec `/book-check`.
5. Pour une nouvelle langue, utiliser `/book-language-create fr-CA`, puis lancer explicitement les commandes de traduction et `/book-language-build fr-CA`.

Les commandes OpenCode sont dans `.opencode/commands/`. Les scripts déterministes sont dans `scripts/`. Les commandes `scriptable-*` sont des commandes OpenCode destinées à être invoquées via `opencode run`, sous réserve de compatibilité de la version installée. Elles ne sont pas des scripts shell autonomes.

**Limites explicites :** moteur d'images désactivé; prompts et chemins uniquement. La validation des marges et exigences de publication doit utiliser les spécifications officielles actuelles et enregistrer la date et les sources. Un contrôle local ne garantit jamais l'acceptation par une plateforme.
"""
    files['config/project.md']=f"""# Fiche projet
- Titre : {config['title']}
- Sous-titre : {config['subtitle'] or '(aucun)'}
- Auteur : {config['author']}
- Description : {config['description']}
- Type : {config['book_type']}
- Public : {config['audience']}
- Langue initiale : {lang}
- Volume cible : environ {config['target_pages_approx']} pages
- Niveau technique : {config['technical_level']['initial']} -> {config['technical_level']['final']}/100
- Polices : {config['fonts']}
- Contraintes : {config['constraints']}
"""
    files['config/editorial.md']="""# Politique éditoriale

- Priorité à la clarté, la cohérence, l'originalité, l'exactitude et l'utilité.
- Ne pas inventer de citations, études, références, données ou témoignages.
- Définir les termes techniques à leur première occurrence et maintenir le glossaire.
- Éviter répétitions, remplissage et promesses excessives.
- Les pages cibles sont approximatives. Signaler les écarts sans gonfler artificiellement le contenu.
- Le ton et les conventions doivent rester cohérents dans tous les chapitres et toutes les langues.
"""
    files['config/technical.md']=f"""# Configuration technique
- Mode de mise en page : {config['publishing']['layout']}
- Affichage du code : {', '.join(config['code_display']) if config['code_display'] else 'non spécifié'}
- Exécution : isolée via Docker sans réseau ou bubblewrap Linux; refus d'exécuter si aucun runtime d'isolation n'est disponible.
- Images : préparation uniquement, aucun moteur lancé.
- Formats : {', '.join(config['publishing']['formats'])}

## Isolation du code
Le script `scripts/safe_exec.py` accepte seulement Python, JavaScript (si Node est présent) et shell sous contrôles. Exécution dans un répertoire temporaire, timeout et limites de sortie. Le shell n'est jamais accepté par défaut; activation explicite requise. L'isolation applicative n'est pas un bac à sable de sécurité système équivalent à un conteneur. Pour du code non fiable, utiliser une VM/conteneur sans réseau et sans secrets.
"""
    files['config/workflow.md']=f"""# Workflow
- Mode : {config['workflow_mode']}
- Validation des chapitres : {config['chapter_validation']}
- Recherche : {config['research_mode']}
- Apprentissage : {', '.join(config['learning_features']) if config['learning_features'] else 'aucun'}
- Les tâches sont suivies dans `state/` et `docs/PROGRESS.md`.
- Les erreurs doivent être journalisées, avec étape, date, sortie et action de reprise.
- Aucun fichier final ne doit être annoncé comme créé si l'outil requis n'a pas réussi.
"""
    files['config/publishing.md']="# Formats et spécifications de publication\n\n"+json.dumps(config['publishing'],ensure_ascii=False,indent=2)+"\n\nLes spécifications officielles doivent être recherchées au moment du contrôle. Enregistrer URL, date de consultation, version/règle vérifiée et résultat dans `docs/REFERENCE.md`. Si elles ne peuvent pas être vérifiées, marquer le contrôle comme non vérifié.\n"
    files['config/illustrations.md']="""# Politique des illustrations

- Politique : une image distincte par langue (`distinct_image_per_language`).
- Moteur : préparation uniquement. Aucun appel à ComfyUI, FastSDCPU ou service distant.
- Chaque illustration possède un ID stable indépendant de la langue et un chemin/fichier par langue, par exemple `ILL-CH003-001-fr-FR.png`.
- Les textes utilisent `{{ILL:ILL-CH003-001}}`; le résolveur utilise le catalogue de la langue active.
- Fichier de catalogue par langue : `languages/<code>/illustrations/ILLUSTRATIONS.md`, colonnes `ID | symbole | légende | description | prompt | chemin relatif | mode | statut`.
- Les images fournies par l'utilisateur ne sont jamais écrasées. Un PNG vide n'est créé que si le chemin n'existe pas, et reste marqué `PLACEHOLDER_EMPTY`.
- Contrôles : ID dupliqué, image absente/vide, marqueur non résolu, entrée orpheline, code langue incorrect, prompt absent pour mode IA.
"""
    files['config/generator-input.json']=json_dump(config)
    files['config/sources.md']="# Sources documentaires\n\nMode de recherche : "+config['research_mode']+".\n\n| ID | Sujet / affirmation | Source | Date consultée | Fiabilité / limites | Où utilisée |\n|---|---|---|---|---|---|\n"
    files['docs/REFERENCE.md']="# Références et conformité\n\nConsigner ici les sources de contenu et les sources officielles de spécifications de publication, avec URL, date de consultation et règle vérifiée. Aucun lien ni résultat ne doit être inventé.\n"
    files['docs/STYLE_GUIDE.md']="# Guide de style\n\nÀ compléter au cours de la planification : ton, point de vue, longueur des sections, conventions typographiques, tutoiement/vouvoiement, traitement des exemples, règles d'accessibilité et conventions propres au genre.\n"
    files['docs/GLOSSARY.md']="# Glossaire\n\n| Terme source | Définition | Équivalent par langue | Première occurrence |\n|---|---|---|---|\n"
    files['docs/PROGRESS.md']="# État du projet\n\n- [ ] Plan éditorial\n- [ ] Sommaire validé\n- [ ] Chapitres rédigés\n- [ ] Relecture globale\n- [ ] Illustrations préparées et vérifiées\n- [ ] Manuscrit assemblé\n- [ ] Couvertures spécifiées\n- [ ] Livrables construits\n- [ ] Contrôles finaux\n\nDernière mise à jour : génération initiale. Aucune production éditoriale n'est réputée achevée.\n"
    files['docs/DECISIONS.md']=f"# Décisions projet\n\n- Images distinctes par langue.\n- Moteur d'images désactivé : préparation de prompts et chemins seulement.\n- Exécution de code isolée et contrôlée; aucun résultat non vérifié.\n- Création d'une langue sans génération de contenu automatique.\n- Formats choisis : {', '.join(config['publishing']['formats'])}.\n- Les pages cibles sont indicatives.\n"
    files['docs/WORKFLOW.md']="# Workflow opérationnel\n\n1. Planifier. 2. Valider le sommaire. 3. Rédiger chapitre par chapitre ou par plages. 4. Valider. 5. Préparer les illustrations. 6. Assembler. 7. Construire les formats. 8. Contrôler et archiver le rapport.\n"
    files['prompts/planning/BOOK_PLAN.md']="# Prompt de planification\n\nProduis un plan éditorial approfondi à partir des fichiers de configuration. Pose les questions manquantes. Identifie objectifs, public, progression, chapitres, activités, risques d'exactitude, besoins de recherche et critères d'acceptation.\n"
    files['prompts/writing/CHAPTER.md']="# Prompt de rédaction\n\nRédige uniquement le chapitre demandé selon le sommaire validé. Vérifie cohérence, progression, originalité, niveau, références et marqueurs d'illustration. Ne simule aucun résultat d'exécution.\n"
    files['prompts/reviewing/REVIEW.md']="# Prompt de relecture\n\nVérifie exactitude, logique, structure, répétitions, lisibilité, terminologie, références, code, illustrations et alignement avec le sommaire. Sépare les erreurs certaines des recommandations éditoriales.\n"
    files['prompts/translation/TRANSLATE.md']="# Prompt de traduction\n\nTraduis l'élément désigné vers la langue cible en préservant sens, voix, niveau, structure, références et marqueurs. Consulte glossaire et style guide. Ne supprime aucun contenu sans le signaler.\n"
    files['prompts/illustrations/ILLUSTRATION.md']="# Prompt de préparation d'illustration\n\nDécris précisément sujet, composition, point de vue, motifs, densité, contraintes, format et lisibilité. Prépare un prompt et un chemin cible par langue. Ne lance aucun moteur d'images.\n"
    files['prompts/covers/COVER.md']="# Prompt de préparation de couverture\n\nPrépare la spécification et le prompt, si demandé, pour le format exact. Indique dimensions, résolution, fonds perdus, zones de sécurité, textes et placement. N'invente pas les dimensions du dos sans pagination, papier et spécifications officielles vérifiés.\n"
    files['templates/covers/COVER_SPEC.md']="# Spécification couverture\n\n- Format : À renseigner\n- Langue : À renseigner\n- Dimensions exactes : à vérifier\n- Résolution : à vérifier\n- Fond perdu / zone de sécurité : à vérifier\n- Textes requis : titre, auteur, quatrième, tranche si applicable\n- Chemin cible : `covers/`\n- Prompt : à préparer si génération externe demandée\n- Statut : `SPECIFICATION_PENDING`\n"
    files['templates/chapters/CHAPTER_BRIEF_TEMPLATE.md']=CHAPTER_BRIEF_TEMPLATE
    files['templates/layouts/README.md']="# Modèles de mise en page\n\nLes modèles doivent être adaptés au format et testés avec les dépendances présentes. Aucun gabarit ne garantit à lui seul la conformité à une plateforme.\n"
    files['templates/reports/BUILD_REPORT.md']="# Rapport de construction\n\n- Date :\n- Langue :\n- Format :\n- Outil/version :\n- Statut :\n- Pages / dimensions :\n- Polices / caractères :\n- Illustrations manquantes :\n- Contrôles réussis :\n- Avertissements :\n- Contrôles manuels restants :\n"
    files['scripts/safe_exec.py']=SAFE_EXEC
    files['scripts/validate_project.py']=VALIDATOR
    files['scripts/assemble.py']=ASSEMBLER
    files['scripts/build.py']=BUILDER
    files['scripts/status.py']=STATUS
    files['scripts/invoke_command.py']=INVOKER
    files['scripts/prepare_illustration.py']=PREPARE_ILLUSTRATION
    files['scripts/chapter_briefs.py']=CHAPTER_BRIEF_TOOL
    files['scripts/requirements.txt']="# Dépendances optionnelles pour la compilation; le validateur de base utilise la bibliothèque standard Python.\n# Pandoc et LaTeX sont des exécutables système, pas des packages pip.\n"
    files['state/chapters/README.md']="# État des chapitres\n\nLe statut de chaque chapitre est consigné ici par OpenCode ou par les scripts de suivi.\n"
    files['state/chapter-briefs/README.md']="# État des briefs de chapitres\n\nUn chapitre ne peut être rédigé que lorsque son brief détaillé est marqué APPROVED.\n"
    files['state/builds/README.md']="# État des constructions\n"
    files['state/translations/README.md']="# État des traductions\n"
    files['logs/.gitkeep']=""
    # format-specific cover specs, including separate print and screen/ebook assets
    for fid,spec in config['publishing']['format_specs'].items():
        if fid == 'kdp_ebook':
            files['templates/covers/KDP_PRINT_COVER.md'] = f"# Couverture KDP brochée\n\n- Dimensions du livre : {spec['size']}\n- Marges intérieures du contenu : {json.dumps(spec['margins'],ensure_ascii=False)}\n- Dimensions complètes de la couverture (quatrième + tranche + première) : à calculer à partir de la pagination finale, papier et spécifications KDP actuelles\n- Fonds perdus / zones de sécurité / résolution : à vérifier officiellement\n- Langue : {lang}\n- Chemin cible : `languages/{lang}/covers/kdp-print-wrap.png`\n- Statut : `SPECIFICATION_PENDING`\n"
            files['templates/covers/KDP_EBOOK_COVER.md'] = f"# Couverture Kindle numérique\n\n- Type : image de couverture numérique, distincte de la couverture brochée\n- Dimensions/résolution : à vérifier selon les exigences officielles actuelles\n- Langue : {lang}\n- Chemin cible : `languages/{lang}/covers/kdp-ebook-cover.png`\n- Prompt : à préparer, moteur d'images désactivé\n- Statut : `SPECIFICATION_PENDING`\n"
        elif fid in ('pdf_print_screen', 'etsy_both'):
            files[f"templates/covers/{fid.upper()}_PRINT_COVER.md"] = f"# Couverture impression : {spec['label']}\n\n- Dimensions : {spec['size']}\n- Marges : {json.dumps(spec['margins'],ensure_ascii=False)}\n- Fonds perdus / zones de sécurité : à vérifier selon la plateforme\n- Langue : {lang}\n- Chemin cible : `languages/{lang}/covers/{fid}-print-cover.png`\n- Statut : `SPECIFICATION_PENDING`\n"
            screen=spec.get('screen',{})
            files[f"templates/covers/{fid.upper()}_SCREEN_COVER.md"] = f"# Couverture écran : {spec['label']}\n\n- Dimensions : {screen.get('size','à définir')}\n- Résolution et profil couleur : à vérifier selon la destination\n- Langue : {lang}\n- Chemin cible : `languages/{lang}/covers/{fid}-screen-cover.png`\n- Statut : `SPECIFICATION_PENDING`\n"
        else:
            files[f"templates/covers/{fid.upper()}_COVER.md"] = f"# Couverture : {spec['label']}\n\n- Dimensions : {spec['size']}\n- Marges : {json.dumps(spec['margins'],ensure_ascii=False)}\n- Résolution : à vérifier selon spécification officielle\n- Fonds perdus / zone sûre : à vérifier\n- Langue : {lang}\n- Chemin cible : `languages/{lang}/covers/{fid}-cover.png`\n- Prompt : à préparer, moteur d'images désactivé\n- Statut : `SPECIFICATION_PENDING`\n"
    for fid in config['publishing']['formats']:
        if fid == 'epub':
            files['templates/covers/EPUB_COVER.md'] = f"# Couverture EPUB\n\n- Type : couverture intégrée au livre numérique\n- Dimensions exactes et métadonnées : à vérifier selon les spécifications du distributeur ciblé\n- Langue : {lang}\n- Chemin cible : `languages/{lang}/covers/epub-cover.png`\n- Prompt : à préparer, moteur d'images désactivé\n- Statut : `SPECIFICATION_PENDING`\n"
    # languages directories
    lang_files=make_language_files(lang, config, primary=True)
    files.update(lang_files)
    # Commands in OpenCode-supported directory .opencode/commands
    for name,(desc,task) in COMMANDS.items(): files[f'.opencode/commands/{name}.md']=command_body(name,desc,task,lang)
    for name,(desc,task) in COMMANDS.items(): files[f'.opencode/commands/scriptable-{name}.md']=command_body('scriptable-'+name,desc,"Commande scriptable : effectuer la tâche suivante de manière non interactive si les arguments suffisent, sinon poser une question et ne pas supposer. "+task,lang)
    # executable platform helpers inside generated project
    files['scripts/platform/run-opencode.sh']="#!/usr/bin/env sh\nset -eu\ncommand -v opencode >/dev/null 2>&1 || { echo 'OpenCode introuvable dans PATH.' >&2; exit 127; }\nexec opencode run \"$*\"\n"
    files['scripts/platform/run-opencode.bat']='@echo off\nwhere opencode >nul 2>nul || (echo OpenCode introuvable dans PATH. 1>&2 & exit /b 127)\nopencode run %*\n'
    files['scripts/platform/run-opencode.ps1']="if (-not (Get-Command opencode -ErrorAction SilentlyContinue)) { Write-Error 'OpenCode introuvable dans PATH.'; exit 127 }\nopencode run @args\nexit $LASTEXITCODE\n"
    for rel,content in files.items(): write_file(target,rel,content,force=overwrite)
    for rel in ['scripts/platform/run-opencode.sh']:
        try: (target/rel).chmod(0o755)
        except OSError: pass
    # create initial chapter directories and no fake chapter content
    (target/f'languages/{lang}/chapters').mkdir(parents=True,exist_ok=True)
    (target/f'languages/{lang}/chapter-briefs').mkdir(parents=True,exist_ok=True)
    (target/f'languages/{lang}/output').mkdir(parents=True,exist_ok=True)
    (target/'output').mkdir(exist_ok=True)
    if config['git']['enabled']:
        if shutil.which('git'):
            subprocess.run(['git','init'],cwd=target,check=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            if config['git']['initial_commit']:
                subprocess.run(['git','add','.'],cwd=target,check=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                subprocess.run(['git','-c','user.name=Book Project Generator','-c','user.email=generator@localhost','commit','-m','Initial book project scaffold'],cwd=target,check=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        else: print("AVERTISSEMENT : Git demandé mais non installé; dépôt non initialisé.")
    return target

def make_language_files(lang, config, primary=False):
    base=f'languages/{lang}/'
    return {
        base+'SUMMARY.md':f"# Sommaire\n\nLivre : {config['title']}\nLangue : {lang}\n\n> À produire avec `/book-summary`.\n",
        base+'chapters/README.md':f"# Chapitres ({lang})\n\nCréer un fichier par chapitre, par exemple `CH001.md`. Un chapitre final ne doit être rédigé qu'après approbation de son brief dans `../chapter-briefs/`.\n",
        base+'chapter-briefs/README.md':f"# Briefs détaillés des chapitres ({lang})\n\nUn fichier par chapitre, par exemple `CH001.md`. Définir précisément objectifs, sections, explications, exemples, exercices avec énoncés, critères de réussite, corrigés attendus, illustrations et sources avant rédaction.\n\nWorkflow : `/book-chapter-brief CH001` → `/book-chapter-brief-edit CH001` → statut `APPROVED` explicite → `/book-chapter CH001`.\n",
        base+'chapter-briefs/INDEX.md':f"# Index des briefs ({lang})\n\n| Chapitre | Fichier | Statut | Dernière vérification | Notes |\n|---|---|---|---|---|\n\nAucune description détaillée créée. Ajouter une ligne pour chaque brief.\n",
        base+'manuscript/README.md':"# Manuscrit assemblé\n\nFichiers assemblés uniquement après validation.\n",
        base+'illustrations/ILLUSTRATIONS.md':"# Catalogue des illustrations\n\n| ID | Symbole | Légende | Description | Prompt | Chemin relatif | Mode | Statut |\n|---|---|---|---|---|---|---|---|\n",
        base+'illustrations/images/.gitkeep':'',
        base+'covers/FOURTH_COVER.md':f"# Quatrième de couverture ({lang})\n\nÀ rédiger et valider.\n",
        base+'covers/README.md':"# Couvertures\n\nUne spécification et un livrable distinct par format requis.\n",
        base+'output/README.md':"# Livrables\n\nAucun livrable généré à l'initialisation.\n",
        base+'language.json':json_dump({"language_code":lang,"primary":primary,"image_policy":"distinct_image_per_language","content_generation_on_create":False,"created_at_utc":datetime.now(timezone.utc).isoformat()})
    }

CHAPTER_BRIEF_TEMPLATE = """# Brief détaillé du chapitre CHXXX

- **Titre provisoire :** À définir depuis le sommaire
- **Langue :** À renseigner
- **Statut :** `DRAFT`
- **Version :** 1
- **Dépendances / prérequis :** À définir
- **Objectif général :** À définir
- **Résultats d'apprentissage observables :**
  - [ ] À définir

## 1. Place dans la progression du livre
Décrire le lien avec les chapitres précédents et suivants, les connaissances supposées et les limites de périmètre.

## 2. Plan de contenu détaillé
Pour chaque section, préciser l'intention, les notions exactes, les explications nécessaires, les exemples, les erreurs fréquentes et le niveau de détail attendu.

### 2.1 Section à définir
- **But de la section :**
- **Notions à couvrir :**
- **Explications indispensables :**
- **Exemple(s) concret(s) :**
- **Contre-exemple / piège :**
- **Vérifications factuelles ou sources à rechercher :**
- **Transition vers la section suivante :**

## 3. Exemples, études de cas ou démonstrations
Décrire précisément chaque exemple et ce qu'il doit démontrer. Pour du code, indiquer langage/version, fichiers, prérequis, commande d'exécution et résultat attendu. Les résultats non exécutés doivent rester identifiés comme théoriques.

## 4. Exercices et activités
Créer une sous-section par exercice. Si aucun exercice n'est requis, expliquer pourquoi.

### EX-CHXXX-01 : Titre de l'exercice
- **Objectif évalué :**
- **Type / difficulté / durée indicative :**
- **Énoncé complet destiné au lecteur :**
- **Contexte, données et matériel fourni :**
- **Consignes numérotées :**
- **Contraintes et critères de réussite :**
- **Indices éventuels :**
- **Corrigé attendu / solution de référence :**
- **Explication pédagogique du corrigé :**
- **Erreurs fréquentes à expliquer :**
- **Emplacement de la correction :** selon la configuration éditoriale du livre

## 5. Illustration(s) à prévoir
Pour chaque illustration : identifiant stable, objectif pédagogique, légende provisoire, description de composition, emplacement, prompt éventuel et chemin d'image propre à la langue. Ne jamais déclarer l'image générée.

## 6. Vocabulaire et cohérence
- **Termes à définir :**
- **Termes du glossaire à réutiliser :**
- **Liens avec les autres chapitres :**
- **Répétitions à éviter :**

## 7. Sources et points à vérifier
Lister les affirmations nécessitant une source, les références fiables attendues et les incertitudes. Ne jamais inventer de référence.

## 8. Conclusion du chapitre
- **Synthèse des idées clés :**
- **Points à retenir :**
- **Transition vers le chapitre suivant :**

## 9. Critères de complétude avant rédaction
- [ ] Toutes les sections sont décrites avec assez de détail pour rédiger sans inventer le périmètre.
- [ ] Les exercices ont des énoncés complets et un corrigé attendu, si applicable.
- [ ] Les objectifs correspondent au contenu et aux exercices.
- [ ] Les illustrations prévues ont un ID et un chemin propre à la langue.
- [ ] Les sources à vérifier sont identifiées.
- [ ] Le brief est cohérent avec le sommaire et les autres briefs.
- [ ] Validation explicite de l'utilisateur reçue avant de passer le statut à `APPROVED`.
"""

CHAPTER_BRIEF_TOOL = r'''#!/usr/bin/env python3
"""Manage and validate detailed chapter briefs before chapter drafting."""
import argparse, re, sys
from pathlib import Path
REQUIRED = ["## 1. Place dans la progression du livre", "## 2. Plan de contenu détaillé", "## 4. Exercices et activités", "## 9. Critères de complétude avant rédaction"]
def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument('--root',default='.'); p.add_argument('--lang',required=True); p.add_argument('--action',choices=['list','validate','init'],default='list'); p.add_argument('--chapter',help='Chapter ID, e.g. CH001'); a=p.parse_args()
 root=Path(a.root).resolve(); folder=root/'languages'/a.lang/'chapter-briefs'
 if not folder.is_dir(): print('Brief directory not found:',folder,file=sys.stderr); return 2
 if a.action=='init':
  if not a.chapter or not re.fullmatch(r'CH[0-9]{3,4}',a.chapter): p.error('--chapter must look like CH001')
  dest=folder/(a.chapter+'.md')
  if dest.exists(): print('Refusing to overwrite existing brief:',dest,file=sys.stderr); return 3
  template=root/'templates/chapters/CHAPTER_BRIEF_TEMPLATE.md'
  if not template.is_file(): print('Brief template missing:',template,file=sys.stderr); return 4
  dest.write_text(template.read_text(encoding='utf-8').replace('CHXXX',a.chapter).replace('À renseigner',a.lang),encoding='utf-8')
  index=folder/'INDEX.md'
  if index.exists():
   content=index.read_text(encoding='utf-8')
   if f'| {a.chapter} |' not in content:
    lines=content.splitlines(); sep=next((i for i,line in enumerate(lines) if line.startswith('|---')),None)
    row=f'| {a.chapter} | {a.chapter}.md | DRAFT | À vérifier | Créé par script |'
    if sep is not None: lines.insert(sep+1,row)
    else: lines.append(row)
    index.write_text('\n'.join(lines)+'\n',encoding='utf-8')
  print('Created draft brief:',dest); print('Status remains DRAFT; do not draft the chapter until explicitly approved.'); return 0
 briefs=sorted(folder.glob('CH*.md'))
 if a.action=='list':
  if not briefs: print('No chapter briefs yet. Use --action init --chapter CH001 or /book-chapter-brief.')
  for f in briefs:
   m=re.search(r'^- \*\*Statut :\*\* `([^`]+)`',f.read_text(encoding='utf-8'),re.M)
   print(f'{f.stem}\t{m.group(1) if m else "STATUS_MISSING"}\t{f.relative_to(root)}')
  return 0
 errors=[]
 for f in briefs:
  body=f.read_text(encoding='utf-8'); m=re.search(r'^- \*\*Statut :\*\* `([^`]+)`',body,re.M); status=m.group(1) if m else 'STATUS_MISSING'
  missing=[h for h in REQUIRED if h not in body]
  if status not in {'DRAFT','IN_REVIEW','APPROVED'}: errors.append(f'{f.name}: invalid/missing status {status}')
  if missing: errors.append(f'{f.name}: missing required sections: {", ".join(missing)}')
  if status=='APPROVED' and ('[ ] Toutes les sections' in body or '[ ] Les exercices' in body): errors.append(f'{f.name}: approval checklist still unchecked; review manually')
 if errors: print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr); return 1
 print(f'Validated structure of {len(briefs)} brief(s). This does not prove editorial quality or user approval.'); return 0
if __name__=='__main__': sys.exit(main())
'''

PREPARE_ILLUSTRATION = r'''#!/usr/bin/env python3
"""Register an illustration target for one language without generating image content."""
import argparse, re, sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); p.add_argument('--lang',required=True); p.add_argument('--id',required=True); p.add_argument('--filename',required=True); p.add_argument('--mode',choices=['ai_prompt','user_provided'],required=True); p.add_argument('--caption',default='À compléter'); p.add_argument('--description',default='À compléter'); p.add_argument('--prompt',default='null'); a=p.parse_args()
 if not re.fullmatch(r'[A-Za-z0-9-]+',a.id): p.error('invalid illustration ID')
 if not re.fullmatch(r'[A-Za-z0-9-]+\.png',a.filename): p.error('filename must be a safe PNG basename')
 if a.lang not in a.filename: p.error('filename must contain the language code')
 root=Path(a.root).resolve(); ld=root/'languages'/a.lang
 if not ld.is_dir(): print('Language directory does not exist:',ld,file=sys.stderr); return 2
 cat=ld/'illustrations/ILLUSTRATIONS.md'; imgdir=ld/'illustrations/images'; imgdir.mkdir(parents=True,exist_ok=True); cat.parent.mkdir(parents=True,exist_ok=True)
 text=cat.read_text(encoding='utf-8') if cat.exists() else '# Catalogue des illustrations\n\n| ID | Symbole | Légende | Description | Prompt | Chemin relatif | Mode | Statut |\n|---|---|---|---|---|---|---|---|\n'
 if any(line.startswith('| '+a.id+' |') for line in text.splitlines()): print('Illustration ID already exists in catalog; refusing duplicate:',a.id,file=sys.stderr); return 3
 path=imgdir/a.filename; status='PROMPT_PENDING' if a.mode=='ai_prompt' else 'USER_IMAGE_PENDING'
 if a.mode=='user_provided' and not path.exists(): path.touch(); status='PLACEHOLDER_EMPTY'
 elif path.exists() and path.stat().st_size==0: status='PLACEHOLDER_EMPTY'
 elif path.exists(): status='FILE_PRESENT_REVIEW_REQUIRED'
 prompt=a.prompt if a.mode=='ai_prompt' else 'null'
 rel='images/'+a.filename
 row=f'| {a.id} | ◇ | {a.caption.replace("|", "\\|")} | {a.description.replace("|", "\\|")} | {prompt.replace("|", "\\|")} | {rel} | {a.mode} | {status} |'
 cat.write_text(text.rstrip()+'\n'+row+'\n',encoding='utf-8')
 print('Catalog updated:',cat); print('Image target:',path); print('Status:',status)
 if status=='PLACEHOLDER_EMPTY': print('WARNING: empty placeholder only; replace it with a real image before publication.')
 return 0
if __name__=='__main__': sys.exit(main())
'''

INVOKER = r'''#!/usr/bin/env python3
"""Run a project OpenCode command by passing its Markdown prompt to `opencode run`."""
import argparse, re, shutil, subprocess, sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument('command',help='Command basename, e.g. scriptable-book-plan'); p.add_argument('--root',default='.'); p.add_argument('--args',default=''); p.add_argument('--dry-run',action='store_true'); a=p.parse_args()
 if not re.fullmatch(r'[a-z0-9-]+',a.command): p.error('invalid command name')
 root=Path(a.root).resolve(); f=root/'.opencode/commands'/f'{a.command}.md'
 if not f.is_file(): print('Command file not found:',f,file=sys.stderr); return 2
 raw=f.read_text(encoding='utf-8'); body=re.sub(r'^---\s*\n.*?\n---\s*\n','',raw,count=1,flags=re.S)
 body=body.replace('$ARGUMENTS',a.args)
 if a.dry_run: print(body); return 0
 if not shutil.which('opencode'): print('OpenCode not found in PATH',file=sys.stderr); return 127
 cp=subprocess.run(['opencode','run',body],cwd=root,check=False)
 return cp.returncode
if __name__=='__main__': sys.exit(main())
'''

SAFE_EXEC = r'''#!/usr/bin/env python3
"""Fail-closed code runner requiring Docker or Linux bubblewrap isolation."""
import argparse, os, shutil, subprocess, sys, tempfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument('--language',choices=['python','javascript','shell'],required=True); p.add_argument('--file',required=True); p.add_argument('--timeout',type=int,default=5); p.add_argument('--max-output',type=int,default=20000); p.add_argument('--allow-shell',action='store_true'); a=p.parse_args()
 if a.timeout<1 or a.timeout>30: p.error('timeout must be 1..30 seconds')
 if a.language=='shell' and not a.allow_shell: p.error('shell disabled; explicit --allow-shell required')
 src=Path(a.file).resolve()
 if not src.is_file(): p.error('source file not found')
 if src.stat().st_size>256_000: p.error('source exceeds 256 KB')
 docker=shutil.which('docker')
 bwrap=shutil.which('bwrap') if sys.platform.startswith('linux') else None
 if docker:
  image={'python':'python:3.12-alpine','javascript':'node:22-alpine','shell':'alpine:3.20'}[a.language]
  if a.language=='python': run=['python3','-I','/work/source']
  elif a.language=='javascript': run=['node','--disable-proto=throw','/work/source']
  else: run=['/bin/sh','-eu','/work/source']
  cmd=[docker,'run','--rm','--network','none','--read-only','--tmpfs','/tmp:rw,noexec,nosuid,size=16m','--memory=256m','--cpus=1','--pids-limit=32','--cap-drop=ALL','--security-opt=no-new-privileges','--user=65534:65534','-v',str(src)+':/work/source:ro','-w','/tmp',image]+run
 elif bwrap:
  with tempfile.TemporaryDirectory(prefix='bookgen-exec-') as td:
   cmd=[bwrap,'--die-with-parent','--unshare-all','--new-session','--ro-bind','/usr','/usr']
   for d in ['/bin','/lib','/lib64','/usr/local']:
    if Path(d).exists() and d!='/usr': cmd += ['--ro-bind',d,d]
   cmd += ['--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/work','--ro-bind',str(src),'/work/source','--chdir','/tmp','--setenv','HOME','/tmp','--setenv','PATH','/usr/local/bin:/usr/bin:/bin','--setenv','LANG','C']
   if a.language=='python': run=[sys.executable,'-I','/work/source']
   elif a.language=='javascript':
    node=shutil.which('node')
    if not node: p.error('Node.js unavailable')
    run=[node,'--disable-proto=throw','/work/source']
   else: run=['/bin/sh','-eu','/work/source']
   cmd += run
   return run_isolated(cmd,a)
 else:
  print('REFUSED: no isolation runtime available. Install Docker or (Linux) bubblewrap; code was not executed.',file=sys.stderr); return 126
 return run_isolated(cmd,a)

def run_isolated(cmd,a):
 try:
  cp=subprocess.run(cmd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=a.timeout,check=False)
 except subprocess.TimeoutExpired:
  print('STATUS=TIMEOUT'); return 124
 out=cp.stdout[:a.max_output].decode('utf-8','replace'); err=cp.stderr[:a.max_output].decode('utf-8','replace')
 print('STATUS='+('SUCCESS' if cp.returncode==0 else 'FAILED'))
 print('EXIT_CODE='+str(cp.returncode)); print('--- STDOUT ---'); print(out); print('--- STDERR ---'); print(err)
 print('ISOLATION=network-disabled container or Linux namespace sandbox')
 return cp.returncode
if __name__=='__main__': sys.exit(main())
'''

VALIDATOR = r'''#!/usr/bin/env python3
"""Validate book project structure, illustration markers and catalogs."""
import argparse, re, sys
from pathlib import Path

def validate(root, lang=None):
 errors=[]; warnings=[]
 for req in ['AGENTS.md','opencode.json','config/project.md','config/editorial.md','config/workflow.md','docs/PROGRESS.md','docs/DECISIONS.md']:
  if not (root/req).is_file(): errors.append(f'Missing required file: {req}')
 langs=[root/'languages'/lang] if lang else sorted((root/'languages').glob('*')) if (root/'languages').exists() else []
 for ld in langs:
  if not ld.is_dir(): errors.append(f'Language directory missing: {ld}'); continue
  code=ld.name; cat=ld/'illustrations/ILLUSTRATIONS.md'
  briefdir=ld/'chapter-briefs'
  if not briefdir.is_dir(): errors.append(f'{code}: chapter-briefs directory missing')
  chapters_dir=ld/'chapters'
  for chapter in (chapters_dir.glob('CH*.md') if chapters_dir.exists() else []):
   brief=briefdir/(chapter.stem+'.md')
   if not brief.is_file(): errors.append(f'{code}: chapter {chapter.stem} has no detailed brief; drafting must follow an approved brief')
   else:
    btxt=brief.read_text(encoding='utf-8')
    status=re.search(r'^- \*\*Statut :\*\* `([^`]+)`',btxt,re.M)
    if not status or status.group(1)!='APPROVED': errors.append(f'{code}: chapter {chapter.stem} brief is not APPROVED')
  if not cat.is_file(): errors.append(f'{code}: illustration catalog missing'); continue
  text=cat.read_text(encoding='utf-8')
  ids=[]; paths=[]
  for line in text.splitlines():
   if not line.startswith('|') or line.startswith('|---') or 'ID |' in line: continue
   cols=[x.strip() for x in line.strip('|').split('|')]
   if len(cols)<8: continue
   iid, symbol, caption, desc, prompt, rel, mode, status=cols[:8]
   if not iid or iid.startswith('---'): continue
   if iid in ids: errors.append(f'{code}: duplicate illustration ID {iid}')
   ids.append(iid)
   if rel and rel.lower() not in ('chemin relatif','path'):
    p=(ld/'illustrations'/rel).resolve(); paths.append(p)
    if code not in p.name: errors.append(f'{code}: image path must include language code: {rel}')
    if not p.exists(): warnings.append(f'{code}: image missing: {p.relative_to(root)}')
    elif p.stat().st_size==0: warnings.append(f'{code}: empty placeholder image: {p.relative_to(root)}')
   if mode.lower() in ('ia','ai_prompt','prompt') and prompt.lower() in ('','null','à préparer'): warnings.append(f'{code}: AI illustration without prompt: {iid}')
  for ch in (ld/'chapters').glob('*.md') if (ld/'chapters').exists() else []:
   for marker in re.findall(r'\{\{ILL:([^}]+)\}\}',ch.read_text(encoding='utf-8')):
    if marker not in ids: errors.append(f'{code}: unresolved illustration marker {marker} in {ch.relative_to(root)}')
  if len(paths)!=len(set(paths)): errors.append(f'{code}: duplicate illustration image path in catalog')
  used_ids=set()
  for ch in (ld/'chapters').glob('*.md') if (ld/'chapters').exists() else []:
   used_ids.update(re.findall(r'\{\{ILL:([^}]+)\}\}',ch.read_text(encoding='utf-8')))
  for iid in ids:
   if iid not in used_ids: warnings.append(f'{code}: catalog illustration not referenced in chapter marker: {iid}')
  if not list((ld/'chapters').glob('CH*.md')): warnings.append(f'{code}: no chapter files yet')
 return errors,warnings

def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); p.add_argument('--lang'); a=p.parse_args(); root=Path(a.root).resolve(); errors,warnings=validate(root,a.lang)
 for x in errors: print('ERROR:',x)
 for x in warnings: print('WARNING:',x)
 print(f'RESULT: {len(errors)} error(s), {len(warnings)} warning(s)')
 return 1 if errors else 0
if __name__=='__main__': sys.exit(main())
'''
ASSEMBLER = r'''#!/usr/bin/env python3
"""Resolve illustration placeholders and concatenate approved chapters."""
import argparse, re, sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); p.add_argument('--lang',required=True); p.add_argument('--output'); a=p.parse_args(); root=Path(a.root).resolve(); ld=root/'languages'/a.lang
 if not ld.is_dir(): print('Language not found:',a.lang,file=sys.stderr); return 2
 cat=ld/'illustrations/ILLUSTRATIONS.md'; entries={}
 if cat.exists():
  for line in cat.read_text(encoding='utf-8').splitlines():
   if not line.startswith('|') or line.startswith('|---') or 'ID |' in line: continue
   c=[x.strip() for x in line.strip('|').split('|')]
   if len(c)>=8 and c[0]: entries[c[0]]=c[5]
 chapters=sorted((ld/'chapters').glob('CH*.md'))
 if not chapters: print('No CH*.md files found',file=sys.stderr); return 3
 out=['<!-- Generated file. Edit source chapters, not this file. -->',f'<!-- Language: {a.lang} -->','']
 unresolved=[]
 for f in chapters:
  content=f.read_text(encoding='utf-8')
  def repl(m):
   iid=m.group(1); rel=entries.get(iid)
   if not rel: unresolved.append((f.name,iid)); return f'**[ILLUSTRATION NOT CATALOGUED: {iid}]**'
   path=ld/'illustrations'/rel
   if not path.exists() or path.stat().st_size==0: unresolved.append((f.name,iid)); return f'**[ILLUSTRATION MISSING: {iid} ({rel})]**'
   return f'![{iid}](../illustrations/{rel})'
  out += [content.replace('\r\n','\n'), '']
  out[-2]=re.sub(r'\{\{ILL:([^}]+)\}\}',repl,out[-2])
 dest=Path(a.output).resolve() if a.output else ld/'manuscript'/'MANUSCRIPT.md'; dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists(): print('Refusing to overwrite existing file:',dest,file=sys.stderr); return 4
 dest.write_text('\n'.join(out).rstrip()+'\n',encoding='utf-8')
 print('Assembled:',dest)
 if unresolved:
  print('WARNING: unresolved/missing illustrations:')
  for x in unresolved: print(' -',x[0],x[1])
  return 5
 return 0
if __name__=='__main__': sys.exit(main())
'''
BUILDER = r'''#!/usr/bin/env python3
"""Build enabled PDF/EPUB deliverables with Pandoc; never invent unresolved specs."""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

PRINT_IDS={'pdf_print','pdf_print_screen','kdp_print','kdp_ebook','etsy_print','etsy_both'}

def size_vars(size):
 s=size.lower().replace('×','x').replace(',','.')
 if s=='a4': return ['-V','geometry:a4paper']
 if s=='a5': return ['-V','geometry:a5paper']
 m=re.search(r'([0-9.]+)\s*x\s*([0-9.]+)\s*pouces',s)
 if m: return ['-V',f'geometry:paperwidth={m.group(1)}in,paperheight={m.group(2)}in']
 m=re.search(r'([0-9.]+)\s*x\s*([0-9.]+)\s*(in|inch|inches|mm|cm|pouces)',s)
 if m:
  unit=m.group(3)
  unit='in' if unit in ('in','inch','inches','pouces') else unit
  return ['-V',f'geometry:paperwidth={m.group(1)}{unit},paperheight={m.group(2)}{unit}']
 return []

def margin_vars(margins):
 if margins.get('mode')!='manual': return None
 keys=['inner','outer','top','bottom']; vals=[]
 for k in keys:
  v=str(margins.get(k,'')).strip()
  if not re.fullmatch(r'[0-9]+(?:[.,][0-9]+)?\s*(mm|cm|in|pt)',v,re.I): return None
  vals.append(k+'='+v.replace(' ', '').replace(',', '.'))
 return ['-V','geometry:'+','.join(vals)]

def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); p.add_argument('--lang',required=True); p.add_argument('--format',choices=['pdf','epub','all'],default='all'); p.add_argument('--force',action='store_true'); a=p.parse_args(); root=Path(a.root).resolve(); ld=root/'languages'/a.lang
 manuscript=ld/'manuscript/MANUSCRIPT.md'; cfgfile=root/'config/generator-input.json'
 if not manuscript.is_file(): print('Manuscript missing. Run scripts/assemble.py first.',file=sys.stderr); return 2
 if not cfgfile.is_file(): print('config/generator-input.json missing; cannot determine enabled formats.',file=sys.stderr); return 2
 if not shutil.which('pandoc'): print('Pandoc not installed; build not performed.',file=sys.stderr); return 3
 cfg=json.loads(cfgfile.read_text(encoding='utf-8')); pub=cfg.get('publishing',{}); selected=pub.get('formats',[]); specs=pub.get('format_specs',{}); report={'language':a.lang,'created':[],'skipped':[],'errors':[],'notes':[]}
 want_pdf=a.format in ('pdf','all'); want_epub=a.format in ('epub','all')
 pdf_profiles=[]
 for fid in selected:
  if fid not in PRINT_IDS or not want_pdf: continue
  spec=specs.get(fid)
  if not spec: report['errors'].append(f'{fid}: print specification missing'); continue
  print_spec={k:v for k,v in spec.items() if k!='screen'}
  pdf_profiles.append((fid,'print',print_spec))
  if fid in ('pdf_print_screen','etsy_both') and spec.get('screen'):
   pdf_profiles.append((fid,'screen',{'size':spec['screen']['size'],'margins':spec['screen'].get('margins',{'mode':'not_applicable'})}))
 groups={}
 for fid,kind,spec in pdf_profiles:
  key=json.dumps({'kind':kind,'size':spec.get('size'),'margins':spec.get('margins')},sort_keys=True,ensure_ascii=False)
  groups.setdefault(key,{'spec':spec,'targets':[]})['targets'].append(f'{fid}:{kind}')
 for key,group in groups.items():
  spec=group['spec']; margins=spec.get('margins',{})
  if margins.get('mode')=='official_lookup':
   report['skipped'].append({'targets':group['targets'],'reason':'Official margins not resolved. Verify official specs and enter verified values before building.'}); continue
  if margins.get('mode') not in ('manual','not_applicable'):
   report['skipped'].append({'targets':group['targets'],'reason':'Margin mode not buildable until verified.'}); continue
  name='screen' if any(t.endswith(':screen') for t in group['targets']) else 'print'
  suffix='-'.join(sorted({t.split(':')[0] for t in group['targets']}))
  out=ld/'output'/f'{a.lang}-{name}-{suffix}.pdf'; out.parent.mkdir(parents=True,exist_ok=True)
  if out.exists() and not a.force: report['errors'].append(f'Refusing to overwrite {out}'); continue
  dimensions=size_vars(str(spec.get('size','')))
  if not dimensions: report['errors'].append(f'Unsupported or invalid page dimensions for {group["targets"]}: {spec.get("size")}'); continue
  cmd=['pandoc',str(manuscript),'-o',str(out),'--pdf-engine=xelatex']
  cmd+=dimensions
  if margins.get('mode')=='manual':
   mv=margin_vars(margins)
   if not mv: report['errors'].append(f'Invalid manual margins for {group["targets"]}'); continue
   cmd+=mv
  if not shutil.which('xelatex'): report['skipped'].append({'targets':group['targets'],'reason':'xelatex not installed'}); continue
  cp=subprocess.run(cmd,cwd=root,check=False)
  if cp.returncode: report['errors'].append(f'PDF build failed for {group["targets"]}: exit {cp.returncode}')
  else: report['created'].append({'path':str(out.relative_to(root)),'targets':group['targets'],'kind':'PDF'})
 if want_epub and ('epub' in selected or 'kdp_ebook' in selected):
  out=ld/'output'/f'{a.lang}-ebook.epub'; out.parent.mkdir(parents=True,exist_ok=True)
  if out.exists() and not a.force: report['errors'].append(f'Refusing to overwrite {out}')
  else:
   cp=subprocess.run(['pandoc',str(manuscript),'-o',str(out)],cwd=root,check=False)
   if cp.returncode: report['errors'].append(f'EPUB build failed: exit {cp.returncode}')
   else:
    targets=[x for x in ('epub','kdp_ebook') if x in selected]
    report['created'].append({'path':str(out.relative_to(root)),'targets':targets,'kind':'EPUB source deliverable'})
 if any(x in selected for x in ('kdp_print','kdp_ebook')): report['notes'].append('KDP upload acceptance is not tested. Verify final PDF, cover template, fonts, trim size, bleed and official current requirements.')
 if any(x in selected for x in ('etsy_print','etsy_both')): report['notes'].append('Etsy product listing and acceptance are not tested.')
 reportpath=ld/'output'/'BUILD_REPORT.json'
 if reportpath.exists() and not a.force: print('Refusing to overwrite report:',reportpath,file=sys.stderr); return 4
 reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 1 if report['errors'] else (3 if not report['created'] and report['skipped'] else 0)
if __name__=='__main__': sys.exit(main())
'''
STATUS = r'''#!/usr/bin/env python3
"""Print a factual status overview without claiming unfinished work is done."""
import argparse, re
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); a=p.parse_args(); root=Path(a.root).resolve()
 print('Project:',root)
 for ld in sorted((root/'languages').glob('*')) if (root/'languages').exists() else []:
  if not ld.is_dir(): continue
  chapters=list((ld/'chapters').glob('CH*.md')) if (ld/'chapters').exists() else []
  briefs=list((ld/'chapter-briefs').glob('CH*.md')) if (ld/'chapter-briefs').exists() else []
  approved=sum(1 for b in briefs if re.search(r'^- \*\*Statut :\*\* `APPROVED`',b.read_text(encoding='utf-8'),re.M))
  cat=ld/'illustrations/ILLUSTRATIONS.md'; manuscript=ld/'manuscript/MANUSCRIPT.md'
  outputs=list((ld/'output').glob('*')) if (ld/'output').exists() else []
  print(f'{ld.name}: briefs={len(briefs)} (approved={approved}), chapters={len(chapters)}, catalog={cat.exists()}, manuscript={manuscript.exists()}, outputs={len([x for x in outputs if x.is_file() and x.suffix.lower() in {".pdf",".epub",".docx",".html",".mobi"}])}')
 print('Review docs/PROGRESS.md for editorial status; filesystem presence is not proof of quality or platform acceptance.')
if __name__=='__main__': main()
'''

def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--non-interactive-config',help='JSON file containing a full config object for tests/automation'); ap.add_argument('--output',help='Target project directory (non-interactive or override)'); ap.add_argument('--force',action='store_true',help='Allow overwriting files in target; use only deliberately'); ap.add_argument('--version',action='version',version=VERSION); args=ap.parse_args()
 try:
  if args.non_interactive_config:
   config=json.loads(Path(args.non_interactive_config).read_text(encoding='utf-8'))
   if not args.output and not config.get('project_parent'): raise ValueError('project_parent or --output required')
   target=Path(args.output).resolve() if args.output else Path(config['project_parent'])/config['project_name']
  else:
   config=gather_config(args); target=Path(args.output).resolve() if args.output else Path(config['project_parent'])/config['project_name']
  if target.exists() and any(target.iterdir()) and not args.force:
   print(f'ERREUR : le dossier cible existe et n’est pas vide : {target}\nAucun fichier n’a été modifié. Choisissez un autre nom ou relancez avec --force après sauvegarde.',file=sys.stderr); return 2
  if target.exists() and args.force:
   print('ATTENTION : --force autorise le remplacement des fichiers générés portant les mêmes chemins, sans supprimer les fichiers supplémentaires.')
  target.mkdir(parents=True,exist_ok=True)
  # Preserve config entered at generation time for traceability.
  result=build_project(config,target,overwrite=args.force)
  print('\nProjet créé :',result)
  print('Étapes suivantes : ouvrir ce dossier puis lancer opencode; commencer par /book-plan.')
  print('Contrôle structurel : python scripts/validate_project.py --root .')
  return 0
 except (KeyboardInterrupt,UserAbort): print('\nAnnulé.',file=sys.stderr); return 130
 except Exception as e: print('ERREUR :',e,file=sys.stderr); return 1
if __name__=='__main__': sys.exit(main())
