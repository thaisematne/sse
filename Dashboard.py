import streamlit as st
from PIL import Image
import os

# 1. FORÇAR O CAMINHO ABSOLUTO DAS IMAGENS
# Isso garante que o Streamlit ache as imagens na mesma pasta do app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "image_c889bf.png")
VESSEL_PATH = os.path.join(BASE_DIR, "image_c88946.jpg")

# Definição de Cores Corporativas AKOFS
AKOFS_RED = "#D32F2F"
TEXT_WHITE = "#FAFAFA"

st.set_page_config(
    page_title="Dashboard | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURAÇÃO DA SIDEBAR (LOGO E IDENTIDADE) ---
try:
    logo = Image.open(LOGO_PATH)
    st.sidebar.image(logo, use_container_width=True)
except FileNotFoundError:
    st.sidebar.markdown(f"<h1 style='color: {AKOFS_RED}; text-align: center;'>AKOFS</h1>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Subsea Planner Pro")
st.sidebar.markdown("*Navegue pelos módulos acima no menu.*")

# --- 3. ÁREA PRINCIPAL (HERO SECTION) ---
st.markdown(f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <h1 style='color: {TEXT_WHITE}; font-size: 3em; margin-bottom: 0;'>Subsea Planner Pro</h1>
        <h3 style='color: {AKOFS_RED}; font-weight: normal; margin-top: 0;'>Assistente Tático de Engenharia Offshore</h3>
    </div>
""", unsafe_allow_html=True)

try:
    vessel_img = Image.open(VESSEL_PATH)
    # Estilo CSS para bordas arredondadas e sombra
    st.markdown("""
        <style>
            .stImage > img {
                border-radius: 15px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5), 0 6px 20px 0 rgba(0, 0, 0, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)
    st.image(vessel_img, use_container_width=True, caption="MPSV AKOFS Santos em operação.")
except FileNotFoundError:
    st.warning(f"Erro: Imagem do navio não encontrada no caminho absoluto: {VESSEL_PATH}")

st.divider()

# --- 4. VISÃO GERAL DOS MÓDULOS (CARDS) ---
st.markdown("## Visão Geral do Sistema")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<h3 style='color: {AKOFS_RED};'>📅 1. Cronograma de Prontidão</h3>", unsafe_allow_html=True)
    st.markdown("""
        **Planejamento tático de atividades de convés e mergulho.**
        * Sequenciamento de etapas (Navegação, DP, ROV, BAP).
        * Cálculo de duração total em HH:MM.
        * Previsão otimista de prontidão operacional.
        ---
    """)

with col2:
    st.markdown(f"<h3 style='color: {AKOFS_RED};'>⚖️ 2. Validação de Seal Test</h3>", unsafe_allow_html=True)
    st.markdown("""
        **Auditoria rápida de estanqueidade em barreiras subsea.**
        * Cálculo de queda de pressão (P1 - P2).
        * Verificação de critérios Petrobras (ex: < 10% em 15min).
        * Checklist de conformidade para segurança operacional.
        ---
    """)

with col3:
    st.markdown(f"<h3 style='color: {AKOFS_RED};'>⚓ 3. Simulador Tático de Clash</h3>", unsafe_allow_html=True)
    st.markdown("""
        **Prevenção de entrelaçamento (clash) de cabos e umbilicais.**
        * Visualização 2D da sombra do navio vs. BAP vs. Dive Points.
        * Cálculo de deriva (superfície ao fundo).
        * Simulação tática de tether management durante a docagem.
        ---
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>AKOFS Offshore © 2026 - Subsea Planner Pro v1.0</div>", unsafe_allow_html=True)
