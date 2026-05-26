import streamlit as st
import pandas as pd
import os
import base64

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA E LOGO NO MENU
# ==========================================
st.set_page_config(
    page_title="Validação do Seal Test | Subsea Planner Pro", 
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
st.markdown("### Validação do Seal Test")
st.write("Fluxo contínuo de cálculos preparatórios, conversões e monitoramento de estanqueidade.")
st.divider()

# ==========================================
# ETAPA 1: PRESSÃO HIDROSTÁTICA E MÁXIMA
# ==========================================
st.markdown("### 1. Parâmetros de Profundidade e Limites (HPU)")
col1, col2, col3 = st.columns(3)

with col1:
    profundidade = st.number_input("Lâmina D'água - LDA (m)", min_value=0.0, value=2000.0, step=10.0)
with col2:
    fator_densidade = st.number_input("Fator de Conversão (psi/m)", value=1.46, step=0.01) # Default alterado para 1.46
with col3:
    rwp = st.number_input("RWP do Equipamento (psi)", min_value=0.0, value=5000.0, step=100.0)

pressao_hidrostatica = profundidade * fator_densidade
pressao_max_hpu = rwp - pressao_hidrostatica

col_r1, col_r2 = st.columns(2)
col_r1.metric("Pressão Hidrostática (PLDA)", f"{pressao_hidrostatica:.2f} psi")
col_r2.metric("Pressão Máxima Permitida na HPU", f"{pressao_max_hpu:.2f} psi")

st.divider()

# ==========================================
# ETAPA 2: CONVERSOR ABSOLUTA / RELATIVA SUBSEA
# ==========================================
st.markdown("### 2. Conversor de Pressão Subsea (Absoluta ↔ Relativa)")
st.write("Esta conversão vincula e utiliza a Pressão Hidrostática calculada na Etapa 1.")
col_c1, col_c2, col_c3 = st.columns([1, 1, 2])

with col_c1:
    p_atm = st.number_input("Pressão Atmosférica Local (psi)", value=14.7, step=0.1)
with col_c2:
    direcao_conversao = st.selectbox("Direção da Conversão", ["Relativa ➔ Absoluta (Fundo)", "Absoluta (Fundo) ➔ Relativa"])
with col_c3:
    valor_converter = st.number_input("Valor a Converter (psi)", value=0.0, step=10.0)

if direcao_conversao == "Relativa ➔ Absoluta (Fundo)":
    resultado_conv = valor_converter + pressao_hidrostatica + p_atm
    st.info(f"**Resultado:** {valor_converter:.2f} psig + {pressao_hidrostatica:.2f} psi (Hidrostática) + {p_atm:.2f} psi (Atm) = **{resultado_conv:.2f} psia**")
else:
    resultado_conv = valor_converter - pressao_hidrostatica - p_atm
    st.info(f"**Resultado:** {valor_converter:.2f} psia - {pressao_hidrostatica:.2f} psi (Hidrostática) - {p_atm:.2f} psi (Atm) = **{resultado_conv:.2f} psig**")

st.divider()

# ==========================================
# ETAPA 3: TESTE DE ESTANQUEIDADE COMPLETO
# ==========================================
st.markdown("### 3. Teste de Estanqueidade e Laudo")

# --- Configurações do Teste ---
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    p_teste_nominal = st.number_input("Pressão Nominal de Teste (psig)", min_value=1.0, value=5000.0, step=100.0)
with col_t2:
    tipo_leitura = st.selectbox("Leitura dos Sensores", ["Relativa (psig)", "Absoluta (psia)"], 
                                help="Selecione Absoluta se o sensor subsea registrar a pressão total (incluindo a coluna d'água).")
with col_t3:
    portas_sel = st.radio("Portas em Teste", ["Porta A", "Porta B", "Portas A e B Simultâneas"])

# --- Cálculos de Aceitação ---
limite_042 = p_teste_nominal * 0.0042
limite_063 = p_teste_nominal * 0.0063

st.markdown("#### 🎯 Limites de Aceitação (PE-2SUB-00406)")
col_l1, col_l2 = st.columns(2)
with col_l1:
    st.success(f"🟢 **Limite 0,42% (Aprovação):** Queda Máx. de **{limite_042:.1f} psi** em 5 min")
with col_l2:
    st.warning(f"🔴 **Limite 0,63% (Reprovação):** Acima de **{limite_063:.1f} psi** em 5 min")

st.markdown("#### ⏱️ Tabela de Monitoramento")

# --- Estruturação Dinâmica da Tabela ---
if portas_sel == "Portas A e B Simultâneas":
    cols_tabela = ["Minuto do Teste", "Pressão A", "Pressão B"]
    colunas_analise = ["Pressão A", "Pressão B"]
elif portas_sel == "Porta A":
    cols_tabela = ["Minuto do Teste", "Pressão A"]
    colunas_analise = ["Pressão A"]
else:
    cols_tabela = ["Minuto do Teste", "Pressão B"]
    colunas_analise = ["Pressão B"]

# Reseta/Atualiza as colunas se mudar a seleção de portas
if "tab_est" not in st.session_state or list(st.session_state.tab_est.columns) != cols_tabela:
    df_init = pd.DataFrame({"Minuto do Teste": [0, 5, 10, 15, 20]})
    for c in colunas_analise:
        df_init[c] = 0.0
    st.session_state.tab_est = df_init

# Renderiza a tabela editável
df_leituras = st.data_editor(st.session_state.tab_est, num_rows="dynamic", use_container_width=True)

# --- Análise e Laudo Inteligente ---
st.markdown("#### 📊 Análise da Janela de Teste")
minutos_disponiveis = df_leituras["Minuto do Teste"].tolist()
inicio_selecionado = st.selectbox("Selecionar o Minuto 0 (Início da Estabilização):", options=minutos_disponiveis)

if st.button("Gerar Laudo de 10 Minutos", type="primary"):
    idx_0 = df_leituras.index[df_leituras["Minuto do Teste"] == inicio_selecionado].tolist()[0]
    
    if len(df_leituras) <= idx_0 + 2:
        st.error(f"Preencha as pressões dos minutos {inicio_selecionado + 5} e {inicio_selecionado + 10} na tabela acima.")
    else:
        if tipo_leitura == "Absoluta (psia)":
            st.info(f"ℹ️ **Conversão Automática Subsea:** Sensores em Absoluta. Subtraindo {pressao_hidrostatica:.2f} psi (Hidrostática) e {p_atm:.2f} psi (Atm) para obter o equivalente relativo.")

        # Cria colunas lado a lado para laudos individuais ou simultâneos
        cols_resultado = st.columns(len(colunas_analise))
        
        for i, porta in enumerate(colunas_analise):
            with cols_resultado[i]:
                st.markdown(f"### Resultado: {porta}")
                
                p_0 = df_leituras.iloc[idx_0][porta]
                p_5 = df_leituras.iloc[idx_0 + 1][porta]
                p_10 = df_leituras.iloc[idx_0 + 2][porta]

                # Conversão matemática automatizada baseada na Etapa 1 e 2
                if tipo_leitura == "Absoluta (psia)":
                    p_0_exib = p_0 - pressao_hidrostatica - p_atm
                    p_5_exib = p_5 - pressao_hidrostatica - p_atm
                    p_10_exib = p_10 - pressao_hidrostatica - p_atm
                else:
                    p_0_exib, p_5_exib, p_10_exib = p_0, p_5, p_10

                st.write(f"- **P0 (Início):** {p_0_exib:.1f} psig")
                st.write(f"- **P5 (Intermediário):** {p_5_exib:.1f} psig")
                st.write(f"- **P10 (Final):** {p_10_exib:.1f} psig")

                # Deltas de queda (independem da unidade, mas usam a escala real)
                queda_5_iniciais = p_0 - p_5
                queda_5_finais = p_5 - p_10

                st.markdown("**📉 Quedas Registradas:**")
                st.write(f"Iniciais (0-5m): **{queda_5_iniciais:.1f} psi** | Finais (5-10m): **{queda_5_finais:.1f} psi**")

                # Critérios rígidos de diagnóstico
                if queda_5_iniciais <= limite_042:
                    if queda_5_finais <= limite_042 and queda_5_finais < queda_5_iniciais:
                        st.success(f"🏆 **{porta} APROVADA:** Queda nos 5 minutos finais é decrescente e abaixo de 0,42%.")
                    elif queda_5_finais >= queda_5_iniciais:
                        st.error(f"❌ **{porta} REPROVADA:** A taxa de queda nos 5 minutos finais NÃO é decrescente.")
                    else:
                        st.error(f"❌ **{porta} REPROVADA:** Queda nos 5 minutos finais ultrapassou o limite de 0,42%.")
                elif queda_5_iniciais < limite_063:
                    st.warning(f"🔄 **{porta} - REPRESSURIZAR:** Queda inicial entre 0,42% e 0,63%. Descarte a janela ou reinicie.")
                else:
                    st.error(f"❌ **{porta} REPROVADA:** Queda inicial ultrapassou o limite crítico de 0,63%.")
