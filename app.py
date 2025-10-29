# Fichier: app.py (Dashboard Single Page Professionnel)

import streamlit as st
import pandas as pd
import papermill as pm
import nbformat
import tempfile
import os
import base64
from plotly.io import from_json
import time

st.set_page_config(
    page_title="Tableau de Bord d'Analyse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_custom_css():
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                background-attachment: fixed;
            }

            /* SIDEBAR STYLING */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
                border-right: none;
                box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
            }

            [data-testid="stSidebar"] .sidebar-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                text-align: center;
                padding: 2.5rem 1.5rem;
                margin: -1rem -1rem 2rem -1rem;
                border-bottom: 3px solid #818CF8;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }

            [data-testid="stSidebar"] .sidebar-header i {
                font-size: 3.5em;
                color: #FFFFFF;
                margin-bottom: 0.75rem;
                display: block;
                text-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            }

            [data-testid="stSidebar"] .sidebar-header h2 {
                color: #FFFFFF !important;
                margin: 0;
                font-size: 1.4em;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }

            [data-testid="stSidebar"] .sidebar-section {
                padding: 1.5rem 1rem;
                margin-bottom: 1rem;
            }

            [data-testid="stSidebar"] h3 {
                color: #818CF8 !important;
                font-size: 0.85em;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin-bottom: 1.25rem;
                padding-left: 0.75rem;
                border-left: 4px solid #818CF8;
            }

            [data-testid="stSidebar"] * {
                color: #E5E7EB !important;
            }

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] .sidebar-header * {
                color: #FFFFFF !important;
            }

            [data-testid="stSidebar"] [data-testid="stFileUploader"] {
                background-color: #1f2937;
                border: 2px dashed #4B5563;
                border-radius: 12px;
                padding: 1.25rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            [data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
                border-color: #818CF8;
                background-color: #374151;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(129, 140, 248, 0.3);
            }

            [data-testid="stSidebar"] .stSuccess {
                background-color: rgba(16, 185, 129, 0.2) !important;
                color: #6EE7B7 !important;
                border-left: 4px solid #10B981;
                padding: 0.75rem;
                border-radius: 8px;
                font-size: 0.9em;
                font-weight: 500;
            }

            [data-testid="stSidebar"] .stButton > button {
                background: linear-gradient(135deg, #818CF8 0%, #6366F1 100%);
                color: white !important;
                font-weight: 700;
                border: none;
                box-shadow: 0 6px 20px rgba(129, 140, 248, 0.5);
                padding: 1rem 2rem;
                font-size: 1.05em;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border-radius: 10px;
            }

            [data-testid="stSidebar"] .stButton > button:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 30px rgba(129, 140, 248, 0.7);
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            }

            [data-testid="stSidebar"] hr {
                border: none;
                height: 1px;
                background: linear-gradient(to right, transparent, #4B5563, transparent);
                margin: 1.5rem 0;
            }

            /* MAIN CONTENT AREA */
            .main .block-container {
                max-width: 1500px;
                padding: 2rem 3rem;
            }

            .dashboard-header {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.9) 100%);
                backdrop-filter: blur(10px);
                padding: 3rem 2.5rem;
                border-radius: 20px;
                margin-bottom: 2.5rem;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.4);
                position: relative;
                overflow: hidden;
            }

            .dashboard-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }

            .dashboard-header h1 {
                color: #1a1f2e !important;
                font-size: 2.75em;
                font-weight: 800;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .dashboard-header p {
                color: #4B5563 !important;
                font-size: 1.2em;
                margin-top: 0.75rem;
                margin-bottom: 0;
                font-weight: 500;
            }

            .dashboard-section {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 2.5rem;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                margin-bottom: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.5);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .dashboard-section:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
            }

            .section-header {
                display: flex;
                align-items: center;
                margin-bottom: 2rem;
                padding-bottom: 1rem;
                border-bottom: 3px solid #F3F4F6;
            }

            .section-header i {
                font-size: 2em;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-right: 1rem;
            }

            .section-header h2 {
                color: #111827 !important;
                font-size: 1.75em;
                font-weight: 700;
                margin: 0;
            }

            .info-card {
                background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                border: 2px solid #E5E7EB;
                margin-bottom: 1.5rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .info-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 5px;
                height: 100%;
                background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            }

            .info-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
                border-color: #818CF8;
            }

            .info-card i {
                font-size: 2.5em;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem;
                display: block;
            }

            .info-card h3 {
                color: #1F2937 !important;
                font-size: 1.25em;
                font-weight: 700;
                margin-bottom: 0.75rem;
            }

            .info-card p {
                color: #6B7280 !important;
                font-size: 1em;
                line-height: 1.7;
                margin: 0;
            }

            .stat-card {
                background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
                padding: 2rem;
                border-radius: 14px;
                border: 2px solid #E5E7EB;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                text-align: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .stat-card::before {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }

            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
                border-color: #818CF8;
            }

            .stat-card i {
                font-size: 2.5em;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.75rem;
            }

            .stat-value {
                font-size: 2.25em;
                font-weight: 800;
                color: #1F2937 !important;
                margin: 0.5rem 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .stat-label {
                font-size: 0.95em;
                color: #6B7280 !important;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }

            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white !important;
                font-weight: 700;
                padding: 1rem 2.5rem;
                border-radius: 12px;
                border: none;
                box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                width: 100%;
                font-size: 1.1em;
                letter-spacing: 0.5px;
            }

            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 35px rgba(102, 126, 234, 0.6);
            }

            [data-testid="stExpander"] {
                background-color: rgba(255, 255, 255, 0.9) !important;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                margin-bottom: 1rem;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            }

            [data-testid="stExpander"]:hover {
                border-color: #818CF8;
                box-shadow: 0 4px 15px rgba(129, 140, 248, 0.2);
            }

            [data-testid="stExpander"] summary {
                color: #1F2937 !important;
                font-weight: 600;
            }

            .stSuccess {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
                color: #059669 !important;
                border-left: 5px solid #10B981;
                padding: 1.25rem;
                border-radius: 10px;
                font-weight: 500;
            }

            .stError {
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
                color: #DC2626 !important;
                border-left: 5px solid #EF4444;
                padding: 1.25rem;
                border-radius: 10px;
                font-weight: 500;
            }

            .stWarning {
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%) !important;
                color: #D97706 !important;
                border-left: 5px solid #F59E0B;
                padding: 1.25rem;
                border-radius: 10px;
                font-weight: 500;
            }

            .stInfo {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%) !important;
                color: #2563EB !important;
                border-left: 5px solid #3B82F6;
                padding: 1.25rem;
                border-radius: 10px;
                font-weight: 500;
            }

            [data-testid="stDataFrame"] {
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                border: 2px solid #E5E7EB;
            }

            .stProgress > div > div {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                height: 8px;
                border-radius: 10px;
            }

            hr {
                margin: 3rem 0;
                border: none;
                height: 2px;
                background: linear-gradient(to right, transparent, rgba(102, 126, 234, 0.3), transparent);
            }

            [data-testid="stFileUploader"] {
                background: rgba(255, 255, 255, 0.9);
                border: 3px dashed #D1D5DB;
                border-radius: 14px;
                padding: 2rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            [data-testid="stFileUploader"]:hover {
                border-color: #818CF8;
                background: rgba(255, 255, 255, 1);
                box-shadow: 0 8px 25px rgba(129, 140, 248, 0.2);
            }

            code {
                background: #F3F4F6 !important;
                color: #1F2937 !important;
                padding: 0.2rem 0.5rem;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
            }

            .dashboard-section p,
            .dashboard-section span:not(.stat-value):not(.stat-label),
            .dashboard-section div {
                color: #374151 !important;
            }

        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(icon_class, title):
    st.markdown(f"""
        <div class="section-header">
            <i class="{icon_class}"></i>
            <h2>{title}</h2>
        </div>
    """, unsafe_allow_html=True)


def info_card_icon(icon_class, title, description):
    st.markdown(f"""
        <div class="info-card">
            <i class="{icon_class}"></i>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)


def stat_card(icon_class, value, label):
    st.markdown(f"""
        <div class="stat-card">
            <i class="{icon_class}"></i>
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def render_notebook(notebook_path):
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

                for output in cell.outputs:
                    if output.output_type == 'stream':
                        st.text(output.text)

                    elif output.output_type in ('display_data', 'execute_result'):
                        data = output.data

                        if 'text/html' in data:
                            st.markdown(data['text/html'], unsafe_allow_html=True)

                        elif 'image/png' in data:
                            st.image(base64.b64decode(data['image/png']), use_column_width=True)

                        elif 'application/vnd.plotly.v1+json' in data:
                            import json
                            plotly_data = data['application/vnd.plotly.v1+json']
                            if isinstance(plotly_data, str):
                                fig = from_json(plotly_data)
                            else:
                                fig = from_json(json.dumps(plotly_data))
                            st.plotly_chart(fig, use_container_width=True)

                        elif 'text/plain' in data:
                            st.text(data['text/plain'])

                    elif output.output_type == 'error':
                        st.error(f"Erreur détectée: {output.ename} - {output.evalue}")
                        with st.expander("Voir la trace complète de l'erreur"):
                            st.code('\n'.join(output.traceback))

                st.markdown("---")
                cell_number += 1

        st.markdown('</div>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("Le fichier de résultats n'a pas encore été généré. Veuillez lancer une analyse.")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture du notebook : {e}")


def execute_notebook_job(notebook_file, dataset_file, params):
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

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Une erreur est survenue lors de l'exécution: {str(e)}")
        st.session_state['output_notebook_path'] = None

    finally:
        if input_path and os.path.exists(input_path):
            os.remove(input_path)
        if dataset_path and os.path.exists(dataset_path):
            os.remove(dataset_path)


load_custom_css()

if 'output_notebook_path' not in st.session_state:
    st.session_state.output_notebook_path = None
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <i class="fas fa-chart-line"></i>
            <h2>Dashboard Analytics</h2>
        </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
        <div class="sidebar-footer">
            <p><i class='fas fa-code'></i> Powered by Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="dashboard-header">
        <h1><i class="fas fa-chart-bar"></i> Tableau de Bord d'Analyse de Données</h1>
        <p>Plateforme interactive pour transformer vos notebooks Jupyter en analyses professionnelles</p>
    </div>
""", unsafe_allow_html=True)

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

if st.session_state.output_notebook_path:
    render_notebook(st.session_state.output_notebook_path)
elif st.session_state.analysis_run:
    st.info("L'analyse est en cours d'exécution. Les résultats s'afficheront ici une fois terminée.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #4B5563; padding: 2rem 0;'>
        <p style='margin: 0; font-size: 1.1em; font-weight: 600;'><i class='fas fa-code'></i> Propulsé par Streamlit & Papermill</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.95em;'>Plateforme d'analyse de données interactive</p>
    </div>
""", unsafe_allow_html=True)
