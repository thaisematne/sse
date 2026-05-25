import streamlit as st
import streamlit.components.v1 as components
import datetime
import json
import os
import uuid
import base64
from PIL import Image

# 1. GERENCIAMENTO DE CAMINHOS E IDENTIDADE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "image_c889bf.png")
ARQUIVO_DADOS = "dados_prontidao.json"
AKOFS_RED = "#D32F2F"

st.set_page_config(page_title="Cronograma | Subsea Planner Pro", page_icon="⚓", layout="wide")

# Função para injetar a logo no PDF via Base64
def get_base64_logo(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64_logo(LOGO_PATH)

# ==========================================
# 2. ESTILO CSS (TELA vs IMPRESSÃO A4)
# ==========================================
st.markdown(f"""
    <style>
    /* Estilo para a TELA (Dark Mode) */
    .screen-header {{ margin-bottom: 2rem; }}
    
    /* ==========================================
       REGRAS DE IMPRESSÃO (CSS PRINT)
       ========================================== */
    @media print {{
        /* Configuração da Página A4 */
        @page {{
            size: A4 portrait;
            margin: 10mm 15mm;
        }}
        
        /* Reset de Cores: Fundo Branco e Texto Preto */
        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background-color: white !important;
            color: black !important;
        }}
        
        /* Ocultar elementos de UI do Streamlit */
        section[data-testid="stSidebar"], 
        header[data-testid="stHeader"], 
        footer, .stButton, iframe, 
        [data-testid="stNotification"],
        .no-print {{ 
            display: none !important; 
        }}

        /* Ocultar colunas de Ações (6, 7 e 8) na tabela */
        div[data-testid="column"]:nth-child(6),
        div[data-testid="column"]:nth-child(7),
        div[data-testid="column"]:nth-child(8) {{
            display: none !important;
        }}

        /* Ajuste de colunas para ocupar 100% da largura */
        div[data-testid="column"]:nth-child(1) {{ width: 5% !important; }}
        div[data-testid="column"]:nth-child(2) {{ width: 20% !important; }}
        div[data-testid="column"]:nth-child(3) {{ width: 45% !important; }}
        div[data-testid="column"]:nth-child(4) {{ width: 20% !important; }}
        div[data-testid="column"]:nth-child(5) {{ width: 10% !important; }}

        /* Cabeçalho de Impressão Centralizado */
        .print-header {{
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
            border-bottom: 2px solid black !important;
            margin-bottom: 20px !important;
            padding-bottom: 10px !important;
        }}
        
        .print-logo {{ height: 50px !important; margin-bottom: 10px !important; }}
        
        /* Compactação de Fontes para Página Única */
        p, div, span, label, input {{
            font-size: 10pt !important;
            color: black !important;
        }}
        h1 {{ font-size: 18pt !important; margin: 0 !important; }}
        h3 {{ font-size: 12pt !important; margin: 5px 0 !important; }}

        /* Remover bordas de inputs na impressão */
        input {{ border: none !important; border-bottom: 1px solid #ccc !important; }}
        
        /* Destaque do Resumo Operacional */
        .resumo-box {{
            border: 2px solid black !important;
            padding: 15px !important;
            margin-top: 20px !important;
            background-color: #f0f0f0 !important;
            border-radius: 5px !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE DADOS
# ==========================================
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 4. CONTEÚDO DA PÁGINA
# ==========================================

# CABEÇALHO (Visível na tela e formatado para Print)
if logo_b64:
    st.markdown(f"""
        <div class="print-header">
            <img src="data:image/png;base64,{logo_b64}" class="print-logo">
            <h1>Subsea Planner Pro</h1>
            <h3 style="color: {AKOFS_RED};">Cronograma de Prontidão</h3>
        </div>
    """, unsafe_allow_html=True)

# PASSO 1: DATA E HORA DE INÍCIO
st.subheader("1. Início da Operação")
c_in1, c_in2, c_in3 = st.columns([1, 1, 2])
with c_in1:
    data_inicio = st.date_input("Data", datetime.date.today())
with c_in2:
    hora_inicio = st.time_input("Hora", datetime.time(6, 0))

# PASSO 2: ADICIONAR ETAPAS (OCULTO NA IMPRESSÃO)
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.divider()
st.subheader("2. Adicionar Nova Etapa")
col_add1, col_add2, col_add3, col_add4 = st.columns([2, 3, 1.5, 1])

with col_add1:
    loc = st.text_input("Locação", placeholder="Ex: 9-BUZ-39", key="in_loc")
with col_add2:
    etp = st.text_input("Etapa", placeholder="Descrever atividade...", key="in_etp")
with col_add3:
    resp = st.text_input("Responsável", value="MPSV", key="in_resp")
with col_add4:
    tempo = st.text_input("HH:MM", value="01:00", key="in_tempo")

if st.button("➕ Adicionar à Lista", type="primary"):
    if loc and etp:
        try:
            h, m = map(int, tempo.split(':'))
            st.session_state.db["programacao"].append({
                "id": str(uuid.uuid4()), "loc": loc, "etp": etp, "resp": resp, "h": h, "m": m
            })
            salvar_dados(st.session_state.db)
            st.rerun()
        except: st.error("Formato de tempo inválido (HH:MM)")
st.markdown('</div>', unsafe_allow_html=True)

# PASSO 3: TABELA DE PROGRAMAÇÃO
st.divider()
st.subheader("3. Programação Atual")

if st.session_state.db["programacao"]:
    # Header da Tabela
    h_col = st.columns([0.4, 1.5, 3, 1.5, 1, 0.4, 0.4, 0.4])
    cols_txt = ["#", "Locação", "Etapa", "Responsável", "Tempo", "", "", ""]
    for i, texto in enumerate(cols_txt): h_col[i].write(f"**{texto}**")

    # Linhas da Tabela
    for idx, item in enumerate(st.session_state.db["programacao"]):
        c = st.columns([0.4, 1.5, 3, 1.5, 1, 0.4, 0.4, 0.4])
        uid = item["id"]
        
        c[0].write(f"{idx+1}")
        c[1].write(item["loc"])
        c[2].write(item["etp"])
        c[3].write(item["resp"])
        c[4].write(f"{item['h']:02d}:{item['m']:02d}")
        
        # Botões de Ação (Ocultos no Print via CSS)
        if c[5].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db); st.rerun()
            
        if c[6].button("⬇️", key=f"dw_{uid}") and idx < len(st.session_state.db["programacao"])-1:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx+1] = st.session_state.db["programacao"][idx+1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db); st.rerun()
            
        if c[7].button("❌", key=f"del_{uid}"):
            st.session_state.db["programacao"].pop(idx)
            salvar_dados(st.session_state.db); st.rerun()

# PASSO 4: RESUMO OPERACIONAL (DESTAQUE NO PRINT)
st.divider()
total_m = sum(i['h']*60 + i['m'] for i in st.session_state.db["programacao"])
duracao = f"{total_m//60:02d}h {total_m%60:02d}m"
previsao = (datetime.datetime.combine(data_inicio, hora_inicio) + datetime.timedelta(minutes=total_m)).strftime("%d/%m/%Y às %H:%M")

st.markdown(f"""
    <div class="resumo-box">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <p style="margin:0; font-weight: bold; text-transform: uppercase;">Duração Total Estimada</p>
                <h2 style="margin:0; color: {AKOFS_RED};">{duracao}</h2>
            </div>
            <div>
                <p style="margin:0; font-weight: bold; text-transform: uppercase;">Previsão de Prontidão</p>
                <h2 style="margin:0; color: {AKOFS_RED};">{previsao}</h2>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# BOTÕES DE CONTROLE FINAL (OCULTOS NO PRINT)
st.markdown('<div class="no-print" style="margin-top: 2rem;">', unsafe_allow_html=True)
col_fin1, col_fin2, col_fin3 = st.columns([1.5, 1.5, 3])

with col_fin1:
    components.html(f"""
        <button onclick="window.parent.print()" style="
            background-color: {AKOFS_RED}; color: white; border: none; 
            padding: 10px 20px; border-radius: 5px; cursor: pointer; 
            width: 100%; font-weight: bold;">🖨️ Imprimir Relatório A4</button>
    """, height=50)

with col_fin2:
    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        st.session_state.db["programacao"] = []
        salvar_dados(st.session_state.db)
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar (Streamlit padrão)
st.sidebar.image(LOGO_PATH, use_container_width=True) if os.path.exists(LOGO_PATH) else st.sidebar.title("AKOFS")
st.sidebar.markdown("---")
