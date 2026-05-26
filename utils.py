import streamlit as st
import os
from PIL import Image

def carregar_sidebar():
    """Carrega o logo da AKOFS no topo da barra lateral."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(root_dir, "image_c889bf.png")
    
    if os.path.exists(logo_path):
        logo_lateral = Image.open(logo_path)
        st.sidebar.image(logo_lateral, use_container_width=True)
    else:
        st.sidebar.markdown("## 🔴 AKOFS Offshore")
    
    st.sidebar.markdown("---")

def aplicar_estilo_global():
    """Aplica formatação CSS que será compartilhada por todas as páginas."""
    st.markdown("""
        <style>
        /* Exemplo: Ajuste de margens ou fontes que você queira padronizar */
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)
