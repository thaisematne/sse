import streamlit as st
import datetime
import json
import os
import uuid

# 1. CONFIGURAÇÃO E DADOS
ARQUIVO_DADOS = "dados_prontidao.json"
ETAPAS_DEFAULT = [
    "Navegar para a locação", "Check list de DP", "Descer ROV", "Inspeção inicial",
    "Descer equipamento", "Instalar equipamento", "Manuseio de EFL", "Manuseio de HFL",
    "Manuseio de válvula", "Etapas da UEP", "Realizar testes / intervenção",
    "Limpeza", "Desmobilizar equipamento", "Recolher equipamento",
    "Inspeção final", "Subir ROV", "Aguardar prontidão", "Outros"
]

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# 2. INTERFACE PRINCIPAL
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# Parâmetros Iniciais
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# Inserção de Etapas
st.subheader("Adicionar Nova Etapa")
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
locacao = col1.text_input("Locação")
etapa_sel = col2.selectbox("Etapa", st.session_state.db["base_etapas"])
resp = col3.text_input("Responsável", value="MPSV")
tempo = col4.text_input("Tempo (HH:MM)", value="01:00")

if st.button("Adicionar"):
    try:
        h, m = map(int, tempo.split(':'))
        st.session_state.db["programacao"].append({
            "id": str(uuid.uuid4()), "Locação": locacao, "Etapa": etapa_sel, 
            "Responsável": resp, "Horas": h, "Minutos": m
        })
        salvar_dados(st.session_state.db)
        st.rerun()
    except: st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# Listagem e Edição
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed")
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed")
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed")
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed")
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db); st.rerun()
        if c[5].button("⬇️", key=f"dw_{uid}") and idx < len(st.session_state.db["programacao"])-1:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx+1] = st.session_state.db["programacao"][idx+1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state.db); st.rerun()
        if c[6].button("❌", key=f"del_{uid}"):
            st.session_state.db["programacao"].pop(idx)
            salvar_dados(st.session_state.db); st.rerun()

# Resumo
st.divider()
tot_h = sum(i["Horas"] for i in st.session_state.db["programacao"])
tot_m = sum(i["Minutos"] for i in st.session_state.db["programacao"])
tot_h += tot_m // 60
tot_m %= 60

fim_dt = datetime.datetime.combine(data_inicio, hora_inicio) + datetime.timedelta(hours=tot_h, minutes=tot_m)
st.metric("Duração Total", f"{tot_h:02d}h {tot_m:02d}m")
st.metric("Previsão de Prontidão", fim_dt.strftime("%d/%m/%Y às %H:%M"))
