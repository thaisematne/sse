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
# 2. MOTOR DE IMPRESSÃO (CSS RADICAL)
# ==========================================
st.markdown(f"""
<style>
/* Estilos para a Tela */
.print-only {{ display: none; }}

@media print {{
    /* 1. RESET TOTAL DE CORES */
    * {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        background-color: transparent !important;
        color: black !important;
    }}
    
    html, body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {{
        background-color: white !important;
    }}

    /* 2. ELIMINAÇÃO DE FUNDOS ESCUROS (INPUTS E MÉTRICAS) */
    div[data-baseweb], div[data-baseweb] *, [data-testid="stMetric"], [data-testid="stMetricValue"] * {{
        background-color: white !important;
        background: white !important;
        border-color: #eee !important;
    }}

    /* 3. SUPRESSÃO DE CONTEÚDO (CONFORME SOLICITADO) */
    header, section[data-testid="stSidebar"], footer, .stButton, iframe, 
    div[data-testid="stNotification"], .no-print, hr {{
        display: none !important;
    }}

    /* Oculta colunas de ações na tabela (6, 7 e 8) */
    div[data-testid="column"]:nth-child(6),
    div[data-testid="column"]:nth-child(7),
    div[data-testid="column"]:nth-child(8) {{
        display: none !important;
    }}

    /* Oculta as linhas de input (Data/Hora e Cadastro) */
    div.element-container:has(input), div.element-container:has(select) {{
        display: none !important;
    }}

    /* 4. REDISTRIBUIÇÃO DO LAYOUT */
    div[data-testid="column"]:nth-child(1) {{ width: 5% !important; flex: none !important; }}
    div[data-testid="column"]:nth-child(2) {{ width: 25% !important; flex: none !important; }}
    div[data-testid="column"]:nth-child(3) {{ width: 45% !important; flex: none !important; }}
    div[data-testid="column"]:nth-child(4) {{ width: 15% !important; flex: none !important; }}
    div[data-testid="column"]:nth-child(5) {{ width: 10% !important; flex: none !important; }}

    /* 5. CABEÇALHO IMPOSTO E CENTRALIZADO */
    .print-header {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        border-bottom: 3px solid black !important;
        margin-bottom: 25px !important;
        padding-bottom: 15px !important;
        width: 100% !important;
    }}
    .print-logo {{ height: 80px !important; margin-bottom: 15px !important; }}
    .print-title {{ font-size: 38pt !important; font-weight: 900 !important; margin: 0 !important; color: {AKOFS_RED} !important; }}
    .print-subtitle {{ font-size: 18pt !important; margin-top: 5px !important; color: #555 !important; }}

    /* 6. COMPACTAÇÃO PARA PÁGINA ÚNICA */
    @page {{ size: A4 portrait; margin: 12mm 15mm; }}
    p, div, span, label, input {{ font-size: 10pt !important; line-height: 1.1 !important; }}
    .stMetricValue div {{ font-size: 24pt !important; font-weight: bold !important; color: {AKOFS_RED} !important; }}
    
    .print-only {{ display: block !important; margin-bottom: 15px !important; font-weight: bold; text-align: center; }}
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CONTEÚDO (ORDEM LÓGICA)
# ==========================================

# Cabeçalho de Impressão (Centralizado)
st.markdown(f"""
<div class="print-header">
    {f'<img src="data:image/png;base64,{logo_b64}" class="print-logo">' if logo_b64 else ''}
    <div class="print-title">Subsea Planner Pro</div>
    <div class="print-subtitle">Cronograma de Prontidão Operacional</div>
</div>
""", unsafe_allow_html=True)

# PARTE 1: INÍCIO DA OPERAÇÃO (Visível apenas na tela)
st.markdown('<div class="no-print"><h3>⏱️ Início da Operação</h3>', unsafe_allow_html=True)
c_h1, c_h2, _ = st.columns([1, 1, 2])
with c_h1: data_op = st.date_input("Data", datetime.date.today())
with c_h2: hora_op = st.time_input("Hora", datetime.time(6, 0))
st.markdown('</div>', unsafe_allow_html=True)

# Data da Operação para o PDF
st.markdown(f'<div class="print-only">INÍCIO DA OPERAÇÃO: {data_op.strftime("%d/%m/%Y")} às {hora_op.strftime("%H:%M")}</div>', unsafe_allow_html=True)

# PARTE 2: ADICIONAR ETAPA (Oculto na Impressão)
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

# PARTE 3: PROGRAMAÇÃO ATUAL
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
        
        c[0].markdown(f"<div style='margin-top:8px;'>{idx+1}</div>", unsafe_allow_html=True)
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

# PARTE 4: RESUMO OPERACIONAL
st.divider()
st.subheader("🎯 Resumo Operacional")
tot_m = sum(int(i.get("Horas", 0))*60 + int(i.get("Minutos", 0)) for i in st.session_state.db["programacao"])
fim_dt = datetime.datetime.combine(data_op, hora_op) + datetime.timedelta(minutes=tot_m)

colA, colB = st.columns(2)
colA.metric("Duração Total", f"{tot_m//60:02d}h {tot_m%60:02d}m")
colB.metric("Previsão de Prontidão", fim_dt.strftime("%d/%m/%Y às %H:%M"))

# Botões Finais (Apenas Tela)
st.markdown('<div class="no-print"><hr>', unsafe_allow_html=True)
cb1, cb2, _ = st.columns([1.2, 1, 2])
with cb1:
    components.html(f"""
        <button onclick="window.parent.print()" style="background:{AKOFS_RED};color:white;border:none;padding:12px;border-radius:5px;width:100%;font-weight:bold;cursor:pointer;font-family:sans-serif;">
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
