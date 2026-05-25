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

            nova_etapa = {
                "id": str(uuid.uuid4()),
                "Locação": locacao,
                "Etapa": etapa_final,
                "Responsável": responsavel,
                "Horas": horas,
                "Minutos": minutos
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
    st.info("💡 **Edite os textos e números livremente**. Use as setas ao lado de cada linha para reordenar ou o ❌ para apagar.")

    # Cabeçalho da Lista
    hc1, hc2, hc3, hc4, hc5, hc6, hc_acoes = st.columns([0.4, 2, 3, 1.5, 0.8, 0.8, 1.5])
    hc1.write("**#**")
    hc2.write("**Locação**")
    hc3.write("**Etapa**")
    hc4.write("**Responsável**")
    hc5.write("**Hrs**")
    hc6.write("**Min**")
    hc_acoes.write("**Ações**")

    # Função de salvamento em tempo real
    def atualizar_campo(index, campo, chave_widget):
        st.session_state.db["programacao"][index][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    # Renderiza as etapas com os botões ao lado
    for idx, item in enumerate(st.session_state.db["programacao"]):
        if "id" not in item:
            item["id"] = str(uuid.uuid4())
            
        uid = item["id"]

        c1, c2, c3, c4, c5, c6, c_up, c_down, c_del = st.columns([0.4, 2, 3, 1.5, 0.8, 0.8, 0.5, 0.5, 0.5])
        
        c1.markdown(f"<div style='margin-top: 8px; font-weight: bold;'>{idx+1}</div>", unsafe_allow_html=True)
        
        c2.text_input("Locação", value=item["Locação"], key=f"loc_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"loc_{uid}"))
        c3.text_input("Etapa", value=item["Etapa"], key=f"et_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"et_{uid}"))
        c4.text_input("Responsável", value=item["Responsável"], key=f"resp_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"resp_{uid}"))
        c5.number_input("Hrs", min_value=0, value=int(item["Horas"]), key=f"h_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Horas", f"h_{uid}"))
        c6.number_input("Min", min_value=0, max_value=59, value=int(item["Minutos"]), key=f"m_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Minutos", f"m_{uid}"))
        
        with c_up:
            if st.button("⬆️", key=f"up_{uid}", help="Subir"):
                if idx > 0:
                    prog = st.session_state.db["programacao"]
                    prog[idx], prog[idx-1] = prog[idx-1], prog[idx]
                    salvar_dados(st.session_state.db)
                    st.rerun()
        with c_down:
            if st.button("⬇️", key=f"dw_{uid}", help="Descer"):
                if idx < len(st.session_state.db["programacao"]) - 1:
                    prog = st.session_state.db["programacao"]
                    prog[idx], prog[idx+1] = prog[idx+1], prog[idx]
                    salvar_dados(st.session_state.db)
                    st.rerun()
        with c_del:
            if st.button("❌", key=f"del_{uid}", help="Excluir"):
                st.session_state.db["programacao"].pop(idx)
                salvar_dados(st.session_state.db)
                st.rerun()

    # ==========================================
    # 3. CÁLCULO FINAL DE PRONTIDÃO
    # ==========================================
    st.divider()
    st.subheader("🎯 Análise de Prontidão")

    colA, colB, colC = st.columns(3)

    with colA:
        data_inicio = st.date_input("Data de Início", datetime.date.today())
        hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

    total_horas = sum(item["Horas"] for item in st.session_state.db["programacao"])
    total_minutos = sum(item["Minutos"] for item in st.session_state.db["programacao"])

    total_horas += total_minutos // 60
    total_minutos = total_minutos % 60

    inicio_datetime = datetime.datetime.combine(data_inicio, hora_inicio)
    termino_datetime = inicio_datetime + datetime.timedelta(hours=total_horas, minutes=total_minutos)

    with colB:
        st.metric(label="Duração Total Estimada", value=f"{int(total_horas):02d}h {int(total_minutos):02d}m")
    with colC:
        st.metric(label="Previsão de Prontidão", value=termino_datetime.strftime("%d/%m/%Y às %H:%M"))

    st.divider()
    if st.button("🗑️ Apagar Tudo e Começar Novo Registro"):
        st.session_state.db["programacao"] = []
        salvar_dados(st.session_state.db)
        st.rerun()
