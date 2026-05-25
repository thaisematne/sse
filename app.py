import streamlit as st
from PIL import Image
import os

# Definição de Cores Corporativas AKOFS (para uso em textos HTML)
AKOFS_RED = "#D32F2F"
TEXT_WHITE = "#FAFAFA"

st.set_page_config(
    page_title="Dashboard | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. CONFIGURAÇÃO DA SIDEBAR (LOGO E IDENTIDADE) ---
# Carregamento da Logo (Certifique-se que o arquivo image_c889bf.png está na raiz)
if os.path.exists("image_c889bf.png"):
    logo = Image.open("image_c889bf.png")
    st.sidebar.image(logo, use_column_width=True)
else:
    st.sidebar.markdown(f"<h1 style='color: {AKOFS_RED}; text-align: center;'>AKOFS</h1>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Subsea Planner Pro")
st.sidebar.markdown("*Navegue pelos módulos acima no menu.*")


# --- 2. ÁREA PRINCIPAL (HERO SECTION COM IMAGEM CORPORATIVA) ---
# Título Principal Estilizado
st.markdown(f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <h1 style='color: {TEXT_WHITE}; font-size: 3em; margin-bottom: 0;'>Subsea Planner Pro</h1>
        <h3 style='color: {AKOFS_RED}; font-weight: normal; margin-top: 0;'>Assistente Tático de Engenharia Offshore</h3>
    </div>
""", unsafe_allow_html=True)

# Carregamento da Imagem do Navio (Certifique-se que o arquivo image_c88946.jpg está na raiz)
if os.path.exists("image_c88946.jpg"):
    vessel_img = Image.open("image_c88946.jpg")
    # Imagem com bordas arredondadas e sombra suave para visual premium
    st.markdown("""
        <style>
            .stImage > img {
                border-radius: 15px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5), 0 6px 20px 0 rgba(0, 0, 0, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)
    st.image(vessel_img, use_column_width=True, caption="MPSV AKOFS Santos em operação.")
else:
    st.warning("Imagem corporativa (image_c88946.jpg) não encontrada na raiz do repositório.")

st.divider()

# --- 3. VISÃO GERAL DOS MÓDULOS (CARDS INFORMATIVOS) ---
st.markdown("## Visão Geral do Sistema")
col1, col2, col3 = st.columns(3)

# Card 1: Readiness Schedule
with col1:
    st.markdown(f"<h3 style='color: {AKOFS_RED};'>📅 1. Cronograma de Prontidão</h3>", unsafe_allow_html=True)
    st.markdown("""
        **Planejamento tático de atividades de convés e mergulho.**
        * Sequenciamento de etapas (Navegação, DP, ROV, BAP).
        * Cálculo de duração total em HH:MM.
        * Previsão otimista de prontidão operacional.
        ---
    """)
    # st.page_link("pages/1_Cronograma_de_Prontidao.py", label="Acessar Módulo 1", icon="➡️")

# Card 2: Seal Test Validation
with col2:
    st.markdown(f"<h3 style='color: {AKOFS_RED};'>⚖️ 2. Validação de Seal Test</h3>", unsafe_allow_html=True)
    st.markdown("""
        **Auditoria rápida de estanqueidade em barreiras subsea.**
        * Cálculo de queda de pressão (P1 - P2).
        * Verificação de critérios Petrobras (ex: < 10% em 15min).
        * Checklist de conformidade para segurança operacional.
        ---
    """)
    # st.page_link("pages/2_Validacao_de_Seal_Test.py", label="Acessar Módulo 2", icon="➡️")

# Card 3: Tactical Clash Simulator
with col3:
    st.markdown(f"<h3 style='color: {AKOFS_RED};'>⚓ 3. Simulador Tático de Clash</h3>", unsafe_allow_html=True)
    st.markdown("""
        **Prevenção de entrelaçamento (clash) de cabos e umbilicais.**
        * Visualização 2D da sombra do navio vs. BAP vs. Dive Points.
        * Cálculo de deriva (superfície ao fundo).
        * Simulação tática de tether management durante a docagem.
        ---
    """)
    # st.page_link("pages/3_Simulador_Tatico_de_Clash.py", label="Acessar Módulo 3", icon="➡️")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>AKOFS Offshore © 2024 - Subsea Planner Pro v1.0</div>", unsafe_allow_html=True)
