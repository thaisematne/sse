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

# --- REGRAS DE ESTILO CSS PARA IMPRESSÃO EM 1 PÁGINA VERTICAL ---
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
    .print-header-text h1 {
        font-size: 2.2em;
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
        
        /* Configuração Estrita de Folha Vertical (Portrait) */
        @page {
            size: A4 portrait;
            margin: 8mm 12mm 8mm 12mm;
        }
        
        /* Ocultar Interface, Subtítulos de marcação e a COLUNA DE AÇÕES */
        section[data-testid="stSidebar"], 
        header[data-testid="stHeader"], 
        .stButton, 
        iframe,
        div[data-testid="stNotification"],
        .no-print,
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6),
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7),
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(8) { 
            display: none !important; 
        }

        /* Oculta as linhas de formulário de cadastro (que contém o Selectbox da Etapa) */
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) {
            display: none !important;
        }
        
        /* Reset de Fundo para Todos os Componentes */
        html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"],
        div[data-baseweb="input"], div[data-baseweb="base-input"], 
        div[data-baseweb="select"], div[data-testid="stTimeInput"],
        div[data-testid="stSelectbox"], div[data-testid="stDateInput"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
        }
        
        /* Formatação Limpa dos Inputs da Tabela */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="base-input"] > input,
        div[class*="stSelectbox"] > div,
        div[class*="stTimeInput"] > div,
        input, select, textarea {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            border-bottom: 1px dashed #999 !important;
            box-shadow: none !important;
            color: #000000 !important;
        }
        
        /* Centralização Absoluta do Cabeçalho no Relatório */
        .print-header {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            border-bottom: 2px solid #000000 !important;
            margin-bottom: 20px !important;
            padding-bottom: 10px !important;
            background: #FFFFFF !important;
            width: 100% !important;
        }
        .print-header-text {
            text-align: center !important;
            width: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }
        .print-header-text h1 {
            font-size: 28pt !important; /* LETRA MAIOR E COM MAIS DESTAQUE */
            margin: 0 !important;
            padding: 0 !important;
            color: #D32F2F !important;
        }
        .print-header-text h3 {
            font-size: 14pt !important;
            margin: 5px 0 0 0 !important;
            color: #666666 !important;
        }
        .print-logo-img {
            height: 65px !important;
            margin: 0 auto 12px auto !important;
            display: block !important;
        }
        
        /* Compactação Geral de Fontes para Forçar Página Única */
        p, div, span, label, input, .stMarkdown {
            font-size: 9.5pt !important;
            line-height: 1.1 !important;
            margin-bottom: 0px !important;
        }
        h2 { font-size: 11pt !important; }
        h3 { font-size: 10.5pt !important; }
        
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 8px !important;
        }
        hr {
            margin: 5px 0 !important;
            border-color: #000000 !important;
        }

        /* ==========================================
           DESTAQUE MÁXIMO DO RESUMO OPERACIONAL NA IMPRESSÃO
           ========================================== */
        div[data-testid="stMetric"] {
            border: 2px solid #000000 !important;
            background-color: #F5F5F5 !important;
            padding: 12px !important;
            border-radius: 6px !important;
            text-align: center !important;
            box-shadow: none !important;
        }
        div[data-testid="stMetric"] * {
            background-color: transparent !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 22pt !important; 
            font-weight: 800 !important;
            color: #D32F2F !important; 
        }
        div[data-testid="stMetricLabel"] div {
            font-size: 11pt !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
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

if "Outros" not in st.session_state.db["base_etapas"]:
    st.session_state.db["base_etapas"].append("Outros")
if "Limpeza" not in st.session_state.db["base_etapas"]:
    st.session_state.db["base_etapas"].insert(-2, "Limpeza")

def parse_tempo(tempo_str):
    try:
        tempo_str = str(tempo_str).strip()
        if ":" in tempo_str:
            partes = tempo_str.split(":")
            return int(partes[0]), int(partes[1])
        elif tempo_str.isdigit():
            return int(tempo_str), 0
    except:
        pass
    return 0, 0

# ==========================================
# 1. PARÂMETROS INICIAIS (DATA E HORA)
# ==========================================
st.markdown('<h3 class="no-print">⏱️ Início da Operação</h3>', unsafe_allow_html=True)
col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))
    
st.markdown('<hr class="no-print">', unsafe_allow_html=True)

# ==========================================
# 2. ÁREA DE INSERÇÃO DE ETAPAS (OCULTADA NA IMPRESSÃO)
# ==========================================
with st.container():
    st.markdown('<h3 class="no-print">Adicionar Nova Etapa</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])

    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39DA-RJS)", key="new_locacao")
    
    with col2:
        etapa_selecionada = st.selectbox("Selecione a Etapa", st.session_state.db["base_etapas"], key="new_etapa_sel")
        etapa_final = etapa_selecionada
        salvar_na_base = False
        
        if etapa_selecionada == "Outros":
            etapa_manual = st.text_input("Descreva a nova etapa:", placeholder="Digite aqui...", key="new_etapa_manual")
            etapa_final = etapa_manual
            salvar_na_base = st.checkbox("💾 Salvar na lista padrão", key="new_salvar_base")

    with col3:
        responsavel = st.text_input("Responsável", value="MPSV", key="new_responsavel")
    with col4:
        tempo_input = st.text_input("Tempo (HH:MM)", value="01:00", help="Use o formato HH:MM (ex: 01:30)", key="new_tempo")

    if st.button("➕ Adicionar à Programação", type="primary", key="btn_adicionar"):
        h, m = parse_tempo(tempo_input)
        
        if not locacao:
            st.error("Por favor, preencha a Locação.")
        elif etapa_selecionada == "Outros" and not etapa_final.strip():
            st.error("Por favor, descreva a etapa.")
        else:
            if salvar_na_base and etapa_final not in st.session_state.db["base_etapas"]:
                st.session_state.db["base_etapas"].insert(-1, etapa_final)

            nova_etapa = {
                "id": str(uuid.uuid4()),
                "Locação": locacao,
                "Etapa": etapa_final,
                "Responsável": responsavel,
                "Horas": h,
                "Minutos": m
            }
            st.session_state.db["programacao"].append(nova_etapa)
            salvar_dados(st.session_state.db)
            st.success("Etapa adicionada com sucesso!")
            st.rerun()

