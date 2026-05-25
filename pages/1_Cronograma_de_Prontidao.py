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

# --- CABEÇALHO UNIFICADO COM CENTRALIZAÇÃO ---
if os.path.exists(logo_path):
    logo_base64 = obter_base64_imagem(logo_path)
    header_html = f"""
    <div class="print-header">
        <img src="data:image/png;base64,{logo_base64}" class="print-logo-img">
        <div class="print-header-text">
            <h1 style="color: {AKOFS_RED}; margin: 0;">Subsea Planner Pro</h1>
            <h3 style="margin: 5px 0 0 0; font-weight: normal; color: #aaa;">Cronograma de Prontidão</h3>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='color: {AKOFS_RED}; text-align: center;'>Subsea Planner Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Cronograma de Prontidão</h3>", unsafe_allow_html=True)

# --- REGRAS DE ESTILO CSS PARA IMPRESSÃO PROFISSIONAL ---
st.markdown(
    """
    <style>
    /* Estilização do cabeçalho na tela */
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
            margin: 10mm 15mm;
        }
        
        /* Ocultar Interface e elementos desnecessários */
        section[data-testid="stSidebar"], 
        header[data-testid="stHeader"], 
        .stButton, 
        iframe,
        div[data-testid="stNotification"],
        .no-print,
        hr { 
            display: none !important; 
        }

        /* OCULTAR COLUNAS DE AÇÕES (Cabeçalho e Botões) */
        /* Alvos: Coluna 6 do header e Colunas 6, 7 e 8 das linhas */
        div[data-testid="column"]:nth-child(n+6) {
            display: none !important;
        }

        /* OCULTAR FORMULÁRIO DE ADICIONAR ETAPA */
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]),
        div[data-testid="stHorizontalBlock"]:has(input[key="new_locacao"]) {
            display: none !important;
        }
        
        /* Reset de Fundo e Containers */
        html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
        }
        
        /* Centralização e Aumento do Cabeçalho no PDF */
        .print-header {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
            border-bottom: 2.5px solid #000000 !important;
            margin-bottom: 30px !important;
            padding-bottom: 15px !important;
            width: 100% !important;
        }
        .print-header-text h1 {
            font-size: 36pt !important; /* TITULO BEM MAIOR NA IMPRESSÃO */
            font-weight: 900 !important;
            color: #D32F2F !important;
        }
        .print-header-text h3 {
            font-size: 16pt !important;
            color: #444444 !important;
            font-weight: bold !important;
        }
        .print-logo-img {
            height: 70px !important;
            margin: 0 0 15px 0 !important;
        }
        
        /* Distribuição das colunas para ocupar 100% da largura sem as ações */
        div[data-testid="column"]:nth-child(1) { width: 5% !important; flex: none !important; }
        div[data-testid="column"]:nth-child(2) { width: 25% !important; flex: none !important; }
        div[data-testid="column"]:nth-child(3) { width: 40% !important; flex: none !important; }
        div[data-testid="column"]:nth-child(4) { width: 20% !important; flex: none !important; }
        div[data-testid="column"]:nth-child(5) { width: 10% !important; flex: none !important; }

        /* Estilo dos campos na tabela */
        input {
            border: none !important;
            border-bottom: 1px solid #ccc !important;
            background: transparent !important;
            font-size: 10pt !important;
        }

        /* Resumo Operacional */
        div[data-testid="stMetric"] {
            border: 2px solid #000000 !important;
            background-color: #F8F8F8 !important;
            padding: 15px !important;
            text-align: center !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 24pt !important;
            font-weight: 800 !important;
            color: #D32F2F !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

ARQUIVO_DADOS = "dados_prontidao.json"

ETAPAS_DEFAULT = [
    "Navegar para a locação", "Check list de DP", "Descer ROV",
    "Inspeção inicial", "Descer equipamento", "Instalar equipamento",
    "Manuseio de EFL", "Manuseio de HFL", "Manuseio de válvula",
    "Etapas da UEP", "Realizar testes / intervenção",
    "Limpeza", "Desmobilizar equipamento", "Recolher equipamento",
    "Inspeção final", "Subir ROV", "Aguardar prontidão", "Outros"
]

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

def parse_tempo(tempo_str):
    try:
        tempo_str = str(tempo_str).strip()
        if ":" in tempo_str:
            partes = tempo_str.split(":")
            return int(partes[0]), int(partes[1])
        elif tempo_str.isdigit():
            return int(tempo_str), 0
    except: pass
    return 0, 0

# ==========================================
# 1. PARÂMETROS INICIAIS
# ==========================================
st.markdown('<h3 class="no-print">⏱️ Início da Operação</h3>', unsafe_allow_html=True)
col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))
st.divider()

