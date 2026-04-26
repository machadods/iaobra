"""
OBRAS PAGE
Gerenciamento de obras.
"""

import streamlit as st
from src.ui.styles import load_css
from src.services.obra_service import ObraService

def render():
    """Renderiza página de obras."""
    load_css()
    
    st.markdown("<div class='title'>🏗️ Minhas Obras</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Crie, atualize e acompanhe suas obras</div>", unsafe_allow_html=True)
    
    # Abas
    aba1, aba2, aba3 = st.tabs(["📋 Listar", "➕ Nova Obra", "📊 Estatísticas"])
    
    # Instanciar Service
    obra_service = ObraService()
    
    # ABA 1: LISTAR OBRAS
    with aba1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        obras = obra_service.listar_obras()
        
        if not obras:
            st.info("Nenhuma obra criada ainda. Acesse a aba 'Nova Obra' para começar!")
        else:
            for obra in obras:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{obra.nome}**")
                    st.caption(f"📍 {obra.endereco}")
                with col2:
                    st.write(f"Status: {obra.status}")
                with col3:
                    if st.button("Ver", key=f"ver_{obra.id}"):
                        st.session_state.obra_selecionada = obra.id
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ABA 2: CRIAR NOVA OBRA
    with aba2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        nome = st.text_input("📝 Nome da Obra", placeholder="Ex: Casa João Silva")
        endereco = st.text_input("📍 Endereço", placeholder="Rua, número, bairro, cidade")
        descricao = st.text_area("📄 Descrição", placeholder="Detalhes da obra")
        
        col1, col2 = st.columns(2)
        with col1:
            proprietario = st.text_input("👤 Proprietário")
        with col2:
            responsavel = st.text_input("👷 Responsável")
        
        orcamento_total = st.number_input("💰 Orçamento Total (R$)", min_value=0.0, step=1000.0)
        
        if st.button("Criar Obra", use_container_width=True):
            if nome and endereco:
                obra = obra_service.criar_obra(
                    nome=nome,
                    endereco=endereco,
                    descricao=descricao,
                    proprietario=proprietario,
                    responsavel=responsavel,
                    orcamento_total=orcamento_total,
                )
                st.success(f"✅ Obra '{obra.nome}' criada com sucesso!")
                st.rerun()
            else:
                st.error("❌ Preencha nome e endereço!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ABA 3: ESTATÍSTICAS
    with aba3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        obras = obra_service.listar_obras()
        
        if obras:
            em_andamento = len(obra_service.listar_por_status("em_andamento"))
            finalizadas = len(obra_service.listar_por_status("finalizada"))
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Obras", len(obras))
            col2.metric("Em Andamento", em_andamento)
            col3.metric("Finalizadas", finalizadas)
        else:
            st.info("Sem obras para exibir estatísticas")
        
        st.markdown("</div>", unsafe_allow_html=True)
