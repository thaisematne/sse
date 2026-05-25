import streamlit as st
import streamlit.components.v1 as components
import datetime
import json
import os
import uuid
import base64
from PIL import Image

# ==========================================
# 1. CONFIGURAÇÃO INICIAL E IDENTIDADE
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
LOGO_PATH = os.path.join(root_dir, "image_c889bf.png")
ARQUIVO_DADOS = "dados_prontidao.json"
AKOFS_RED = "#D32F2F"

st.set_page_config(page_title="Cronograma | Subsea Planner Pro", page_icon="⚓", layout="wide")

def obter_base64_imagem(caminho_img):
    if os.path.exists(caminho_img):
        with open(caminho_img, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = obter_base64_imagem(LOGO_PATH)

# ==========================================
# 2. MOTOR CSS (TELA vs. IMPRESSÃO A4)
# Código blindado contra SyntaxError (sem f-strings no CSS)
# ==========================================
css_style = """
<style>
/* ==========================================
   REGRAS EXCLUSIVAS DE IMPRESSÃO (A4 VERTICAL)
   ========================================== */
@media print {
    /* Força a fidelidade de cores e texto preto */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color: #000000 !important;
    }
    
    @page {
        size: A4 portrait;
        margin: 15mm;
    }
    
    /* OCULTA TUDO O QUE NÃO FOR O RELATÓRIO (Sidebar, Formulários, Botões) */
    section[data-testid="stSidebar"], 
    header[data-testid="stHeader"], 
    .stButton, iframe, div[data-testid="stNotification"], 
    .no-print { 
        display: none !important; 
    }
    
    html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* OCULTA A COLUNA DE AÇÕES NA TABELA (Colunas 6, 7 e 8) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6),
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7),
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(8) { 
        display: none !important; 
    }

    /* REDISTRIBUI AS COLUNAS PARA OCUPAR 100% DA FOLHA A4 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) { width: 5% !important; flex: none !important; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) { width: 25% !important; flex: none !important; }
    div[data-testid="stHorizontalBlock"] > div[data
