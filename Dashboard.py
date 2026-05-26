import streamlit as st
from PIL import Image
import os

# ==========================================
# 1. CONFIGURAÇÃO E ESTILO GLOBAL
# ==========================================
st.set_page_config(
    page_title="Dashboard | Subsea Planner Pro", 
    page_icon="⚓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores Corporativas AKOFS
AKOFS_RED = "#D32F2F"

# CSS para imposição visual e padronização
st.markdown(f"""
    <style>
    /* Títulos Principais */
    h1 {{
        color: {AKOFS_RED} !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
    }}
    h2, h3 {{
        font-weight: 700 !important;
        color: #f0f2f6 !important;
    }}
    /* Estilização dos Cartões dos Módulos */
    .modulo-card {{
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {AKOFS_RED};
        margin-bottom: 20px;
        transition: transform 0.2s;
    }}
    .modulo-card:hover {{
        transform: translateY(-5px);
        background-color: #262a3d;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGO NO TOPO DA SIDEBAR (CORRIGIDO)
# ==========================================
# Captura o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Define o caminho para o arquivo JPG correto
logo_path = os.path.join(current_dir, "image_c88946.jpg")

# Tenta carregar a imagem JPG
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    # Exibe no topo da sidebar
    st.sidebar.image(logo, use_container_width=True)
else:
    # Fallback caso a imagem não seja encontrada
    st.sidebar.markdown(f"<h2 style='text-align: center; color: {AKOFS_RED};'>🔴 AKOFS Offshore</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação Principal")

# ==========================================
# 3. CONTEÚDO IMPONENTE DO DASHBOARD
# ==========================================

# Cabeçalho Principal
st.title("Subsea Planner Pro")
st.subheader("Central de Gestão Integrada | AKOFS Offshore")
st.write(f"Bem-vinda, **Thaís**. Selecione um módulo abaixo ou utilize o menu lateral para iniciar.")

st.divider()

# --- LAYOUT DE MÓDULOS EM CARTÕES VISUAIS ---
st.markdown("## 🛠️ Módulos de Operação")

# Criação de 3 colunas para os cartões
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="modulo-card">
            <h3>⏱️ Cronograma de Prontidão</h3>
            <p>Planejamento detalhado de etapas operacionais, cálculo automático de tempos e previsão de prontidão de equipamentos subsea.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Cronograma", key="btn_cron", use_container_width=True):
        # Substitua pelo caminho real se necessário
        st.switch_page("pages/1_Cronograma_de_Prontidao.py") 

with col2:
    st.markdown(f"""
        <div class="modulo-card">
            <h3>📜 Gestão de PTW</h3>
            <p>Controle centralizado de Permissões de Trabalho (PTW). Monitore status, validades e garanta conformidade com as normas de segurança.</p>
        </div>
    """, unsafe_allow_html=True)
    # Desabilitado até que o módulo exista
    st.button("Módulo em Desenvolvimento", key="btn_ptw", use_container_width=True, disabled=True)

with col3:
    st.markdown(f"""
        <div class="modulo-card">
            <h3>📊 KPIs Operacionais</h3>
            <p>Visualização em tempo real dos principais indicadores de performance (NPT, eficiência de ROV, tempos de manuseio). </p>
        </div>
    """, unsafe_allow_html=True)
    # Desabilitado até que o módulo exista
    st.button("Módulo em Desenvolvimento", key="btn_kpi", use_container_width=True, disabled=True)

st.divider()

# --- SEÇÃO DE STATUS RÁPIDO ---
st.markdown("## 📈 Status da Frota")
c_stat1, c_stat2, c_stat3 = st.columns(3)

with c_stat1:
    st.metric(label="Status do Sistema", value="Online", delta="Operacional")
with c_stat2:
    st.metric(label="Módulos Ativos", value="1 / 3", delta="-2 em desenvolvimento")
with c_stat3:
    st.write("Última atualização de dados: **Hoje, 06:00**")
    st.write(f"Versão: **2026.1**")
