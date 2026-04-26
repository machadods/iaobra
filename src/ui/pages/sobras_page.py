"""
SOBRAS PAGE
Mercado de sobras.
"""

import streamlit as st
from src.ui.styles import load_css
from src.services.sobras_service import SobrasService
from src.services.obra_service import ObraService

def render():
    """Renderiza página de sobras."""
    load_css()
    
    st.markdown("<div class='title'>♻️ Mercado de Sobras</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Venda materiais que sobraram e ganhe renda extra</div>", unsafe_allow_html=True)
    
    obra_service = ObraService()
    sobras_service = SobrasService()
    
    obras = obra_service.listar_obras()
    if obras:
        obras_nomes = {o.id: o.nome for o in obras}
        id_obra = st.selectbox(
            "Selecione a obra",
            options=list(obras_nomes.keys()),
            format_func=lambda x: obras_nomes[x],
            key="sobras_obra"
        )
    else:
        id_obra = None
    
    aba1, aba2 = st.tabs(["📤 Publicar Sobra", "🛒 Marketplace"])
    
    # ABA 1: PUBLICAR
    with aba1:
        if not id_obra:
            st.error("❌ Crie uma obra primeiro!")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            material = st.text_input("📦 Item", placeholder="Ex: 12 pisos 60x60, tinta branca 3L")
            descricao = st.text_area("📝 Descrição", height=80)
            
            col1, col2 = st.columns(2)
            with col1:
                quantidade = st.number_input("Quantidade", min_value=1.0, step=1.0)
                unidade = st.selectbox("Unidade", ["un", "m²", "m³", "kg", "L"])
            with col2:
                preco = st.number_input("💰 Preço (R$)", min_value=0.0, step=0.01)
                vendedor = st.text_input("Seu nome", placeholder="")
            
            foto = st.file_uploader("📸 Foto do item", type=["jpg", "png"])
            
            if st.button("📤 Publicar", use_container_width=True):
                if material and quantidade and preco:
                    sobra = sobras_service.publicar_sobra(
                        id_obra=id_obra,
                        material=material,
                        quantidade=quantidade,
                        unidade=unidade,
                        preco=preco,
                        descricao=descricao,
                        foto=None,  # TODO: Implementar upload
                        vendedor=vendedor,
                    )
                    st.success("✅ Sobra publicada!")
                    st.rerun()
                else:
                    st.error("❌ Preencha os campos obrigatórios!")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ABA 2: MARKETPLACE
    with aba2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Pesquisa
        col1, col2 = st.columns([3, 1])
        with col1:
            pesquisa = st.text_input("🔍 Pesquisar material")
        with col2:
            st.write("")
            ordenar = st.selectbox("Ordenar", ["Preço (menor)", "Preço (maior)", "Recente"])
        
        sobras = sobras_service.listar_disponiveis()
        
        if pesquisa:
            sobras = [s for s in sobras if pesquisa.lower() in s.material.lower()]
        
        if not sobras:
            st.info("Nenhuma sobra disponível")
        else:
            # Exibir em grid
            cols = st.columns(3)
            for idx, sobra in enumerate(sobras):
                with cols[idx % 3]:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.write(f"**{sobra.material}**")
                    st.caption(f"{sobra.quantidade} {sobra.unidade}")
                    st.metric("Preço", f"R$ {sobra.preco:.2f}")
                    st.write(sobra.descricao[:100] + "...")
                    if st.button("ℹ️ Detalhes", key=f"sobra_{sobra.id}"):
                        st.session_state.sobra_selecionada = sobra.id
                    st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
