"""
DIARIO PAGE
Registros diários de obra.
"""

import streamlit as st
from datetime import date
from src.ui.styles import load_css
from src.services.diario_service import DiarioService
from src.services.obra_service import ObraService

def render():
    """Renderiza página de diário."""
    load_css()
    
    st.markdown("<div class='title'>📓 Diário da Obra</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Registre o que aconteceu hoje de forma rápida e visual</div>", unsafe_allow_html=True)
    
    obra_service = ObraService()
    diario_service = DiarioService()
    
    # Selecionar obra
    obras = obra_service.listar_obras()
    if not obras:
        st.error("❌ Crie uma obra primeiro!")
        return
    
    obras_nomes = {o.id: o.nome for o in obras}
    id_obra_selecionada = st.selectbox(
        "Selecione a obra",
        options=list(obras_nomes.keys()),
        format_func=lambda x: obras_nomes[x]
    )
    
    # Abas
    aba1, aba2 = st.tabs(["📝 Novo Registro", "📜 Histórico"])
    
    # ABA 1: NOVO REGISTRO
    with aba1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        registro_texto = st.text_area(
            "📝 Registro",
            placeholder="Exemplo:\n• Rebocamos a sala\n• Chegaram 12 sacos de cimento\n• A equipe finalizou o contrapiso"
        )
        
        foto = st.file_uploader("📸 Foto do dia", type=["jpg", "png"])
        video = st.file_uploader("🎥 Vídeo (opcional)", type=["mp4", "avi"])
        audio = st.file_uploader("🎤 Áudio (opcional)", type=["mp3", "wav"])
        
        if st.button("💾 Salvar Registro", use_container_width=True):
            if registro_texto.strip():
                # TODO: Processar uploads de mídia
                diario = diario_service.criar_registro(
                    id_obra=id_obra_selecionada,
                    registro_texto=registro_texto,
                    fotos=[],  # TODO: Implementar upload
                    videos=[],
                    audio=None,
                )
                st.success("✅ Registro salvo com sucesso!")
                st.rerun()
            else:
                st.error("❌ Escreva um registro!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ABA 2: HISTÓRICO
    with aba2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        registros = diario_service.listar_por_obra(id_obra_selecionada)
        
        if not registros:
            st.info("Nenhum registro para esta obra")
        else:
            for reg in reversed(registros):
                with st.expander(f"📅 {reg.data_registro.strftime('%d/%m/%Y')}"):
                    st.write(reg.registro_texto)
        
        st.markdown("</div>", unsafe_allow_html=True)
