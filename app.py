# Fichier: app.py (Dashboard Universel - Adapte automatiquement les notebooks)

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
    page_title="Tableau de Bord d'Analyse Universel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Injection de CSS Personnalisé avec Icônes Font Awesome ---
def load_custom_css():
    """
    Injecte du CSS personnalisé pour une apparence professionnelle et moderne.
    """
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            /* Import de polices modernes */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Configuration globale */
            html, body, [class*="css"] {
                font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #FFFFFF !important;
                background-color: #F9FAFB;
            }
            
            /* Barre latérale moderne - Style Dashboard */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
                border-right: 2px solid #2d3748;
                padding: 0;
                box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
            }
            
            [data-testid="stSidebar"] > div:first-child {
                padding: 0;
            }
            
            /* Sidebar header avec logo */
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
            
            /* Sidebar sections */
            [data-testid="stSidebar"] .sidebar-section {
                padding: 1.5rem 1rem;
                border-bottom: 1px solid #2d3748;
            }
            
            /* Sidebar menu items */
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
            
            /* Tous les textes de la sidebar */
            [data-testid="stSidebar"] * {
                color: #E5E7EB !important;
            }
            
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h4,
            [data-testid="stSidebar"] h5 {
                color: #FFFFFF !important;
            }
            
            /* Sidebar file uploader */
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
            
            /* Sidebar success messages */
            [data-testid="stSidebar"] .stSuccess {
                background-color: rgba(16, 185, 129, 0.15) !important;
                color: #6EE7B7 !important;
                border-left: 4px solid #10B981;
                padding: 0.75rem;
                border-radius: 6px;
                font-size: 0.9em;
            }
            
            /* Sidebar button principale */
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
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            }
            
            /* Container principal */
            .main .block-container {
                max-width: 1400px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            /* Header avec gradient */
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
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .dashboard-header p {
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.1em;
                margin-top: 0.5rem;
                margin-bottom: 0;
            }
            
            /* Sections du dashboard */
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
            
            /* Cartes d'information */
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
            
            /* Stat cards */
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
            
            /* Messages d'alerte */
            .stSuccess {
                background-color: #D1FAE5 !important;
                color: #065F46 !important;
                border-left: 4px solid #10B981;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stSuccess * {
                color: #065F46 !important;
            }
            
            .stError {
                background-color: #FEE2E2 !important;
                color: #991B1B !important;
                border-left: 4px solid #EF4444;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stError * {
                color: #991B1B !important;
            }
            
            .stWarning {
                background-color: #FEF3C7 !important;
                color: #92400E !important;
                border-left: 4px solid #F59E0B;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stWarning * {
                color: #92400E !important;
            }
            
            .stInfo {
                background-color: #DBEAFE !important;
                color: #1E40AF !important;
                border-left: 4px solid #3B82F6;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stInfo * {
                color: #1E40AF !important;
            }
            
            /* Expandeurs */
            [data-testid="stExpander"] {
                background-color: #374151 !important;
                border: 1px solid #4B5563;
                border-radius: 8px;
                margin-bottom: 1rem;
            }
            
            [data-testid="stExpander"] summary {
                color: #FFFFFF !important;
            }
            
            [data-testid="stExpander"] p,
            [data-testid="stExpander"] span,
            [data-testid="stExpander"] div,
            [data-testid="stExpander"] label {
                color: #FFFFFF !important;
            }
            
            /* Dataframes */
            [data-testid="stDataFrame"] {
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                border: 1px solid #E5E7EB;
            }
            
            /* Progress bar */
            .stProgress > div > div {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }
            
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- Fonction pour afficher des sections avec icônes ---
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


# --- Fonction pour adapter automatiquement le notebook ---
def adapt_notebook_for_dataset(notebook_file, dataset_path):
    """
    Adapte automatiquement le notebook pour utiliser le dataset uploadé.
    - Remplace les chemins d'accès aux fichiers par le dataset uploadé
    - Supprime/commente les cellules d'upload de fichiers
    - Injecte le chemin du dataset dans une variable globale
    """
    try:
        # Lire le notebook - GÉRER LE CAS OÙ LE FICHIER A DÉJÀ ÉTÉ LU
        if hasattr(notebook_file, 'read'):
            # Réinitialiser le pointeur de fichier au début
            notebook_file.seek(0)
            notebook_content = notebook_file.read()
        else:
            notebook_content = notebook_file
        
        # Décoder si nécessaire
        if isinstance(notebook_content, bytes):
            notebook_content = notebook_content.decode('utf-8')
        
        nb = nbformat.reads(notebook_content, as_version=4)
        
        # Patterns à détecter pour l'upload de fichiers
        upload_patterns = [
            r'files\.upload\(\)',  # Google Colab
            r'input\(',  # Jupyter input
            r'st\.file_uploader',  # Streamlit
            r'FileUpload',  # ipywidgets
            r'pd\.read_csv\s*\(',  # Lecture de fichiers CSV - CAPTURE TOUS LES read_csv
            r'pd\.read_excel\s*\(',  # Lecture de fichiers Excel
            r'open\s*\(',  # Open file
        ]
        
        # Variable pour stocker le nom de la variable du dataframe
        df_variable_name = 'df'
        
        # Nouvelle cellule d'injection du dataset
        injection_cell = nbformat.v4.new_code_cell(source=f"""
# 🔄 CELLULE INJECTÉE AUTOMATIQUEMENT PAR LE DASHBOARD
# Cette cellule charge automatiquement le dataset uploadé sur la plateforme

import pandas as pd
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Configuration pour afficher les graphiques
import matplotlib
matplotlib.use('Agg')  # Backend pour sauvegarder les figures
plt.ioff()  # Mode non-interactif pour capturer les sorties

# Chemin du dataset uploadé sur la plateforme
DATASET_PATH = r'{dataset_path}'

# Chargement automatique du dataset
if os.path.exists(DATASET_PATH):
    # Détection automatique du type de fichier
    file_extension = os.path.splitext(DATASET_PATH)[1].lower()
    
    if file_extension == '.csv':
        df = pd.read_csv(DATASET_PATH)
    elif file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(DATASET_PATH)
    elif file_extension == '.json':
        df = pd.read_json(DATASET_PATH)
    elif file_extension == '.parquet':
        df = pd.read_parquet(DATASET_PATH)
    else:
        # Tentative de lecture CSV par défaut
        df = pd.read_csv(DATASET_PATH)
    
    # IMPORTANT: Créer les variables train et test avec le même dataset
    # Pour permettre la compatibilité avec les notebooks qui utilisent train/test
    train = df.copy()
    test = df.copy()
    
    print(f"✅ Dataset chargé avec succès: {{df.shape[0]}} lignes, {{df.shape[1]}} colonnes")
    print(f"📊 Colonnes disponibles: {{list(df.columns)}}")
    print(f"")
    print(f"💡 Variables créées:")
    print(f"   - 'df' : DataFrame principal")
    print(f"   - 'train' : Copie du dataset (pour compatibilité)")
    print(f"   - 'test' : Copie du dataset (pour compatibilité)")
    print(f"")
    print(f"⚠️ Note: Si votre notebook utilise train/test séparés,")
    print(f"   pensez à faire un train_test_split après le chargement.")
    
    # Afficher un aperçu
    display(df.head())
else:
    print(f"❌ Erreur: Fichier non trouvé à {{DATASET_PATH}}")
    df = pd.DataFrame()  # DataFrame vide par sécurité
    train = pd.DataFrame()
    test = pd.DataFrame()
""")
        
        # Traiter chaque cellule du notebook
        modified_cells = []
        injection_done = False
        has_imports = False
        
        # VÉRIFICATION: S'assurer qu'il y a des cellules
        if not nb.cells or len(nb.cells) == 0:
            st.warning("⚠️ Le notebook semble vide. Ajout de la cellule d'injection uniquement.")
            nb.cells = [injection_cell]
            
            # Sauvegarder le notebook modifié
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb", mode='w', encoding='utf-8') as temp_nb:
                nbformat.write(nb, temp_nb)
                modified_notebook_path = temp_nb.name
            
            return modified_notebook_path
        
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                cell_source = cell.source
                
                # Détecter si la cellule contient des imports
                if 'import' in cell_source.lower():
                    has_imports = True
                
                # Détecter les cellules d'upload/lecture de fichiers
                is_upload_cell = any(re.search(pattern, cell_source) for pattern in upload_patterns)
                
                if is_upload_cell:
                    # Commenter la cellule d'upload
                    commented_source = '\n'.join([f'# {line}' for line in cell_source.split('\n')])
                    cell.source = f"""
# ⚠️ CELLULE DÉSACTIVÉE AUTOMATIQUEMENT PAR LE DASHBOARD
# Cette cellule a été détectée comme cellule d'upload/lecture de fichier
# Les données sont maintenant chargées automatiquement via les variables:
#   - 'df' : DataFrame principal
#   - 'train' : pour compatibilité avec notebooks train/test
#   - 'test' : pour compatibilité avec notebooks train/test

{commented_source}

# 💡 Utilisez directement les variables 'df', 'train' ou 'test' pour accéder aux données
# 📝 Si vous avez besoin de séparer train/test, utilisez train_test_split après
"""
                    st.info(f"📝 Cellule #{i+1} adaptée: Lecture de fichier désactivée (variables df/train/test disponibles)")
                
                # Injecter la cellule de chargement juste après les imports
                if not injection_done and has_imports and 'import' in cell_source.lower():
                    modified_cells.append(cell)
                    modified_cells.append(injection_cell)
                    injection_done = True
                    continue
                
                modified_cells.append(cell)
            else:
                modified_cells.append(cell)
        
        # Si l'injection n'a pas été faite (pas d'imports détectés), l'ajouter au début
        if not injection_done:
            modified_cells.insert(0, injection_cell)
            st.info("📝 Cellule d'injection ajoutée au début du notebook (aucun import détecté)")
        
        # Créer le nouveau notebook
        nb.cells = modified_cells
        
        # Sauvegarder le notebook modifié
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb", mode='w', encoding='utf-8') as temp_nb:
            nbformat.write(nb, temp_nb)
            modified_notebook_path = temp_nb.name
        
        return modified_notebook_path
        
    except nbformat.reader.NotJSONError as e:
        st.error(f"❌ Le fichier n'est pas un notebook Jupyter valide: {str(e)}")
        raise e
    except json.JSONDecodeError as e:
        st.error(f"❌ Erreur de format JSON dans le notebook: {str(e)}")
        raise e
    except Exception as e:
        st.error(f"❌ Erreur lors de l'adaptation du notebook: {str(e)}")
        import traceback
        with st.expander("🔍 Trace complète de l'erreur"):
            st.code(traceback.format_exc())
        raise e


# --- Fonction de rendu des sorties du Notebook ---
def render_notebook(notebook_path):
    """
    Lit un fichier notebook .ipynb et affiche ses sorties de manière professionnelle.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        section_header("fas fa-chart-line", "Résultats de l'analyse")
        
        cell_number = 1
        total_cells = len([cell for cell in nb.cells if cell.cell_type == 'code'])
        
        st.info(f"📊 Le notebook contient {total_cells} cellules de code. Affichage des résultats...")
        
        for i, cell in enumerate(nb.cells):
            
            if cell.cell_type == 'markdown':
                st.markdown(cell.source)
                
            elif cell.cell_type == 'code':
                # Afficher le code dans un expander
                with st.expander(f"💻 Code de la cellule #{cell_number}", expanded=False):
                    st.code(cell.source, language='python')
                
                # Vérifier s'il y a des sorties
                if not cell.outputs:
                    st.caption(f"ℹ️ Cellule #{cell_number}: Pas de sortie (code exécuté sans affichage)")
                    cell_number += 1
                    continue
                
                has_output = False
                
                # Traiter chaque sortie
                for output_idx, output in enumerate(cell.outputs):
                    
                    # === STREAM OUTPUT (print statements) ===
                    if output.output_type == 'stream':
                        if hasattr(output, 'text') and output.text.strip():
                            st.text(output.text)
                            has_output = True
                    
                    # === DISPLAY_DATA / EXECUTE_RESULT ===
                    elif output.output_type in ('display_data', 'execute_result'):
                        data = output.data
                        
                        # 1. Images PNG (Matplotlib, Seaborn) - PRIORITÉ MAXIMALE
                        if 'image/png' in data:
                            try:
                                img_data = base64.b64decode(data['image/png'])
                                st.image(img_data, use_column_width=True, caption=f"📈 Figure de la cellule #{cell_number}")
                                has_output = True
                                continue  # Skip autres formats pour cette sortie
                            except Exception as e:
                                st.warning(f"⚠️ Impossible d'afficher l'image: {str(e)}")
                        
                        # 2. Images JPEG
                        if 'image/jpeg' in data:
                            try:
                                img_data = base64.b64decode(data['image/jpeg'])
                                st.image(img_data, use_column_width=True, caption=f"📈 Figure de la cellule #{cell_number}")
                                has_output = True
                                continue
                            except Exception as e:
                                st.warning(f"⚠️ Impossible d'afficher l'image JPEG: {str(e)}")
                        
                        # 3. Graphiques Plotly (JSON)
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
                            except Exception as e:
                                st.error(f"❌ Erreur Plotly: {str(e)}")
                        
                        # 4. HTML (tableaux pandas, etc.)
                        if 'text/html' in data:
                            html_content = data['text/html']
                            # Vérifier que c'est du vrai HTML (pas juste des balises vides)
                            if '<div' in html_content or '<table' in html_content:
                                # Nettoyer le HTML des scripts Plotly si présents
                                if 'plotly' not in html_content.lower():
                                    st.markdown(html_content, unsafe_allow_html=True)
                                    has_output = True
                                    continue
                        
                        # 5. Texte brut (résultats, DataFrames en mode texte)
                        if 'text/plain' in data:
                            text_content = data['text/plain']
                            # Filtrer les représentations d'objets inutiles
                            if (not text_content.startswith('<') and 
                                len(text_content.strip()) > 0 and
                                'Figure' not in text_content and
                                'matplotlib.figure.Figure' not in text_content and
                                'AxesSubplot' not in text_content):
                                
                                # Vérifier si c'est un DataFrame
                                if '\n' in text_content and ('|' in text_content or text_content.count(' ') > 10):
                                    st.text(text_content)
                                    has_output = True
                                # Ou d'autres résultats textuels
                                elif len(text_content) < 5000:  # Limiter la taille
                                    st.text(text_content)
                                    has_output = True
                    
                    # === ERRORS ===
                    elif output.output_type == 'error':
                        st.error(f"❌ Erreur détectée dans la cellule #{cell_number}: {output.ename} - {output.evalue}")
                        with st.expander("🔍 Voir la trace complète de l'erreur"):
                            st.code('\n'.join(output.traceback))
                        has_output = True
                
                # Si aucune sortie n'a été capturée
                if not has_output:
                    st.caption(f"ℹ️ Cellule #{cell_number}: Code exécuté sans sortie visible")
                
                st.markdown("---")
                cell_number += 1
        
        st.success(f"✅ Toutes les {total_cells} cellules ont été exécutées et affichées!")
        st.markdown('</div>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("⚠️ Le fichier de résultats n'a pas encore été généré. Veuillez lancer une analyse.")
    except Exception as e:
        st.error(f"❌ Une erreur est survenue lors de la lecture du notebook : {e}")
        with st.expander("🔍 Détails de l'erreur"):
            import traceback
            st.code(traceback.format_exc())


# --- Fonction d'exécution avec Papermill ---
def execute_notebook_job(notebook_file, dataset_file):
    """
    Gère l'exécution du notebook de manière sécurisée.
    """
    adapted_notebook_path, dataset_path = None, None
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📁 Préparation des fichiers...")
        progress_bar.progress(10)
        time.sleep(0.3)
        
        # Sauvegarder le dataset
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(dataset_file.name)[1]) as temp_dataset:
            temp_dataset.write(dataset_file.getvalue())
            dataset_path = temp_dataset.name
        
        status_text.text("🔧 Adaptation automatique du notebook...")
        progress_bar.progress(30)
        time.sleep(0.3)
        
        # Adapter le notebook pour utiliser le dataset uploadé
        adapted_notebook_path = adapt_notebook_for_dataset(notebook_file, dataset_path)
        
        status_text.text("▶️ Exécution de l'analyse en cours...")
        progress_bar.progress(50)
        
        # Chemin de sortie
        output_path = os.path.join(tempfile.gettempdir(), f"output_{int(time.time())}.ipynb")
        
        # Exécuter le notebook adapté avec capture des sorties
        pm.execute_notebook(
            input_path=adapted_notebook_path,
            output_path=output_path,
            kernel_name='python3',
            progress_bar=False,
            # CRUCIAL: Ces paramètres garantissent la capture de toutes les sorties
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
            
            Le notebook nécessite des bibliothèques qui ne sont pas installées.
            
            **Solution:** Installez les dépendances manquantes avec:
            ```bash
            pip install {module_name}
            ```
            
            **Bibliothèques couramment requises:**
            - scikit-learn
            - pandas
            - numpy
            - matplotlib
            - seaborn
            - plotly
            """)
        else:
            st.error(f"❌ Une erreur est survenue lors de l'exécution: {str(e)}")
        
        with st.expander("🔍 Détails de l'erreur"):
            st.code(error_msg)
        
        st.session_state['output_notebook_path'] = None
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Une erreur inattendue est survenue: {str(e)}")
        with st.expander("🔍 Trace complète"):
            import traceback
            st.code(traceback.format_exc())
        st.session_state['output_notebook_path'] = None
        
    finally:
        # Nettoyage des fichiers temporaires
        if adapted_notebook_path and os.path.exists(adapted_notebook_path):
            try:
                os.remove(adapted_notebook_path)
            except:
                pass
        if dataset_path and os.path.exists(dataset_path):
            try:
                os.remove(dataset_path)
            except:
                pass


