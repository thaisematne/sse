import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Plano de Clash 2D Completo", layout="wide")
st.title("Módulo 3: Plano Tático de Segurança (Com Deriva e LDA)")

# --- 1. Configurações de Offset (Navio) ---
with st.expander("⚙️ Controle Dimensional"):
    col_d1, col_d2 = st.columns(2)
    # ROVs
    x_xlx23 = col_d1.number_input("X - ROV XLX-23", value=5.0)
    y_xlx23 = col_d1.number_input("Y - ROV XLX-23", value=-10.0)
    x_xlx24 = col_d2.number_input("X - ROV XLX-24", value=-5.0)
    y_xlx24 = col_d2.number_input("Y - ROV XLX-24", value=-10.0)
    # Umbilical (Fixo)
    x_umb, y_umb = 5.0, 15.0
    st.info(f"Umbilical de Controle fixado em: X={x_umb}, Y={y_umb}")

# --- 2. Parâmetros de Operação ---
col_op1, col_op2 = st.columns(2)
aproamento = col_op1.slider("Aproamento do Navio (°)", 0, 359, 0)
lda = col_op2.number_input("Lâmina D'água (m)", value=2000.0)

st.subheader("Configuração da Deriva")
derivas = {}
cols = st.columns(3)
for i, nome in enumerate(["XLX-23", "XLX-24", "Umbilical"]):
    with cols[i]:
        st.markdown(f"**{nome}**")
        d = st.number_input(f"Dist. Deriva (m)", value=0.0, key=f"dist_{nome}")
        dir_ = st.number_input(f"Dir. (°) {nome}", value=0.0, key=f"dir_{nome}")
        derivas[nome] = (d, np.radians(dir_))

if st.button("Atualizar Plano de Clash", type="primary"):
    fig = go.Figure()
    H = np.radians(aproamento)
    
    # Desenhar Navio com Proa
    navio = [[-10, -50], [10, -50], [10, 30], [0, 50], [-10, 30], [-10, -50]]
    nx = [x*np.cos(H) + y*np.sin(H) for x, y in navio]
    ny = [-x*np.sin(H) + y*np.cos(H) for x, y in navio]
    fig.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="lightgray", name="Skandi Santos"))

    # Plotar equipamentos (Superfície + Fundo/Dive Point)
    cores = {"XLX-23": "orange", "XLX-24": "red", "Umbilical": "blue"}
    theta = np.linspace(0, 2*np.pi, 50)
    
    for nome, (xi, yi) in {"XLX-23": (x_xlx23, y_xlx23), "XLX-24": (x_xlx24, y_xlx24), "Umbilical": (x_umb, y_umb)}.items():
        # Superfície (rotacionado)
        xs = xi*np.cos(H) + yi*np.sin(H)
        ys = -xi*np.sin(H) + yi*np.cos(H)
        
        # Fundo (superfície + deriva)
        d, ang = derivas[nome]
        xf = xs + d * np.sin(ang)
        yf = ys + d * np.cos(ang)
        
        # Cabo
        fig.add_trace(go.Scatter(x=[xs, xf], y=[ys, yf], mode='lines+markers', name=nome, line=dict(color=cores[nome])))
        
        # Safety Zone (Dive Point no fundo)
        fig.add_trace(go.Scatter(
            x=xf + 5*np.cos(theta), y=yf + 5*np.sin(theta),
            mode='lines', line=dict(color=cores[nome], dash='dash'), name=f"Safety {nome}", fill='toself', opacity=0.3
        ))

    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=800, template="plotly_white", title="Plano 2D: Relação entre Superfície e Dive Point")
    st.plotly_chart(fig, use_container_width=True)
