import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Plano de Clash 2D & Docagem", layout="wide")
st.title("Módulo 3: Plano Tático de Segurança e Manobra")

# --- 1. Configurações de Offset ---
with st.expander("⚙️ Controle Dimensional - Posições no Convés (As-Built)"):
    col_d1, col_d2 = st.columns(2)
    x_xlx23 = col_d1.number_input("X - ROV XLX-23", value=0.0)
    y_xlx23 = col_d1.number_input("Y - ROV XLX-23", value=5.0)
    
    x_xlx24 = col_d2.number_input("X - ROV XLX-24", value=12.0)
    y_xlx24 = col_d2.number_input("Y - ROV XLX-24", value=5.0)
    
    x_umb = col_d1.number_input("X - Umbilical de Controle", value=-12.0)
    y_umb = col_d1.number_input("Y - Umbilical de Controle", value=5.0)
    
    x_crane = col_d2.number_input("X - Guindaste (Equipamento)", value=16.0)
    y_crane = col_d2.number_input("Y - Guindaste (Equipamento)", value=-20.0)

# --- 2. Painel Principal de Operação ---
st.markdown("### Parâmetros Dinâmicos da Operação")
st.info("Altere o aproamento do navio aqui e veja como os TMSs e Tethers se comportam no fundo.")

col_op1, col_op2, col_op3 = st.columns([2, 1, 1])
aproamento = col_op1.slider("Aproamento do Navio (°)", 0, 359, 0)
eq_heading = col_op2.number_input("Heading Assentamento (°)", min_value=0, max_value=359, value=45)
lda = col_op3.number_input("Lâmina D'água (m)", value=2000.0)

st.markdown("#### Deriva (Deslocamento Superfície -> Fundo)")
derivas = {}
cols = st.columns(4)
for i, nome in enumerate(["XLX-23", "XLX-24", "Umbilical", "Guindaste"]):
    with cols[i]:
        d = st.number_input(f"Dist. (m) {nome}", value=0.0, key=f"dist_{nome}")
        dir_ = st.number_input(f"Dir. (°) {nome}", value=0.0, key=f"dir_{nome}")
        derivas[nome] = (d, np.radians(dir_))

# --- Matemática Base (Posições dos TMSs no Fundo) ---
H = np.radians(aproamento)
equip_coords = {
    "XLX-23": (x_xlx23, y_xlx23),
    "XLX-24": (x_xlx24, y_xlx24),
    "Umbilical": (x_umb, y_umb),
    "Guindaste": (x_crane, y_crane)
}

pos_fundo = {} # Guarda as posições x,y reais na LDA (Onde estão os TMSs e o Equipamento)
for nome, (xi, yi) in equip_coords.items():
    xs = xi*np.cos(H) + yi*np.sin(H)
    ys = -xi*np.sin(H) + yi*np.cos(H)
    d, ang = derivas[nome]
    pos_fundo[nome] = (xs + d * np.sin(ang), ys + d * np.cos(ang))

st.divider()

# --- Separação das Visões ---
tab1, tab2 = st.tabs(["🗺️ Visão Global (Superfície e Descida)", "⚓ Visão Tática de Fundo (Docagem do ROV)"])

# ==========================================
# TAB 1: VISÃO GLOBAL (O que já tínhamos)
# ==========================================
with tab1:
    fig1 = go.Figure()
    
    # Navio
    navio = [[-10, -50], [10, -50], [10, 30], [0, 50], [-10, 30], [-10, -50]]
    nx = [x*np.cos(H) + y*np.sin(H) for x, y in navio]
    ny = [-x*np.sin(H) + y*np.cos(H) for x, y in navio]
    fig1.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="lightgray", line=dict(color="black"), name="Skandi Santos"))

    cores = {"XLX-23": "orange", "XLX-24": "red", "Umbilical": "blue", "Guindaste": "green"}
    theta = np.linspace(0, 2*np.pi, 50)
    
    for nome in equip_coords.keys():
        xi, yi = equip_coords[nome]
        xs = xi*np.cos(H) + yi*np.sin(H)
        ys = -xi*np.sin(H) + yi*np.cos(H)
        xf, yf = pos_fundo[nome]
        
        fig1.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines+markers', name=nome, line=dict(color=cores[nome])))
        fig1.add_trace(go.Scatter(
            x=xf + 5*np.cos(theta), y=yf + 5*np.sin(theta),
            mode='lines', line=dict(color=cores[nome], dash='dash'), name=f"Safety {nome}", fill='toself', opacity=0.3
        ))

    fig1.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=700, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)


