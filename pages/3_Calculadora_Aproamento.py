import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Plano de Clash 2D", layout="wide")
st.title("Módulo 3: Plano de Clash 2D (Skandi Santos)")

# --- Configurações (Mantendo a estrutura anterior) ---
with st.expander("⚙️ Controle Dimensional"):
    col_d1, col_d2 = st.columns(2)
    x_xlx23 = col_d1.number_input("X - ROV XLX-23", value=5.0)
    y_xlx23 = col_d1.number_input("Y - ROV XLX-23", value=15.0)
    x_xlx24 = col_d2.number_input("X - ROV XLX-24", value=-5.0)
    y_xlx24 = col_d2.number_input("Y - ROV XLX-24", value=15.0)
    x_umb = col_d1.number_input("X - Umbilical", value=0.0)
    y_umb = col_d1.number_input("Y - Umbilical", value=0.0)
    x_crane = col_d2.number_input("X - Guindaste", value=-10.0)
    y_crane = col_d2.number_input("Y - Guindaste", value=-20.0)

equipamentos = {
    "ROV XLX-23": (x_xlx23, y_xlx23, "orange"),
    "ROV XLX-24": (x_xlx24, y_xlx24, "red"),
    "Umbilical": (x_umb, y_umb, "blue"),
    "Guindaste": (x_crane, y_crane, "green")
}

aproamento = st.slider("Aproamento do Navio (°)", 0, 359, 0)
st.divider()

if st.button("Gerar Plano 2D de Segurança", type="primary"):
    fig = go.Figure()
    H_rad = np.radians(aproamento)
    
    # 1. Desenhar silhueta do Navio (Simples retângulo)
    # Ajuste estes valores conforme as dimensões reais do Skandi Santos
    comp = 100 
    larg = 20
    navio_x = [-larg/2, larg/2, larg/2, -larg/2, -larg/2]
    navio_y = [-comp/2, -comp/2, comp/2, comp/2, -comp/2]
    
    # Rotacionar silhueta
    n_x_rot = [x*np.cos(H_rad) + y*np.sin(H_rad) for x, y in zip(navio_x, navio_y)]
    n_y_rot = [-x*np.sin(H_rad) + y*np.cos(H_rad) for x, y in zip(navio_x, navio_y)]
    
    fig.add_trace(go.Scatter(x=n_x_rot, y=n_y_rot, fill="toself", fillcolor="lightgray", line=dict(color="black"), name="Navio"))

    # 2. Plotar Equipamentos e Safety Zones
    for nome, (x, y, cor) in equipamentos.items():
        x_rot = x * np.cos(H_rad) + y * np.sin(H_rad)
        y_rot = -x * np.sin(H_rad) + y * np.cos(H_rad)
        
        # Ponto do equipamento
        fig.add_trace(go.Scatter(x=[x_rot], y=[y_rot], mode='markers+text', name=nome, marker=dict(size=12, color=cor), text=[nome], textposition="top center"))
        
        # Círculo de 10m (Safety Zone)
        theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter(
            x=x_rot + 10 * np.cos(theta),
            y=y_rot + 10 * np.sin(theta),
            mode='lines', line=dict(color=cor, dash='dash'), name=f"Safety {nome}", fill='toself', fillcolor=f"rgba({cor}, 0.1)"
        ))

    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), height=800, template="plotly_white", title="Plano 2D: Risco de Clash (Raio 10m)")
    st.plotly_chart(fig, use_container_width=True)
