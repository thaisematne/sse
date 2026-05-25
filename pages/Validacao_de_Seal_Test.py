import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Validação de Seal Test | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inserção da Logo na Sidebar (Menu Lateral)
st.sidebar.markdown("## 🔴 AKOFS Offshore")
st.sidebar.markdown("---")

st.title("Subsea Planner Pro")
st.markdown("### Módulo 2: Validação de Seal Test")
st.divider()

tab1, tab2, tab3 = st.tabs(["Pressão Hidrostática", "Pressão Máxima de Teste", "Teste de Estanqueidade"])

# --- TAB 1 e 2 omitidas para focar na interface limpa, mas funcionais ---
with tab1:
    st.subheader("Cálculo de Pressão Hidrostática (PLDA)")
    col_p1, col_p2 = st.columns(2)
    profundidade = col_p1.number_input("Lâmina D'água - LDA (m)", min_value=0.0, value=2000.0, step=10.0)
    fator_densidade = col_p2.number_input("Fator de Conversão (psi/m)", value=1.47, step=0.01)
    pressao_hidrostatica = profundidade * fator_densidade
    st.metric("Pressão Hidrostática Resultante", f"{pressao_hidrostatica:.2f} psi")

with tab2:
    st.subheader("Pressão Máxima de Teste na HPU")
    col_t1, col_t2 = st.columns(2)
    rwp = col_t1.number_input("RWP do Equipamento (psi)", min_value=0.0, value=5000.0, step=100.0)
    plda = col_t2.number_input("Pressão Hidrostática (PLDA)", min_value=0.0, value=float(pressao_hidrostatica), step=10.0)
    st.metric("Pressão Máxima Permitida na HPU", f"{(rwp - plda):.2f} psi")

# --- TAB 3: O NOVO TESTE DE ESTANQUEIDADE ---
with tab3:
    st.subheader("Critérios de Aceitação e Monitoramento")
    
    p_teste = st.number_input("Pressão Nominal de Teste (psi)", min_value=1.0, value=5000.0, step=100.0)
    
    limite_042 = p_teste * 0.0042
    limite_063 = p_teste * 0.0063
    
    st.markdown("### 🎯 Limites de Aceitação Calculados")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.info(f"🟢 **Limite 0,42% (Para Aprovação):** Queda Máxima de **{limite_042:.1f} psi** em 5 min")
    with col_l2:
        st.warning(f"🔴 **Limite 0,63% (Reprovação Imediata):** Acima de **{limite_063:.1f} psi** em 5 min")

    st.markdown("---")
    st.markdown("### ⏱️ Tabela de Monitoramento")
    st.write("Você pode digitar as pressões acompanhando o relógio. Adicione linhas se precisar de mais tempo de acomodação.")

    # Criação de uma tabela editável no Streamlit
    if 'tabela_pressoes' not in st.session_state:
        st.session_state.tabela_pressoes = pd.DataFrame({
            "Minuto do Teste": [0, 5, 10, 15, 20],
            "Pressão Registrada (psi)": [0.0, 0.0, 0.0, 0.0, 0.0]
        })

    # Mostra a tabela interativa onde você digita os dados
    df_leituras = st.data_editor(st.session_state.tabela_pressoes, num_rows="dynamic", use_container_width=True)

    st.markdown("### 📊 Análise Inteligente da Janela de Teste")
    st.write("A pressão demorou a estabilizar? Sem problemas. Escolha abaixo qual minuto você quer considerar como o **Minuto 0 (Início)** do seu teste.")
    
    minutos_disponiveis = df_leituras["Minuto do Teste"].tolist()
    inicio_selecionado = st.selectbox("Considerar o Início do Teste a partir do minuto:", options=minutos_disponiveis)

    if st.button("Analisar esta Janela de 10 minutos", type="primary"):
        idx_0 = df_leituras.index[df_leituras["Minuto do Teste"] == inicio_selecionado].tolist()[0]
        
        # Verifica se preencheu pelo menos mais 10 minutos para frente
        if len(df_leituras) <= idx_0 + 2:
            st.error(f"Você precisa preencher as pressões dos minutos {inicio_selecionado + 5} e {inicio_selecionado + 10} na tabela acima para fazer a análise completa.")
        else:
            p_0 = df_leituras.iloc[idx_0]["Pressão Registrada (psi)"]
            p_5 = df_leituras.iloc[idx_0 + 1]["Pressão Registrada (psi)"]
            p_10 = df_leituras.iloc[idx_0 + 2]["Pressão Registrada (psi)"]

            queda_5_iniciais = p_0 - p_5
            queda_5_finais = p_5 - p_10
            queda_total = p_0 - p_10

            st.write("---")
            # Apresentação das métricas isoladas e totais
            st.markdown("#### 📉 Resumo das Quedas")
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("Queda 5 Min. Iniciais", f"{queda_5_iniciais:.1f} psi")
            col_r2.metric("Taxa/Queda 5 Min. Finais", f"{queda_5_finais:.1f} psi")
            col_r3.metric("Queda Total (10 min)", f"{queda_total:.1f} psi")

            st.markdown("#### 📋 Diagnóstico (PE-2SUB-00406)")
            # Lógica
            if queda_5_iniciais <= limite_042:
                if queda_5_finais <= limite_042 and queda_5_finais < queda_5_iniciais:
                    st.success("🏆 **TESTE APROVADO!** A queda nos 5 minutos finais é decrescente em relação ao início e está dentro do limite de 0,42%.")
                elif queda_5_finais >= queda_5_iniciais:
                    st.error("❌ **REPROVADO:** A taxa de queda nos 5 minutos finais NÃO é decrescente (a pressão caiu mais rápido ou igual ao período anterior).")
                else:
                    st.error("❌ **REPROVADO:** A queda nos 5 minutos finais ultrapassou o limite de 0,42%.")
            elif queda_5_iniciais < limite_063:
                st.info("🔄 **AÇÃO REQUERIDA (REPRESSURIZAR):** A queda nos primeiros 5 minutos está entre 0,42% e 0,63%. Você deve repressurizar ou descartar esta janela de tempo e testar os próximos minutos.")
            else:
                st.error("❌ **REPROVADO:** A queda nos primeiros 5 minutos ultrapassou 0,63%. Obrigatório Repressurizar e reiniciar o ciclo.")
