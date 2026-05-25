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
    "Limpeza", "Desmobilizar equipamento", "Recolher equipamento",
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
if "Limpeza" not in st.session_state.db["base_etapas"]:
    st.session_state.db["base_etapas"].insert(-2, "Limpeza")

def parse_tempo(tempo_str):
    try:
        tempo_str = str(tempo_str).strip()
        if ":" in tempo_str:
            partes = tempo_str.split(":")
            return int(partes[0]), int(partes[1])
        elif tempo_str.isdigit():
            return int(tempo_str), 0
    except:
        pass
    return 0, 0

# ==========================================
# 1. ÁREA DE INSERÇÃO DE ETAPAS
# ==========================================
with st.container():
    st.subheader("Adicionar Nova Etapa")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])

    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39DA-RJS)")
    
    with col2:
        etapa_selecionada = st.selectbox("Selecione a Etapa", st.session_state.db["base_etapas"])
        etapa_final = etapa_selecionada
        salvar_na_base = False
        
        if etapa_selecionada == "Outros":
            etapa_manual = st.text_input("Descreva a nova etapa:", placeholder="Digite aqui...")
            etapa_final = etapa_manual
            salvar_na_base = st.checkbox("💾 Salvar na lista padrão")

    with col3:
        responsavel = st.text_input("Responsável", value="MPSV")
    with col4:
        tempo_input = st.text_input("Tempo (HH:MM)", value="01:00", help="Use o formato HH:MM (ex: 01:30)")

    if st.button("➕ Adicionar à Programação", type="primary"):
        h, m = parse_tempo(tempo_input)
        
        if not locacao:
            st.error("Por favor, preencha a Locação.")
        elif etapa_selecionada == "Outros" and not etapa_final.strip():
            st.error("Por favor, descreva a etapa.")
        else:
            if salvar_na_base and etapa_final not in st.session_state.db["base_etapas"]:
                st.session_state.db["base_etapas"].insert(-1, etapa_final)

            nova_etapa = {
                "id": str(uuid.uuid4()),
                "Locação": locacao,
                "Etapa": etapa_final,
                "Responsável": responsavel,
                "Horas": h,
                "Minutos": m
            }
            st.session_state.db["programacao"].append(nova_etapa)
            salvar_dados(st.session_state.db)
            st.success("Etapa adicionada com sucesso!")
            st.rerun()

st.divider()

# ==========================================
# 2. LISTA DINÂMICA (EDIÇÃO E REORDENAÇÃO)
# ==========================================
if st.session_state.db["programacao"]:
    st.subheader("📋 Programação Atual")
    st.info("💡 **Edite os textos livremente**. Digite o tempo como HH:MM e use as setas para reordenar.")

    hc1, hc2, hc3, hc4, hc5, hc_acoes = st.columns([0.4, 2, 3, 1.5, 1.2, 1.5])
    hc1.write("**#**")
