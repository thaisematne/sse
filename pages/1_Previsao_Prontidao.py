import streamlit as st
import datetime
import json
import os
import uuid

st.set_page_config(page_title="Previsão de Prontidão", layout="wide")
st.title("Módulo 1: Previsão Otimista de Prontidão")

ARQUIVO_DADOS = "dados_prontidao.json"

ETAPAS_DEFAULT = [
    "Navegar para a locação", "Check list de DP", "Descer ROV",
    "Inspeção inicial", "Descer equipamento", "Instalar equipamento",
    "Manuseio de EFL", "Manuseio de HFL", "Manuseio de válvula",
    "Etapas da UEP", "Realizar testes / intervenção",
    "Desmobilizar equipamento", "Recolher equipamento",
    "Inspeção final", "Subir ROV", "Aguardar prontidão", "Outros"
]

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

if "Outros" not in st.session_state.db["base_etapas"]:
    st.session_state.db["base_etapas"].append("Outros")

# ==========================================
# 1. ÁREA DE INSERÇÃO DE ETAPAS
# ==========================================
with st.container():
    st.subheader("Adicionar Nova Etapa")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])

    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39DA-RJS)")
    
    with col2:
        etapa_selecionada = st.selectbox("Selecione a Etapa", st.session_state.db["base_etapas"])
        etapa_final = etapa_selecionada
        salvar_na_base = False
        
        if etapa_selecionada == "Outros":
            etapa_manual = st.text_input("Descreva a nova etapa:", placeholder="Digite aqui...")
            etapa_final = etapa_manual
            salvar_na_base = st.checkbox("💾 Salvar na lista padrão do sistema")

    with col3:
        responsavel = st.text_input("Responsável", value="MPSV")
    with col4:
        horas = st.number_input("Horas (hh)", min_value=0, max_value=200, value=1, step=1)
    with col5:
        minutos = st.number_input("Minutos (mm)", min_value=0, max_value=59, value=0, step=5)

    if st.button("➕ Adicionar à Programação", type="primary"):
        if not locacao:
            st.error("Por favor, preencha a Locação.")
        elif etapa_selecionada == "Outros" and not etapa_final.strip():
            st.error("Por favor, descreva a etapa que você selecionou como 'Outros'.")
        else:
            if salvar_na_base and etapa_final not in st.session_state.db["base_etapas"]:
                st.session_state.db["base_etapas"].insert(-1, etapa_final)

            # O ID único (uuid) é o segredo para os botões de reordenação funcionarem sem perder o texto
            nova_etapa = {
                "
