import streamlit as st
from PIL import Image
import os
import base64

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO
# ==========================================
st.set_page_config(
    page_title="Dashboard | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores Corporativas AKOFS
AKOFS_RED = "#D32F2F"

# ==========================================
# 2. LOGO FIXO NO TOPO DO MENU LATERAL (ACIMA DOS LINKS)
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")
logo_corpo_path = os.path.join(root_dir, "image_c88946.jpg")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    # Injeta o logo centralizado exatamente acima da lista de páginas nativa
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# CSS para o visual do corpo do Dashboard
st.markdown(f"""
    <style>
    .main {{
        background-color: #0e1117;
    }}
    .titulo-imponente {{
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: {AKOFS_RED} !important;
        text-align: center;
        margin-top: -20px;
    }}
    .subtitulo-imponente {{
        font-size: 1.5rem !important;
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }}
    .modulo-card {{
        background-color: #1e2130;
        padding: 30px;
        border-radius: 15px;
        border-top: 6px solid {AKOFS_RED};
        height: 250px;
        text-align: center;
        margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CABEÇALHO E LOGO CENTRALIZADO NO CORPO
# ==========================================
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
with col_img2:
    if os.path.exists(logo_corpo_path):
        st.image(logo_corpo_path, use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align: center; color: {AKOFS_RED};'>🔴 AKOFS Offshore</h1>", unsafe_allow_html=True)

st.markdown('<h1 class="titulo-imponente">Subsea Planner Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-imponente">Central de Gestão Operacional | AKOFS Offshore</p>', unsafe_allow_html=True)

st.write("Bem-vinda, **Thaís**. Selecione abaixo a ferramenta desejada para iniciar as operações.")
st.divider()

# ==========================================
# 4. MÓDULOS DE OPERAÇÃO
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="modulo-card">
            <h2>⏱️</h2>
            <h3>Cronograma de Prontidão</h3>
            <p>Gerenciamento de etapas operacionais e previsões de prontidão.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Cronograma", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Cronograma_de_Prontidao.py")

with col2:
    st.markdown("""
        <div class="modulo-card">
            <h2>🔏</h2>
            <h3>Validação de Seal Test</h3>
            <p>Conferência técnica e validação de testes de vedação subsea.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Seal Test", use_container_width=True):
        st.switch_page("pages/2_Validação_de_Seal_Test.py")

with col3:
    st.markdown("""
        <div class="modulo-card">
            <h2>⚙️</h2>
            <h3>Simulador Tático de Clash</h3>
            <p>Simulação de cenários e tempos operacionais críticos.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Simulador", use_container_width=True):
        st.switch_page("pages/3_Simulador_Subsea.py")

st.divider()
st.caption("Versão 2026.1 | AKOFS Offshore")