# --- Interface Utilisateur ---
load_custom_css()

if 'output_notebook_path' not in st.session_state:
    st.session_state.output_notebook_path = None
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <i class="fas fa-brain"></i>
            <h2>Dashboard Universel</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Section Upload
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-cloud-upload-alt'></i> Fichiers", unsafe_allow_html=True)
    
    st.markdown("**Notebook Jupyter**")
    uploaded_notebook = st.file_uploader(
        "Sélectionnez votre notebook",
        type=['ipynb'],
        help="N'importe quel notebook Jupyter (.ipynb)",
        label_visibility="collapsed",
        key="notebook_upload"
    )
    
    if uploaded_notebook:
        st.success(f"✓ {uploaded_notebook.name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Jeu de Données**")
    uploaded_dataset = st.file_uploader(
        "Sélectionnez vos données",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="Formats supportés: CSV, Excel, JSON, Parquet",
        label_visibility="collapsed",
        key="dataset_upload"
    )
    
    if uploaded_dataset:
        file_extension = os.path.splitext(uploaded_dataset.name)[1]
        st.success(f"✓ {uploaded_dataset.name} ({file_extension})")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bouton d'action
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    if st.button("🚀 LANCER L'ANALYSE", type="primary", use_container_width=True, key="run_analysis_btn"):
        if uploaded_notebook and uploaded_dataset:
            st.session_state.analysis_run = True
            execute_notebook_job(uploaded_notebook, uploaded_dataset)
        else:
            st.error("⚠️ Fichiers manquants")
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
        <h1><i class="fas fa-rocket"></i> Dashboard Universel d'Analyse de Données</h1>
        <p>Exécutez n'importe quel notebook Jupyter avec vos propres données en quelques clics</p>
    </div>
