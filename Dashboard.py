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

# --- CONTEÚDO DO DASHBOARD ---
st.title("Subsea Planner Pro")
st.subheader("Bem-vinda, Thaís")

# Exemplo da estrutura de descrição dos módulos que você usava
st.markdown("""
### Módulos do Sistema
Utilize o menu lateral para navegar entre as ferramentas de gestão:
- **Cronograma de Prontidão:** Planejamento e acompanhamento de etapas operacionais.
- **Gestão de PTW:** Controle de permissões de trabalho e conformidade.
- **KPIs Operacionais:** Monitoramento de indicadores de performance subsea.
""")

col1, col2 = st.columns(2)
with col1:
    st.info("Sistema de Gestão de Processos Offshore")
with col2:
    st.write("Versão 2026.1 - AKOFS Offshore")

# Adicione aqui os demais componentes que você tinha no seu dashboard anterior
