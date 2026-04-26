"""
CLIENTE PAGE
Dashboard somente leitura para o proprietário acompanhar a obra.
"""

import streamlit as st
from src.models.usuario import Usuario


def render_cliente_dashboard(usuario: Usuario, obra_service, diario_service, orcamento_service):
    st.markdown(f"## 👷 Acompanhamento da Obra — {usuario.nome}")
    st.markdown("*Você está no modo de visualização. Apenas o Mestre de Obras pode editar.*")
    st.divider()

    obras = obra_service.listar_obras()
    obras_permitidas = [o for o in obras if usuario.pode_ver_obra(o.id)]

    if not obras_permitidas:
        st.info("Nenhuma obra vinculada à sua conta ainda. Aguarde o Mestre de Obras configurar seu acesso.")
        return

    obra_nomes = {o.id: o.nome for o in obras_permitidas}
    obra_selecionada_id = st.selectbox(
        "Selecione a obra:",
        options=list(obra_nomes.keys()),
        format_func=lambda x: obra_nomes[x],
    )

    obra = obra_service.obter_obra(obra_selecionada_id)
    if not obra:
        return

    # --- Cabeçalho da obra ---
    col1, col2, col3 = st.columns(3)
    status_cor = {"em_andamento": "🟢", "paralisada": "🟡", "finalizada": "🔵"}.get(obra.status, "⚪")
    with col1:
        st.metric("Status", f"{status_cor} {obra.status.replace('_', ' ').title()}")
    with col2:
        st.metric("Mestre Responsável", obra.responsavel or "—")
    with col3:
        st.metric("Orçamento Total", f"R$ {obra.orcamento_total:,.2f}" if obra.orcamento_total else "—")

    st.markdown(f"📍 **Endereço:** {obra.endereco}")
    if obra.descricao:
        st.markdown(f"📋 **Descrição:** {obra.descricao}")

    st.divider()

    # --- Abas ---
    aba_diario, aba_orcamento = st.tabs(["📓 Diário da Obra", "💰 Orçamento"])

    with aba_diario:
        st.markdown("### Registros do Diário")
        entradas = diario_service.listar_por_obra(obra_selecionada_id)
        if not entradas:
            st.info("Nenhum registro ainda.")
        else:
            for entrada in reversed(entradas):
                with st.expander(f"📅 {entrada.data_registro or 'Sem data'}", expanded=False):
                    st.write(entrada.registro_texto or entrada.texto or "—")
                    if getattr(entrada, "fotos", None):
                        st.caption(f"📸 {len(entrada.fotos)} foto(s) anexada(s)")

    with aba_orcamento:
        st.markdown("### Orçamento da Obra")
        itens = orcamento_service.listar_por_obra(obra_selecionada_id)
        if not itens:
            st.info("Nenhum item no orçamento ainda.")
        else:
            total = sum(getattr(i, "preco_total", 0) or 0 for i in itens)
            st.metric("Total do Orçamento", f"R$ {total:,.2f}")
            for item in itens:
                st.markdown(
                    f"• **{item.material}** — {item.quantidade} {item.unidade} × R$ {item.preco_unitario:.2f} = **R$ {item.preco_total:.2f}**"
                )
