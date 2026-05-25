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
            font-weight: 800 !important;
            color: #D32F2F !important;
        }
        div[data-testid="stMetricLabel"] div {
            font-size: 11pt !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
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
# 2. ÁREA DE INSERÇÃO DE ETAPAS (OCULTADA NA IMPRESSÃO)
# ==========================================
st.markdown('<div class="no-print">', unsafe_allow_html=True)
with st.container():
    st.subheader("➕ Adicionar Nova Etapa")
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

    if st.button("Adicionar à Programação", type="primary", key="btn_adicionar"):
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
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. LISTA DINÂMICA / TABELA DO CRONOGRAMA
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
    # 4. CÁLCULO FINAL / RESUMO OPERACIONAL
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

    st.divider()
    
    # Linha de Controle Inferior (Apenas em Tela)
    st.markdown('<div class="no-print">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
