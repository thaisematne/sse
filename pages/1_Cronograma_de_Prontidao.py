import streamlit as st
import datetime
import json
import os
import uuid
from PIL import Image

# Força o sistema a buscar a logo na pasta anterior (raiz)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
logo_path = os.path.join(root_dir, "image_c889bf.png")

st.set_page_config(
    page_title="Cronograma de Prontidão | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar com Logo
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
else:
    st.sidebar.markdown("## 🔴 AKOFS Offshore")
st.sidebar.markdown("---")

# Título Principal
AKOFS_RED = "#D32F2F"
st.markdown(f"<h1 style='color: {AKOFS_RED};'>Subsea Planner Pro</h1>", unsafe_allow_html=True)
st.markdown("### Cronograma de Prontidão")
st.divider()

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
# 1. PARÂMETROS INICIAIS (DATA E HORA)
# ==========================================
st.subheader("⏱️ Início da Operação")
col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))
    
st.divider()

# ==========================================
# 2. ÁREA DE INSERÇÃO DE ETAPAS 
# ==========================================
with st.container():
    st.subheader("Adicionar Nova Etapa")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])

    with col1:
        locacao = st.text_input("Locação (Ex: 9-BUZ-39DA-RJS)", key="new_locacao")
    
    with col2:
        etapa_selecionada = st.selectbox("Selecione a Etapa", st.session_state.db["base_etapas"], key="new_etapa_sel")
        etapa_final = etapa_selecionada
        salvar_na_base = False
        
        if etapa_selecionada == "Outros":
            etapa_manual = st.text_input("Descreva a nova etapa:", placeholder="Digite aqui...", key="new_etapa_manual")
            etapa_final = etapa_manual
            salvar_na_base = st.checkbox("💾 Salvar na lista padrão", key="new_salvar_base")

    with col3:
        responsavel = st.text_input("Responsável", value="MPSV", key="new_responsavel")
    with col4:
        tempo_input = st.text_input("Tempo (HH:MM)", value="01:00", help="Use o formato HH:MM (ex: 01:30)", key="new_tempo")

    if st.button("➕ Adicionar à Programação", type="primary", key="btn_adicionar"):
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
# 3. LISTA DINÂMICA (EDIÇÃO E REORDENAÇÃO)
# ==========================================
if st.session_state.db["programacao"]:
    st.subheader("📋 Programação Atual")
    st.info("💡 **Edite os textos livremente**. Digite o tempo como HH:MM e use as setas para reordenar.")

    hc1, hc2, hc3, hc4, hc5, hc_acoes = st.columns([0.4, 2, 3, 1.5, 1.2, 1.5])
    hc1.write("**#**")
    hc2.write("**Locação**")
    hc3.write("**Etapa**")
    hc4.write("**Responsável**")
    hc5.write("**Tempo**")
    hc_acoes.write("**Ações**")

    def atualizar_campo(index, campo, chave_widget):
        st.session_state.db["programacao"][index][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(index, chave_widget):
        h, m = parse_tempo(st.session_state[chave_widget])
        st.session_state.db["programacao"][index]["Horas"] = h
        st.session_state.db["programacao"][index]["Minutos"] = m
        salvar_dados(st.session_state.db)

    for idx, item in enumerate(st.session_state.db["programacao"]):
        if "id" not in item:
            item["id"] = str(uuid.uuid4())
            
        uid = item["id"]

        c1, c2, c3, c4, c5, c_up, c_down, c_del = st.columns([0.4, 2, 3, 1.5, 1.2, 0.5, 0.5, 0.5])
        
        c1.markdown(f"<div style='margin-top: 8px; font-weight: bold;'>{idx+1}</div>", unsafe_allow_html=True)
        
        c2.text_input("Locação", value=item["Locação"], key=f"loc_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"loc_{uid}"))
        c3.text_input("Etapa", value=item["Etapa"], key=f"et_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"et_{uid}"))
        c4.text_input("Responsável", value=item["Responsável"], key=f"resp_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"resp_{uid}"))
        
        tempo_formatado = f"{int(item.get('Horas', 0)):02d}:{int(item.get('Minutos', 0)):02d}"
        c5.text_input("Tempo", value=tempo_formatado, key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
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
    # 4. CÁLCULO FINAL E BOTÕES DE AÇÃO
    # ==========================================
    st.divider()
    st.subheader("🎯 Resumo Operacional")

    total_horas = sum(int(item.get("Horas", 0)) for item in st.session_state.db["programacao"])
    total_minutos = sum(int(item.get("Minutos", 0)) for item in st.session_state.db["programacao"])

    total_horas += total_minutos // 60
    total_minutos = total_minutos % 60

    inicio_datetime = datetime.datetime.combine(data_inicio, hora_inicio)
    termino_datetime = inicio_datetime + datetime.timedelta(hours=total_horas, minutes=total_minutos)

    colA, colB = st.columns(2)
    with colA:
        st.metric(label="Duração Total Estimada", value=f"{int(total_horas):02d}h {int(total_minutos):02d}m")
    with colB:
        st.metric(label="Previsão de Prontidão", value=termino_datetime.strftime("%d/%m/%Y às %H:%M"))

    st.divider()
    
    # Linha de botões finais
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        # Botão personalizado com CSS e JS para imprimir/salvar PDF nativo
        st.markdown(
            f"""
            <a href="javascript:window.print()" class="btn-print">
                🖨️ Imprimir / Salvar PDF
            </a>
            <style>
            .btn-print {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: {AKOFS_RED};
                color: white !important;
                padding: 0.5rem 1rem;
                text-decoration: none;
                border-radius: 0.5rem;
                font-weight: 600;
                width: 100%;
                text-align: center;
                font-family: "Source Sans Pro", sans-serif;
            }}
            .btn-print:hover {{
                background-color: #b71c1c;
            }}
            /* Magia para limpar a tela na hora de imprimir o PDF */
            @media print {{
                section[data-testid="stSidebar"] {{ display: none !important; }}
                header[data-testid="stHeader"] {{ display: none !important; }}
                .btn-print {{ display: none !important; }}
                .stButton {{ display: none !important; }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    with col_btn2:
        if st.button("🗑️ Limpar Programação", key="btn_reset_total", use_container_width=True):
            st.session_state.db["programacao"] = []
            salvar_dados(st.session_state.db)
            st.rerun()
