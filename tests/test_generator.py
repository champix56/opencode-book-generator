import importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bookgen', ROOT/'generators/bookgen.py')
bookgen=importlib.util.module_from_spec(spec); spec.loader.exec_module(bookgen)

class GeneratorTests(unittest.TestCase):
    def config(self, parent, name='test-book'):
        return {
            'schema_version':1,'generator_version':'1.2.0','created_at_utc':'2026-10-19T00:00:00+00:00',
            'title':'Livre de test','subtitle':'','author':'Auteur Test','description':'Description de test',
            'book_type':'Guide pratique','audience':'Débutant','initial_language':'fr-FR','target_pages_approx':80,
            'technical_level':{'initial':0,'final':30},'fonts':'automatique','constraints':'aucune',
            'learning_features':['Aucun'],'code_display':[],
            'publishing':{'formats':['pdf_print','epub'],'format_specs':{'pdf_print':{'label':'PDF impression','size':'A5','margins':{'mode':'manual','inner':'18 mm','outer':'12 mm','top':'12 mm','bottom':'15 mm'}}},'layout':'Markdown + Pandoc + LaTeX'},
            'research_mode':'standalone','workflow_mode':'Enchaîner toutes les étapes sans arrêt','chapter_validation':'Automatique puis manuelle',
            'illustrations':[{'type':'explanatory_auto','label':'Illustrations explicatives','mode':'ai_prompt'}],
            'illustration_policy':'distinct_image_per_language','image_engine':'preparation_only','code_execution':'isolated_controlled','language_creation':'prepare_only',
            'git':{'enabled':False,'initial_commit':False},'project_parent':str(parent),'project_name':name
        }

    def test_generates_project_and_commands(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'
            bookgen.build_project(self.config(td), target)
            self.assertTrue((target/'AGENTS.md').exists())
            self.assertTrue((target/'config/generator-input.json').exists())
            self.assertTrue((target/'.opencode/commands/book-plan.md').exists())
            self.assertTrue((target/'.opencode/commands/scriptable-book-language-build.md').exists())
            self.assertTrue((target/'languages/fr-FR/illustrations/ILLUSTRATIONS.md').exists())
            self.assertIn('distinct_image_per_language',(target/'config/illustrations.md').read_text())

    def test_validator_accepts_fresh_project_with_warnings(self):
        specv=importlib.util.spec_from_file_location('validator', ROOT/'generators/bookgen.py')
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            # structural files should exist
            for name in ['AGENTS.md','opencode.json','config/project.md','config/editorial.md','config/workflow.md','docs/PROGRESS.md','docs/DECISIONS.md']:
                self.assertTrue((target/name).is_file(),name)

    def test_refuses_nonempty_target_without_force(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; target.mkdir(); (target/'keep.txt').write_text('keep')
            with self.assertRaises(FileExistsError):
                bookgen.write_file(target,'keep.txt','overwrite',force=False)
            self.assertEqual((target/'keep.txt').read_text(),'keep')


    def test_prepare_user_illustration_creates_empty_placeholder_only_if_missing(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td), target)
            script=target/'scripts/prepare_illustration.py'
            cmd=['python3',str(script),'--root',str(target),'--lang','fr-FR','--id','ILL-CH001-001','--filename','ILL-CH001-001-fr-FR.png','--mode','user_provided']
            cp=subprocess.run(cmd,text=True,capture_output=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            image=target/'languages/fr-FR/illustrations/images/ILL-CH001-001-fr-FR.png'
            self.assertTrue(image.exists()); self.assertEqual(image.stat().st_size,0)
            image.write_bytes(b'actual-image')
            cp=subprocess.run(cmd,text=True,capture_output=True)
            self.assertNotEqual(cp.returncode,0)
            self.assertEqual(image.read_bytes(),b'actual-image')

    def test_language_creation_command_does_not_request_automatic_translation(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td), target)
            body=(target/'.opencode/commands/book-language-create.md').read_text()
            self.assertIn('Ne traduis rien',body)
            self.assertIn('chemin image distinct',body)


    def test_all_generated_python_scripts_compile_and_command_dry_run(self):
        import py_compile, subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td), target)
            for script in (target/'scripts').rglob('*.py'):
                py_compile.compile(str(script),doraise=True)
            cp=subprocess.run(['python3',str(target/'scripts/invoke_command.py'),'scriptable-book-plan','--root',str(target),'--args','initial plan','--dry-run'],text=True,capture_output=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            self.assertIn('initial plan',cp.stdout)

    def test_project_validator_script_reports_clean_structure(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td), target)
            cp=subprocess.run(['python3',str(target/'scripts/validate_project.py'),'--root',str(target)],text=True,capture_output=True)
            self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
            self.assertIn('0 error(s)',cp.stdout)


    def test_assembler_reports_missing_image_instead_of_claiming_success(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td), target)
            chapter=target/'languages/fr-FR/chapters/CH001.md'
            chapter.write_text('# Chapitre test\n\nCette illustration est requise pour expliquer le sujet au lecteur.\n\n{{ILL:ILL-CH001-001}}\n',encoding='utf-8')
            cat=target/'languages/fr-FR/illustrations/ILLUSTRATIONS.md'
            cat.write_text('# Catalogue\n\n| ID | Symbole | Légende | Description | Prompt | Chemin relatif | Mode | Statut |\n|---|---|---|---|---|---|---|---|\n| ILL-CH001-001 | ◇ | Test | Description | null | images/ILL-CH001-001-fr-FR.png | user_provided | PLACEHOLDER_EMPTY |\n',encoding='utf-8')
            cp=subprocess.run(['python3',str(target/'scripts/assemble.py'),'--root',str(target),'--lang','fr-FR'],text=True,capture_output=True)
            self.assertEqual(cp.returncode,5,cp.stdout+cp.stderr)
            manuscript=target/'languages/fr-FR/manuscript/MANUSCRIPT.md'
            self.assertIn('ILLUSTRATION MISSING',manuscript.read_text(encoding='utf-8'))


    def test_questionnaire_has_no_preset_editorial_answers_and_accepts_custom_values(self):
        from unittest.mock import patch
        from contextlib import redirect_stdout
        import io
        answers=[
            'My custom title','', 'Pen name','A fully custom description', '14','My bespoke book type',
            '10','A very specific audience','en-US','137','12','77','My chosen font','No constraints',
            '0','n','1,3',
            '1','2','15 mm','12 mm','12 mm','15 mm',
            '1','2','15 mm','12 mm','12 mm','15 mm',
            '3','1','3','3','0','n','/tmp','my custom folder'
        ]
        with patch('builtins.input',side_effect=answers), redirect_stdout(io.StringIO()):
            cfg=bookgen.gather_config(None)
        self.assertEqual(cfg['title'],'My custom title')
        self.assertEqual(cfg['book_type'],'My bespoke book type')
        self.assertEqual(cfg['audience'],'A very specific audience')
        self.assertEqual(cfg['initial_language'],'en-US')
        self.assertEqual(cfg['target_pages_approx'],137)
        self.assertEqual(cfg['publishing']['formats'],['pdf_print','kdp_print'])
        self.assertEqual(cfg['project_name'],'my-custom-folder')


    def test_chapter_brief_workflow_is_generated_and_gates_drafting(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            briefdir=target/'languages/fr-FR/chapter-briefs'
            self.assertTrue((briefdir/'README.md').is_file())
            self.assertTrue((briefdir/'INDEX.md').is_file())
            self.assertTrue((target/'templates/chapters/CHAPTER_BRIEF_TEMPLATE.md').is_file())
            create=(target/'.opencode/commands/book-chapter-brief.md').read_text(encoding='utf-8')
            edit=(target/'.opencode/commands/book-chapter-brief-edit.md').read_text(encoding='utf-8')
            chapter=(target/'.opencode/commands/book-chapter.md').read_text(encoding='utf-8')
            self.assertIn('aucune correction ni solution',create)
            self.assertIn('plan éditorial intermédiaire',create)
            self.assertIn('supprimer',edit)
            self.assertIn('APPROVED',chapter)
            self.assertTrue((target/'.opencode/commands/scriptable-book-chapter-brief.md').is_file())
            self.assertTrue((target/'.opencode/commands/scriptable-book-chapter-brief-edit.md').is_file())
            self.assertIn('APPROVED', (target/'AGENTS.md').read_text(encoding='utf-8'))

    def test_chapter_brief_helper_init_list_validate_and_no_overwrite(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            helper=target/'scripts/chapter_briefs.py'
            cp=subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','init','--chapter','CH001'],text=True,capture_output=True)
            self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
            brief=target/'languages/fr-FR/chapter-briefs/CH001.md'
            self.assertIn('Énoncé destiné au lecteur',brief.read_text(encoding='utf-8'))
            self.assertNotIn('Corrigé attendu / solution de référence',brief.read_text(encoding='utf-8'))
            cp2=subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','init','--chapter','CH001'],text=True,capture_output=True)
            self.assertEqual(cp2.returncode,3)
            cp3=subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','list'],text=True,capture_output=True)
            self.assertEqual(cp3.returncode,0,cp3.stderr); self.assertIn('CH001',cp3.stdout); self.assertIn('DRAFT',cp3.stdout)
            cp4=subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','validate'],text=True,capture_output=True)
            self.assertEqual(cp4.returncode,0,cp4.stdout+cp4.stderr)


    def test_validator_blocks_chapter_without_approved_brief(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            (target/'languages/fr-FR/chapters/CH001.md').write_text('# Chapitre sans brief approuvé\n',encoding='utf-8')
            cp=subprocess.run(['python3',str(target/'scripts/validate_project.py'),'--root',str(target)],text=True,capture_output=True)
            self.assertEqual(cp.returncode,1,cp.stdout+cp.stderr)
            self.assertIn('no detailed brief',cp.stdout)

    def test_generated_project_contains_multiplatform_python_environment_scripts_and_tutorial(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            for name in ['scripts/setup_venv.sh','scripts/setup_venv.bat','scripts/setup_venv.ps1',
                         'scripts/install.sh','scripts/install.bat','scripts/install.ps1',
                         'scripts/run_python.sh','scripts/run_python.bat','scripts/run_python.ps1',
                         'scripts/requirements.txt','scripts/platform/run-opencode.sh',
                         'scripts/platform/run-opencode.bat','scripts/platform/run-opencode.ps1']:
                self.assertTrue((target/name).is_file(),name)
            readme=(target/'README.md').read_text(encoding='utf-8')
            for marker in ['Étape 1 : prérequis et installation','Étape 4 : préparer puis approuver les briefs synthétiques',
                           'Étape 10 : compiler les livrables','scripts/run_python.sh','scripts/install.bat']:
                self.assertIn(marker,readme)
            self.assertIn('💡 Explication imagée',(target/'prompts/writing/CHAPTER.md').read_text(encoding='utf-8'))
            import subprocess
            for shell_script in target.rglob('*.sh'):
                cp=subprocess.run(['bash','-n',str(shell_script)],text=True,capture_output=True)
                self.assertEqual(cp.returncode,0,f'{shell_script}: {cp.stderr}')

    def test_chapter_brief_approval_requires_explicit_flag_and_updates_index(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            helper=target/'scripts/chapter_briefs.py'
            subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','init','--chapter','CH001'],check=True,capture_output=True,text=True)
            brief=target/'languages/fr-FR/chapter-briefs/CH001.md'
            body=brief.read_text(encoding='utf-8')
            body=body.replace('À définir depuis le sommaire','Fondamentaux')
            body=body.replace('À définir en une ou deux phrases','Comprendre les notions essentielles.')
            body=body.replace('À définir brièvement','Aucun').replace('À définir','éléments définis').replace('À compléter','complété').replace('À renseigner','fr-FR')
            body=body.replace('### 2.1 Point à définir','### 2.1 Comprendre la notion centrale')
            body=body.replace('- **Notions / sous-points :**','- **Notions / sous-points :** définition et application')
            body=body.replace('- **Intention de traitement (résumé bref, pas le texte final) :**','- **Intention de traitement (résumé bref, pas le texte final) :** présenter les bases et leurs usages')
            body=body.replace('### VIS-CH001-01 : Type et titre court','Aucun selon la configuration')
            body=body.replace("### EX-CH001-01 : Titre de l'exercice",'Aucun selon la configuration')
            body=body.replace('- [ ]','- [x]')
            brief.write_text(body,encoding='utf-8')
            refused=subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','approve','--chapter','CH001'],text=True,capture_output=True)
            self.assertEqual(refused.returncode,5)
            approved=subprocess.run(['python3',str(helper),'--root',str(target),'--lang','fr-FR','--action','approve','--chapter','CH001','--confirm-approval'],text=True,capture_output=True)
            self.assertEqual(approved.returncode,0,approved.stdout+approved.stderr)
            self.assertIn('`APPROVED`',brief.read_text(encoding='utf-8'))
            self.assertIn('| CH001 | CH001.md | APPROVED |',(target/'languages/fr-FR/chapter-briefs/INDEX.md').read_text(encoding='utf-8'))

    def test_assembler_refuses_outline_only_chapter(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            (target/'languages/fr-FR/chapters/CH001.md').write_text('# Chapitre vide\n\n- Point à développer\n',encoding='utf-8')
            cp=subprocess.run(['python3',str(target/'scripts/assemble.py'),'--root',str(target),'--lang','fr-FR'],text=True,capture_output=True)
            self.assertEqual(cp.returncode,6,cp.stdout+cp.stderr)
            self.assertIn('without prose paragraphs',cp.stderr)
            self.assertFalse((target/'languages/fr-FR/manuscript/MANUSCRIPT.md').exists())

    def test_validator_warns_when_chapter_is_only_an_outline(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'book'; bookgen.build_project(self.config(td),target)
            briefdir=target/'languages/fr-FR/chapter-briefs'; briefdir.mkdir(exist_ok=True)
            brief=(target/'templates/chapters/CHAPTER_BRIEF_TEMPLATE.md').read_text(encoding='utf-8').replace('CHXXX','CH001').replace('À renseigner','fr-FR').replace('`DRAFT`','`APPROVED`')
            (briefdir/'CH001.md').write_text(brief,encoding='utf-8')
            (target/'languages/fr-FR/chapters/CH001.md').write_text('# Chapitre 1\n\n- Définition\n- Exemple\n',encoding='utf-8')
            cp=subprocess.run(['python3',str(target/'scripts/validate_project.py'),'--root',str(target)],text=True,capture_output=True)
            self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
            self.assertIn('only',cp.stdout)
            self.assertIn('no prose paragraphs',cp.stdout)

    def test_language_catalogs_are_per_language(self):
        files=bookgen.make_language_files('es-ES',self.config('/tmp'),False)
        self.assertIn('languages/es-ES/illustrations/ILLUSTRATIONS.md',files)
        self.assertIn('languages/es-ES/language.json',files)
        self.assertIn('"content_generation_on_create": false',files['languages/es-ES/language.json'])

if __name__=='__main__': unittest.main()
