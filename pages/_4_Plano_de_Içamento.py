import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
import datetime
import json

# ==========================================
# 0. CONFIGURAÇÃO E LOGO NO MENU
# ==========================================
st.set_page_config(page_title="Plano de Içamento | Subsea Planner Pro", page_icon="⚓", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "pages" in current_dir else current_dir
sidebar_logo_path = os.path.join(root_dir, "image_c889bf.png")

if os.path.exists(sidebar_logo_path):
    with open(sidebar_logo_path, "rb") as f:
        sidebar_logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: ""; display: block;
            background-image: url("data:image/png;base64,{sidebar_logo_b64}");
            background-size: contain; background-repeat: no-repeat;
            background-position: center; height: 70px; margin: 20px 15px 10px 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

AKOFS_RED = "#D32F2F"
st.markdown(f"<h1 style='color: {AKOFS_RED};'>Subsea Planner Pro</h1>", unsafe_allow_html=True)
st.markdown("### Plano de Içamento de Cargas Submarinas (Lift Plan)")

# ==========================================
# 1. GESTÃO DE DADOS DA QUINZENA
# ==========================================
ARQUIVO_INVENTARIO = "inventario_quinzena.json"

def carregar_inventario():
    if os.path.exists(ARQUIVO_INVENTARIO):
        try:
            with open(ARQUIVO_INVENTARIO, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {
        "acessorios": [
            "Cinta 4m x 10T", "Cinta 6m x 10T", "Cinta 4m (8 dobrada) x 10T", 
            "Cinta 7m x 40T", "Cinta 3m x 1T (Aduchada)", "Cinta 4m x 2T (Aduchada)"
        ],
        "ferragens": [
            "Manilha 8.5T", "Manilha 12T", "Manilha 17T", "Manilha de ROV 55T",
            "Nautillus 10T", "Nautillus 22T", "Master Link 26T"
        ]
    }

def salvar_inventario(dados):
    with open(ARQUIVO_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if 'inventario' not in st.session_state:
    st.session_state.inventario = carregar_inventario()

# ==========================================
# ABAS DE NAVEGAÇÃO
# ==========================================
tab_plano, tab_config = st.tabs(["🏗️ Criar Plano de Içamento", "⚙️ Configuração da Quinzena (Inventário)"])

# --- ABA 2: CONFIGURAÇÃO DA QUINZENA ---
with tab_config:
    st.markdown("### Gestão de Acessórios a Bordo")
    st.write("Edite os itens disponíveis para esta quinzena. Isso servirá como referência para a montagem.")
    
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.subheader("Cintas e Eslingas")
        df_cintas = pd.DataFrame({"Item": st.session_state.inventario["acessorios"]})
        edit_cintas = st.data_editor(df_cintas, num_rows="dynamic", use_container_width=True, key="edit_cintas")
    
    with col_i2:
        st.subheader("Ferragens (Manilhas, Master Links, etc)")
        df_ferragens = pd.DataFrame({"Item": st.session_state.inventario["ferragens"]})
        edit_ferragens = st.data_editor(df_ferragens, num_rows="dynamic", use_container_width=True, key="edit_ferragens")

    if st.button("💾 Salvar Inventário da Quinzena"):
        st.session_state.inventario["acessorios"] = edit_cintas["Item"].dropna().tolist()
        st.session_state.inventario["ferragens"] = edit_ferragens["Item"].dropna().tolist()
        salvar_inventario(st.session_state.inventario)
        st.success("Inventário atualizado com sucesso!")

# --- ABA 1: PLANO DE IÇAMENTO ---
with tab_plano:
    # 2. DADOS GERAIS
    st.markdown("#### 📋 1. Informações da Carga e Locação")
    col1, col2, col3, col4 = st.columns(4)
    data_op = col1.date_input("Data da Operação", datetime.date.today())
    locacao = col2.text_input("Locação (Ex: 7-MRO-38-RJS)", value="")
    equipamento = col3.text_input("Equipamento", value="ANM AS-300")
    peso_ar = col4.number_input("Peso no Ar (ton)", min_value=0.0, value=37.6, step=0.1)

    col5, col6, col7 = st.columns(3)
    lda = col5.number_input("Lâmina D'água - LDA (m)", min_value=0, value=1500, step=50)
    prof_inspecao = col6.number_input("Prof. de Inspeção ROV (m)", min_value=0, value=1450, step=50)
    vel_descida = col7.text_input("Velocidade de Descida", value="20 a 30 m/min")

    st.divider()

    # 3. ESPECIFICAÇÃO DO GUINDASTE
    st.markdown("#### 🏗️ 2. Especificação do Guindaste")
    col_g1, col_g2 = st.columns(2)
    guincho_sel = col_g1.radio("Guincho Selecionado", ["Principal (AHC-250T)", "Auxiliar (AHC-20T)"], horizontal=True)

    def calcular_capacidade_lda(guincho, lda_val):
        if "Principal" in guincho:
            if lda_val <= 1: return 190.0
            elif lda_val <= 1000: return 220.0
            elif lda_val <= 1500: return 230.0
            elif lda_val <= 2000: return 221.0
            else: return 199.0
        else:
            if lda_val <= 500: return 20.0
            elif lda_val <= 1000: return 18.0
            elif lda_val <= 1500: return 15.0
            elif lda_val <= 2000: return 12.0
            else: return 9.0

    cap_lda = calcular_capacidade_lda(guincho_sel, lda)
    col_g2.metric(f"Capacidade do Guincho na LDA de {lda}m", f"{cap_lda} ton")

    st.divider()

    # 4. CONSTRUTOR DINÂMICO DE LINGADA E DESENHO
    st.markdown("#### 🔗 3. Arranjo de Içamento (Construtor 100% Flexível)")
    st.write("Digite os componentes do arranjo (de cima para baixo). Você pode adicionar, excluir ou editar as linhas como preferir clicando na tabela.")
    
    # Inicializa ou carrega um arranjo em branco
    if 'df_lingada' not in st.session_state:
        st.session_state.df_lingada = pd.DataFrame({
            "Componentes do Arranjo": ["Moitão Principal", "Cinta 7m x 40T", "Manilha de ROV 55T", "Conexão na Carga"]
        })

    # Botões para carregar templates rápidos
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("🔄 Carregar Template: Guincho Principal"):
        st.session_state.df_lingada = pd.DataFrame({"Componentes do Arranjo": ["Moitão Principal (250T)", "Cinta 7m x 40T", "Manilha de ROV 55T", "Conexão na Carga"]})
        st.rerun()
    if col_btn2.button("🔄 Carregar Template: Guincho Auxiliar"):
        st.session_state.df_lingada = pd.DataFrame({"Componentes do Arranjo": ["Moitão Auxiliar (20T)", "Cinta 6m x 10T", "Manilha 12T", "Nautillus 10T", "Costura na Carga"]})
        st.rerun()

    col_l1, col_l2 = st.columns([1.5, 1])
    
    with col_l1:
        # Data Editor totalmente livre para digitação
        df_editado = st.data_editor(
            st.session_state.df_lingada, 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Componentes do Arranjo": st.column_config.TextColumn("Descrição do Componente (Edite ou Adicione)")
            }
        )
    
    with col_l2:
        # Motor de Desenho Realista (Plotly)
        fig = go.Figure()
        y_pos = 10
        passo_y = 2
        
        itens_lingada = df_editado["Componentes do Arranjo"].dropna().tolist()
        
        for i, item in enumerate(itens_lingada):
            nome_upper = str(item).upper()
            if "MOITÃO" in nome_upper or "BLOCO" in nome_upper:
                fig.add_trace(go.Scatter(x=[0], y=[y_pos], mode="markers+text", marker=dict(symbol="triangle-down", size=30, color="#D32F2F"), text=[item], textposition="middle right", name=item))
            elif "CINTA" in nome_upper or "ESLINGA" in nome_upper:
                fig.add_trace(go.Scatter(x=[0, 0], y=[y_pos+passo_y/2, y_pos-passo_y], mode="lines", line=dict(color="orange", width=5), name=item))
                fig.add_trace(go.Scatter(x=[0], y=[y_pos - passo_y/2], mode="text", text=[item], textposition="middle right", showlegend=False))
            elif "MANILHA" in nome_upper or "NAUTILLUS" in nome_upper or "LINK" in nome_upper:
                fig.add_trace(go.Scatter(x=[0], y=[y_pos], mode="markers+text", marker=dict(symbol="circle-open", size=20, color="gray", line=dict(width=4)), text=[item], textposition="middle right", name=item))
            else:
                fig.add_trace(go.Scatter(x=[0], y=[y_pos], mode="markers+text", marker=dict(symbol="diamond", size=15, color="blue"), text=[item], textposition="middle right", name=item))
            
            y_pos -= passo_y

        # Desenha a Carga no final
        y_pos -= 1
        fig.add_trace(go.Scatter(
            x=[0], y=[y_pos], mode="markers+text", 
            marker=dict(symbol="square", size=50, color="#262a3d", line=dict(color="#D32F2F", width=3)), 
            text=[f"CARGA: {equipamento}"], textposition="bottom center", textfont=dict(size=14, color="black"), name="Carga"
        ))

        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2, 5]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500, margin=dict(l=0, r=0, t=30, b=0),
            plot_bgcolor="white", title="Diagrama Estrutural do Arranjo"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 5. CHECKLIST PARA EXECUÇÃO NO CONVÉS
    st.markdown("#### ✅ 4. Verificação Pré-Içamento (Checklist Físico)")
    st.info("⚠️ Estes itens não devem ser marcados aqui. Eles serão exportados com espaços em branco `[ ]` para que a equipe de convés realize a checagem e assinatura no momento da operação.")
    
    st.markdown("""
    - [  ] Instalar contrapino na farpela da bola / bloco
    - [  ] Instalar contrapino nas manilhas da lingada de içamento
    - [  ] Conferir manilhas Subsea na posição travada
    - [  ] Transponder Instalado
    - [  ] Equipe do ROV verificou o arranjo de içamento
    - [  ] Gancho ou manilhas de manuseio ROV inspecionadas
    """)

    # 6. MOTOR DE EXPORTAÇÃO
    texto_exportacao = f"""=========================================================
       PLANO DE IÇAMENTO DE CARGAS SUBMARINAS
                 SUBSEA LIFT PLAN
=========================================================
DATA DA OPERAÇÃO : {data_op.strftime('%d/%m/%Y')}
NAVIO            : AKOFS SANTOS
EQUIPAMENTO      : {equipamento}
LOCAÇÃO          : {locacao}

---------------------------------------------------------
1. DADOS DA CARGA E GUINDASTE
---------------------------------------------------------
Peso no Ar       : {peso_ar} ton
Lâmina D'água    : {lda} m
Prof. Inspeção   : {prof_inspecao} m
Velocidade       : {vel_descida}
Guincho Usado    : {guincho_sel}
Capacidade Permit: {cap_lda} ton na LDA atual

---------------------------------------------------------
2. ARRANJO DA LINGADA (De Cima para Baixo)
---------------------------------------------------------
"""
    for i, item in enumerate(itens_lingada):
        texto_exportacao += f"{i+1}. {item}\n"
        
    texto_exportacao += f"""
---------------------------------------------------------
3. CHECKLIST OPERACIONAL (Verificação Física)
---------------------------------------------------------
[  ] Instalar contrapino na farpela da bola / bloco
[  ] Instalar contrapino nas manilhas da lingada de içamento
[  ] Conferir manilhas Subsea na posição travada
[  ] Transponder Instalado
[  ] Equipe do ROV verificou o arranjo de içamento
[  ] Gancho ou manilhas de manuseio ROV inspecionadas

OBS: Durante os últimos 100 metros de descida, o operador do 
guindaste deve comunicar ao SSE a profundidade a cada 10m.

Aprovado por: _________________________ (Líder de Convés)
Aprovado por: _________________________ (SSE)
Aprovado por: _________________________ (ROV Sup)
Aprovado por: _________________________ (Op. Guindaste)
=========================================================
"""

    st.download_button(
        label="💾 Exportar Lift Plan (Relatório TXT)",
        data=texto_exportacao,
        file_name=f"Lift_Plan_{equipamento.replace(' ', '_')}.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )
