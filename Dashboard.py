# ==========================================
# 4. MÓDULOS HABILITADOS (AJUSTADO)
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="modulo-card">
            <h2>⏱️</h2>
            <h3>Cronograma de Prontidão</h3>
            <p>Gerenciamento de etapas operacionais e previsões de prontidão.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Cronograma", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Cronograma_de_Prontidao.py")

with col2:
    st.markdown("""
        <div class="modulo-card">
            <h2>🔏</h2>
            <h3>Validação de Seal Test</h3>
            <p>Conferência técnica e validação de testes de vedação subsea.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Seal Test", use_container_width=True):
        st.switch_page("pages/2_Validacao_de_Seal_Test.py")

with col3:
    st.markdown("""
        <div class="modulo-card">
            <h2>⚙️</h2>
            <h3>Simulador Tático de Clash</h3>
            <p>Simulação de cenários e tempos operacionais críticos.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Acessar Simulador", use_container_width=True):
        st.switch_page("pages/3_Simulador_Tatico_de_Clash.py")
