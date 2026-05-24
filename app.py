import streamlit as st
import pandas as pd
import datetime

# 1. Configuração inicial da página
st.set_page_config(page_title="Assistente de Operações", layout="wide")
st.title("Módulo 1: Previsão Otimista de Prontidão")

# 2. Base de Dados das Etapas (Pode ser expandida conforme sua necessidade)
# Os tempos estão em horas (ex: 0.5 = 30 minutos, 1.0 = 1 hora)
BASE_DADOS_ETAPAS = {
    "Navegar para a locação": {"responsavel": "MPSV", "duracao_h": 1.0},
    "Check list de DP": {"responsavel": "MPSV", "duracao_h": 0.5},
    "Descer ROV": {"responsavel": "MPSV", "duracao_h": 1.0},
    "Inspeção inicial": {"responsavel": "MPSV", "duracao_h": 0.5},
    "Descer SCMMB": {"responsavel": "MPSV", "duracao_h": 1.0},
    "Instalar o SCMMB": {"responsavel": "MPSV", "duracao_h": 1.0},
    "Instalar os EFL e HFL": {"responsavel": "MPSV", "duracao_h": 3.0},
    "Subir ROV": {"responsavel": "MPSV", "duracao_h": 1.0},
    "Outra Atividade (Manual)": {"responsavel": "MPSV", "duracao_h": 0.0}
}

# 3. Inicializar a memória do sistema (Session State) para guardar as etapas adicionadas
if 'etapas_adicionadas' not in st.session_state:
    st.session_state.etapas_adicionadas = []

# 4. Interface de Entrada de Dados
with st.container():
    st.subheader("Adicionar Nova Etapa")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39DA-RJS)")
    with col2:
        etapa_selecionada = st.selectbox("Selecione a Etapa", list(BASE_DADOS_ETAPAS.keys()))
    with col3:
        # Puxa automaticamente da base de dados, mas permite edição
        responsavel_padrao = BASE_DADOS_ETAPAS[etapa_selecionada]["responsavel"]
        responsavel = st.text_input("Responsável", value=responsavel_padrao)
    with col4:
        # Puxa automaticamente da base de dados, mas permite edição
        duracao_padrao = BASE_DADOS_ETAPAS[etapa_selecionada]["duracao_h"]
        duracao_horas = st.number_input("Duração (em Horas)", value=float(duracao_padrao), step=0.5)

    if st.button("Adicionar Etapa à Programação"):
        if locacao:
            nova_etapa = {
                "Locação": locacao,
                "Etapa": etapa_selecionada,
                "Responsável": responsavel,
                "Duração (Horas)": duracao_horas
            }
            st.session_state.etapas_adicionadas.append(nova_etapa)
            st.success(f"Etapa '{etapa_selecionada}' adicionada com sucesso!")
        else:
            st.error("Por favor, preencha o campo de Locação.")

st.divider()

# 5. Tabela de Previsão e Resultados
if st.session_state.etapas_adicionadas:
    st.subheader("Programação Atual")
    
    # Converte os dados em uma tabela para visualização
    df_programacao = pd.DataFrame(st.session_state.etapas_adicionadas)
    
    # Botão para limpar a tabela caso precise recomeçar
    if st.button("Limpar Programação"):
        st.session_state.etapas_adicionadas = []
        st.rerun()

    # Exibe a tabela interativa (permite deletar linhas nativamente no Streamlit)
    st.dataframe(df_programacao, use_container_width=True)
    
    # 6. Cálculos de Tempo
    duracao_total_horas = df_programacao["Duração (Horas)"].sum()
    
    st.subheader("Análise de Prontidão")
    colA, colB, colC = st.columns(3)
    
    with colA:
        data_inicio = st.date_input("Data de Início da Operação", datetime.date.today())
        hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0)) # Padrão 06:00
    
    # Combina data e hora de início
    inicio_datetime = datetime.datetime.combine(data_inicio, hora_inicio)
    
    # Calcula data/hora de término adicionando a duração total
    termino_datetime = inicio_datetime + datetime.timedelta(hours=duracao_total_horas)
    
    with colB:
        st.metric(label="Duração Otimista Total", value=f"{duracao_total_horas} Horas")
    
    with colC:
        st.metric(label="Previsão de Prontidão (Término)", value=termino_datetime.strftime("%d/%m/%Y %H:%M"))

else:
    st.info("Nenhuma etapa adicionada. Selecione as etapas acima para construir sua previsão de prontidão.")
st.divider()

# ==========================================
# MÓDULO 2: ANÁLISE DE PRESSÕES
# ==========================================
st.title("Módulo 2: Análise de Pressões (PE-2SUB-00406)")

tab1, tab2, tab3 = st.tabs(["Pressão Hidrostática", "Pressão Máxima de Teste", "Teste de Estanqueidade"])

