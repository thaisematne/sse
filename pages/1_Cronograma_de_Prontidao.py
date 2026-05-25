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
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(3) { width: 45% !important; flex: none !important; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) { width: 15% !important; flex: none !important; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(5) { width: 10% !important; flex: none !important; }
    
    /* Transforma as caixas de input da tela em texto limpo no papel */
    input, select, textarea, div[data-baseweb="base-input"] > input {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px dashed #ccc !important;
        box-shadow: none !important;
        color: #000000 !important;
        padding: 0px !important;
        font-size: 10pt !important;
    }
    
    /* CABEÇALHO CENTRALIZADO DE RELATÓRIO */
    .print-header {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        border-bottom: 2px solid #000000 !important;
        margin-bottom: 20px !important;
        padding-bottom: 10px !important;
    }
    .print-logo-img { height: 45px !important; margin-bottom: 10px !important; }
    
    /* COMPACTAÇÃO DE FONTES PARA GARANTIR PÁGINA ÚNICA */
    p, div, span, label, .stMarkdown { font-size: 10pt !important; }
    h1 { font-size: 16pt !important; margin: 0 !important; }
    h3 { font-size: 12pt !important; margin: 5px 0 !important; }
    
    /* DESTAQUE DE MOLDURA PARA O RESUMO OPERACIONAL */
    div[data-testid="stMetric"] {
        border: 2px solid #000000 !important;
        background-color: #F5F5F5 !important;
        padding: 10px !important;
        border-radius: 5px !important;
        text-align: center !important;
    }
    div[data-testid="stMetricValue"] div { 
        font-size: 20pt !important; 
        font-weight: bold !important; 
        color: COLOR_AKOFS !important; 
    }
}
</style>
"""
# Troca a cor via replace para evitar conflito de chaves no Python
st.markdown(css_style.replace("COLOR_AKOFS", AKOFS_RED), unsafe_allow_html=True)

# --- SIDEBAR (VISÍVEL APENAS NA TELA) ---
if os.path.exists(LOGO_PATH):
    st.sidebar.image(Image.open(LOGO_PATH), use_container_width=True)
else:
    st.sidebar.markdown("## 🔴 AKOFS Offshore")
st.sidebar.markdown("---")

# ==========================================
# 3. LÓGICA DE DADOS (COM PROTEÇÃO ANTI-ERRO)
# ==========================================
ETAPAS_DEFAULT = [
    "Navegar para a locação", "Check list de DP", "Descer ROV", "Inspeção inicial", 
    "Descer equipamento", "Instalar equipamento", "Manuseio de EFL", "Manuseio de HFL", 
    "Manuseio de válvula", "Etapas da UEP", "Realizar testes / intervenção", "Limpeza", 
    "Desmobilizar equipamento", "Recolher equipamento", "Inspeção final", "Subir ROV", 
    "Aguardar prontidão", "Outros"
]

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 4. CABEÇALHO DO DOCUMENTO
# ==========================================
img_html = f'<img src="data:image/png;base64,{logo_base64}" class="print-logo-img">' if logo_base64 else ""
header_html = f"""
<div class="print-header">
    {img_html}
    <h1 style="color: {AKOFS_RED}; margin-bottom: 0;">Subsea Planner Pro</h1>
    <h3 style="margin-top: 5px; color: #888;">Cronograma de Prontidão</h3>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==========================================
# PASSO 1: DATA E HORA DE INÍCIO
# ==========================================
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.subheader("⏱️ Início da Operação")
col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))
st.divider()
st.markdown('</div>', unsafe_allow_html=True)

# Este bloco só aparece no papel impresso, organizando a Data/Hora como um cabeçalho técnico
metadata_html = f"""
<div style="display: none;" class="print-only-block">
    <strong>INÍCIO DA OPERAÇÃO:</strong> {data_inicio.strftime('%d/%m/%Y')} às {hora_inicio.strftime('%H:%M')}
</div>
<style>@media print {{ .print-only-block {{ display: block !important; margin-bottom: 15px !important; text-align: center; font-size: 11pt !important; }} }}</style>
"""
st.markdown(metadata_html, unsafe_allow_html=True)

# ==========================================
# PASSO 2: ADICIONAR NOVA ETAPA (OCULTO NO PRINT)
# ==========================================
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.subheader("➕ Adicionar Nova Etapa")
col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])

with col1:
    locacao = st.text_input("Locação", placeholder="Ex: 9-BUZ-39", key="new_loc")
with col2:
    etp_sel = st.selectbox("Etapa", st.session_state.db["base_etapas"], key="new_etp_sel")
    if etp_sel == "Outros":
        etp_final = st.text_input("Descreva a etapa:", key="new_etp_man")
    else:
        etp_final = etp_sel
with col3:
    resp = st.text_input("Responsável", value="MPSV", key="new_resp")
with col4:
    tempo = st.text_input("Tempo (HH:MM)", value="01:00", key="new_tempo")

