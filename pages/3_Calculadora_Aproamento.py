import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Plano de Clash 2D Profissional", layout="wide")
st.title("Módulo 3: Plano Tático de Segurança (Skandi Santos)")

# --- 1. Configurações de Offset (Navio) ---
with st.expander("⚙️ Controle de Posicionamento no Convés"):
    col_d1, col_d2 = st.columns(2)
    # Posições dos ROVs (Editáveis)
    x_xlx23 = col_d1.number_input("X - ROV XLX-23", value=5.0)
    y_xlx23 = col_d1.number_input("Y - ROV XLX-23", value=-10.0)
    x_xlx24 = col_d2.number_input("X - ROV XLX-24", value=-5.0)
    y_xlx24 = col_d2.number_input("Y - ROV XLX-24", value=-10.0)
    # Posição do Umbilical (Fixa conforme solicitado)
    x_umb, y_umb = 5.0, 15.0
    st.info(f"Umbilical de Controle fixado em: X={x_umb}, Y={y_umb}")

# --- 2. Parâmetros de Deriva ---
aproamento = st.slider("Aproamento do Navio (°)", 0, 359, 0)
st.divider()

equipamentos = {
    "ROV XLX-23": {"pos": (x_xlx23, y_xlx23), "cor": "orange"},
    "ROV XLX-24": {"pos": (x_xlx24, y_xlx24), "cor": "red"},
    "Umbilical":  {"pos": (x_umb, y_umb), "cor": "blue"}
}

if st.button("Atualizar Plano de Clash", type="primary"):
    fig = go.Figure()
    H = np.radians(aproamento)
    
    # Desenhar Navio com Proa
    # [x, y] coordenadas do shape (proa em y=50)
    navio = [[-10, -50], [10, -50], [10, 30], [0, 50], [-10, 30], [-10, -50]]
    nx = [x*np.cos(H) + y*np.sin(H) for x, y in navio]
    ny = [-x*np.sin(H) + y*np.cos(H) for x, y in navio]
    fig.add_trace(go.Scatter(x=nx, y=ny, fill="toself", fillcolor="lightgray", line=dict(color="black"), name="Skandi Santos"))

    # Plotar equipamentos e zonas de 5m
    theta = np.linspace(0, 2*np.pi, 50)
    for nome, dados in equipamentos.items():
        xi, yi = dados["pos"]
        xs = xi*np.cos(H) + yi*np.sin(H)
        ys = -xi*np.sin(H) + yi*np.cos(H)
        
        # Ponto
        fig.add_trace(go.Scatter(x=[xs], y=[ys], mode='markers+text', name=nome, marker=dict(size=12, color=dados["cor"]), text=[nome], textposition="top center"))
        
        # Safety Zone 5m
        fig.add_trace(go.Scatter(
            x=xs + 5*np.cos(theta), y=ys + 5*np.sin(theta),
            mode='lines', line=dict(color=dados["cor"], dash='dash'), name=f"Safety {nome}", fill='toself', opacity=0.2
        ))

    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=800, template="plotly_white", title="Plano 2D: Zona de Segurança 5m")
    st.plotly_chart(fig, use_container_width=True)
