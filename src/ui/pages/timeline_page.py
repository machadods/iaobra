"""
TIMELINE PAGE
Simulador temporal da obra (Fase 4+).
"""

import streamlit as st
from src.ui.styles import load_css

def render():
    """Renderiza página de timeline."""
    load_css()
    
    st.markdown("<div class='title'>⏰ Simulador Temporal da Obra</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Viaje no tempo e reviva cada momento da construção</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.info("🚀 Simulador temporal será implementado na Fase 4")
    st.write("Fase 4 permitirá:")
    st.write("- 📺 Navegação visual por timeline")
    st.write("- 📸 Snapshots de cada fase da obra")
    st.write("- 🎥 Vídeo 360° de cada momento")
    st.write("- 🎬 Simulação acelerada do progresso")
    st.markdown("</div>", unsafe_allow_html=True)
