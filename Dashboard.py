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

# Configuração do Logo no Topo da Sidebar
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "image_c889bf.png")

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
else:
    st.sidebar.markdown("## 🔴 AKOFS Offshore")

st.sidebar.markdown("---")

# Conteúdo do Dashboard
st.title("Subsea Planner Pro")
st.subheader("Bem-vinda, Thaís")

# Manter a estrutura do seu dashboard anterior aqui
# Exemplo básico:
col1, col2 = st.columns(2)
with col1:
    st.write("Acesse os módulos através do menu lateral.")
with col2:
    st.info("Sistema de Gestão Offshore")

# Adicione aqui os demais componentes que você tinha no seu dashboard anterior