# ==========================================
# 2. ÁREA DE INSERÇÃO (OCULTADA NO PDF)
# ==========================================
with st.container():
    st.markdown('<h3 class="no-print">➕ Adicionar Nova Etapa</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])
    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39)", key="new_locacao")
    with col2:
        etapa_sel = st.selectbox("Selecione a Etapa", st.session_state.db["base_etapas"], key="new_etapa_sel")
        etapa_final = etapa_sel
        if etapa_sel == "Outros":
            etapa_final = st.text_input("Descreva a etapa:", key="new_etapa_manual")
    with col3:
        responsavel = st.text_input("Responsável", value="MPSV", key="new_responsavel")
    with col4:
        tempo_input = st.text_input("Tempo (HH:MM)", value="01:00", key="new_tempo")

    if st.button("Adicionar à Programação", type="primary", key="btn_adicionar"):
        h, m = parse_tempo(tempo_input)
        if locacao and etapa_final:
            nova_etapa = {
                "id": str(uuid.uuid4()), "Locação": locacao, "Etapa": etapa_final,
                "Responsável": responsavel, "Horas": h, "Minutos": m
            }
            st.session_state.db["programacao"].append(nova_etapa)
            salvar_dados(st.session_state.db)
            st.rerun()

# ==========================================
# 3. PROGRAMAÇÃO ATUAL
# ==========================================
if st.session_state.db["programacao"]:
    st.markdown("### 📋 Programação Atual")
    
    # Header da tabela
    hc = st.columns([0.4, 2, 3, 1.5, 1.2, 1.5])
    for i, t in enumerate(["#", "Locação", "Etapa", "Responsável", "Tempo", "Ações"]):
        hc[i].write(f"**{t}**")

    def update_field(idx, field, key):
        st.session_state.db["programacao"][idx][field] = st.session_state[key]
        salvar_dados(st.session_state.db)

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item.get("id", str(uuid.uuid4()))
        c = st.columns([0.4, 2, 3, 1.5, 1.2, 0.5, 0.5, 0.5])
        
        c[0].markdown(f"<div style='margin-top: 8px;'>{idx+1}</div>", unsafe_allow_html=True)
        c[1].text_input("Loc", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=update_field, args=(idx, "Locação", f"l_{uid}"))
        c[2].text_input("Etp", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=update_field, args=(idx, "Etapa", f"e_{uid}"))
        c[3].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=update_field, args=(idx, "Responsável", f"r_{uid}"))
        tempo_str = f"{int(item.get('Horas', 0)):02d}:{int(item.get('Minutos', 0)):02d}"
        c[4].text_input("T", value=tempo_str, key=f"t_{uid}", label_visibility="collapsed")
        
        with c[5]:
            if st.button("⬆️", key=f"up_{uid}") and idx > 0:
                prog = st.session_state.db["programacao"]
                prog[idx], prog[idx-1] = prog[idx-1], prog[idx]
                salvar_dados(st.session_state.db); st.rerun()
        with c[6]:
            if st.button("⬇️", key=f"dw_{uid}") and idx < len(st.session_state.db["programacao"]) - 1:
                prog = st.session_state.db["programacao"]
                prog[idx], prog[idx+1] = prog[idx+1], prog[idx]
                salvar_dados(st.session_state.db); st.rerun()
        with c[7]:
            if st.button("❌", key=f"del_{uid}"):
                st.session_state.db["programacao"].pop(idx)
                salvar_dados(st.session_state.db); st.rerun()

# ==========================================
# 4. RESUMO E IMPRESSÃO
# ==========================================
st.divider()
total_h = sum(int(i.get("Horas", 0)) for i in st.session_state.db["programacao"])
total_m = sum(int(i.get("Minutos", 0)) for i in st.session_state.db["programacao"])
total_h += total_m // 60
total_m %= 60

inicio_dt = datetime.datetime.combine(data_inicio, hora_inicio)
fim_dt = inicio_dt + datetime.timedelta(hours=total_h, minutes=total_m)

st.subheader("🎯 Resumo Operacional")
colA, colB = st.columns(2)
colA.metric("Duração Total Estimada", f"{total_h:02d}h {total_m:02d}m")
colB.metric("Previsão de Prontidão", fim_dt.strftime("%d/%m/%Y às %H:%M"))

st.divider()
col_print, col_clear, _ = st.columns([1, 1, 2])
with col_print:
    components.html(f"""
        <button onclick="window.parent.print()" style="background:{AKOFS_RED};color:white;border:none;padding:10px;border-radius:5px;width:100%;font-weight:bold;cursor:pointer;">
        🖨️ Imprimir Relatório PDF
        </button>""", height=50)
with col_clear:
    if st.button("🗑️ Limpar Programação", use_container_width=True):
        st.session_state.db["programacao"] = []
        salvar_dados(st.session_state.db); st.rerun()