# ==========================================
# TAB 2: VISÃO TÁTICA DE FUNDO (Docagem)
# ==========================================
with tab2:
    st.markdown("### Configuração da Manobra")
    col_m1, col_m2 = st.columns(2)
    rov_principal = col_m1.selectbox("ROV Principal (Doca na Face 1)", ["XLX-23", "XLX-24"])
    rov_obs = "XLX-24" if rov_principal == "XLX-23" else "XLX-23"
    face_obs = col_m2.selectbox(f"Posição do ROV de Observação ({rov_obs})", ["Face 2 (Boreste/90°)", "Face 4 (Bombordo/270°)"])
    
    if st.button("Simular Manobra Subsea", type="primary"):
        fig2 = go.Figure()
        
        # O centro da operação no fundo é onde o guindaste desceu o equipamento
        x_eq, y_eq = pos_fundo["Guindaste"]
        
        # 1. Desenhar o Equipamento no Fundo (Rotacionado para o Heading de Assentamento)
        dim_eq = 4.0 # Tamanho fictício do equipamento (4x4 metros)
        eq_rad = np.radians(eq_heading)
        # Quadrado centralizado na origem e depois rotacionado e transladado
        box = [[-dim_eq/2, -dim_eq/2], [dim_eq/2, -dim_eq/2], [dim_eq/2, dim_eq/2], [-dim_eq/2, dim_eq/2], [-dim_eq/2, -dim_eq/2]]
        bx = [x_eq + (x*np.cos(eq_rad) + y*np.sin(eq_rad)) for x, y in box]
        by = [y_eq + (-x*np.sin(eq_rad) + y*np.cos(eq_rad)) for x, y in box]
        
        fig2.add_trace(go.Scatter(x=bx, y=by, fill="toself", fillcolor="lightgreen", line=dict(color="green", width=2), name="Equipamento"))
        
        # Indicar a Face 1 (Frente) do Equipamento para clareza
        f1_x = x_eq + (dim_eq/2 + 1) * np.sin(eq_rad)
        f1_y = y_eq + (dim_eq/2 + 1) * np.cos(eq_rad)
        fig2.add_trace(go.Scatter(x=[f1_x], y=[f1_y], mode="text", text=["Face 1"], textfont=dict(color="darkgreen", size=14), showlegend=False))

        # 2. Posicionar os ROVs no Fundo
        # Distâncias em relação ao centro do equipamento
        dist_docagem = dim_eq/2 + 1.5 
        dist_obs = dim_eq/2 + 4.0     
        
        ang_f1 = eq_rad
        ang_f2 = eq_rad + np.pi/2
        ang_f4 = eq_rad - np.pi/2
        
        pos_rovs_fundo = {}
        # ROV Principal (Face 1)
        pos_rovs_fundo[rov_principal] = (x_eq + dist_docagem * np.sin(ang_f1), y_eq + dist_docagem * np.cos(ang_f1))
        
        # ROV Obs (Face 2 ou 4)
        ang_obs = ang_f2 if "Face 2" in face_obs else ang_f4
        pos_rovs_fundo[rov_obs] = (x_eq + dist_obs * np.sin(ang_obs), y_eq + dist_obs * np.cos(ang_obs))

        # 3. Desenhar TMSs, ROVs e Tethers
        for rov in ["XLX-23", "XLX-24"]:
            cor = cores[rov]
            tms_x, tms_y = pos_fundo[rov]
            rov_x, rov_y = pos_rovs_fundo[rov]
            
            # Ponto do TMS (Quadrado vazio)
            fig2.add_trace(go.Scatter(x=[tms_x], y=[tms_y], mode='markers+text', marker=dict(size=12, symbol="square-open", color=cor, line=dict(width=3)), name=f"TMS {rov}", text=[f"TMS {rov}"], textposition="top center"))
            
            # Ponto do ROV (Círculo cheio)
            fig2.add_trace(go.Scatter(x=[rov_x], y=[rov_y], mode='markers', marker=dict(size=14, color=cor), name=f"ROV {rov} (Docado)" if rov == rov_principal else f"ROV {rov} (Obs)"))
            
            # Linha do Tether (Pontilhada ligando TMS ao ROV)
            fig2.add_trace(go.Scatter(x=[tms_x, rov_x], y=[tms_y, rov_y], mode='lines', line=dict(color=cor, width=2, dash='dot'), name=f"Tether {rov}"))

        fig2.update_layout(
            yaxis=dict(scaleanchor="x", scaleratio=1), 
            height=700, 
            template="plotly_white", 
            title="Análise de Cruzamento de Tether (Tether Management System vs ROV)"
        )
        st.plotly_chart(fig2, use_container_width=True)