if st.button("Adicionar à Programação", type="primary"):
    try:
        h, m = 0, 0
        if ":" in tempo:
            partes = tempo.split(":")
            h = int(partes[0])
            m = int(partes[1])
        else:
            h = int(tempo)
        
        nova = {
            "id": str(uuid.uuid4()),
            "Locação": locacao,
            "Etapa": etp_final,
            "Responsável": resp,
            "Horas": h,
            "Minutos": m
        }
        st.session_state.db["programacao"].append(nova)
        salvar_dados(st.session_state.db)
        st.rerun()
    except Exception:
        st.error("Tempo inválido. Use HH:MM")
st.divider()
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PASSO 3: PROGRAMAÇÃO ATUAL (EDITÁVEL NA TELA / LIMPA NO PRINT)
# ==========================================
st.subheader("📋 Programação Atual")

if st.session_state.db["programacao"]:
    hc = st.columns([0.4, 2, 3, 1.5, 1, 0.4, 0.4, 0.4])
    for i, t in enumerate(["#", "Locação", "Etapa", "Responsável", "Tempo", "Ações", "", ""]):
        if t: hc[i].write(f"**{t}**")

    def update_val(idx, field, key):
        st.session_state.db["programacao"][idx][field] = st.session_state[key]
        salvar_dados(st.session_state.db)

    def update_time(idx, key):
        try:
            t_str = st.session_state[key]
            if ":" in t_str:
                partes = t_str.split(":")
                st.session_state.db["programacao"][idx]["Horas"] = int(partes[0])
                st.session_state.db["programacao"][idx]["Minutos"] = int(partes[1])
            else:
                st.session_state.db["programacao"][idx]["Horas"] = int(t_str)
                st.session_state.db["programacao"][idx]["Minutos"] = 0
            salvar_dados(st.session_state.db)
        except Exception: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        if "id" not in item: 
            item["id"] = str(uuid.uuid4())
        uid = item["id"]
        c = st.columns([0.4, 2, 3, 1.5, 1, 0.4, 0.4, 0.4])
        
        c[0].markdown(f"<div style='margin-top:8px;'>{idx+1}</div>", unsafe_allow_html=True)
        
        # Blindagem contra erros de dados antigos
        l_val = item.get("Locação", item.get("loc", ""))
        e_val = item.get("Etapa", item.get("etp", ""))
        r_val = item.get("Responsável", item.get("resp", ""))
        h_val = item.get("Horas", item.get("h", 0))
        m_val = item.get("Minutos", item.get("m", 0))

        c[1].text_input("Loc", value=l_val, key=f"l_{uid}", label_visibility="collapsed", on_change=update_val, args=(idx, "Locação", f"l_{uid}"))
        c[2].text_input("Etp", value=e_val, key=f"e_{uid}", label_visibility="collapsed", on_change=update_val, args=(idx, "Etapa", f"e_{uid}"))
        c[3].text_input("Resp", value=r_val, key=f"r_{uid}", label_visibility="collapsed", on_change=update_val, args=(idx, "Responsável", f"r_{uid}"))
        c[4].text_input("Tmp", value=f"{int(h_val):02d}:{int(m_val):02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=update_time, args=(idx, f"t_{uid}"))

        if c[5].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db)
            st.rerun()
            
        if c[6].button("⬇️", key=f"dw_{uid}") and idx < len(st.session_state.db["programacao"])-1:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx+1] = st.session_state.db["programacao"][idx+1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db)
            st.rerun()
            
        if c[7].button("❌", key=f"del_{uid}"):
            st.session_state.db["programacao"].pop(idx)
            salvar_dados(st.session_state.db)
            st.rerun()

# ==========================================
# PASSO 4: RESUMO OPERACIONAL E CONTROLES
# ==========================================
st.divider()
st.subheader("🎯 Resumo Operacional")

tot_h = sum(int(i.get("Horas", i.get("h", 0))) for i in st.session_state.db.get("programacao", []))
tot_m = sum(int(i.get("Minutos", i.get("m", 0))) for i in st.session_state.db.get("programacao", []))
tot_h += tot_m // 60
tot_m = tot_m % 60

dt_inicio = datetime.datetime.combine(data_inicio, hora_inicio)
dt_fim = dt_inicio + datetime.timedelta(hours=tot_h, minutes=tot_m)

colA, colB = st.columns(2)
colA.metric("Duração Total Estimada", f"{tot_h:02d}h {tot_m:02d}m")
colB.metric("Previsão de Prontidão", dt_fim.strftime("%d/%m/%Y às %H:%M"))

# Botões de ação isolados na classe .no-print
st.markdown('<div class="no-print">', unsafe_allow_html=True)
st.divider()
cb1, cb2, cb3 = st.columns([1, 1, 2])
with cb1:
    btn_html = f"""
        <button onclick="window.parent.print()" style="
            background-color: {AKOFS_RED}; color: white; padding: 0.6rem; 
            border: none; border-radius: 0.5rem; width: 100%; font-weight: bold; 
            cursor: pointer; font-family: sans-serif; font-size: 1rem;">
            🖨️ Imprimir PDF A4
        </button>
    """
    components.html(btn_html, height=45)

with cb2:
    if st.button("🗑️ Limpar Programação", use_container_width=True):
        st.session_state.db["programacao"] = []
        salvar_dados(st.session_state.db)
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
