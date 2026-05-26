import streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_stateimport streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_stateimport streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_stateimport streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_stateimport streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_stateimport streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_stateimport streamlit as st
import datetime
import json
import os
import uuid
import base64

# ==========================================
# 0. LOGO FIXO NO TOPO DO MENU LATERAL
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 70px;
            margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. CONFIGURAÇÃO E DADOS
# ==========================================
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
        except: 
            pass
    return {"base_etapas": ETAPAS_DEFAULT, "programacao": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = carregar_dados()

# ==========================================
# 2. INTERFACE PRINCIPAL
# ==========================================
st.title("Subsea Planner Pro")
st.subheader("Cronograma de Prontidão")

# --- Parâmetros Iniciais ---
col_d1, col_d2 = st.columns(2)
with col_d1:
    data_inicio = st.date_input("Data de Início", datetime.date.today())
with col_d2:
    hora_inicio = st.time_input("Hora de Início", datetime.time(6, 0))

st.divider()

# --- Inserção de Etapas ---
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
    except: 
        st.error("Formato de tempo inválido (HH:MM)")

st.divider()

# --- Listagem e Edição ---
st.subheader("Programação Atual")
if st.session_state.db["programacao"]:
    
    # Funções de atualização em tempo real
    def atualizar_campo(idx, campo, chave_widget):
        st.session_state.db["programacao"][idx][campo] = st.session_state[chave_widget]
        salvar_dados(st.session_state.db)

    def atualizar_tempo(idx, chave_widget):
        try:
            h, m = map(int, st.session_state[chave_widget].split(':'))
            st.session_state.db["programacao"][idx]["Horas"] = h
            st.session_state.db["programacao"][idx]["Minutos"] = m
            salvar_dados(st.session_state.db)
        except: 
            pass

    for idx, item in enumerate(st.session_state.db["programacao"]):
        uid = item["id"]
        c = st.columns([2, 3, 2, 1, 0.5, 0.5, 0.5])
        
        c[0].text_input("Locação", value=item["Locação"], key=f"l_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Locação", f"l_{uid}"))
        c[1].text_input("Etapa", value=item["Etapa"], key=f"e_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Etapa", f"e_{uid}"))
        c[2].text_input("Resp", value=item["Responsável"], key=f"r_{uid}", label_visibility="collapsed", on_change=atualizar_campo, args=(idx, "Responsável", f"r_{uid}"))
        c[3].text_input("Tempo", value=f"{item['Horas']:02d}:{item['Minutos']:02d}", key=f"t_{uid}", label_visibility="collapsed", on_change=atualizar_tempo, args=(idx, f"t_{uid}"))
        
        if c[4].button("⬆️", key=f"up_{uid}") and idx > 0:
            st.session_state.db["programacao"][idx], st.session_state.db["programacao"][idx-1] = st.session_state.db["programacao"][idx-1], st.session_state.db["programacao"][idx]
            salvar_dados(st.session_state
