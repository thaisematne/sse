import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os
import base64

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA E LOGO NO MENU
# ==========================================
st.set_page_config(
    page_title="Simulador Subsea | Subsea Planner Pro", 
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
st.markdown("### Simulador Subsea")
st.divider()

# ==========================================
# 2. CONTROLE DIMENSIONAL
# ==========================================
with st.expander("⚙️ Controle Dimensional - Posições no Convés (As-Built)"):
    nome_equip = st.text_input("Nome do Equipamento/Estrutura", value="BAP")
    
    col_d1, col_d2 = st.columns(2)
    x_xlx23 = col_d1.number_input("X - ROV XLX-23", value=0.0)
    y_xlx23 = col_d1.number_input("Y - ROV XLX-23", value=5.0)
    
    x_xlx24 = col_d2.number_input("X - ROV XLX-24", value=12.0)
    y_xlx24 = col_d2.number_input("Y - ROV XLX-24", value=5.0)
    
    x_umb = col_d1.number_input("X - Umbilical de Controle", value=-12.0)
    y_umb = col_d1.number_input("Y - Umbilical de Controle", value=5.0)
    
    x_crane = col_d2.number_input(f"X - Guindaste ({nome_equip})", value=16.0)
    y_crane = col_d2.number_input(f"Y - Guindaste ({nome_equip})", value=-20.0)

# ==========================================
# 3. PAINEL DE OPERAÇÃO
# ==========================================
st.markdown("### Parâmetros Dinâmicos da Operação")
st.info("Simule a influência da proa e da correnteza no tether management e disposição de cabos na LDA.")

col_op1, col_op2, col_op3 = st.columns([2, 1, 1])
aproamento = col_op1.slider("Aproamento do Skandi Santos (°)", 0, 359, 0)
eq_heading = col_op2.number_input("Heading de Assentamento do ROV (°)", min_value=0, max_value=359, value=120, help="Direção para onde o ROV estará olhando quando estiver docado no painel.")
lda = col_op3.number_input("Lâmina D'água (m)", value=2000.0)

st.markdown("#### Deriva (Deslocamento Superfície -> Fundo)")
derivas = {}
cols = st.columns(4)
for i, nome in enumerate(["XLX-23", "XLX-24", "Umbilical", "Guindaste"]):
    with cols[i]:
        label_exibicao = nome_equip if nome == "Guindaste" else nome
        d = st.number_input(f"Dist. (m) {label_exibicao}", value=0.0, key=f"dist_{nome}")
        dir_ = st.number_input(f"Dir. (°) {label_exibicao}", value=0.0, key=f"dir_{nome}")
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
tab1, tab2 = st.tabs(["🗺️ Visão Global (Superfície e Descida)", "⚓ Visão Tática de Fundo (Manobra Subsea)"])

# --- TAB 1: VISÃO GLOBAL ---
with tab1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="lightgray", line=dict(color="black"), name="Skandi Santos"))

    for nome in equip_coords.keys():
        xs, ys = pos_superficie[nome]
        xf, yf = pos_fundo[nome]
        label_exibicao = nome_equip if nome == "Guindaste" else nome
        
        fig1.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines+markers', name=label_exibicao, line=dict(color=cores[nome])))
        fig1.add_trace(go.Scatter(
            x=xf + 5*np.cos(theta), y=yf + 5*np.sin(theta),
            mode='lines', line=dict(color=cores[nome], dash='dash'), name=f"Safety {label_exibicao}", fill='toself', opacity=0.3
        ))

    fig1.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=700, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

