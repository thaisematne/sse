import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Plano de Clash 2D com Deriva", layout="wide")
st.title("Módulo 3: Plano de Clash 2D (Com Deriva e LDA)")

# --- 1. Configurações Dimensionais ---
with st.expander("⚙️ Controle Dimensional (Navio)"):
    col_d1, col_d2 = st.columns(2)
    x_eq = {"XLX-23": [col_d1.number_input("X - ROV XLX-23", value=5.0), col_d1.number_input("Y - ROV XLX-23", value=15.0)],
            "XLX-24": [col_d2.number_input("X - ROV XLX-24", value=-5.0), col_d2.number_input("Y - ROV XLX-24", value=15.0)],
            "Umbilical": [col_d1.number_input("X - Umbilical", value=0.0), col_d1.number_input("Y - Umbilical", value=0.0)],
            "Guindaste": [col_d2.number_input("X - Guindaste", value=-10.0), col_d2.number_input("Y - Guindaste", value=-20.0)]}

# --- 2. Parâmetros de Operação ---
col_op1, col_op2 = st.columns(2)
aproamento = col_op1.slider("Aproamento do Navio (°)", 0, 359, 0)
lda = col_op2.number_input("Lâmina D'água (m)", value=2000.0)

st.subheader("Configuração da Deriva por Equipamento")
derivas = {}
cols = st.columns(4)
for i, (nome, pos) in enumerate(x_eq.items()):
    with cols[i]:
        st.markdown(f"**{nome}**")
        d = st.number_input(f"Dist. Deriva (m) {nome}", value=0.0, key=f"dist_{nome}")
        dir_ = st.number_input(f"Dir. (°) {nome}", value=0.0, key=f"dir_{nome}")
        derivas[nome] = (d, np.radians(dir_))

if st.button("Atualizar Plano de Clash", type="primary"):
    fig = go.Figure()
    H = np.radians(aproamento)
    
    # Desenhar Navio Rotacionado
    navio = [[-10, -50], [10, -50], [10, 50], [-10, 50], [-10, -50]]
    nx = [x*np.cos(H) + y*np.sin(H) for x, y in navio]
    ny = [-x*np.sin(H) + y*np.cos(H) for x, y in navio]
    fig.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="lightgray", name="Navio"))

    # Plotar cada equipamento
    for nome, (xi, yi) in x_eq.items():
        # Ponto superfície (rotacionado)
        xs = xi*np.cos(H) + yi*np.sin(H)
        ys = -xi*np.sin(H) + yi*np.cos(H)
        
        # Ponto fundo (superfície + deriva)
        d, ang = derivas[nome]
        xf = xs + d * np.sin(ang)
        yf = ys + d * np.cos(ang)
        
        # Desenhar linha do cabo (plano XY)
        fig.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines+markers', name=nome))
        
        # Desenhar Zona de Segurança de 10m no Dive Point (fundo)
        theta = np.linspace(0, 2*np.pi, 50)
        fig.add_trace(go.Scatter(
            x=xf + 10*np.cos(theta), y=yf + 10*np.sin(theta),
            mode='lines', line=dict(dash='dash'), name=f"Safety {nome}", fill='toself', opacity=0.3
        ))

    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=800, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
