import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Previsão de Prontidão", layout="wide")
st.title("Módulo 1: Previsão Otimista de Prontidão")

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

if 'etapas_adicionadas' not in st.session_state:
    st.session_state.etapas_adicionadas = []

with st.container():
    st.subheader("Adicionar Nova Etapa")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39DA-RJS)")
    with col2:
        etapa_selecionada = st.selectbox("Selecione a Etapa", list(BASE_DADOS_ETAPAS.keys()))
    with col3:
        responsavel_padrao = BASE_DADOS_ETAPAS[etapa_selecionada]["responsavel"]
        responsavel = st.text_input("Responsável", value=responsavel_padrao)
    with col4:
        duracao_padrao = BASE_DADOS_ETAPAS[etapa_selecionada]["duracao_h"]
        duracao_horas = st.number_input("Duração (em Horas)", value=float(duracao_padrao), step=0.5)

    if st.button("Adicionar Etapa à Programação"):
        if locacao:
            nova_etapa = {"Locação": locacao, "Etapa": etapa_selecionada, "Responsável": responsavel, "Duração (Horas)": duracao_horas}
            st.session_state.etapas_adicionadas.append(nova_etapa)
            st.success(f"Etapa adicionada com sucesso!")
        else:
            st.error("Por favor, preencha a Locação.")

st.divider()

if st.session_state.etapas_adicionadas:
    st.subheader("Programação Atual")
    df_programacao = pd.DataFrame(st.session_state.etapas_adicionadas)
    
    if st.button("Limpar Programação"):
        st.session_state.etapas_adicionadas = []
        st.rerun()

    st.dataframe(df_programacao, use_container_width=True)
    
    duracao_total_horas = df_programacao["Duração (Horas)"].sum()
    
    st.subheader("Análise de Prontidão")
    colA, colB, colC = st.columns(3)
    
    with colA:
        data_inicio = st.date_input("Data de Início", datetime.date.today())
        hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))
    
    inicio_datetime = datetime.datetime.combine(data_inicio, hora_inicio)
    termino_datetime = inicio_datetime + datetime.timedelta(hours=duracao_total_horas)
    
    with colB:
        st.metric(label="Duração Total", value=f"{duracao_total_horas} Horas")
    with colC:
        st.metric(label="Previsão de Prontidão", value=termino_datetime.strftime("%d/%m/%Y %H:%M"))
