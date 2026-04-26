"""
HOME PAGE
Página inicial da aplicação.
"""

import streamlit as st
from src.ui.styles import load_css

def render():
    """Renderiza página inicial."""
    load_css()
    
    st.markdown("<div class='title'>🏗️ IAOBRA - Mestre Digital</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sua plataforma de acompanhamento de obras com IA</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>📊 Obras Ativas</h3>", unsafe_allow_html=True)
        st.metric("Total", "0", "Em andamento")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>📓 Registros Hoje</h3>", unsafe_allow_html=True)
        st.metric("Total", "0", "Últimas 24h")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>💰 Orçamento</h3>", unsafe_allow_html=True)
        st.metric("Investido", "R$ 0,00", "Fase 1")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""
    <h3>👋 Bem-vindo!</h3>
    <p>Esta é a Fase 1 do IAObras - CRUD básico e diário digital.</p>
    <p><strong>Próximos passos:</strong></p>
    <ul>
        <li>✅ Criar sua primeira obra</li>
        <li>📓 Registrar atividades diárias</li>
        <li>💰 Gerenciar orçamento de materiais</li>
        <li>♻️ Listar sobras para venda</li>
    </ul>
    <p>Fases futuras: Mídia (2), IA (3), Timeline (4), VR/AR (5), MCLLM (6)</p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
