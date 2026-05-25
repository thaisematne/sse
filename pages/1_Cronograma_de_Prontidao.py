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
# 2. MOTOR DE IMPRESSÃO BLINDADO
# ==========================================
css_style = """
<style>
/* Estilos para a Tela */
.print-only { display: none; }

@media print {
    /* RESET DE CORES */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color: #000000 !important;
    }
    html, body, .stApp, .block-container { background-color: white !important; }

    /* SUPRESSÃO DE ELEMENTOS DE TELA */
    header, section[data-testid="stSidebar"], footer, .stButton, iframe, 
    .no-print, div[data-testid="stNotification"], hr { display: none !important; }

    /* OCULTAR COLUNAS DE AÇÕES (6, 7 e 8) E FORMULÁRIOS */
    div[data-testid="column"]:nth-child(n+6) { display: none !important; }
    div.element-container:has(input), div.element-container:has(select) { display: none !important; }

    /* DISTRIBUIÇÃO DAS COLUNAS (Tabela ocupa a folha toda) */
    div[data-testid="column"]:nth-child(1) { width: 5% !important; flex: 0 0 5% !important; }
    div[data-testid="column"]:nth-child(2) { width: 25% !important; flex: 0 0 25% !important; }
    div[data-testid="column"]:nth-child(3) { width: 45% !important; flex: 0 0 45% !important; }
    div[data-testid="column"]:nth-child(4) { width: 15% !important; flex: 0 0 15% !important; }
    div[data-testid="column"]:nth-child(5) { width: 10% !important; flex: 0 0 10% !important; }

    /* CONVERSÃO DE INPUTS PARA TEXTO FIXO (SOLUÇÃO DA FONTE BRANCA) */
    input { 
        display: none !important; 
    }
    .print-text { 
        display: block !important; 
        border-bottom: 1px dashed #ccc !important;
        padding: 5px 0 !important;
        font-size: 11pt !important;
    }

    /* CABEÇALHO CENTRALIZADO */
    .print-header {
        display: flex !important; flex-direction: column !important;
        align-items: center !important; text-align: center !important;
        border-bottom: 3px solid black !important;
        margin-bottom: 30px !important; padding-bottom: 15px !important;
    }
    .print-logo { height: 80px !important; margin-bottom: 10px !important; }
    .print-title { font-size: 42pt !important; font-weight: 900 !important; color: #D32F2F !important; margin: 0 !important; }
    .print-subtitle { font-size: 16pt !important; color: #555 !important; font-weight: bold !important; }

    /* RESUMO OPERACIONAL */
    div[data-testid="stMetric"] {
        border: 2px solid black !important; padding: 15px !important; text-align: center !important;
    }
    .stMetricValue div { font-size: 26pt !important; color: #D32F2F !important; }
    
    @page { size: A4 portrait; margin: 15mm; }
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# ==========================================
# 3. CONTEÚDO
# ==========================================

# Cabeçalho
st.markdown(f"""
<div class="print-header">
    {f'<img src="data:image/png;base64,{logo_b64}" class="print-logo">' if logo_b64 else ''}
    <div class="print-title">Subsea Planner Pro</div>
    <div class="print-subtitle">Cronograma de Prontidão Operacional</div>
</div>
""", unsafe_allow_html=True)

# PARTE 1: INÍCIO (Tela)
st.markdown('<div class="no-print"><h3>⏱️ Início da Operação</h3>', unsafe_allow_html=True)
c_h1, c_h2, _ = st.columns([1, 1, 2])
with c_h1: data_op = st.date_input("Data", datetime.date.today())
with c_h2: hora_op = st.time_input("Hora", datetime.time(6, 0))
st.markdown('</div>', unsafe_allow_html=True)

# ADICIONAR ETAPA (Tela)
st.markdown('<div class="no-print"><hr><h3>➕ Adicionar Etapa</h3>', unsafe_allow_html=True)
c_a1, c_h2, c_h3, c_h4 = st.columns([2, 3, 1.5, 1])
with c_a1: loc_in = st.text_input("Locação", key="ni_loc")
with c_h2: etp_in = st.text_input("Etapa", key="ni_etp")
with c_h3: res_in = st.text_input("Resp.", value="MPSV", key="ni_res")
with c_h4: tmp_in = st.text_input("Tempo", value="01:00", key="ni_tmp")
if st.button("Adicionar à Lista"):
    h, m = map(int, tmp_in.split(':'))
    st.session_state.db["programacao"].append({"id":str(uuid.uuid4()), "Locação":loc_in, "Etapa":etp_in, "Responsável":res_in, "Horas":h, "Minutos":m})
    salvar_dados(st.session_state.db); st.rerun()
st.markdown('</div><hr>', unsafe_allow_html=True)

# PROGRAMAÇÃO ATUAL
st.subheader("📋 Programação Atual")
if st.session_state.db["programacao"]:
    hc = st.columns([0.4, 2, 3, 1.5, 1, 0.4, 0.4, 0.4])
    for i, t in enumerate(["#", "Locação", "Etapa", "Responsável", "Tempo", "Ações"]): hc[i].write(f"**{t}**")

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item.get("id", str(uuid.uuid4()))
        c = st.columns([0.4, 2, 3, 1.5, 1, 0.5, 0.5, 0.5])
        c[0].write(f"{idx+1}")
        
        # Exibe como input na tela, e como texto simples no print (via CSS)
        c[1].text_input("Loc", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed")
        c[1].markdown(f'<div class="print-text">{item["Locação"]}</div>', unsafe_allow_html=True)
        
        c[2].text_input("Etp", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed")
        c[2].markdown(f'<div class="print-text">{item["Etapa"]}</div>', unsafe_allow_html=True)
        
        c[3].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed")
        c[3].markdown(f'<div class="print-text">{item["Responsável"]}</div>', unsafe_allow_html=True)
        
        t_val = f"{int(item.get('Horas',0)):02d}:{int(item.get('Minutos',0)):02d}"
        c[4].text_input("Tmp", value=t_val, key=f"t_{uid}", label_visibility="collapsed")
        c[4].markdown(f'<div class="print-text">{t_val}</div>', unsafe_allow_html=True)
        
        if c[5].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db); st.rerun()
        if c[6].button("⬇️", key=f"dw_{uid}") and idx < len(st.session_state.db["programacao"])-1:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx+1] = st.session_state.db["programacao"][idx+1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db); st.rerun()
        if c[7].button("❌", key=f"del_{uid}"):
            st.session_state.db["programacao"].pop(idx)
            salvar_dados(st.session_state.db); st.rerun()

# RESUMO
st.divider()
st.subheader("🎯 Resumo Operacional")
tot_m = sum(int(i.get("Horas",0))*60 + int(i.get("Minutos",0)) for i in st.session_state.db["programacao"])
fim_dt = datetime.datetime.combine(data_op, hora_op) + datetime.timedelta(minutes=tot_m)

c1, c2 = st.columns(2)
c1.metric("Duração Total", f"{tot_m//60:02d}h {tot_m%60:02d}m")
c2.metric("Previsão de Prontidão", fim_dt.strftime("%d/%m/%Y às %H:%M"))

st.markdown('<div class="no-print"><hr>', unsafe_allow_html=True)
if st.button("🖨️ Imprimir PDF"): components.html("<script>window.print()</script>")
st.markdown('</div>', unsafe_allow_html=True)
