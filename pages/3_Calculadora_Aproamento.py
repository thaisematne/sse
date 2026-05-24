import streamlit as st
import numpy as np
import plotly.graph_objects as go
from itertools import combinations

st.set_page_config(page_title="Análise de Clash", layout="wide")
st.title("Módulo 3: Calculadora de Aproamento e Análise de Clash")

st.info("Simulação geométrica 3D de umbilicais e cabos para prevenção de entrelaçamento offshore.")

# 1. Configurações Dimensionais do Navio
with st.expander("⚙️ Controle Dimensional do Navio (Parâmetros Fixos)"):
    st.write("Transcreva os dados do documento RP-PRM-DIMCON. O eixo Y representa Proa/Popa e X representa Estibordo/Bombordo a partir do Ponto Zero.")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        x_xlx23 = st.number_input("X - ROV XLX-23 (m)", value=5.0)
        y_xlx23 = st.number_input("Y - ROV XLX-23 (m)", value=15.0)
        x_umb = st.number_input("X - Umbilical Controle (m)", value=0.0)
        y_umb = st.number_input("Y - Umbilical Controle (m)", value=0.0)
        
    with col_d2:
        x_xlx24 = st.number_input("X - ROV XLX-24 (m)", value=-5.0)
        y_xlx24 = st.number_input("Y - ROV XLX-24 (m)", value=15.0)
        x_crane = st.number_input("X - Guindaste (m)", value=-10.0)
        y_crane = st.number_input("Y - Guindaste (m)", value=-20.0)

equipamentos_locais = {
    "ROV XLX-23": (x_xlx23, y_xlx23),
    "ROV XLX-24": (x_xlx24, y_xlx24),
    "Umbilical": (x_umb, y_umb),
    "Guindaste": (x_crane, y_crane)
}

st.divider()

# 2. Dados Operacionais da Simulação
st.subheader("Parâmetros da Simulação")
col_op1, col_op2 = st.columns(2)
with col_op1:
    aproamento = st.slider("Aproamento do Navio (Graus)", min_value=0, max_value=359, value=0)
with col_op2:
    lda = st.number_input("Lâmina D'água - LDA (m)", min_value=10.0, value=2000.0, step=50.0)

st.markdown("### Comportamento da Deriva (Dive Point para Fundo)")
st.write("Informe a direção (Norte Verdadeiro) e a distância que o equipamento será arrastado ou posicionado.")

derivas = {}
cols_deriva = st.columns(4)
for i, eq in enumerate(equipamentos_locais.keys()):
    with cols_deriva[i]:
        st.markdown(f"**{eq}**")
        dir_graus = st.number_input(f"Direção (°)", min_value=0, max_value=359, value=0, key=f"dir_{eq}")
        dist_m = st.number_input(f"Distância (m)", min_value=0.0, value=0.0, step=5.0, key=f"dist_{eq}")
        derivas[eq] = {"dir": dir_graus, "dist": dist_m}

st.divider()

# 3. Matemática de Translação e Plotagem
if st.button("Executar Análise de Clash", type="primary"):
    
    # Converte aproamento do navio para radianos
    H_rad = np.radians(aproamento)
    
    posicoes_superficie = {}
    posicoes_fundo = {}
    
    for eq, (x, y) in equipamentos_locais.items():
        # Matriz de rotação para superfície
        x_sup = x * np.cos(H_rad) + y * np.sin(H_rad)
        y_sup = -x * np.sin(H_rad) + y * np.cos(H_rad)
        posicoes_superficie[eq] = np.array([x_sup, y_sup, 0])
        
        # Projeção no fundo com a deriva
        d_rad = np.radians(derivas[eq]["dir"])
        d_dist = derivas[eq]["dist"]
        x_fundo = x_sup + d_dist * np.sin(d_rad)
        y_fundo = y_sup + d_dist * np.cos(d_rad)
        posicoes_fundo[eq] = np.array([x_fundo, y_fundo, -lda])

    # Função para calcular distância mínima em 3D
    def min_dist_3d(p1_sup, p1_fundo, p2_sup, p2_fundo, steps=100):
        z_vals = np.linspace(0, -lda, steps)
        min_d = float('inf')
        for z in z_vals:
            t = z / (-lda)
            pos1 = p1_sup + t * (p1_fundo - p1_sup)
            pos2 = p2_sup + t * (p2_fundo - p2_sup)
            dist = np.linalg.norm(pos1 - pos2)
            if dist < min_d:
                min_d = dist
        return min_d

    # Análise de cruzamentos
    st.subheader("Relatório de Distâncias de Segurança")
    raio_seguranca = 10.0
    houve_clash = False
    
    pares = list(combinations(equipamentos_locais.keys(), 2))
    for eq1, eq2 in pares:
        distancia = min_dist_3d(posicoes_superficie[eq1], posicoes_fundo[eq1], 
                                posicoes_superficie[eq2], posicoes_fundo[eq2])
        
        if distancia < raio_seguranca:
            houve_clash = True
            st.error(f"🔴 **ALERTA CRÍTICO:** {eq1} e {eq2} | Distância mínima: **{distancia:.1f}m** (Viola o raio de {raio_seguranca}m)")
        else:
            st.success(f"🟢 **SEGURO:** {eq1} e {eq2} | Distância mínima: **{distancia:.1f}m**")

    # Renderização do Gráfico 3D
    st.subheader("Visualização Espacial (Superfície até LDA)")
    fig = go.Figure()
    
    cores = {"ROV XLX-23": "orange", "ROV XLX-24": "red", "Umbilical": "blue", "Guindaste": "green"}
    
    for eq in equipamentos_locais.keys():
        sup = posicoes_superficie[eq]
        fundo = posicoes_fundo[eq]
        
        # Linha representando o cabo
        fig.add_trace(go.Scatter3d(
            x=[sup[0], fundo[0]],
            y=[sup[1], fundo[1]],
            z=[sup[2], fundo[2]],
            mode='lines+markers',
            name=eq,
            line=dict(color=cores[eq], width=5),
            marker=dict(size=4)
        ))
        
    fig.update_layout(
        scene=dict(
            xaxis_title='Leste/Oeste (m)',
            yaxis_title='Norte/Sul (m)',
            zaxis_title='Profundidade (m)'
        ),
        height=700,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