# --- TAB 2: VISÃO TÁTICA DE FUNDO ---
with tab2:
    st.markdown("### Configuração da Manobra")
    col_m1, col_m2, col_m3 = st.columns(3)
    
    rov_principal = col_m1.selectbox("ROV Principal", ["XLX-23", "XLX-24"])
    rov_obs = "XLX-24" if rov_principal == "XLX-23" else "XLX-23"
    
    face_principal_str = col_m2.selectbox("Painel de Docagem do ROV Principal", [
        "Face 1 (Painel Principal)", "Face 2 (Boreste / 90°)", "Face 3 (Popa / 180°)", "Face 4 (Bombordo / 270°)"
    ])
    
    face_obs_str = col_m3.selectbox(f"Posição do ROV Observador ({rov_obs})", [
        "Face 1 (Painel Principal)", "Face 2 (Boreste / 90°)", "Face 3 (Popa / 180°)", "Face 4 (Bombordo / 270°)"
    ], index=3)
    
    if st.button("Simular Manobra Subsea", type="primary"):
        fig2 = go.Figure()
        
        # Sombra do Navio
        fig2.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="rgba(200, 200, 200, 0.2)", line=dict(color="lightgray", dash="dash"), name="Sombra do Navio", hoverinfo="skip"))
        
        # Plotar Dive Points e Umbilical
        for nome in ["XLX-23", "XLX-24", "Umbilical"]:
            xs, ys = pos_superficie[nome]
            xf, yf = pos_fundo[nome]
            cor = cores[nome]
            
            fig2.add_trace(go.Scatter(x=[xs], y=[ys], mode='markers+text', marker=dict(size=10, symbol="x", color=cor, line=dict(width=2)), name=f"DP {nome}", text=[f"DP {nome}"], textposition="top right"))
            fig2.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines', line=dict(color=cor, width=1, dash='solid'), name=f"Cabo {nome}", opacity=0.4))
            
            if nome == "Umbilical":
                fig2.add_trace(go.Scatter(x=[xf], y=[yf], mode='markers+text', marker=dict(size=12, symbol="circle", color=cor), name="Umbilical (Fundo)", text=["Umbilical na Água"], textposition="bottom center"))
                fig2.add_trace(go.Scatter(x=xf + 5*np.cos(theta), y=yf + 5*np.sin(theta), mode='lines', line=dict(color=cor, dash='dash'), name=f"Safety Umbilical", fill='toself', opacity=0.1))

        # --- Resolução Angular das Faces ---
        if "Face 1" in face_principal_str: f_p_deg, f_p_rad = 0, 0.0
        elif "Face 2" in face_principal_str: f_p_deg, f_p_rad = 90, np.pi/2
        elif "Face 3" in face_principal_str: f_p_deg, f_p_rad = 180, np.pi
        else: f_p_deg, f_p_rad = 270, -np.pi/2

        if "Face 1" in face_obs_str: f_o_rad = 0.0
        elif "Face 2" in face_obs_str: f_o_rad = np.pi/2
        elif "Face 3" in face_obs_str: f_o_rad = np.pi
        else: f_o_rad = -np.pi/2

        # Rotação da Estrutura calculada com base na direção do ROV e painel escolhido
        eq_heading_calc = (eq_heading + 180 - f_p_deg) % 360
        eq_rad = np.radians(eq_heading_calc)

        # Desenhar o Equipamento Geométrico Personalizado
        x_eq, y_eq = pos_fundo["Guindaste"]
        dim_eq = 4.0
        
        box = [[-dim_eq/2, -dim_eq/2], [dim_eq/2, -dim_eq/2], [dim_eq/2, dim_eq/2], [-dim_eq/2, dim_eq/2], [-dim_eq/2, -dim_eq/2]]
        bx = [x_eq + (x*np.cos(eq_rad) + y*np.sin(eq_rad)) for x, y in box]
        by = [y_eq + (-x*np.sin(eq_rad) + y*np.cos(eq_rad)) for x, y in box]
        fig2.add_trace(go.Scatter(x=bx, y=by, fill="toself", fillcolor="lightgreen", line=dict(color="darkgreen", width=3), name=nome_equip))
        
        # Textos das Faces no Sentido Horário
        faces_config = [("F1", 0), ("F2", np.pi/2), ("F3", np.pi), ("F4", -np.pi/2)]
        for nome_face, ang_offset in faces_config:
            f_ang = eq_rad + ang_offset
            fx = x_eq + (dim_eq/2 + 1.2) * np.sin(f_ang)
            fy = y_eq + (dim_eq/2 + 1.2) * np.cos(f_ang)
            fig2.add_trace(go.Scatter(x=[fx], y=[fy], mode="text", text=[nome_face], textfont=dict(color="darkgreen", size=12, weight="bold"), showlegend=False))

        # Distâncias de Posicionamento
        dist_docagem = dim_eq/2 + 2.0 
        dist_obs = dim_eq/2 + 5.0     
        
        pos_rovs_fundo = {}
        heading_rov = {}
        
        # ROV Principal: Docado na Face Escolhida olhando para o Heading de Assentamento
        pos_rovs_fundo[rov_principal] = (x_eq + dist_docagem * np.sin(eq_rad + f_p_rad), y_eq + dist_docagem * np.cos(eq_rad + f_p_rad))
        heading_rov[rov_principal] = np.radians(eq_heading)
        
        # ROV Observador: Posicionado na sua respectiva face olhando para a estrutura
        pos_rovs_fundo[rov_obs] = (x_eq + dist_obs * np.sin(eq_rad + f_o_rad), y_eq + dist_obs * np.cos(eq_rad + f_o_rad))
        heading_rov[rov_obs] = eq_rad + f_o_rad + np.pi

        # Desenhar TMS, Tethers e ROVs
        rov_shape = [[-1.5, -1], [1.5, -1], [1.5, 0.5], [0, 1.5], [-1.5, 0.5], [-1.5, -1]]

        for rov in ["XLX-23", "XLX-24"]:
            cor = cores[rov]
            tms_x, tms_y = pos_fundo[rov]
            rov_x, rov_y = pos_rovs_fundo[rov]
            h_rov = heading_rov[rov]
            
            # TMS
            fig2.add_trace(go.Scatter(x=[tms_x], y=[tms_y], mode='markers+text', marker=dict(size=14, symbol="square-open", color=cor, line=dict(width=3)), name=f"TMS {rov}", text=[f"TMS {rov}"], textposition="top center"))
            
            # ROV Rotacionado
            rx_rot = [rov_x + (x*np.cos(h_rov) + y*np.sin(h_rov)) for x, y in rov_shape]
            ry_rot = [rov_y + (-x*np.sin(h_rov) + y*np.cos(h_rov)) for x, y in rov_shape]
            fig2.add_trace(go.Scatter(x=rx_rot, y=ry_rot, fill="toself", fillcolor=cor, line=dict(color="black"), name=f"ROV {rov}", hoverinfo="name"))
            
            # Tether (Linha de Fundo)
            fig2.add_trace(go.Scatter(x=[tms_x, rov_x], y=[tms_y, rov_y], mode='lines', line=dict(color=cor, width=2, dash='dot'), name=f"Tether {rov}"))

        fig2.update_layout(
            yaxis=dict(scaleanchor="x", scaleratio=1), 
            height=850, 
            template="plotly_white", 
            title=f"Análise de Tether Management (Visão Tática de Manobra no Fundo)"
        )
        st.plotly_chart(fig2, use_container_width=True)
