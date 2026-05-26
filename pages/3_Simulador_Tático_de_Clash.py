import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os
import base64

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA E LOGO NO MENU
# ==========================================
st.set_page_config(
    page_title="Simulador Tático de Clash | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    
    css_sidebar = """
    <style>
    [data-testid="stSidebarNav"]::before {
        content: "";
        display: block;
        background-image: url("data:image/png;base64,LOGO_BASE64_AQUI");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        height: 70px;
        margin: 20px 15px 10px 15px;
    }
    </style>
    """
    st.markdown(css_sidebar.replace("LOGO_BASE64_AQUI", sidebar_logo_b64), unsafe_allow_html=True)

# ==========================================
# 1. CABEÇALHO
# ==========================================
AKOFS_RED = "#D32F2F"
st.markdown(f"<h1 style='color: {AKOFS_RED};'>Subsea Planner Pro</h1>", unsafe_allow_html=True)
st.markdown("### Simulador Tático de Clash")
st.divider()

# ==========================================
# 2. CONTROLE DIMENSIONAL
# ==========================================
with st.expander("⚙️ Controle Dimensional - Posições no Convés (As-Built)"):
    col_d1, col_d2 = st.columns(2)
    x_xlx23 = col_d1.number_input("X - ROV XLX-23", value=0.0)
    y_xlx23 = col_d1.number_input("Y - ROV XLX-23", value=5.0)
    
    x_xlx24 = col_d2.number_input("X - ROV XLX-24", value=12.0)
    y_xlx24 = col_d2.number_input("Y - ROV XLX-24", value=5.0)
    
    x_umb = col_d1.number_input("X - Umbilical de Controle", value=-12.0)
    y_umb = col_d1.number_input("Y - Umbilical de Controle", value=5.0)
    
    x_crane = col_d2.number_input("X - Guindaste (BAP/Equipamento)", value=16.0)
    y_crane = col_d2.number_input("Y - Guindaste (BAP/Equipamento)", value=-20.0)

# ==========================================
# 3. PAINEL DE OPERAÇÃO
# ==========================================
st.markdown("### Parâmetros Dinâmicos da Operação")
st.info("Simule a influência da proa e da correnteza no tether management e disposição de cabos na LDA.")

col_op1, col_op2, col_op3 = st.columns([2, 1, 1])
aproamento = col_op1.slider("Aproamento do Skandi Santos (°)", 0, 359, 0)
eq_heading = col_op2.number_input("Heading Assentamento BAP (°)", min_value=0, max_value=359, value=45)
lda = col_op3.number_input("Lâmina D'água (m)", value=2000.0)

st.markdown("#### Deriva (Deslocamento Superfície -> Fundo)")
derivas = {}
cols = st.columns(4)
for i, nome in enumerate(["XLX-23", "XLX-24", "Umbilical", "Guindaste"]):
    with cols[i]:
        d = st.number_input(f"Dist. (m) {nome}", value=0.0, key=f"dist_{nome}")
        dir_ = st.number_input(f"Dir. (°) {nome}", value=0.0, key=f"dir_{nome}")
        derivas[nome] = (d, np.radians(dir_))

# --- Matemática Base (Posições no Fundo) ---
H = np.radians(aproamento)
equip_coords = {
    "XLX-23": (x_xlx23, y_xlx23),
    "XLX-24": (x_xlx24, y_xlx24),
    "Umbilical": (x_umb, y_umb),
    "Guindaste": (x_crane, y_crane)
}

pos_fundo = {}
pos_superficie = {}
for nome, (xi, yi) in equip_coords.items():
    xs = xi*np.cos(H) + yi*np.sin(H)
    ys = -xi*np.sin(H) + yi*np.cos(H)
    pos_superficie[nome] = (xs, ys)
    
    d, ang = derivas[nome]
    pos_fundo[nome] = (xs + d * np.sin(ang), ys + d * np.cos(ang))

# Shape do Navio Base
navio = [[-10, -50], [10, -50], [10, 30], [0, 50], [-10, 30], [-10, -50]]
nx = [x*np.cos(H) + y*np.sin(H) for x, y in navio]
ny = [-x*np.sin(H) + y*np.cos(H) for x, y in navio]

cores = {"XLX-23": "orange", "XLX-24": "red", "Umbilical": "blue", "Guindaste": "green"}
theta = np.linspace(0, 2*np.pi, 50)

st.divider()

# ==========================================
# 4. VISÕES E SIMULAÇÃO
# ==========================================
tab1, tab2 = st.tabs(["🗺️ Visão Global (Superfície e Descida)", "⚓ Visão Tática de Fundo (Docagem BAP)"])

# --- TAB 1: VISÃO GLOBAL ---
with tab1:
    fig1 = go.Figure()
    # Navio Forte
    fig1.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="lightgray", line=dict(color="black"), name="Skandi Santos"))

    for nome in equip_coords.keys():
        xs, ys = pos_superficie[nome]
        xf, yf = pos_fundo[nome]
        
        fig1.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines+markers', name=nome, line=dict(color=cores[nome])))
        fig1.add_trace(go.Scatter(
            x=xf + 5*np.cos(theta), y=yf + 5*np.sin(theta),
            mode='lines', line=dict(color=cores[nome], dash='dash'), name=f"Safety {nome}", fill='toself', opacity=0.3
        ))

    fig1.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=700, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

# --- TAB 2: VISÃO TÁTICA DE FUNDO ---
with tab2:
    st.markdown("### Configuração da Manobra")
    col_m1, col_m2 = st.columns(2)
    rov_principal = col_m1.selectbox("ROV Principal (Doca na Face 1)", ["XLX-23", "XLX-24"])
    rov_obs = "XLX-24" if rov_principal == "XLX-23" else "XLX-23"
    face_obs = col_m2.selectbox(f"Posição do ROV Obs ({rov_obs})", ["Face 2 (Boreste/90°)", "Face 4 (Bombordo/270°)"])
    
    if st.button("Simular Manobra Subsea", type="primary"):
        fig2 = go.Figure()
        
        # 1. Desenhar a Sombra do Navio
        fig2.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="rgba(200, 200, 200, 0.2)", line=dict(color="lightgray", dash="dash"), name="Sombra do Navio", hoverinfo="skip"))
        
        # 2. Plotar Dive Points e Umbilical de Controle
        for nome in ["XLX-23", "XLX-24", "Umbilical"]:
            xs, ys = pos_superficie[nome]
            xf, yf = pos_fundo[nome]
            cor = cores[nome]
            
            # Marcação do Dive Point (Superfície)
            fig2.add_trace(go.Scatter(x=[xs], y=[ys], mode='markers+text', marker=dict(size=10, symbol="x", color=cor, line=dict(width=2)), name=f"DP {nome}", text=[f"DP {nome}"], textposition="top right"))
            
            # Linha de descida do cabo na água
            fig2.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines', line=dict(color=cor, width=1, dash='solid'), name=f"Cabo {nome}", opacity=0.4))
            
            # Umbilical no fundo
            if nome == "Umbilical":
                fig2.add_trace(go.Scatter(x=[xf], y=[yf], mode='markers+text', marker=dict(size=12, symbol="circle", color=cor), name="Umbilical (Fundo)", text=["Umbilical na Água"], textposition="bottom center"))
                fig2.add_trace(go.Scatter(x=xf +