# --- TAB 1: Pressão Hidrostática ---
with tab1:
    st.subheader("Cálculo de Pressão Hidrostática (PLDA)")
    st.info("Fator de conversão prático baseado no documento: 2000 m = 2940 psi (Fator ~ 1.47 psi/m).")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        profundidade = st.number_input("Lâmina D'água - LDA (m)", min_value=0.0, value=2000.0, step=10.0)
    with col_p2:
        fator_densidade = st.number_input("Fator de Conversão (psi/m)", value=1.47, step=0.01)
        
    pressao_hidrostatica = profundidade * fator_densidade
    st.metric("Pressão Hidrostática Resultante", f"{pressao_hidrostatica:.2f} psi")

# --- TAB 2: Pressão Máxima de Teste ---
with tab2:
    st.subheader("Pressão Máxima de Teste na HPU")
    st.latex(r"P_{MAX} \le RWP - PLDA")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        rwp = st.number_input("RWP do Equipamento (psi)", min_value=0.0, value=5000.0, step=100.0)
    with col_t2:
        plda = st.number_input("Pressão Hidrostática (PLDA) em psi", min_value=0.0, value=float(pressao_hidrostatica), step=10.0)
        
    p_max = rwp - plda
    st.metric("Pressão Máxima Permitida na HPU", f"{p_max:.2f} psi")

# --- TAB 3: Teste de Estanqueidade ---
with tab3:
    st.subheader("Critérios de Aceitação de Teste de Estanqueidade")
    
    p_teste = st.number_input("Pressão Nominal de Teste (psi)", min_value=1.0, value=5000.0, step=100.0)
    
    st.markdown("### Leitura dos Ciclos de Pressão")
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        p_0 = st.number_input("Pressão Inicial (0 min)", value=float(p_teste + 200), step=1.0)
    with col_e2:
        p_5 = st.number_input("Pressão aos 5 min", value=float(p_0 - 15), step=1.0)
    with col_e3:
        p_10 = st.number_input("Pressão aos 10 min (Preencher se solicitado)", value=float(p_5 - 5), step=1.0)
        
    st.markdown("### Histórico da Operação")
    primeiro_ciclo = st.checkbox("Este é o primeiro ciclo de pressurização (Não há ciclo anterior para comparar)", value=True)
    
    queda_ciclo_anterior = 0.0
    if not primeiro_ciclo:
        queda_ciclo_anterior = st.number_input("Taxa de Queda no Ciclo Anterior (psi/5min)", min_value=0.0, value=50.0, step=1.0)

    if st.button("Analisar Estanqueidade (Gerar Diagnóstico)"):
        queda_5min = p_0 - p_5
        queda_10min = p_5 - p_10
        
        limite_042 = p_teste * 0.0042
        limite_063 = p_teste * 0.0063
        
        st.write("---")
        st.write(f"**Análise dos primeiros 5 minutos:**")
        st.write(f"Queda real: **{queda_5min:.1f} psi** | Limite 0,42%: **{limite_042:.1f} psi** | Limite 0,63%: **{limite_063:.1f} psi**")
        
        # Lógica do Fluxograma da Petrobras
        condicao_queda_042 = queda_5min <= limite_042
        condicao_taxa_menor_anterior = primeiro_ciclo or (queda_5min < queda_ciclo_anterior)
        
        if condicao_queda_042 and condicao_taxa_menor_anterior:
            st.success("✅ 1ª Etapa (5 min) Aprovada: Queda $\le 0,42\%$ e taxa decrescente. Analisando os 5 minutos finais...")
            
            st.write(f"**Análise dos 5 minutos finais (5 a 10 min):**")
            st.write(f"Queda real: **{queda_10min:.1f} psi**")
            
            if queda_10min <= limite_042:
                if queda_10min < queda_5min:
                    st.success("🏆 **TESTE APROVADO!** Taxa de queda final é decrescente e encontra-se dentro do limite exigido.")
                else:
                    st.error("❌ **TESTE REPROVADO!** A taxa de queda nos 5 minutos finais não foi decrescente em relação aos 5 primeiros minutos.")
            else:
                st.error("❌ **TESTE REPROVADO!** A queda nos 5 minutos finais ultrapassou o limite de $0,42\%$.")
                
        else:
            st.warning("⚠️ Queda inicial maior que $0,42\%$ ou taxa não foi menor que a do ciclo anterior. Direcionando para avaliação secundária...")
            
            condicao_queda_063 = queda_5min < limite_063
            
            if condicao_queda_063:
                if condicao_taxa_menor_anterior:
                    st.info("🔄 **AÇÃO REQUERIDA: REPRESSURIZAR!** A queda é $< 0,63\%$ e a taxa é menor que a do ciclo anterior. Efetue repressurização e inicie um novo ciclo.")
                else:
                    st.error("❌ **TESTE REPROVADO!** A taxa de queda não é menor que a do ciclo anterior.")
            else:
                st.error("❌ **TESTE REPROVADO!** A queda nos primeiros 5 minutos é maior ou igual a $0,63\%$ da pressão de teste.")
