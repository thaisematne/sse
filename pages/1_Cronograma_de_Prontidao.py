import streamlit as st
import streamlit.components.v1 as components
import datetime
import json
import os
import uuid
import base64
from PIL import Image

# 1. CONFIGURAÇÃO DE AMBIENTE
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
LOGO_PATH = os.path.join(root_dir, "image_c889bf.png")
ARQUIVO_DADOS = "dados_prontidao.json"
AKOFS_RED = "#D32F2F"

st.set_page_config(page_title="Relatório | Subsea Planner Pro", page_icon="⚓", layout="wide")

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

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64(LOGO_PATH)

# ==========================================
# 2. MOTOR DE IMPRESSÃO BLINDADO (CSS)
# ==========================================
css_style = """
<style>
/* Estilos para a Tela */
.print-only { display: none; }

@media print {
    /* 1. BLINDAGEM TOTAL DE CORES (Resolve a fonte branca) */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important; /* Força os inputs a ficarem pretos */
        text-shadow: none !important;
    }
    
    html, body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    /* Remove fundos dos inputs do Streamlit */
    div[data-baseweb], div[data-baseweb] * {
        background-color: transparent !important;
        background: none !important;
        border-color: #000000 !important;
    }

    /* 2. SUPRESSÃO DE ELEMENTOS DE TELA E MENU */
    header, section[data-testid="stSidebar"], footer, .stButton, iframe, 
    div[data-testid="stNotification"], .no-print, hr {
        display: none !important;
    }

    /* Oculta os formulários (Data/Hora e Cadastro de Etapa) */
    div.element-container:has(input), div.element-container:has(select) {
        display: none !important;
    }

    /* 3. ELIMINAÇÃO DAS COLUNAS DE AÇÕES (Cabeçalho e Botões) */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        page-break-inside: avoid !important; /* Evita que a linha corte na mudança de página */
        break-inside: avoid !important;
        border-bottom: 1px solid #EEEEEE !important;
        padding-bottom: 2px !important;
    }
    
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(n+6) {
        display: none !important;
        width: 0 !important;
        flex: 0 0 0 !important;
        overflow: hidden !important;
    }

    /* 4. REDISTRIBUIÇÃO DO LAYOUT PARA 100% DA LARGURA */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) { width: 5% !important; flex: 0 0 5% !important; display: block !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { width: 25% !important; flex: 0 0 25% !important; display: block !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) { width: 45% !important; flex: 0 0 45% !important; display: block !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(4) { width: 15% !important; flex: 0 0 15% !important; display: block !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(5) { width: 10% !important; flex: 0 0 10% !important; display: block !important; }

    /* Formatação limpa dos Inputs de texto */
    input[type="text"] {
        border: none !important;
        border-bottom: 1px dashed #BBBBBB !important;
        padding: 0px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* 5. CABEÇALHO IMPOSTO COM LETRAS MAIORES */
    .print-header {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        border-bottom: 3px solid #000000 !important;
        margin-bottom: 25px !important;
        padding-bottom: 15px !important;
        width: 100% !important;
    }
    .print-logo { height: 80px !important; margin-bottom: 15px !important; }
    .print-title { 
        font-size: 42pt !important; /* LETRA MASSIVA E DESTACADA */
        font-weight: 900 !important; 
        margin: 0 !important; 
        color: COLOR_AKOFS !important; 
        -webkit-text-fill-color: COLOR_AKOFS !important;
    }
    .print-subtitle { font-size: 18pt !important; margin-top: 5px !important; color: #555555 !important; font-weight: bold !important;}

    /* 6. CONFIGURAÇÃO DA FOLHA A4 */
    @page { size: A4 portrait; margin: 12mm 15mm; }
    p, div, span, label, input { font-size: 10.5pt !important; line-height: 1.1 !important; }
    
    /* 7. DESTAQUE DO RESUMO OPERACIONAL */
    div[data-testid="stMetric"] {
        border: 2px solid #000000 !important;
        background-color: #F8F8F8 !important;
        padding: 10px !important;
        border-radius: 6px !important;
        text-align: center !important;
    }
    .stMetricValue div { 
        font-size: 26pt !important; 
        font-weight: 900 !important; 
        color: COLOR_AKOFS !important; 
        -webkit-text-fill-color: COLOR_AKOFS !important;
    }
    
    .print-only { display: block !important; margin-bottom: 15px !important; font-weight: bold; text-align: center; }
}
</style>
"""
st.markdown(css_style.replace("COLOR_AKOFS", AKOFS_RED), unsafe_allow_html=True)

# ==========================================
# 3. CONTEÚDO DA TELA E RELATÓRIO
# ==========================================

# Cabeçalho de Impressão
st.markdown(f"""
<div class="print-header">
    {f'<img src="data:image/png;base64,{logo_b64}" class="print-logo">' if logo_b64 else ''}
    <div class="print-title">Subsea Planner Pro</div>
    <div class="print-subtitle">Cronograma de Prontidão Operacional</div>
</div>
""", unsafe_allow_html=True)

# INÍCIO DA OPERAÇÃO (Visível apenas na tela)
st.markdown('<div class="no-print"><h3>⏱️ Início da Operação</h3>', unsafe_allow_html=True)
c_h1, c_h2, _ = st.columns([1, 1, 2])
with c_h1: data_op = st.date_input("Data", datetime.date.today())
with c_h2: hora_op = st.time_input("Hora", datetime.time(6, 0))
st.markdown('</div>', unsafe_allow_html=True)

