import streamlit as st
from PIL import Image
from utils import carregar_sidebar, aplicar_estilo_global

# 1. Configuração da página
st.set_page_config(
    page_title="Dashboard | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Aplica estilos e sidebar padronizados via utils.py
carregar_sidebar()
aplicar_estilo_global()

# 3. Conteúdo do Dashboard
st.title("Dashboard Principal")
st.write("Bem-vindo ao sistema de gestão Subsea Planner Pro.")

# Exemplo de como você pode organizar o seu dashboard
col1, col2 = st.columns(2)

with col1:
    st.info("Acesso rápido aos módulos:")
    if st.button("Ir para Cronograma de Prontidão"):
        st.switch_page("pages/1_Cronograma_de_Prontidao.py")

with col2:
    st.metric("Status do Sistema", "Online", delta="Operacional")

st.divider()
st.write("Utilize a barra lateral para navegar entre os módulos do sistema.")
