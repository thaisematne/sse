import streamlit as st
import os
from PIL import Image

def carregar_sidebar():
    # Define o caminho raiz independentemente de onde o arquivo utils.py for chamado
    root_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(root_dir, "image_c889bf.png")
    
    # Renderiza o Logo
    if os.path.exists(logo_path):
        logo_lateral = Image.open(logo_path)
        st.sidebar.image(logo_lateral, use_container_width=True)
    else:
        st.sidebar.markdown("## 🔴 AKOFS Offshore")
    
    st.sidebar.markdown("---")
