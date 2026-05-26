import streamlit as st
from PIL import Image
import os

# Configuração da Página
st.set_page_config(
    page_title="Dashboard | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Global
st.markdown("""
    <style>
    .titulo-imponente { font-size: 3rem; font-weight: 800; color: #D32F2F; }
    .card { background-color: #262a3d; padding: 20px; border-radius: 10px; border-top: 5px solid #D32F2F; }
    </style>
""", unsafe_allow_html=True)

# 1. LOGO NO TOPO DA PÁGINA (Capa)
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "image_c88946.jpg")

if os.path.exists(logo_path):
    st.image(logo_path, width=300) # Logo no topo da página
else:
    st.markdown("## 🔴 AKOFS Offshore")

# 2. CABEÇALHO
st.markdown('<h1 class="titulo-imponente">Subsea Planner Pro</h1>', unsafe_allow_html=True)
st.subheader("Central de Gestão Operacional | AKOFS Offshore")
st.write(f"Bem-vinda, **Thaís**. Este é o seu painel de controle executivo.")

st.divider()

# 3. MÓDULOS REAIS
st.markdown("## 🛠️ Módulos de Operação")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card"><h3>⏱️ Cronograma de Prontidão</h3><p>Gerenciamento de etapas e cronograma operacional.</p></div>', unsafe_allow_html=True)
    if st.button("Acessar Cronograma"):
        st.switch_page("pages/1_Cronograma_de_Prontidao.py")

with col2:
    st.markdown('<div class="card"><h3>🔏 Validação de Seal Test</h3><p>Módulo dedicado à conferência e validação dos testes de vedação.</p></div>', unsafe_allow_html=True)
    st.button("Acessar Seal Test", disabled=True)

with col3:
    st.markdown('<div class="card"><h3>⚙️ Simulador</h3><p>Ferramenta de simulação de cenários operacionais subsea.</p></div>', unsafe_allow_html=True)
    st.button("Acessar Simulador", disabled=True)

# Sidebar (Limpa, apenas navegação)
st.sidebar.markdown("### Navegação")
st.sidebar.write("Use os botões acima ou o menu lateral.")
