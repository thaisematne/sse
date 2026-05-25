import streamlit as st
import streamlit.components.v1 as components
import datetime
import json
import os
import uuid
import base64
from PIL import Image

# 1. CONFIGURAÇÃO DE DIRETÓRIOS E LOGO
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
logo_path = os.path.join(root_dir, "image_c889bf.png")

st.set_page_config(
    page_title="Cronograma de Prontidão | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def obter_base64_imagem(caminho_img):
    with open(caminho_img, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Cores Corporativas
AKOFS_RED = "#D32F2F"

# --- SIDEBAR PADRÃO DE NAVEGAÇÃO ---
if os.path.exists(logo_path):
    logo_lateral = Image.open(logo_path)
    st.sidebar.image(logo_lateral, use_container_width=True)
else:
    st.sidebar.markdown("## 🔴 AKOFS Offshore")
st.sidebar.markdown("---")

# ==========================================
# COLHEITA DE PARÂMETROS INICIAIS (ANTES DO CABEÇALHO PARA EXIBIÇÃO DINÂMICA)
# ==========================================
# Renderizado na tela, mas capturado para o cabeçalho de impressão
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.subheader("⏱️ Início da Operação")
col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))
st.markdown('</div>', unsafe_allow_html=True)

# --- CABEÇALHO UNIFICADO COM METADADOS DINÂMICOS DE IMPRESSÃO ---
if os.path.exists(logo_path):
    logo_base64 = obter_base64_imagem(logo_path)
    header_html = f"""
    <div class="print-header">
        <img src="data:image/png;base64,{logo_base64}" class="print-logo-img">
        <div class="print-header-text">
            <h1 style="color: {AKOFS_RED}; margin: 0; font-size: 2.2em;">Subsea Planner Pro</h1>
            <h3 style="margin: 3px 0 8px 0; font-weight: normal; color: #aaa;" class="subtitle-page">Cronograma de Prontidão</h3>
            <div class="print-only operational-metadata">
                <strong>INÍCIO DA OPERAÇÃO:</strong> {data_inicio.strftime('%d/%m/%Y')} às {hora_inicio.strftime('%H:%M')}
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='color: {AKOFS_RED}; text-align: center;'>Subsea Planner Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Cronograma de Prontidão</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='print-only' style='text-align: center; margin-bottom: 15px;'><strong>INÍCIO DA OPERAÇÃO:</strong> {data_inicio.strftime('%d/%m/%Y')} às {hora_inicio.strftime('%H:%M')}</div>", unsafe_allow_html=True)

# --- REGRAS DE ESTILO CSS: ENQUADRAMENTO E DISTRIBUIÇÃO FOCADA ---
st.markdown(
    """
    <style>
    /* Estilização da Logo e Cabeçalho na Tela */
    .print-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #333;
    }
    .print-logo-img {
        height: 55px;
        margin-right: 20px;
    }
    .print-only {
        display: none;
    }
    
    /* ==========================================
       ESTILOS EXCLUSIVOS DE IMPRESSÃO (A4 VERTICAL)
       ========================================== */
    @media print {
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
            color: #000000 !important;
        }
        
        @page {
            size: A4 portrait;
            margin: 12mm 15mm 12mm 15mm;
        }
        
        /* Ocultar tudo o que não seja: Cabeçalho, Programação e Resumo */
        section[data-testid="stSidebar"], 
        header[data-testid="stHeader"], 
        .stButton, 
        iframe,
        div[data-testid="stNotification"],
        .no-print,
        hr { 
            display: none !important; 
        }
        
        .print-only {
            display: block !important;
        }
        
        /* Reset de Fundo e Containers */
        html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
        }
        
        /* Centralização Avançada do Bloco de Cabeçalho */
        .print-header {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            border-bottom: 2px solid #000000 !important;
            margin-bottom: 25px !important;
            padding-bottom: 12px !important;
            background: #FFFFFF !important;
            width: 100% !important;
        }
        .print-header-text { text-align: center !important; }
        .print-logo-img {
            height: 50px !important;
            margin-right: 0px !important;
            margin-bottom: 10px !important;
        }
        .subtitle-page {
            color: #000000 !important;
            font-weight: bold !important;
            font-size: 13pt !important;
        }
        .operational-metadata {
            font-size: 11pt !important;
            margin-top: 5px !important;
            letter-spacing: 0.5px !important;
        }
        
        /* DISTRIBUTION ENGINE: Expande as colunas restantes para 100% da folha */
        div[data-testid="stHorizontalBlock"] {
            border-bottom: 1px solid #D3D3D3 !important;
            padding: 6px 0 !important;
            margin: 0 !important;
            gap: 0px !important;
        }
        /* Header da Tabela com Linha Mais Forte */
        div[data-testid="stHorizontalBlock"]:has(div p strong) {
            border-bottom: 2px solid #000000 !important;
            background-color: #F9F9F9 !important;
        }
        
        /* Dimensionamento Milimétrico das Colunas Ativas */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) { flex: none !important; width: 6% !important; max-width: 6% !important; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) { flex: none !important; width: 24% !important; max-width: 24% !important; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) { flex: none !important; width: 44% !important; max-width: 44% !important; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) { flex: none !important; width: 16% !important; max-width: 16% !important; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(5) { flex: none !important; width: 10% !important; max-width: 10% !important; }
        
        /* Oculta as colunas 6, 7 e 8 (Ações e botões de setas/excluir) */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6),
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7),
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(8) { 
            display: none !important; 
        }
        
        /* Formatação Limpa de Textos e Remoção de Caixas de Input */
        input, select, textarea, div[data-baseweb="base-input"] > input {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #000000 !important;
            padding: 0px !important;
            font-size: 10pt !important;
        }
        p, div, span, label, .stMarkdown {
            font-size: 10pt !important;
            line-height: 1.2 !important;
        }
        
        .block-container { padding: 0rem !important; }
        
        /* MÓDULO DE DESTAQUE: RESUMO OPERACIONAL */
        div[data-testid="stMetric"] {
            border: 2px solid #000000 !important;
            background-color: #F5F5F5 !important;
            padding: 15px !important;
            border-radius: 8px !important;
            text-align: center !important;
            margin-top: 30px !important; /* Afasta elegantemente da tabela */
        }
        div[data-testid="stMetricValue"] div {
            font-size: 24pt !important;
            font-weight: 800 !important