# Data da Operação formatada para o PDF
st.markdown(f'<div class="print-only">INÍCIO DA OPERAÇÃO: {data_op.strftime("%d/%m/%Y")} às {hora_op.strftime("%H:%M")}</div>', unsafe_allow_html=True)

# ADICIONAR ETAPA (Oculto na Impressão)
st.markdown('<div class="no-print"><hr><h3>➕ Adicionar Etapa</h3>', unsafe_allow_html=True)
c_a1, c_h2, c_h3, c_h4 = st.columns([2, 3, 1.5, 1])
with c_a1: loc_in = st.text_input("Locação", placeholder="Ex: 9-BUZ-39", key="ni_loc")
with c_h2: etp_in = st.text_input("Etapa", placeholder="Atividade...", key="ni_etp")
with c_h3: res_in = st.text_input("Responsável", value="MPSV", key="ni_res")
with c_h4: tmp_in = st.text_input("Tempo", value="01:00", key="ni_tmp")

if st.button("Adicionar à Lista", type="primary"):
    if loc_in and etp_in:
        try:
            h, m = map(int, tmp_in.split(':'))
            st.session_state.db["programacao"].append({
                "id": str(uuid.uuid4()), "Locação": loc_in, "Etapa": etp_in, "Responsável": res_in, "Horas": h, "Minutos": m
            })
            salvar_dados(st.session_state.db); st.rerun()
        except: st.error("Use HH:MM")
st.markdown('</div><hr>', unsafe_allow_html=True)

# PROGRAMAÇÃO ATUAL
st.subheader("📋 Programação Atual")
if st.session_state.db["programacao"]:
    
    # Headers
    hc = st.columns([0.4, 2, 3, 1.5, 1.2, 1.5])
    labels = ["#", "Locação", "Etapa", "Responsável", "Tempo", "Ações"]
    for i, l in enumerate(labels): hc[i].write(f"**{l}**")

    def update_db(idx, field, key):
        st.session_state.db["programacao"][idx][field] = st.session_state[key]
        salvar_dados(st.session_state.db)

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item.get("id", str(uuid.uuid4()))
        c = st.columns([0.4, 2, 3, 1.5, 1.2, 0.5, 0.5, 0.5])
        
        c[0].markdown(f"<div style='margin-top:8px; font-weight:bold;'>{idx+1}</div>", unsafe_allow_html=True)
        c[1].text_input("L", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=update_db, args=(idx, "Locação", f"l_{uid}"))
        c[2].text_input("E", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=update_db, args=(idx, "Etapa", f"e_{uid}"))
        c[3].text_input("R", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=update_db, args=(idx, "Responsável", f"r_{uid}"))
        t_val = f"{int(item.get('Horas',0)):02d}:{int(item.get('Minutos',0)):02d}"
        c[4].text_input("T", value=t_val, key=f"t_{uid}", label_visibility="collapsed")
        
        with c[5]:
            if st.button("⬆️", key=f"u_{uid}") and idx > 0:
                st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
                salvar_dados(st.session_state.db); st.rerun()
        with c[6]:
            if st.button("⬇️", key=f"d_{uid}") and idx < len(st.session_state.db["programacao"])-1:
                st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx+1] = st.session_state.db["programacao"][idx+1], st.session_state.db["programacao"][idx]
                salvar_dados(st.session_state.db); st.rerun()
        with c[7]:
            if st.button("❌", key=f"x_{uid}"):
                st.session_state.db["programacao"].pop(idx)
                salvar_dados(st.session_state.db); st.rerun()

# RESUMO OPERACIONAL
st.divider()
st.subheader("🎯 Resumo Operacional")
tot_m = sum(int(i.get("Horas", 0))*60 + int(i.get("Minutos", 0)) for i in st.session_state.db["programacao"])
fim_dt = datetime.datetime.combine(data_op, hora_op) + datetime.timedelta(minutes=tot_m)

colA, colB = st.columns(2)
colA.metric("Duração Total Estimada", f"{tot_m//60:02d}h {tot_m%60:02d}m")
colB.metric("Previsão de Prontidão", fim_dt.strftime("%d/%m/%Y às %H:%M"))

# BOTÕES DE AÇÃO DA TELA (Ocultos no PDF)
st.markdown('<div class="no-print"><hr>', unsafe_allow_html=True)
cb1, cb2, _ = st.columns([1.2, 1, 2])
with cb1:
    components.html(f"""
        <button onclick="window.parent.print()" style="background:{AKOFS_RED};color:white;border:none;padding:12px;border-radius:5px;width:100%;font-weight:bold;cursor:pointer;font-family:sans-serif;font-size:1rem;">
        🖨️ Imprimir Relatório PDF
        </button>""", height=60)
with cb2:
    if st.button("🗑️ Limpar Cronograma", use_container_width=True):
        st.session_state.db["programacao"] = []
        salvar_dados(st.session_state.db); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
if os.path.exists(LOGO_PATH): st.sidebar.image(LOGO_PATH, use_container_width=True)
st.sidebar.markdown("---")
