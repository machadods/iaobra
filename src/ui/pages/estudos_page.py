"""
ESTUDOS PAGE
Formação para mestres (com IA - Fase 3+).
"""

import streamlit as st
from src.ui.styles import load_css

def render():
    """Renderiza página de estudos."""
    load_css()
    
    st.markdown("<div class='title'>📚 Estudar – Formação para Mestres</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Escolha um curso ou faça uma pergunta para a IA</div>", unsafe_allow_html=True)
    
    col_chat, col_menu = st.columns([2, 1], gap="large")
    
    with col_chat:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.info("💡 IA de Estudos será implementada na Fase 3")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_menu:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>📘 Cursos Disponíveis</h3>", unsafe_allow_html=True)
        
        cursos = [
            "📐 Cálculo de Materiais",
            "🧱 Reboco e Acabamento",
            "⚒️ Segurança no Trabalho",
            "🏗️ Organização do Canteiro",
            "🔌 Instalações Elétricas",
            "🚰 Hidráulica Essencial",
            "🪵 Carpintaria para Iniciantes",
        ]
        
        for curso in cursos:
            st.markdown(f"<div class='btn'>{curso}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
