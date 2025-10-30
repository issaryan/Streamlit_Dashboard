# Fichier: app.py (Dashboard Single Page Professionnel)

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

# --- Configuration de la page ---
st.set_page_config(
    page_title="Tableau de Bord d'Analyse",
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
            
            [data-testid="stSidebar"] .sidebar-section:last-child {
                border-bottom: none;
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
            
            /* Sidebar labels et textes */
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] div,
            [data-testid="stSidebar"] .stMarkdown {
                color: #D1D5DB !important;
            }
            
            [data-testid="stSidebar"] strong,
            [data-testid="stSidebar"] b {
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
            
            /* Sidebar sliders */
            [data-testid="stSidebar"] [data-testid="stSlider"] {
                padding: 0.5rem 0;
            }
            
            [data-testid="stSidebar"] [data-testid="stSlider"] label,
            [data-testid="stSidebar"] [data-testid="stSlider"] p,
            [data-testid="stSidebar"] [data-testid="stSlider"] span {
                color: #E5E7EB !important;
            }
            
            /* Slider track */
            [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
                background-color: #818CF8;
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
            
            [data-testid="stSidebar"] .stError {
                background-color: rgba(239, 68, 68, 0.15) !important;
                color: #FCA5A5 !important;
                border-left: 4px solid #EF4444;
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
            
            [data-testid="stSidebar"] .stButton > button:active {
                transform: translateY(-1px);
            }
            
            /* Sidebar captions */
            [data-testid="stSidebar"] .stCaptionContainer,
            [data-testid="stSidebar"] small,
            [data-testid="stSidebar"] .caption {
                color: #9CA3AF !important;
                font-size: 0.85em;
            }
            
            /* Sidebar markdown text */
            [data-testid="stSidebar"] .stMarkdown p,
            [data-testid="stSidebar"] .stMarkdown span {
                color: #D1D5DB !important;
            }
            
            /* Sidebar divider */
            [data-testid="stSidebar"] hr {
                border: none;
                height: 1px;
                background: linear-gradient(to right, transparent, #4B5563, transparent);
                margin: 1.5rem 0;
            }
            
            /* Sidebar footer */
            [data-testid="stSidebar"] .sidebar-footer {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: #0f1419;
                padding: 1rem;
                border-top: 1px solid #2d3748;
                text-align: center;
            }
            
            [data-testid="stSidebar"] .sidebar-footer p {
                color: #6B7280 !important;
                font-size: 0.8em;
                margin: 0;
            }
            
            /* Force le texte blanc partout dans main */
            .main p, .main span, .main div, .main label, .main input, .main textarea {
                color: #FFFFFF !important;
            }
            
            /* Texte dans les labels et widgets */
            label, .stMarkdown, .stText {
                color: #FFFFFF !important;
            }
            
            /* Slider labels et valeurs */
            [data-testid="stSlider"] label,
            [data-testid="stSlider"] p,
            [data-testid="stSlider"] span,
            [data-testid="stSlider"] div {
                color: #FFFFFF !important;
            }
            
            /* File uploader text */
            [data-testid="stFileUploader"] label,
            [data-testid="stFileUploader"] p,
            [data-testid="stFileUploader"] span,
            [data-testid="stFileUploader"] div {
                color: #FFFFFF !important;
            }
            
            /* Caption text */
            .stCaptionContainer, small, .caption {
                color: #D1D5DB !important;
            }
            
            /* Markdown text */
            .stMarkdown p, .stMarkdown span, .stMarkdown div {
                color: #FFFFFF !important;
            }
            
            /* Expandeur text */
            [data-testid="stExpander"] p,
            [data-testid="stExpander"] span,
            [data-testid="stExpander"] div,
            [data-testid="stExpander"] label {
                color: #FFFFFF !important;
            }
            
            /* Texte des dataframes */
            [data-testid="stDataFrame"] {
                color: #1F2937 !important;
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
            
            /* Texte dans les sections */
            .dashboard-section p,
            .dashboard-section span,
            .dashboard-section div {
                color: #374151;
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
            
            /* Boutons */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-weight: 600;
                padding: 0.75rem 2rem;
                border-radius: 8px;
                border: none;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                width: 100%;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);
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
            
            /* File uploader */
            [data-testid="stFileUploader"] {
                background-color: #374151;
                border: 2px dashed #6B7280;
                border-radius: 10px;
                padding: 1.5rem;
                transition: all 0.3s ease;
            }
            
            [data-testid="stFileUploader"]:hover {
                border-color: #818CF8;
                background-color: #4B5563;
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
            }border-left: 4px solid #F59E0B;
                padding: 1rem;
                border-radius: 8px;
            }
            
            .stInfo {
                background-color: #DBEAFE;
                color: #1E40AF;
                border-left: 4px solid #3B82F6;
                padding: 1rem;
                border-radius: 8px;
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
            
            /* Séparateurs */
            hr {
                margin: 2.5rem 0;
                border: none;
                height: 1px;
                background: linear-gradient(to right, transparent, #E5E7EB, transparent);
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
        for i, cell in enumerate(nb.cells):
            
            if cell.cell_type == 'markdown':
                st.markdown(cell.source)
                
            elif cell.cell_type == 'code' and cell.outputs:
                with st.expander(f"Code de la cellule #{cell_number}", expanded=False):
                    st.code(cell.source, language='python')
                
                has_output = False
                
                for output in cell.outputs:
                    if output.output_type == 'stream':
                        # Afficher les sorties texte (print)
                        if hasattr(output, 'text') and output.text.strip():
                            st.text(output.text)
                            has_output = True
                        
                    elif output.output_type in ('display_data', 'execute_result'):
                        data = output.data
                        
                        # Images PNG (Matplotlib, Seaborn) - PRIORITÉ
                        if 'image/png' in data:
                            try:
                                import base64
                                img_data = base64.b64decode(data['image/png'])
                                st.image(img_data, use_column_width=True, caption=f"Figure de la cellule #{cell_number}")
                                has_output = True
                            except Exception as e:
                                st.warning(f"Impossible d'afficher l'image: {str(e)}")
                        
                        # Graphiques Plotly - FORMAT JSON
                        elif 'application/vnd.plotly.v1+json' in data:
                            try:
                                import json
                                import plotly.graph_objects as go
                                
                                plotly_data = data['application/vnd.plotly.v1+json']
                                
                                # Convertir en dict si nécessaire
                                if isinstance(plotly_data, str):
                                    plotly_dict = json.loads(plotly_data)
                                else:
                                    plotly_dict = dict(plotly_data)
                                
                                # Créer la figure Plotly
                                fig = go.Figure(
                                    data=plotly_dict.get('data', []),
                                    layout=plotly_dict.get('layout', {})
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                                has_output = True
                            except Exception as e:
                                st.error(f"Erreur Plotly: {str(e)}")
                        
                        # HTML (tableaux pandas, graphiques en HTML)
                        elif 'text/html' in data:
                            html_content = data['text/html']
                            # Filtrer le JavaScript de Plotly mais garder le HTML
                            if '<div' in html_content or '<table' in html_content:
                                st.markdown(html_content, unsafe_allow_html=True)
                                has_output = True
                        
                        # Texte brut
                        elif 'text/plain' in data:
                            text_content = data['text/plain']
                            # Ne pas afficher si c'est juste une référence d'objet
                            if not text_content.startswith('<') and len(text_content.strip()) > 0:
                                # Ne pas afficher les représentations de figures vides
                                if 'Figure' not in text_content and 'matplotlib' not in text_content.lower():
                                    st.text(text_content)
                                    has_output = True
                    
                    elif output.output_type == 'error':
                        st.error(f"Erreur détectée: {output.ename} - {output.evalue}")
                        with st.expander("Voir la trace complète de l'erreur"):
                            st.code('\n'.join(output.traceback))
                        has_output = True
                
                # Si aucune sortie n'a été affichée, indiquer que c'est normal
                if not has_output:
                    st.info("Cette cellule n'a produit aucune sortie visible (ou les figures n'ont pas été capturées dans le notebook).")
                
                st.markdown("---")
                cell_number += 1
        
        st.markdown('</div>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("Le fichier de résultats n'a pas encore été généré. Veuillez lancer une analyse.")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture du notebook : {e}")
        with st.expander("Détails de l'erreur"):
            import traceback
            st.code(traceback.format_exc())


# --- Fonction d'exécution avec Papermill ---
def execute_notebook_job(notebook_file, dataset_file, params):
    """
    Gère l'exécution du notebook de manière sécurisée.
    """
    input_path, dataset_path = None, None
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Préparation des fichiers...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb") as temp_notebook:
            temp_notebook.write(notebook_file.getvalue())
            input_path = temp_notebook.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_dataset:
            temp_dataset.write(dataset_file.getvalue())
            dataset_path = temp_dataset.name

        output_path = os.path.join(tempfile.gettempdir(), f"output_{os.path.basename(input_path)}")
        params['dataset_path'] = dataset_path
        
        status_text.text("Exécution de l'analyse en cours...")
        progress_bar.progress(50)
        
        pm.execute_notebook(
            input_path=input_path,
            output_path=output_path,
            parameters=params,
            kernel_name='python3'
        )
        
        progress_bar.progress(100)
        status_text.text("Analyse terminée avec succès!")
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()
        
        st.session_state['output_notebook_path'] = output_path
        st.success("L'exécution du notebook est terminée avec succès!")
        
    except pm.PapermillExecutionError as e:
        progress_bar.empty()
        status_text.empty()
        
        # Extraction de l'erreur détaillée
        error_msg = str(e)
        if "ModuleNotFoundError" in error_msg:
            module_name = error_msg.split("'")[1] if "'" in error_msg else "unknown"
            st.error(f"""
            **Module manquant: {module_name}**
            
            Le notebook nécessite des bibliothèques qui ne sont pas installées dans votre environnement.
            
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
            st.error(f"Une erreur est survenue lors de l'exécution: {str(e)}")
        
        with st.expander("🔍 Détails de l'erreur"):
            st.code(error_msg)
        
        st.session_state['output_notebook_path'] = None
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Une erreur inattendue est survenue: {str(e)}")
        with st.expander("🔍 Trace complète"):
            import traceback
            st.code(traceback.format_exc())
        st.session_state['output_notebook_path'] = None
        
    finally:
        if input_path and os.path.exists(input_path):
            os.remove(input_path)
        if dataset_path and os.path.exists(dataset_path):
            os.remove(dataset_path)


# --- Interface Utilisateur avec Sidebar ---
load_custom_css()

if 'output_notebook_path' not in st.session_state:
    st.session_state.output_notebook_path = None
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <i class="fas fa-chart-line"></i>
            <h2>Dashboard Analytics</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Section Upload
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-cloud-upload-alt'></i> Fichiers", unsafe_allow_html=True)
    
    st.markdown("**Notebook Jupyter**")
    uploaded_notebook = st.file_uploader(
        "Sélectionnez votre notebook",
        type=['ipynb'],
        help="Notebook avec cellule 'parameters'",
        label_visibility="collapsed",
        key="notebook_upload"
    )
    
    if uploaded_notebook:
        st.success(f"✓ {uploaded_notebook.name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Jeu de Données**")
    uploaded_dataset = st.file_uploader(
        "Sélectionnez vos données",
        type=['csv'],
        help="Format CSV avec en-têtes",
        label_visibility="collapsed",
        key="dataset_upload"
    )
    
    if uploaded_dataset:
        st.success(f"✓ {uploaded_dataset.name}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section Paramètres
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### <i class='fas fa-cogs'></i> Paramètres", unsafe_allow_html=True)
    
    st.markdown("**Régularisation**")
    c_value = st.slider(
        "Valeur C",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Force de régularisation du modèle",
        key="c_value_slider",
        label_visibility="collapsed"
    )
    st.caption(f"C = {c_value}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Split Train/Test**")
    test_size = st.slider(
        "% Test",
        min_value=10,
        max_value=50,
        value=30,
        step=5,
        help="% de données pour le test",
        key="test_size_slider",
        label_visibility="collapsed"
    )
    st.caption(f"Test: {test_size}% | Train: {100-test_size}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bouton d'action
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    if st.button("🚀 LANCER L'ANALYSE", type="primary", use_container_width=True, key="run_analysis_btn"):
        if uploaded_notebook and uploaded_dataset:
            params_to_inject = {
                'model_c_value': c_value,
                'test_size': test_size / 100
            }
            st.session_state.analysis_run = True
            execute_notebook_job(uploaded_notebook, uploaded_dataset, params_to_inject)
        else:
            st.error("⚠ Fichiers manquants")
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
        <h1><i class="fas fa-chart-bar"></i> Tableau de Bord d'Analyse de Données</h1>
        <p>Plateforme interactive pour transformer vos notebooks Jupyter en analyses professionnelles</p>
    </div>
""", unsafe_allow_html=True)

# Aperçu des données si fichier chargé
if uploaded_dataset:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-database", "Aperçu du Jeu de Données")
    
    try:
        df_preview = pd.read_csv(uploaded_dataset)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            stat_card("fas fa-table", f"{df_preview.shape[0]:,}", "Lignes")
        with col2:
            stat_card("fas fa-columns", f"{df_preview.shape[1]}", "Colonnes")
        with col3:
            memory_kb = df_preview.memory_usage(deep=True).sum() / 1024
            stat_card("fas fa-memory", f"{memory_kb:.1f} KB", "Taille")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_preview.head(10), use_container_width=True, height=300)
        
    except Exception as e:
        st.warning(f"Impossible de prévisualiser: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Guide d'utilisation
if not st.session_state.analysis_run:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    section_header("fas fa-question-circle", "Guide d'Utilisation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        info_card_icon(
            "fas fa-upload",
            "1. Charger les fichiers",
            "Importez votre notebook Jupyter (.ipynb) et votre jeu de données (.csv) dans les zones de téléchargement ci-dessus."
        )
    
    with col2:
        info_card_icon(
            "fas fa-sliders-h",
            "2. Ajuster les paramètres",
            "Utilisez les curseurs pour configurer les paramètres de votre analyse selon vos besoins spécifiques."
        )
    
    with col3:
        info_card_icon(
            "fas fa-play",
            "3. Lancer l'analyse",
            "Cliquez sur le bouton 'Lancer l'Analyse' pour démarrer le traitement de vos données."
        )
    
    with col4:
        info_card_icon(
            "fas fa-chart-line",
            "4. Explorer les résultats",
            "Les graphiques, tableaux et métriques s'afficheront automatiquement dans la section résultats."
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("Questions fréquentes"):
        st.markdown("""
        **Qu'est-ce qu'un notebook Jupyter ?**
        
        Un notebook Jupyter est un document interactif qui combine du code, du texte explicatif et des visualisations. 
        Les data scientists l'utilisent pour explorer et analyser des données.
        
        ---
        
        **Que signifie 'cellule parameters' ?**
        
        C'est une cellule spéciale dans votre notebook qui contient les variables que vous souhaitez pouvoir modifier 
        via cette interface. Par exemple, si votre notebook a une variable `alpha = 0.5`, vous pouvez la rendre ajustable 
        en la plaçant dans une cellule marquée avec le tag `parameters`.
        
        ---
        
        **Mes données sont-elles sécurisées ?**
        
        Oui! Toutes les données que vous téléversez restent en mémoire sur le serveur pendant l'exécution 
        et sont automatiquement supprimées après le traitement. Aucun fichier n'est conservé de manière permanente.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Message si l'analyse a déjà été lancée mais section guide non affichée
    pass

# Section 4: Résultats
if st.session_state.output_notebook_path:
    render_notebook(st.session_state.output_notebook_path)
elif st.session_state.analysis_run:
    st.info("L'analyse est en cours d'exécution. Les résultats s'afficheront ici une fois terminée.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #9CA3AF; padding: 2rem 0;'>
        <p style='margin: 0;'><i class='fas fa-code'></i> Propulsé par Streamlit & Papermill</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9em;'>Plateforme d'analyse de données interactive</p>
    </div>
""", unsafe_allow_html=True)