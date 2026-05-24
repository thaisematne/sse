st.divider()

# ==========================================
# MÓDULO 2: ANÁLISE DE PRESSÕES
# ==========================================
st.title("Módulo 2: Análise de Pressões (PE-2SUB-00406)")

tab1, tab2, tab3 = st.tabs(["Pressão Hidrostática", "Pressão Máxima de Teste", "Teste de Estanqueidade"])

# --- TAB 1: Pressão Hidrostática ---
with tab1:
    st.subheader("Cálculo de Pressão Hidrostática (PLDA)")
    st.info("Fator de conversão prático baseado no documento: 2000 m = 2940 psi (Fator ~ 1.47 psi/m).")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        profundidade = st.number_input("Lâmina D'água - LDA (m)", min_value=0.0, value=2000.0, step=10.0)
    with col_p2:
        fator_densidade = st.number_input("Fator de Conversão (psi/m)", value=1.47, step=0.01)
        
    pressao_hidrostatica = profundidade * fator_densidade
    st.metric("Pressão Hidrostática Resultante", f"{pressao_hidrostatica:.2f} psi")

# --- TAB 2: Pressão Máxima de Teste ---
with tab2:
    st.subheader("Pressão Máxima de Teste na HPU")
    st.latex(r"P_{MAX} \le RWP - PLDA")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        rwp = st.number_input("RWP do Equipamento (psi)", min_value=0.0, value=5000.0, step=100.0)
    with col_t2:
        plda = st.number_input("Pressão Hidrostática (PLDA) em psi", min_value=0.0, value=float(pressao_hidrostatica), step=10.0)
        
    p_max = rwp - plda
    st.metric("Pressão Máxima Permitida na HPU", f"{p_max:.2f} psi")

# --- TAB 3: Teste de Estanqueidade ---
with tab3:
    st.subheader("Critérios de Aceitação de Teste de Estanqueidade")
    
    p_teste = st.number_input("Pressão Nominal de Teste (psi)", min_value=1.0, value=5000.0, step=100.0)
    
    st.markdown("### Leitura dos Ciclos de Pressão")
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        p_0 = st.number_input("Pressão Inicial (0 min)", value=float(p_teste + 200), step=1.0)
    with col_e2:
        p_5 = st.number_input("Pressão aos 5 min", value=float(p_0 - 15), step=1.0)
    with col_e3:
        p_10 = st.number_input("Pressão aos 10 min (Preencher se solicitado)", value=float(p_5 - 5), step=1.0)
        
    st.markdown("### Histórico da Operação")
    primeiro_ciclo = st.checkbox("Este é o primeiro ciclo de pressurização (Não há ciclo anterior para comparar)", value=True)
    
    queda_ciclo_anterior = 0.0
    if not primeiro_ciclo:
        queda_ciclo_anterior = st.number_input("Taxa de Queda no Ciclo Anterior (psi/5min)", min_value=0.0, value=50.0, step=1.0)

    if st.button("Analisar Estanqueidade (Gerar Diagnóstico)"):
        queda_5min = p_0 - p_5
        queda_10min = p_5 - p_10
        
        limite_042 = p_teste * 0.0042
        limite_063 = p_teste * 0.0063
        
        st.write("---")
        st.write(f"**Análise dos primeiros 5 minutos:**")
        st.write(f"Queda real: **{queda_5min:.1f} psi** | Limite 0,42%: **{limite_042:.1f} psi** | Limite 0,63%: **{limite_063:.1f} psi**")
        
        # Lógica do Fluxograma da Petrobras
        condicao_queda_042 = queda_5min <= limite_042
        condicao_taxa_menor_anterior = primeiro_ciclo or (queda_5min < queda_ciclo_anterior)
        
        if condicao_queda_042 and condicao_taxa_menor_anterior:
            st.success("✅ 1ª Etapa (5 min) Aprovada: Queda $\le 0,42\%$ e taxa decrescente. Analisando os 5 minutos finais...")
            
            st.write(f"**Análise dos 5 minutos finais (5 a 10 min):**")
            st.write(f"Queda real: **{queda_10min:.1f} psi**")
            
            if queda_10min <= limite_042:
                if queda_10min < queda_5min:
                    st.success("🏆 **TESTE APROVADO!** Taxa de queda final é decrescente e encontra-se dentro do limite exigido.")
                else:
                    st.error("❌ **TESTE REPROVADO!** A taxa de queda nos 5 minutos finais não foi decrescente em relação aos 5 primeiros minutos.")
            else:
                st.error("❌ **TESTE REPROVADO!** A queda nos 5 minutos finais ultrapassou o limite de $0,42\%$.")
                
        else:
            st.warning("⚠️ Queda inicial maior que $0,42\%$ ou taxa não foi menor que a do ciclo anterior. Direcionando para avaliação secundária...")
            
            condicao_queda_063 = queda_5min < limite_063
            
            if condicao_queda_063:
                if condicao_taxa_menor_anterior:
                    st.info("🔄 **AÇÃO REQUERIDA: REPRESSURIZAR!** A queda é $< 0,63\%$ e a taxa é menor que a do ciclo anterior. Efetue repressurização e inicie um novo ciclo.")
                else:
                    st.error("❌ **TESTE REPROVADO!** A taxa de queda não é menor que a do ciclo anterior.")
            else:
                st.error("❌ **TESTE REPROVADO!** A queda nos primeiros 5 minutos é maior ou igual a $0,63\%$ da pressão de teste.")
