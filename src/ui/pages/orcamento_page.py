"""
ORCAMENTO PAGE
Gerenciamento de orçamento de materiais.
"""

import streamlit as st
from src.ui.styles import load_css
from src.services.orcamento_service import OrcamentoService
from src.services.obra_service import ObraService

def render():
    """Renderiza página de orçamento."""
    load_css()
    
    st.markdown("<div class='title'>💰 Orçamento de Materiais</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Pesquise preços e gerencie materiais</div>", unsafe_allow_html=True)
    
    obra_service = ObraService()
    orcamento_service = OrcamentoService()
    
    obras = obra_service.listar_obras()
    if not obras:
        st.error("❌ Crie uma obra primeiro!")
        return
    
    obras_nomes = {o.id: o.nome for o in obras}
    id_obra_selecionada = st.selectbox(
        "Selecione a obra",
        options=list(obras_nomes.keys()),
        format_func=lambda x: obras_nomes[x],
        key="orcamento_obra"
    )
    
    aba1, aba2 = st.tabs(["➕ Adicionar Material", "📋 Listar"])
    
    # ABA 1: ADICIONAR MATERIAL
    with aba1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            material = st.text_input("🔨 Material", placeholder="Ex: cimento, brita, areia")
            quantidade = st.number_input("📦 Quantidade", min_value=1.0, step=1.0)
        
        with col2:
            unidade = st.selectbox("📐 Unidade", ["un", "kg", "sacos", "m²", "m³", "L"])
            preco_unitario = st.number_input("💵 Preço Unitário (R$)", min_value=0.0, step=0.01)
        
        loja = st.text_input("🏪 Loja", placeholder="Ex: Casa do Construtor")
        observacoes = st.text_area("📝 Observações", height=80)
        
        if st.button("➕ Adicionar", use_container_width=True):
            if material and quantidade and preco_unitario:
                orcamento = orcamento_service.adicionar_material(
                    id_obra=id_obra_selecionada,
                    material=material,
                    quantidade=quantidade,
                    unidade=unidade,
                    preco_unitario=preco_unitario,
                    loja=loja,
                    observacoes=observacoes,
                )
                st.success(f"✅ Material '{material}' adicionado!")
                st.rerun()
            else:
                st.error("❌ Preencha os campos obrigatórios!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ABA 2: LISTAR
    with aba2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        materiais = orcamento_service.listar_por_obra(id_obra_selecionada)
        total = orcamento_service.calcular_total_obra(id_obra_selecionada)
        
        if not materiais:
            st.info("Nenhum material adicionado ainda")
        else:
            # Tabela
            dados = []
            for mat in materiais:
                dados.append({
                    "Material": mat.material,
                    "Qty": f"{mat.quantidade} {mat.unidade}",
                    "Preço Unit.": f"R$ {mat.preco_unitario:.2f}",
                    "Total": f"R$ {mat.preco_total:.2f}",
                    "Loja": mat.loja or "-",
                })
            
            st.dataframe(dados, use_container_width=True, hide_index=True)
            
            # Total
            st.metric("💰 Total da Obra", f"R$ {total:.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
