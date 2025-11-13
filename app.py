# Fichier: app.py (Dashboard Multi-Datasets - Détection Intelligente)

import streamlit as st
import pandas as pd
import papermill as pm
import nbformat
import tempfile
import os
import base64
import json
import time
import plotly.graph_objects as go
import re

# --- Configuration de la page ---
st.set_page_config(
    page_title="Tableau de Bord Multi-Datasets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Injection de CSS Personnalisé ---
def load_custom_css():
    """Injecte du CSS personnalisé pour une apparence professionnelle et moderne."""
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #FFFFFF !important;
                background-color: #F9FAFB;
            }
            
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
                border-right: 2px solid #2d3748;
                padding: 0;
                box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
            }
            
            [data-testid="stSidebar"] .sidebar-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                text-align: center;
                padding: 2rem 1rem;
                margin-bottom: 0;
                border-bottom: 3px solid #818CF8;
            }
            
            [data-testid="stSidebar"] .sidebar-header i {
                font-size: 3em;
                color: #FFFFFF;
                margin-bottom: 0.5rem;
                display: block;
            }
            
            [data-testid="stSidebar"] .sidebar-header h2 {
                color: #FFFFFF !important;
                margin: 0;
                font-size: 1.3em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            [data-testid="stSidebar"] .sidebar-section {
                padding: 1.5rem 1rem;
                border-bottom: 1px solid #2d3748;
            }
            
            [data-testid="stSidebar"] h3 {
                color: #818CF8 !important;
                font-size: 0.85em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin-bottom: 1rem;
                padding-left: 0.5rem;
                border-left: 3px solid #818CF8;
            }
            
            [data-testid="stSidebar"] * {
                color: #E5E7EB !important;
            }
            
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
                color: #FFFFFF !important;
            }
            
            [data-testid="stSidebar"] [data-testid="stFileUploader"] {
                background-color: #1f2937;
                border: 2px dashed #4B5563;
                border-radius: 8px;
                padding: 1rem;
                transition: all 0.3s ease;
            }
            
            [data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
                border-color: #818CF8;
                background-color: #374151;
                transform: translateY(-2px);
            }
            
            [data-testid="stSidebar"] .stSuccess {
                background-color: rgba(16, 185, 129, 0.15) !important;
                color: #6EE7B7 !important;
                border-left: 4px solid #10B981;
                padding: 0.75rem;
                border-radius: 6px;
                font-size: 0.9em;
            }
            
            [data-testid="stSidebar"] .stButton > button {
                background: linear-gradient(135deg, #818CF8 0%, #6366F1 100%);
                color: white !important;
                font-weight: 700;
                border: none;
                box-shadow: 0 4px 15px rgba(129, 140, 248, 0.5);
                padding: 0.75rem 1.5rem;
                font-size: 1em;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
            }
            
            [data-testid="stSidebar"] .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 25px rgba(129, 140, 248, 0.7);
            }
            
            .main .block-container {
                max-width: 1400px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2.5rem 2rem;
                border-radius: 16px;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            }
            
            .dashboard-header h1 {
                color: white;
                font-size: 2.5em;
                font-weight: 700;
                margin: 0;
            }
            
            .dashboard-section {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                margin-bottom: 1.5rem;
                border: 1px solid #E5E7EB;
            }
            
            .section-header {
                display: flex;
                align-items: center;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #F3F4F6;
            }
            
            .section-header i {
                font-size: 1.5em;
                color: #667eea;
                margin-right: 0.75rem;
            }
            
            .section-header h2 {
                color: #111827 !important;
                font-size: 1.5em;
                font-weight: 600;
                margin: 0;
            }
            
            .info-card {
                background: linear-gradient(135deg, #374151 0%, #1F2937 100%);
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                border: 1px solid #4B5563;
                margin-bottom: 1rem;
                transition: all 0.3s ease;
            }
            
            .info-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
                border-color: #818CF8;
            }
            
            .info-card i {
                font-size: 2em;
                color: #818CF8;
                margin-bottom: 0.75rem;
                display: block;
            }
            
            .info-card h3 {
                color: #FFFFFF !important;
                font-size: 1.1em;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .info-card p {
                color: #D1D5DB !important;
                font-size: 0.95em;
                line-height: 1.6;
                margin: 0;
            }
            
            .stat-card {
                background: #374151;
                padding: 1.25rem;
                border-radius: 10px;
                border-left: 4px solid #818CF8;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            }
            
            .stat-card i {
                font-size: 1.75em;
                color: #818CF8;
                margin-bottom: 0.5rem;
            }
            
            .stat-value {
                font-size: 1.75em;
                font-weight: 700;
                color: #FFFFFF !important;
                margin: 0.25rem 0;
            }
            
            .stat-label {
                font-size: 0.9em;
                color: #D1D5DB !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 500;
            }
            
            .stSuccess {
                background-color: #D1FAE5 !important;
                color: #065F46 !important;
                border-left: 4px solid #10B981;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stError {
                background-color: #FEE2E2 !important;
                color: #991B1B !important;
                border-left: 4px solid #EF4444;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stWarning {
                background-color: #FEF3C7 !important;
                color: #92400E !important;
                border-left: 4px solid #F59E0B;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stInfo {
                background-color: #DBEAFE !important;
                color: #1E40AF !important;
                border-left: 4px solid #3B82F6;
                padding: 1rem;
                border-radius: 8px;
            }
            
            [data-testid="stExpander"] {
                background-color: #374151 !important;
                border: 1px solid #4B5563;
                border-radius: 8px;
                margin-bottom: 1rem;
            }
            
            [data-testid="stExpander"] summary {
                color: #FFFFFF !important;
            }
            
            [data-testid="stDataFrame"] {
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                border: 1px solid #E5E7EB;
            }
            
            .stProgress > div > div {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(icon_class, title):
    """Affiche un en-tête de section avec icône."""
    st.markdown(f"""
        <div class="section-header">
            <i class="{icon_class}"></i>
            <h2>{title}</h2>
        </div>
    """, unsafe_allow_html=True)


def info_card_icon(icon_class, title, description):
    """Affiche une carte d'information avec icône."""
    st.markdown(f"""
        <div class="info-card">
            <i class="{icon_class}"></i>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)


def stat_card(icon_class, value, label):
    """Affiche une carte de statistique."""
    st.markdown(f"""
        <div class="stat-card">
            <i class="{icon_class}"></i>
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def detect_dataset_role(filename, df):
    """
    Détecte intelligemment le rôle d'un dataset (train, test, validation, etc.)
    basé sur le nom du fichier et les caractéristiques du dataset.
    """
    filename_lower = filename.lower()
    
    # Patterns pour détecter le rôle
    train_patterns = ['train', 'training', 'entrainement', 'apprentissage', 'fit']
    test_patterns = ['test', 'testing', 'eval', 'evaluation', 'validation']
    
    # Vérification par nom de fichier
    for pattern in train_patterns:
        if pattern in filename_lower:
            return 'train'
    
    for pattern in test_patterns:
        if pattern in filename_lower:
            return 'test'
    
    # Si aucun pattern détecté, essayer de deviner par la taille
    # (généralement train > test)
    return 'unknown'


def adapt_notebook_for_multiple_datasets(notebook_file, dataset_files_dict):
    """
    Adapte automatiquement le notebook pour utiliser plusieurs datasets.
    dataset_files_dict: {'train': path, 'test': path, ...}
    """
    try:
        # Lire le notebook
        if hasattr(notebook_file, 'read'):
            notebook_file.seek(0)
            notebook_content = notebook_file.read()
        else:
            notebook_content = notebook_file
        
        if isinstance(notebook_content, bytes):
            notebook_content = notebook_content.decode('utf-8')
        
        nb = nbformat.reads(notebook_content, as_version=4)
        
        # Patterns à détecter pour l'upload de fichiers
        upload_patterns = [
            r'files\.upload\(\)',
            r'input\(',
            r'st\.file_uploader',
            r'FileUpload',
            r'pd\.read_csv\s*\(',
            r'pd\.read_excel\s*\(',
            r'open\s*\(',
        ]
        
        # Créer la cellule d'injection pour TOUS les datasets
        datasets_code = "# 🔄 CELLULE INJECTÉE AUTOMATIQUEMENT PAR LE DASHBOARD\n"
        datasets_code += "# Chargement automatique de TOUS les datasets uploadés\n\n"
        datasets_code += "import pandas as pd\nimport os\nimport matplotlib.pyplot as plt\nimport warnings\n"
        datasets_code += "warnings.filterwarnings('ignore')\n\n"
        datasets_code += "# Configuration matplotlib\nimport matplotlib\n"
        datasets_code += "matplotlib.use('Agg')\nplt.ioff()\n\n"
        datasets_code += "print('='*70)\nprint('✅ CHARGEMENT DES DATASETS')\nprint('='*70)\n\n"
        
        # Charger chaque dataset
        for role, path in dataset_files_dict.items():
            datasets_code += f"# Chargement du dataset: {role}\n"
            datasets_code += f"DATASET_{role.upper()}_PATH = r'{path}'\n"
            datasets_code += f"if os.path.exists(DATASET_{role.upper()}_PATH):\n"
            datasets_code += f"    file_ext = os.path.splitext(DATASET_{role.upper()}_PATH)[1].lower()\n"
            datasets_code += f"    if file_ext == '.csv':\n"
            datasets_code += f"        {role} = pd.read_csv(DATASET_{role.upper()}_PATH)\n"
            datasets_code += f"    elif file_ext in ['.xlsx', '.xls']:\n"
            datasets_code += f"        {role} = pd.read_excel(DATASET_{role.upper()}_PATH)\n"
            datasets_code += f"    elif file_ext == '.json':\n"
            datasets_code += f"        {role} = pd.read_json(DATASET_{role.upper()}_PATH)\n"
            datasets_code += f"    elif file_ext == '.parquet':\n"
            datasets_code += f"        {role} = pd.read_parquet(DATASET_{role.upper()}_PATH)\n"
            datasets_code += f"    else:\n"
            datasets_code += f"        {role} = pd.read_csv(DATASET_{role.upper()}_PATH)\n"
            datasets_code += f"    print(f'✓ {role.upper()}: {{{role}.shape[0]}} lignes × {{{role}.shape[1]}} colonnes')\n"
            datasets_code += f"else:\n"
            datasets_code += f"    print(f'❌ Fichier {role} introuvable')\n"
            datasets_code += f"    {role} = pd.DataFrame()\n\n"
        
        # Créer aussi 'df' pour compatibilité (pointe vers train si disponible)
        if 'train' in dataset_files_dict:
            datasets_code += "# Variable 'df' pour compatibilité\ndf = train.copy()\n\n"
        elif dataset_files_dict:
            first_role = list(dataset_files_dict.keys())[0]
            datasets_code += f"# Variable 'df' pour compatibilité\ndf = {first_role}.copy()\n\n"
        
        datasets_code += "print('\\n📋 Variables créées:')\n"
        for role in dataset_files_dict.keys():
            datasets_code += f"print(f'   • {role}: {{{role}.shape}}')\n"
        datasets_code += "if 'df' in locals():\n    print(f'   • df: {{df.shape}}')\n"
        datasets_code += "print('='*70)\n\n"
        
        # Afficher aperçu du premier dataset
        first_role = list(dataset_files_dict.keys())[0]
        datasets_code += f"print('\\n📊 Aperçu du dataset {first_role}:')\n"
        datasets_code += f"display({first_role}.head())\n"
        datasets_code += f"print('\\n🔍 Colonnes de {first_role}:')\n"
        datasets_code += f"for i, col in enumerate({first_role}.columns, 1):\n"
        datasets_code += f"    print(f'   {{i:2d}}. {{col}}')\n"
        
        injection_cell = nbformat.v4.new_code_cell(source=datasets_code)
        
        # Traiter les cellules du notebook
        modified_cells = []
        injection_done = False
        has_imports = False
        
        if not nb.cells or len(nb.cells) == 0:
            st.warning("⚠️ Le notebook semble vide.")
            nb.cells = [injection_cell]
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb", mode='w', encoding='utf-8') as temp_nb:
                nbformat.write(nb, temp_nb)
                modified_notebook_path = temp_nb.name
            
            return modified_notebook_path
        
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                cell_source = cell.source
                
                if 'import' in cell_source.lower():
                    has_imports = True
                
                is_upload_cell = any(re.search(pattern, cell_source) for pattern in upload_patterns)
                
                if is_upload_cell:
                    commented_source = '\n'.join([f'# {line}' for line in cell_source.split('\n')])
                    cell.source = f"""
# ⚠️ CELLULE DÉSACTIVÉE AUTOMATIQUEMENT PAR LE DASHBOARD
# Lecture de fichier remplacée par les datasets uploadés
# Variables disponibles: {', '.join(dataset_files_dict.keys())}

{commented_source}
"""
                    st.info(f"📝 Cellule #{i+1} adaptée: Lecture de fichier désactivée")
                
                if not injection_done and has_imports and 'import' in cell_source.lower():
                    modified_cells.append(cell)
                    modified_cells.append(injection_cell)
                    injection_done = True
                    continue
                
                modified_cells.append(cell)
            else:
                modified_cells.append(cell)
        
        if not injection_done:
            modified_cells.insert(0, injection_cell)
            st.info("📝 Cellule d'injection ajoutée au début du notebook")
        
        nb.cells = modified_cells
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb", mode='w', encoding='utf-8') as temp_nb:
            nbformat.write(nb, temp_nb)
            modified_notebook_path = temp_nb.name
        
        return modified_notebook_path
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'adaptation du notebook: {str(e)}")
        import traceback
        with st.expander("🔍 Trace complète de l'erreur"):
            st.code(traceback.format_exc())
        raise e


def render_notebook(notebook_path):
    """Lit et affiche les sorties du notebook."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        section_header("fas fa-chart-line", "Résultats de l'analyse")
        
        cell_number = 1
        total_cells = len([cell for cell in nb.cells if cell.cell_type == 'code'])
        
        st.info(f"📊 Le notebook contient {total_cells} cellules de code.")
        
        for i, cell in enumerate(nb.cells):
            
            if cell.cell_type == 'markdown':
                st.markdown(cell.source)
                
            elif cell.cell_type == 'code':
                with st.expander(f"💻 Code de la cellule #{cell_number}", expanded=False):
                    st.code(cell.source, language='python')
                
                if not cell.outputs:
                    st.caption(f"ℹ️ Cellule #{cell_number}: Pas de sortie")
                    cell_number += 1
                    continue
                
                has_output = False
                
                for output in cell.outputs:
                    if output.output_type == 'stream':
                        if hasattr(output, 'text') and output.text.strip():
                            st.text(output.text)
                            has_output = True
                    
                    elif output.output_type in ('display_data', 'execute_result'):
                        data = output.data
                        
                        if 'image/png' in data:
                            try:
                                img_data = base64.b64decode(data['image/png'])
                                st.image(img_data, use_column_width=True, caption=f"📈 Figure #{cell_number}")
                                has_output = True
                                continue
                            except Exception as e:
                                st.warning(f"⚠️ Impossible d'afficher l'image: {str(e)}")
                        
                        if 'image/jpeg' in data:
                            try:
                                img_data = base64.b64decode(data['image/jpeg'])
                                st.image(img_data, use_column_width=True)
                                has_output = True
                                continue
                            except:
                                pass
                        
                        if 'application/vnd.plotly.v1+json' in data:
                            try:
                                plotly_data = data['application/vnd.plotly.v1+json']
                                if isinstance(plotly_data, str):
                                    plotly_dict = json.loads(plotly_data)
                                else:
                                    plotly_dict = dict(plotly_data)
                                
                                fig = go.Figure(
                                    data=plotly_dict.get('data', []),
                                    layout=plotly_dict.get('layout', {})
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                has_output = True
                                continue
                            except:
                                pass
                        
                        if 'text/html' in data:
                            html_content = data['text/html']
                            if '<div' in html_content or '<table' in html_content:
                                if 'plotly' not in html_content.lower():
                                    st.markdown(html_content, unsafe_allow_html=True)
                                    has_output = True
                                    continue
                        
                        if 'text/plain' in data:
                            text_content = data['text/plain']
                            if (not text_content.startswith('<') and 
                                len(text_content.strip()) > 0 and
                                'Figure' not in text_content and
                                'matplotlib.figure.Figure' not in text_content):
                                
                                if '\n' in text_content and len(text_content) < 5000:
                                    st.text(text_content)
                                    has_output = True
                    
                    elif output.output_type == 'error':
                        st.error(f"❌ Erreur cellule #{cell_number}: {output.ename} - {output.evalue}")
                        with st.expander("🔍 Trace complète"):
                            st.code('\n'.join(output.traceback))
                        has_output = True
                
                if not has_output:
                    st.caption(f"ℹ️ Cellule #{cell_number}: Code exécuté sans sortie visible")
                
                st.markdown("---")
                cell_number += 1
        
        st.success(f"✅ Toutes les {total_cells} cellules ont été exécutées!")
        st.markdown('</div>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("⚠️ Le fichier de résultats n'a pas encore été généré.")
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du notebook: {e}")
        with st.expander("🔍 Détails"):
            import traceback
            st.code(traceback.format_exc())


def execute_notebook_job(notebook_file, dataset_files_dict):
    """Exécute le notebook avec plusieurs datasets."""
    adapted_notebook_path = None
    dataset_paths = {}
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📁 Préparation des fichiers...")
        progress_bar.progress(10)
        time.sleep(0.3)
        
        # Sauvegarder tous les datasets
        for role, file_obj in dataset_files_dict.items():
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_obj.name)[1]) as temp_file:
                temp_file.write(file_obj.getvalue())
                dataset_paths[role] = temp_file.name
        
        status_text.text("🔧 Adaptation automatique du notebook...")
        progress_bar.progress(30)
        time.sleep(0.3)
        
        adapted_notebook_path = adapt_notebook_for_multiple_datasets(notebook_file, dataset_paths)
        
        status_text.text("▶️ Exécution de l'analyse en cours...")
        progress_bar.progress(50)
        
        output_path = os.path.join(tempfile.gettempdir(), f"output_{int(time.time())}.ipynb")
        
        pm.execute_notebook(
            input_path=adapted_notebook_path,
            output_path=output_path,
            kernel_name='python3',
            progress_bar=False,
            request_save_on_cell_execute=True,
            autosave_cell_every=1
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Analyse terminée avec succès!")
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()
        
        st.session_state['output_notebook_path'] = output_path
        st.success("🎉 L'exécution du notebook est terminée avec succès!")
        
    except pm.PapermillExecutionError as e:
        progress_bar.empty()
        status_text.empty()
        
        error_msg = str(e)
        if "ModuleNotFoundError" in error_msg:
            module_name = error_msg.split("'")[1] if "'" in error_msg else "unknown"
            st.error(f"""
            **❌ Module manquant: {module_name}**
            
            Solution: `pip install {module_name}`
            """)
        else:
            st.error(f"❌ Erreur lors de l'exécution: {str(e)}")
        
        with st.expander("🔍 Détails de l'erreur"):
            st.code(error_msg)
        
        st.session_state['output_notebook_path'] = None
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Erreur inattendue: {str(e)}")
        with st.expander("🔍 Trace complète"):
            import traceback
            st.code(traceback.format_exc())
        st.session_state['output_notebook_path'] = None
        
    finally:
        if adapted_notebook_path and os.path.exists(adapted_notebook_path):
            try:
                os.remove(adapted_notebook_path)
            except:
                pass
        for path in dataset_paths.values():
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass


# --- Interface Utilisateur ---
load_custom_css()

if 'output_notebook_path' not in st.session_state:
    st.session_state.output_notebook_path = None
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False
if 'uploaded_datasets' not in st.session_state:
    st.session_state.uploaded_datasets = {}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <i class="fas fa-database"></i>
            <h2>Dashboard Multi-Datasets</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Section Upload Notebook
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-file-code'></i> Notebook", unsafe_allow_html=True)
    
    uploaded_notebook = st.file_uploader(
        "Sélectionnez votre notebook Jupyter",
        type=['ipynb'],
        help="N'importe quel notebook Jupyter (.ipynb)",
        label_visibility="collapsed",
        key="notebook_upload"
    )
    
    if uploaded_notebook:
        st.success(f"✓ {uploaded_notebook.name}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Section Upload Datasets (MULTIPLE)
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-database'></i> Datasets", unsafe_allow_html=True)
    
    st.markdown("**Dataset d'entraînement (Train)**")
    train_dataset = st.file_uploader(
        "Dataset Train",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="Données d'entraînement",
        label_visibility="collapsed",
        key="train_upload"
    )
    
    if train_dataset:
        st.success(f"✓ {train_dataset.name}")
        st.session_state.uploaded_datasets['train'] = train_dataset
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Dataset de test (Test)**")
    test_dataset = st.file_uploader(
        "Dataset Test",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="Données de test",
        label_visibility="collapsed",
        key="test_upload"
    )
    
    if test_dataset:
        st.success(f"✓ {test_dataset.name}")
        st.session_state.uploaded_datasets['test'] = test_dataset
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Dataset de validation (optionnel)**")
    val_dataset = st.file_uploader(
        "Dataset Validation",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="Données de validation (optionnel)",
        label_visibility="collapsed",
        key="val_upload"
    )
    
    if val_dataset:
        st.success(f"✓ {val_dataset.name}")
        st.session_state.uploaded_datasets['validation'] = val_dataset
    
    # Détection automatique si les noms ne correspondent pas
    if train_dataset or test_dataset:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🤖 Détection automatique", expanded=False):
            st.caption("Le système détecte automatiquement le rôle de chaque dataset basé sur son nom de fichier.")
            if train_dataset:
                detected_train = detect_dataset_role(train_dataset.name, None)
                st.write(f"• Train: `{detected_train}` détecté")
            if test_dataset:
                detected_test = detect_dataset_role(test_dataset.name, None)
                st.write(f"• Test: `{detected_test}` détecté")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Bouton d'action
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    
    # Compter les datasets uploadés
    datasets_count = len([d for d in [train_dataset, test_dataset, val_dataset] if d is not None])
    
    if datasets_count > 0:
        st.info(f"📊 {datasets_count} dataset(s) chargé(s)")
    
    if st.button("🚀 LANCER L'ANALYSE", type="primary", use_container_width=True, key="run_analysis_btn"):
        if uploaded_notebook and len(st.session_state.uploaded_datasets) > 0:
            st.session_state.analysis_run = True
            
            # Créer le dictionnaire des datasets avec leurs fichiers
            dataset_files = {}
            if train_dataset:
                dataset_files['train'] = train_dataset
            if test_dataset:
                dataset_files['test'] = test_dataset
            if val_dataset:
                dataset_files['validation'] = val_dataset
            
            execute_notebook_job(uploaded_notebook, dataset_files)
        else:
            if not uploaded_notebook:
                st.error("⚠️ Notebook manquant")
            else:
                st.error("⚠️ Au moins un dataset requis")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="sidebar-footer">
            <p><i class='fas fa-code'></i> Powered by Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT ---
# Header principal
st.markdown("""
    <div class="dashboard-header">
        <h1><i class="fas fa-layer-group"></i> Dashboard Multi-Datasets</h1>
        <p>Exécutez vos notebooks avec plusieurs datasets (train, test, validation) en un clic</p>
    </div>
""", unsafe_allow_html=True)

# Aperçu des datasets uploadés
if train_dataset or test_dataset or val_dataset:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-database", "Aperçu des Datasets")
    
    # Créer des onglets pour chaque dataset
    dataset_tabs = []
    if train_dataset:
        dataset_tabs.append("🎯 Train")
    if test_dataset:
        dataset_tabs.append("🧪 Test")
    if val_dataset:
        dataset_tabs.append("✅ Validation")
    
    tabs = st.tabs(dataset_tabs)
    
    tab_index = 0
    
    if train_dataset:
        with tabs[tab_index]:
            try:
                train_dataset.seek(0)
                file_ext = os.path.splitext(train_dataset.name)[1].lower()
                
                if file_ext == '.csv':
                    df_train = pd.read_csv(train_dataset)
                elif file_ext in ['.xlsx', '.xls']:
                    df_train = pd.read_excel(train_dataset)
                elif file_ext == '.json':
                    df_train = pd.read_json(train_dataset)
                elif file_ext == '.parquet':
                    df_train = pd.read_parquet(train_dataset)
                else:
                    df_train = pd.read_csv(train_dataset)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    stat_card("fas fa-table", f"{df_train.shape[0]:,}", "Lignes")
                with col2:
                    stat_card("fas fa-columns", f"{df_train.shape[1]}", "Colonnes")
                with col3:
                    memory_kb = df_train.memory_usage(deep=True).sum() / 1024
                    stat_card("fas fa-memory", f"{memory_kb:.1f} KB", "Taille")
                with col4:
                    stat_card("fas fa-file", file_ext.upper().replace('.', ''), "Format")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.expander("📋 Colonnes du dataset Train", expanded=False):
                    cols_df = pd.DataFrame({
                        'N°': range(1, len(df_train.columns) + 1),
                        'Colonne': df_train.columns,
                        'Type': df_train.dtypes.values,
                        'Non-null': df_train.count().values,
                        '% Null': [f"{(df_train[col].isnull().sum()/len(df_train)*100):.1f}%" for col in df_train.columns]
                    })
                    st.dataframe(cols_df, use_container_width=True, height=300)
                
                st.markdown("**Aperçu des premières lignes:**")
                st.dataframe(df_train.head(10), use_container_width=True, height=300)
                
            except Exception as e:
                st.error(f"⚠️ Erreur lors de la lecture du dataset Train: {str(e)}")
        
        tab_index += 1
    
    if test_dataset:
        with tabs[tab_index]:
            try:
                test_dataset.seek(0)
                file_ext = os.path.splitext(test_dataset.name)[1].lower()
                
                if file_ext == '.csv':
                    df_test = pd.read_csv(test_dataset)
                elif file_ext in ['.xlsx', '.xls']:
                    df_test = pd.read_excel(test_dataset)
                elif file_ext == '.json':
                    df_test = pd.read_json(test_dataset)
                elif file_ext == '.parquet':
                    df_test = pd.read_parquet(test_dataset)
                else:
                    df_test = pd.read_csv(test_dataset)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    stat_card("fas fa-table", f"{df_test.shape[0]:,}", "Lignes")
                with col2:
                    stat_card("fas fa-columns", f"{df_test.shape[1]}", "Colonnes")
                with col3:
                    memory_kb = df_test.memory_usage(deep=True).sum() / 1024
                    stat_card("fas fa-memory", f"{memory_kb:.1f} KB", "Taille")
                with col4:
                    stat_card("fas fa-file", file_ext.upper().replace('.', ''), "Format")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.expander("📋 Colonnes du dataset Test", expanded=False):
                    cols_df = pd.DataFrame({
                        'N°': range(1, len(df_test.columns) + 1),
                        'Colonne': df_test.columns,
                        'Type': df_test.dtypes.values,
                        'Non-null': df_test.count().values,
                        '% Null': [f"{(df_test[col].isnull().sum()/len(df_test)*100):.1f}%" for col in df_test.columns]
                    })
                    st.dataframe(cols_df, use_container_width=True, height=300)
                
                st.markdown("**Aperçu des premières lignes:**")
                st.dataframe(df_test.head(10), use_container_width=True, height=300)
                
            except Exception as e:
                st.error(f"⚠️ Erreur lors de la lecture du dataset Test: {str(e)}")
        
        tab_index += 1
    
    if val_dataset:
        with tabs[tab_index]:
            try:
                val_dataset.seek(0)
                file_ext = os.path.splitext(val_dataset.name)[1].lower()
                
                if file_ext == '.csv':
                    df_val = pd.read_csv(val_dataset)
                elif file_ext in ['.xlsx', '.xls']:
                    df_val = pd.read_excel(val_dataset)
                elif file_ext == '.json':
                    df_val = pd.read_json(val_dataset)
                elif file_ext == '.parquet':
                    df_val = pd.read_parquet(val_dataset)
                else:
                    df_val = pd.read_csv(val_dataset)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    stat_card("fas fa-table", f"{df_val.shape[0]:,}", "Lignes")
                with col2:
                    stat_card("fas fa-columns", f"{df_val.shape[1]}", "Colonnes")
                with col3:
                    memory_kb = df_val.memory_usage(deep=True).sum() / 1024
                    stat_card("fas fa-memory", f"{memory_kb:.1f} KB", "Taille")
                with col4:
                    stat_card("fas fa-file", file_ext.upper().replace('.', ''), "Format")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Aperçu des premières lignes:**")
                st.dataframe(df_val.head(10), use_container_width=True, height=300)
                
            except Exception as e:
                st.error(f"⚠️ Erreur lors de la lecture du dataset Validation: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Aperçu du notebook
if uploaded_notebook:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-file-code", "Informations sur le Notebook")
    
    try:
        uploaded_notebook.seek(0)
        notebook_content = uploaded_notebook.getvalue()
        
        if not notebook_content or len(notebook_content) == 0:
            st.error("❌ Le fichier notebook est vide.")
        else:
            try:
                nb = nbformat.reads(notebook_content.decode('utf-8'), as_version=4)
            except:
                st.error("❌ Le fichier ne semble pas être un notebook Jupyter valide.")
                raise
        
        if not hasattr(nb, 'cells') or not nb.cells or len(nb.cells) == 0:
            st.warning("⚠️ Le notebook ne contient aucune cellule.")
            code_cells = 0
            markdown_cells = 0
            total_cells = 0
        else:
            code_cells = sum(1 for cell in nb.cells if cell.cell_type == 'code')
            markdown_cells = sum(1 for cell in nb.cells if cell.cell_type == 'markdown')
            total_cells = len(nb.cells)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            stat_card("fas fa-code", code_cells, "Cellules Code")
        with col2:
            stat_card("fas fa-file-alt", markdown_cells, "Cellules Markdown")
        with col3:
            stat_card("fas fa-list", total_cells, "Total Cellules")
        with col4:
            imports = set()
            if total_cells > 0:
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        lines = cell.source.split('\n')
                        for line in lines:
                            if 'import' in line and not line.strip().startswith('#'):
                                try:
                                    parts = line.strip().split()
                                    if len(parts) >= 2:
                                        if parts[0] == 'import':
                                            imports.add(parts[1].split('.')[0])
                                        elif parts[0] == 'from' and len(parts) >= 4:
                                            imports.add(parts[1].split('.')[0])
                                except:
                                    pass
            stat_card("fas fa-puzzle-piece", len(imports), "Bibliothèques")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if imports and len(imports) > 0:
            with st.expander("📦 Bibliothèques détectées", expanded=False):
                st.write("Assurez-vous que ces bibliothèques sont installées:")
                imports_list = sorted(list(imports))
                cols = st.columns(3)
                for idx, lib in enumerate(imports_list):
                    with cols[idx % 3]:
                        st.markdown(f"- `{lib}`")
        
    except Exception as e:
        st.error(f"⚠️ Erreur: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Guide d'utilisation
if not st.session_state.analysis_run:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-question-circle", "Comment ça fonctionne?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        info_card_icon(
            "fas fa-file-upload",
            "1. Charger le notebook",
            "Uploadez votre notebook Jupyter qui nécessite plusieurs datasets."
        )
    
    with col2:
        info_card_icon(
            "fas fa-database",
            "2. Charger les datasets",
            "Uploadez vos datasets: Train (obligatoire), Test (obligatoire), Validation (optionnel)."
        )
    
    with col3:
        info_card_icon(
            "fas fa-magic",
            "3. Détection automatique",
            "Le système détecte et injecte automatiquement vos datasets dans les bonnes variables."
        )
    
    with col4:
        info_card_icon(
            "fas fa-chart-line",
            "4. Visualiser",
            "Tous les résultats, graphiques et métriques s'affichent automatiquement."
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🎯 Fonctionnalités Multi-Datasets"):
        st.markdown("""
        ### Variables créées automatiquement
        
        Le système crée automatiquement les variables suivantes selon vos uploads:
        
        ✅ **Si vous uploadez Train.csv:**
        ```python
        train = pd.read_csv('votre_train.csv')
        ```
        
        ✅ **Si vous uploadez Test.csv:**
        ```python
        test = pd.read_csv('votre_test.csv')
        ```
        
        ✅ **Si vous uploadez Validation.csv:**
        ```python
        validation = pd.read_csv('votre_validation.csv')
        ```
        
        ✅ **Variable 'df' pour compatibilité:**
        ```python
        df = train.copy()  # Pointe vers le dataset train
        ```
        
        ---
        
        ### Exemple de notebook compatible
        
        Votre notebook peut utiliser directement:
        ```python
        # Ces variables sont créées automatiquement!
        print(train.shape)
        print(test.shape)
        
        # Votre code d'analyse
        X_train = train.drop('target', axis=1)
        y_train = train['target']
        
        X_test = test.drop('target', axis=1)
        y_test = test['target']
        
        # Entraînement du modèle
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        ```
        
        **Aucune modification nécessaire!** 🎉
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Résultats
if st.session_state.output_notebook_path:
    render_notebook(st.session_state.output_notebook_path)
elif st.session_state.analysis_run:
    st.info("⏳ L'analyse est en cours d'exécution. Les résultats s'afficheront ici une fois terminée.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #9CA3AF; padding: 2rem 0;'>
        <p style='margin: 0;'><i class='fas fa-layer-group'></i> Dashboard Multi-Datasets</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9em;'>Propulsé par Streamlit & Papermill | Support multi-datasets intelligent</p>
    </div>
""", unsafe_allow_html=True)