st.markdown('<hr class="no-print">', unsafe_allow_html=True)

# ==========================================
# 3. LISTA DINÂMICA (EDIÇÃO E REORDENAÇÃO)
# ==========================================
if st.session_state.db["programacao"]:
    st.subheader("📋 Programação Atual")

    hc1, hc2, hc3, hc4, hc5, hc_acoes = st.columns([0.4, 2, 3, 1.5, 1.2, 1.5])
    hc1.write("**#**")
    hc2.write("**Locação**")
    hc3.write("**Etapa**")
    hc4.write("**Responsável**")
    hc5.write("**Tempo**")
    hc_acoes.write("**Ações**")

    def atualizar_campo(index, campo, chave_widget):
        st.session_state.db["programacao"][index][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(index, chave_widget):
        h, m = parse_tempo(st.session_state[chave_widget])
        st.session_state.db["programacao"][index]["Horas"] = h
        st.session_state.db["programacao"][index]["Minutos"] = m
        salvar_dados(st.session_state.db)

    for idx, item in enumerate(st.session_state.db["programacao"]):
        if "id" not in item:
            item["id"] = str(uuid.uuid4())
            
        uid = item["id"]

        c1, c2, c3, c4, c5, c_up, c_down, c_del = st.columns([0.4, 2, 3, 1.5, 1.2, 0.5, 0.5, 0.5])
        
        c1.markdown(f"<div style='margin-top: 8px; font-weight: bold;'>{idx+1}</div>", unsafe_allow_html=True)
        
        c2.text_input("Locação", value=item["Locação"], key=f"loc_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"loc_{uid}"))
        c3.text_input("Etapa", value=item["Etapa"], key=f"et_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"et_{uid}"))
        c4.text_input("Responsável", value=item["Responsável"], key=f"resp_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"resp_{uid}"))
        
        tempo_formatado = f"{int(item.get('Horas', 0)):02d}:{int(item.get('Minutos', 0)):02d}"
        c5.text_input("Tempo", value=tempo_formatado, key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        with c_up:
            if st.button("⬆️", key=f"up_{uid}", help="Subir"):
                if idx > 0:
                    prog = st.session_state.db["programacao"]
                    prog[idx], prog[idx-1] = prog[idx-1], prog[idx]
                    salvar_dados(st.session_state.db)
                    st.rerun()
        with c_down:
            if st.button("⬇️", key=f"dw_{uid}", help="Descer"):
                if idx < len(st.session_state.db["programacao"]) - 1:
                    prog = st.session_state.db["programacao"]
                    prog[idx], prog[idx+1] = prog[idx+1], prog[idx]
                    salvar_dados(st.session_state.db)
                    st.rerun()
        with c_del:
            if st.button("❌", key=f"del_{uid}", help="Excluir"):
                st.session_state.db["programacao"].pop(idx)
                salvar_dados(st.session_state.db)
                st.rerun()

    # ==========================================
    # 4. CÁLCULO FINAL E BOTÕES DE AÇÃO
    # ==========================================
    st.divider()
    st.subheader("🎯 Resumo Operacional")

    total_horas = sum(int(item.get("Horas", 0)) for item in st.session_state.db["programacao"])
    total_minutos = sum(int(item.get("Minutos", 0)) for item in st.session_state.db["programacao"])

    total_horas += total_minutos // 60
    total_minutos = total_minutos % 60

    inicio_datetime = datetime.datetime.combine(data_inicio, hora_inicio)
    termino_datetime = inicio_datetime + datetime.timedelta(hours=total_horas, minutes=total_minutos)

    colA, colB = st.columns(2)
    with colA:
        st.metric(label="Duração Total Estimada", value=f"{int(total_horas):02d}h {int(total_minutos):02d}m")
    with colB:
        st.metric(label="Previsão de Prontidão", value=termino_datetime.strftime("%d/%m/%Y às %H:%M"))

    st.markdown('<hr class="no-print">', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        components.html(
            f"""
            <button onclick="window.parent.print()" style="
                background-color: {AKOFS_RED};
                color: white;
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.5rem;
                font-weight: 600;
                width: 100%;
                cursor: pointer;
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 1rem;
                box-sizing: border-box;
            ">🖨️ Imprimir / Salvar PDF</button>
            """,
            height=45
        )

    with col_btn2:
        if st.button("🗑️ Limpar Programação", key="btn_reset_total", use_container_width=True):
            st.session_state.db["programacao"] = []
            salvar_dados(st.session_state.db)
            st.rerun()
