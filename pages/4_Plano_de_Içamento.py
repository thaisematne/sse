import streamlit as st
import pandas as pd
import os
import base64
import datetime

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA E LOGO NO MENU
# ==========================================
st.set_page_config(
    page_title="Plano de Içamento | Subsea Planner Pro", 
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
# 1. CABEÇALHO PRINCIPAL
# ==========================================
AKOFS_RED = "#D32F2F"
st.markdown(f"<h1 style='color: {AKOFS_RED};'>Subsea Planner Pro</h1>", unsafe_allow_html=True)
st.markdown("### Plano de Içamento de Cargas Submarinas (Lift Plan)")
st.divider()

# ==========================================
# 2. DADOS GERAIS DA OPERAÇÃO
# ==========================================
st.markdown("#### 📋 1. Informações da Carga e Locação")
col1, col2, col3, col4 = st.columns(4)

data_op = col1.date_input("Data da Operação", datetime.date.today())
locacao = col2.text_input("Locação (Ex: 7-MRO-38-RJS)", value="")
equipamento = col3.text_input("Equipamento", value="ANM AS-300")
peso_ar = col4.number_input("Peso no Ar (ton)", min_value=0.0, value=37.6, step=0.1)

col5, col6, col7 = st.columns(3)
lda = col5.number_input("Lâmina D'água - LDA (m)", min_value=0, value=1500, step=50)
prof_inspecao = col6.number_input("Prof. de Inspeção ROV (m)", min_value=0, value=1450, step=50)
vel_descida = col7.text_input("Velocidade de Descida", value="20 a 30 m/min")

st.divider()

# ==========================================
# 3. SELEÇÃO DE GUINCHO E CÁLCULO DE CAPACIDADE
# ==========================================
st.markdown("#### 🏗️ 2. Especificação do Guindaste")

col_g1, col_g2 = st.columns(2)
guincho_sel = col_g1.radio("Guincho Selecionado", ["Principal (AHC-250T)", "Auxiliar (AHC-20T)"], horizontal=True)

# Lógica de interpolação simples baseada nas tabelas de Winch Calculation
def calcular_capacidade_lda(guincho, lda):
    if "Principal" in guincho:
        if lda <= 1: return 190.0
        elif lda <= 1000: return 220.0
        elif lda <= 1500: return 230.0
        elif lda <= 2000: return 221.0
        else: return 199.0
    else:
        if lda <= 500: return 20.0
        elif lda <= 1000: return 18.0
        elif lda <= 1500: return 15.0
        elif lda <= 2000: return 12.0
        else: return 9.0

cap_lda = calcular_capacidade_lda(guincho_sel, lda)
col_g2.metric(f"Capacidade do Guincho na LDA de {lda}m", f"{cap_lda} ton")

if peso_ar > cap_lda:
    st.error("⚠️ ALERTA CRÍTICO: O peso da carga excede a capacidade do guincho para esta profundidade.")
else:
    st.success("✅ Peso dentro dos limites de operação do guincho para a locação.")

st.divider()

# ==========================================
# 4. CONSTRUTOR DE LINGADA (ARRANJO GRÁFICO)
# ==========================================
st.markdown("#### 🔗 3. Arranjo de Içamento (Construtor de Lingada)")

# CSS para desenhar os blocos empilhados
st.markdown("""
<style>
.rigging-box {
    background-color: #1e2130;
    border: 2px solid #555;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    margin: 5px auto;
    width: 60%;
    font-weight: bold;
}
.rigging-arrow {
    text-align: center;
    font-size: 24px;
    color: #D32F2F;
    margin: -10px 0;
}
</style>
""", unsafe_allow_html=True)

if "Principal" in guincho_sel:
    st.info("Configuração Padrão de Guincho Principal: Conexão direta bloco -> cinta -> equipamento.")
    cinta_princ = st.text_input("Especificação da Cinta (Ex: 4 Cintas 40Ton x 7M)", value="4 Cintas 40Ton x 7M")
    manilha_princ = st.text_input("Especificação da Manilha Subsea", value="Manilha de ROV 55T")
    
    # Desenho Visual - Principal
    st.markdown('<div class="rigging-box" style="border-color: #D32F2F;">🟡 MOITÃO PRINCIPAL DO GUINDASTE 250T</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box">⛓️ {cinta_princ}</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box">🧲 {manilha_princ}</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box" style="background-color: #D32F2F; color: white;">📦 {equipamento.upper()}</div>', unsafe_allow_html=True)

else:
    st.info("Configuração de Guincho Auxiliar: Selecione o arranjo de extensões.")
    extensao_sel = st.selectbox("Arranjo de Extensão (Padrão AKST)", [
        "Extensão 4 metros (Padrão 10T)",
        "Extensão 6 metros (Padrão 10T)",
        "Extensão 4 metros (Heavy 22T)",
        "Extensão 6 metros (Heavy 22T)",
        "Cesta de Ferramentas / Master Link"
    ])
    
    # Determina os componentes baseado na seleção
    if "4 metros (Padrão 10T)" in extensao_sel:
        comp_cinta = "Cinta de 4 metros x 10T"
        comp_manilha = "Manilha de 12T"
        comp_nautillus = "Nautillus 10T"
        comp_costura = "Cinta 4m x 2T aduchada"
    elif "6 metros (Padrão 10T)" in extensao_sel:
        comp_cinta = "Cinta de 6 metros x 10T"
        comp_manilha = "Manilha de 12T"
        comp_nautillus = "Nautillus 10T"
        comp_costura = "Cinta 4m x 1T aduchada"
    elif "4 metros (Heavy 22T)" in extensao_sel:
        comp_cinta = "Cinta de 4 metros (8 dobrada) x 10T"
        comp_manilha = "Manilha de 17T"
        comp_nautillus = "Nautillus 22T"
        comp_costura = "Cinta 4m x 1T aduchada"
    elif "6 metros (Heavy 22T)" in extensao_sel:
        comp_cinta = "Cinta de 6 metros x 10T"
        comp_manilha = "Manilha de 17T"
        comp_nautillus = "Nautillus 22T"
        comp_costura = "Cinta 3m x 1T aduchada"
    else:
        comp_cinta = "Master Link"
        comp_manilha = "Manilha 8.5T"
        comp_nautillus = "Conexão Direta"
        comp_costura = "Alça da Cesta"

    # Desenho Visual - Auxiliar
    st.markdown('<div class="rigging-box" style="border-color: #D32F2F;">⚪ MOITÃO AUXILIAR DO GUINDASTE 20T</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box">⛓️ {comp_cinta}</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box">🧲 {comp_manilha}</div>', unsafe_allow_html=True)
    if "Nautillus" in comp_nautillus:
        st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rigging-box">⚓ {comp_nautillus}</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box">🪢 {comp_costura} (Costura na carga)</div>', unsafe_allow_html=True)
    st.markdown('<div class="rigging-arrow">⬇</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rigging-box" style="background-color: #D32F2F; color: white;">📦 {equipamento.upper()}</div>', unsafe_allow_html=True)

st.divider()

# ==========================================
# 5. CHECKLIST E APROVAÇÕES
# ==========================================
st.markdown("#### ✅ 4. Verificação Pré-Içamento (Checklist de Convés)")

chk1, chk2 = st.columns(2)
with chk1:
    st.checkbox("Instalar contrapino na farpela da bola / bloco")
    st.checkbox("Instalar contrapino nas manilhas da lingada de içamento")
    st.checkbox("Conferir manilhas Subsea na posição travada")
with chk2:
    st.checkbox("Transponder Instalado")
    st.checkbox("Equipe do ROV verificou o arranjo de içamento")
    st.checkbox("Gancho ou manilhas de manuseio ROV inspecionadas")

st.info("📢 Durante os últimos 100 metros de descida, o operador do guindaste deve comunicar ao SSE através do clear comm. a profundidade a cada 10 metros.")

st.button("Salvar e Exportar Lift Plan", type="primary", use_container_width=True)
