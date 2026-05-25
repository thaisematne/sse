import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(page_title="Previsão de Prontidão", layout="wide")
st.title("Módulo 1: Previsão Otimista de Prontidão")

ARQUIVO_DADOS = "dados_prontidao.json"

# Etapas padrão (Baseline)
ETAPAS_DEFAULT = [
    "Navegar para a locação", "Check list de DP", "Descer ROV",
    "Inspeção inicial", "Descer equipamento", "Instalar equipamento",
    "Manuseio de EFL", "Manuseio de HFL", "Manuseio de válvula",
    "Etapas da UEP", "Realizar testes / intervenção",
    "Desmobilizar equipamento", "Recolher equipamento",
    "Inspeção final", "Subir ROV", "Aguardar prontidão", "Outros"
]

# Função para garantir a persistência dos dados (Salvar no Disco)
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

# Garantir que a opção "Outros" sempre exista no final da lista
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
        
        # Se for manual (Outros), abre o campo de texto
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
            # Salvar nova etapa na base, se o usuário pediu
            if salvar_na_base and etapa_final not in st.session_state.db["base_etapas"]:
                # Insere antes da palavra "Outros"
                st.session_state.db["base_etapas"].insert(-1, etapa_final)

            nova_etapa = {
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
# 2. EDIÇÃO, REORDENAÇÃO E TABELA
# ==========================================
if st.session_state.db["programacao"]:
    st.subheader("📋 Programação Atual")
    st.info("💡 **Dica de Edição:** Você pode dar um duplo clique em qualquer célula da tabela para alterar textos, horas ou minutos diretamente.")

    # Converte para Dataframe e gera a Tabela Editável
    df = pd.DataFrame(st.session_state.db["programacao"])
    
    df_editado = st.data_editor(
        df,
        num_rows="dynamic", # Permite excluir linhas selecionando e apertando 'Delete'
        use_container_width=True,
        column_config={
            "Horas": st.column_config.NumberColumn("Horas", min_value=0, step=1),
            "Minutos": st.column_config.NumberColumn("Minutos", min_value=0, max_value=59, step=1)
        }
    )

    # Verifica se houve edição na tabela e salva as modificações
    novo_prog = df_editado.to_dict(orient="records")
    if novo_prog != st.session_state.db["programacao"]:
        st.session_state.db["programacao"] = novo_prog
        salvar_dados(st.session_state.db)
        st.rerun()

    # --- Controle de Reordenação (Subir/Descer) ---
    if len(st.session_state.db["programacao"]) > 1:
        st.markdown("**🔄 Reorganizar Posições:**")
        col_idx, col_up, col_down, _ = st.columns([3, 1, 1, 5])
        
        opcoes_reordem = [f"{i+1} - {item['Etapa']} ({item['Horas']}h {item['Minutos']}m)" for i, item in enumerate(st.session_state.db["programacao"])]
        item_selecionado = col_idx.selectbox("Selecione a etapa para mover:", opcoes_reordem, label_visibility="collapsed")
        idx_selecionado = opcoes_reordem.index(item_selecionado)

        with col_up:
            if st.button("⬆️ Subir"):
                if idx_selecionado > 0:
                    prog = st.session_state.db["programacao"]
                    # Troca as posições
                    prog[idx_selecionado], prog[idx_selecionado-1] = prog[idx_selecionado-1], prog[idx_selecionado]
                    salvar_dados(st.session_state.db)
                    st.rerun()
        with col_down:
            if st.button("⬇️ Descer"):
                if idx_selecionado < len(st.session_state.db["programacao"]) - 1:
                    prog = st.session_state.db["programacao"]
                    # Troca as posições
                    prog[idx_selecionado], prog[idx_selecionado+1] = prog[idx_selecionado+1], prog[idx_selecionado]
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

    # Matemática da Duração (Ajustando overflow de minutos)
    total_horas = sum(item["Horas"] for item in st.session_state.db["programacao"])
    total_minutos = sum(item["Minutos"] for item in st.session_state.db["programacao"])

    # Exemplo: 120 minutos se transformam em +2 Horas e 0 minutos
    total_horas += total_minutos // 60
    total_minutos = total_minutos % 60

    inicio_datetime = datetime.datetime.combine(data_inicio, hora_inicio)
    termino_datetime = inicio_datetime + datetime.timedelta(hours=total_horas, minutes=total_minutos)

    with colB:
        st.metric(label="Duração Total Estimada", value=f"{int(total_horas):02d}h {int(total_minutos):02d}m")
    with colC:
        st.metric(label="Previsão de Prontidão", value=termino_datetime.strftime("%d/%m/%Y às %H:%M"))

    st.divider()
    # Botão de Reset
    if st.button("🗑️ Apagar Tudo e Começar Novo Registro"):
        st.session_state.db["programacao"] = []
        salvar_dados(st.session_state.db)
        st.rerun()
