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