""", unsafe_allow_html=True)

# Aperçu des données si fichier chargé
if uploaded_dataset:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-database", "Aperçu du Jeu de Données")
    
    try:
        # Détection automatique du format et chargement
        file_extension = os.path.splitext(uploaded_dataset.name)[1].lower()
        
        if file_extension == '.csv':
            df_preview = pd.read_csv(uploaded_dataset)
        elif file_extension in ['.xlsx', '.xls']:
            df_preview = pd.read_excel(uploaded_dataset)
        elif file_extension == '.json':
            df_preview = pd.read_json(uploaded_dataset)
        elif file_extension == '.parquet':
            df_preview = pd.read_parquet(uploaded_dataset)
        else:
            df_preview = pd.read_csv(uploaded_dataset)  # Tentative CSV par défaut
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            stat_card("fas fa-table", f"{df_preview.shape[0]:,}", "Lignes")
        with col2:
            stat_card("fas fa-columns", f"{df_preview.shape[1]}", "Colonnes")
        with col3:
            memory_kb = df_preview.memory_usage(deep=True).sum() / 1024
            stat_card("fas fa-memory", f"{memory_kb:.1f} KB", "Taille")
        with col4:
            stat_card("fas fa-file", file_extension.upper().replace('.', ''), "Format")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Affichage des colonnes
        with st.expander("📋 Liste des colonnes", expanded=False):
            cols_info = []
            for col in df_preview.columns:
                dtype = str(df_preview[col].dtype)
                null_count = df_preview[col].isnull().sum()
                cols_info.append({
                    "Colonne": col,
                    "Type": dtype,
                    "Valeurs nulles": null_count,
                    "% Null": f"{(null_count/len(df_preview)*100):.1f}%"
                })
            st.dataframe(pd.DataFrame(cols_info), use_container_width=True, height=300)
        
        st.markdown("**Aperçu des premières lignes:**")
        st.dataframe(df_preview.head(10), use_container_width=True, height=300)
        
    except Exception as e:
        st.warning(f"⚠️ Impossible de prévisualiser: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Aperçu du notebook si chargé
if uploaded_notebook:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-file-code", "Informations sur le Notebook")
    
    try:
        # Réinitialiser le pointeur de fichier
        uploaded_notebook.seek(0)
        notebook_content = uploaded_notebook.getvalue()
        
        # Validation du contenu
        if not notebook_content or len(notebook_content) == 0:
            st.error("❌ Le fichier notebook est vide.")
        else:
            try:
                nb = nbformat.reads(notebook_content.decode('utf-8'), as_version=4)
            except UnicodeDecodeError:
                st.error("❌ Erreur d'encodage du fichier. Assurez-vous qu'il s'agit d'un fichier UTF-8 valide.")
                raise
            except Exception as e:
                st.error(f"❌ Le fichier ne semble pas être un notebook Jupyter valide: {str(e)}")
                raise
        
        # Vérifier que le notebook contient des cellules
        if not hasattr(nb, 'cells') or not nb.cells or len(nb.cells) == 0:
            st.warning("⚠️ Le notebook ne contient aucune cellule.")
            code_cells = 0
            markdown_cells = 0
            total_cells = 0
        else:
            # Statistiques du notebook
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
            # Détecter les imports
            imports = set()
            if total_cells > 0:
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        lines = cell.source.split('\n')
                        for line in lines:
                            if 'import' in line and not line.strip().startswith('#'):
                                try:
                                    # Extraire le nom du module
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
        
        # Afficher les bibliothèques détectées
        if imports and len(imports) > 0:
            with st.expander("📦 Bibliothèques détectées dans le notebook", expanded=False):
                st.write("Assurez-vous que ces bibliothèques sont installées:")
                imports_list = sorted(list(imports))
                cols = st.columns(3)
                for idx, lib in enumerate(imports_list):
                    with cols[idx % 3]:
                        st.markdown(f"- `{lib}`")
        
        # Afficher un aperçu du code
        if total_cells > 0:
            with st.expander("👁️ Aperçu du notebook", expanded=False):
                st.info("Le notebook sera automatiquement adapté pour utiliser votre dataset uploadé.")
                
                cells_to_show = min(5, len(nb.cells))
                for i in range(cells_to_show):
                    cell = nb.cells[i]
                    if cell.cell_type == 'code':
                        st.markdown(f"**Cellule #{i+1} (Code):**")
                        preview_text = cell.source[:500] + ("..." if len(cell.source) > 500 else "")
                        st.code(preview_text, language='python')
                    elif cell.cell_type == 'markdown':
                        st.markdown(f"**Cellule #{i+1} (Markdown):**")
                        preview_text = cell.source[:300] + ("..." if len(cell.source) > 300 else "")
                        st.markdown(preview_text)
                    st.markdown("---")
                
                if len(nb.cells) > 5:
                    st.caption(f"... et {len(nb.cells) - 5} cellule(s) supplémentaire(s)")
        else:
            st.warning("⚠️ Le notebook est vide ou ne contient aucune cellule à afficher.")
        
    except Exception as e:
        st.warning(f"⚠️ Impossible de lire le notebook: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Section: Guide d'utilisation
if not st.session_state.analysis_run:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-question-circle", "Comment ça fonctionne?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        info_card_icon(
            "fas fa-upload",
            "1. Charger les fichiers",
            "Uploadez votre notebook Jupyter et votre dataset (CSV, Excel, JSON, Parquet)."
        )
    
    with col2:
        info_card_icon(
            "fas fa-magic",
            "2. Adaptation automatique",
            "Le système adapte automatiquement votre notebook pour utiliser votre dataset."
        )
    
    with col3:
        info_card_icon(
            "fas fa-play-circle",
            "3. Exécution",
            "Le notebook s'exécute avec vos données, sans modification manuelle nécessaire."
        )
    
    with col4:
        info_card_icon(
            "fas fa-chart-pie",
            "4. Résultats",
            "Visualisez tous les graphiques, tableaux et métriques générés."
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🔧 Fonctionnalités avancées"):
        st.markdown("""
        ### Adaptation Intelligente du Notebook
        
        Le système effectue automatiquement les opérations suivantes:
        
        ✅ **Détection et remplacement des uploads de fichiers**
        - Détecte les cellules qui uploadent des fichiers (Google Colab, Jupyter, etc.)
        - Les désactive automatiquement et les remplace par votre dataset
        
        ✅ **Injection automatique du dataset**
        - Crée une variable `df` contenant vos données
        - Supporte CSV, Excel, JSON, Parquet
        - Détection automatique du format
        
        ✅ **Compatibilité universelle**
        - Fonctionne avec n'importe quel notebook
        - Pas besoin de modifier votre code
        - Conserve toute la logique d'analyse
        
        ✅ **Préservation de l'intégrité**
        - Tous les imports sont conservés
        - Toutes les cellules d'analyse sont exécutées
        - Seules les cellules d'upload sont adaptées
        
        ---
        
        ### Formats de données supportés
        
        | Format | Extension | Description |
        |--------|-----------|-------------|
        | CSV | `.csv` | Valeurs séparées par virgules |
        | Excel | `.xlsx`, `.xls` | Fichiers Microsoft Excel |
        | JSON | `.json` | JavaScript Object Notation |
        | Parquet | `.parquet` | Format Apache Parquet |
        
        ---
        
        ### Comment préparer votre notebook
        
        Votre notebook peut contenir:
        - Des cellules d'import de bibliothèques
        - Des cellules d'upload de fichiers (seront adaptées automatiquement)
        - Des cellules d'analyse et de visualisation
        - Des cellules markdown pour la documentation
        
        **Le système s'occupe du reste!** 🚀
        """)
    
    with st.expander("❓ Questions fréquentes"):
        st.markdown("""
        **Mon notebook utilise Google Colab's files.upload(), est-ce compatible?**
        
        Oui! Le système détecte automatiquement les cellules `files.upload()` et les remplace par votre dataset.
        
        ---
        
        **Dois-je modifier mon notebook avant de l'uploader?**
        
        Non! Le système adapte automatiquement votre notebook. Vous pouvez uploader n'importe quel notebook Jupyter.
        
        ---
        
        **Quelle variable contient mes données?**
        
        Vos données sont automatiquement chargées dans la variable `df` (DataFrame pandas).
        
        ---
        
        **Que se passe-t-il si mon notebook lit plusieurs fichiers?**
        
        Le système remplace le premier fichier détecté. Pour les cas complexes, vous devrez peut-être adapter 
        légèrement votre notebook.
        
        ---
        
        **Mes données sont-elles sécurisées?**
        
        Oui! Les fichiers sont traités en mémoire et automatiquement supprimés après l'exécution. 
        Rien n'est conservé de manière permanente.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Message si l'analyse a déjà été lancée
    pass

# Section: Résultats
if st.session_state.output_notebook_path:
    render_notebook(st.session_state.output_notebook_path)
elif st.session_state.analysis_run:
    st.info("⏳ L'analyse est en cours d'exécution. Les résultats s'afficheront ici une fois terminée.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #9CA3AF; padding: 2rem 0;'>
        <p style='margin: 0;'><i class='fas fa-rocket'></i> Dashboard Universel d'Analyse</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9em;'>Propulsé par Streamlit & Papermill | Compatible avec tous les notebooks Jupyter</p>
    </div>
""", unsafe_allow_html=True)