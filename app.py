"""
IAOBRA v0.2.0
Perfis: admin | construtor | cliente
"""

import streamlit as st
from style import load_css
from src.services.obra_service import ObraService
from src.services.auth_service import AuthService
from src.services.ia_service import IAService
from src.ui.pages.login_page import render_login
from src.utils.db_connection import db

st.set_page_config(page_title="IAOBRA", page_icon=None, layout="wide",
                   initial_sidebar_state="expanded")
load_css()

# ── Checagem de seguranca ─────────────────────────────────────────────
if "security_ok" not in st.session_state:
    from src.utils.security import checar_ambiente
    _alertas = checar_ambiente()
    st.session_state.security_alertas = _alertas
    st.session_state.security_ok = True

# ── Migrations — roda uma vez na subida ───────────────────────────────
if "migrations_ok" not in st.session_state:
    try:
        from database.migrate import rodar
        from config import DATABASE_URL
        novas = rodar(DATABASE_URL)
        if novas:
            st.toast(f"Banco atualizado: {', '.join(novas)}", icon=None)
        st.session_state.migrations_ok = True
    except Exception as _e:
        st.session_state.migrations_ok = False

# ── Limpa sessao antiga quando o codigo muda ──────────────────────────
_VERSAO_SESSAO = "0.2.0"
if st.session_state.get("_versao") != _VERSAO_SESSAO:
    for _k in list(st.session_state.keys()):
        del st.session_state[_k]
    st.session_state["_versao"] = _VERSAO_SESSAO
    st.rerun()

# ── Servicos ──────────────────────────────────────────────────────────
if "auth_service" not in st.session_state:
    st.session_state.auth_service = AuthService()
if "obra_service" not in st.session_state:
    st.session_state.obra_service = ObraService()
if "ia_service" not in st.session_state:
    st.session_state.ia_service = IAService()
if "creditos_service" not in st.session_state:
    from src.services.creditos_service import CreditosService
    st.session_state.creditos_service = CreditosService()
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

auth      = st.session_state.auth_service
ia        = st.session_state.ia_service
obras_svc = st.session_state.obra_service
cred_svc  = st.session_state.creditos_service

# ── Login ─────────────────────────────────────────────────────────────
if "usuario" not in st.session_state:
    render_login(auth)
    st.stop()

u = st.session_state.usuario

# ── Sidebar ───────────────────────────────────────────────────────────
tipo_label = {"admin": "Administrador", "construtor": "Construtor", "cliente": "Cliente"}.get(u.tipo, u.tipo)

st.sidebar.markdown(f"**IAOBRA**")
st.sidebar.markdown(f"{u.nome}")
if u.nome.strip().lower() != tipo_label.lower():
    st.sidebar.markdown(f"*{tipo_label}*")
st.sidebar.divider()

MENUS = {
    "admin": {
        "home":         "Inicio",
        "obras":        "Obras",
        "diario":       "Diario da Obra",
        "orcamento":    "Orcamento",
        "sobras":       "Mercado de Sobras",
        "estudos":      "Estudos com IA",
        "planos":       "Planos e Creditos",
        "admin_panel":  "Painel Admin",
        "contato":      "Fale Conosco",
    },
    "construtor": {
        "home":      "Inicio",
        "obras":     "Obras",
        "diario":    "Diario da Obra",
        "orcamento": "Orcamento",
        "sobras":    "Mercado de Sobras",
        "estudos":   "Estudos com IA",
        "planos":    "Planos e Creditos",
        "contato":   "Fale Conosco",
    },
    "cliente": {
        "home":        "Inicio",
        "acompanhar":  "Acompanhar Obra",
        "contato":     "Fale Conosco",
    },
}

menu = MENUS.get(u.tipo, MENUS["cliente"])
for key, label in menu.items():
    if st.sidebar.button(label, use_container_width=True, key=f"nav_{key}"):
        st.session_state.pagina = key
        st.rerun()

st.sidebar.divider()
# Saldo de creditos
if u.tipo != "admin":
    saldo = cred_svc.saldo(u.id)
    cor = "green" if saldo > 50 else "orange" if saldo > 10 else "red"
    st.sidebar.markdown(
        f"<div style='font-size:0.78rem;color:#475569;'>Creditos IA: "
        f"<strong style='color:{'#10b981' if saldo>50 else '#f59e0b' if saldo>10 else '#ef4444'};'>{saldo}</strong></div>",
        unsafe_allow_html=True,
    )
if ia.configurada:
    modelo_curto = ia.modelo_em_uso.split("/")[-1].replace(":free", "")
    st.sidebar.success(f"IA ativa — {modelo_curto}")
else:
    st.sidebar.warning("IA inativa — configure .env")

if st.sidebar.button("Sair", use_container_width=True, key="nav_sair"):
    del st.session_state.usuario
    st.session_state.pagina = "home"
    st.rerun()

st.sidebar.markdown(f"<small style='color:#1f2937;'>IAOBRA v0.2.0</small>", unsafe_allow_html=True)

# ── Roteamento ────────────────────────────────────────────────────────
pag = st.session_state.pagina


# ── HOME ──────────────────────────────────────────────────────────────
if pag == "home":
    if u.tipo in ("admin", "construtor"):
        obras = obras_svc.listar_obras()
        ativas = [o for o in obras if o.status == "em_andamento"]

        st.markdown('<div class="badge">Plataforma de obras com IA</div>', unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size:2rem;font-weight:800;color:#f1f5f9;margin:0.6rem 0 0.3rem 0;'>Ola, {u.nome}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#374151;font-size:0.9rem;margin-bottom:1.5rem;'>Gerencie obras, registre progresso e use a IA para analises automaticas.</p>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Obras ativas", len(ativas))
        c2.metric("Total de obras", len(obras))
        c3.metric("Clientes", len(auth.listar_clientes()))
        c4.metric("IA", "Ativa" if ia.configurada else "Inativa")

        if not ia.configurada:
            st.warning("Configure OPENROUTER_API_KEY no arquivo .env para ativar a IA.")
    else:
        st.markdown(f"<h2 style='color:#f1f5f9;'>Ola, {u.nome}</h2>", unsafe_allow_html=True)
        st.info("Use o menu lateral para acompanhar sua obra.")


# ── OBRAS ─────────────────────────────────────────────────────────────
elif pag == "obras" and u.tipo in ("admin", "construtor"):
    st.markdown("<h2 style='color:#f1f5f9;'>Obras</h2>", unsafe_allow_html=True)
    aba_nova, aba_lista = st.tabs(["Nova Obra", "Lista de Obras"])

    with aba_nova:
        with st.form("form_obra"):
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome da obra *")
                proprietario = st.text_input("Proprietario")
            with c2:
                endereco = st.text_input("Endereco *")
                responsavel = st.text_input("Mestre responsavel")
            descricao = st.text_area("Descricao da obra", height=100,
                                     placeholder="Quanto mais detalhada, melhor o cronograma gerado pela IA.")
            orcamento_total = st.number_input("Orcamento total (R$)", min_value=0.0, step=1000.0)

            st.markdown("---")
            st.markdown("<p style='color:#475569;font-size:0.82rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;'>Criar login do cliente agora (opcional)</p>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                cli_nome = st.text_input("Nome do cliente")
                cli_user = st.text_input("Usuario do cliente")
            with c4:
                cli_senha = st.text_input("Senha do cliente", type="password",
                                          help="Minimo 8 caracteres")

            criar = st.form_submit_button("Criar obra", use_container_width=True)

        if criar:
            if not nome or not endereco:
                st.error("Preencha nome e endereco.")
            else:
                obra = obras_svc.criar_obra(
                    nome=nome, endereco=endereco, proprietario=proprietario,
                    responsavel=responsavel, descricao=descricao,
                    orcamento_total=orcamento_total,
                )
                st.success(f"Obra '{obra.nome}' criada (ID: {obra.id}).")

                # Criar cliente inline se informado
                if cli_nome and cli_user and cli_senha:
                    try:
                        auth.criar_cliente(
                            nome=cli_nome, username=cli_user,
                            senha=cli_senha, obras_ids=[obra.id],
                        )
                        st.success(f"Cliente '{cli_nome}' criado. Login: {cli_user}")
                    except ValueError as e:
                        st.error(f"Erro ao criar cliente: {e}")
                elif any([cli_nome, cli_user, cli_senha]):
                    st.warning("Para criar o cliente, preencha nome, usuario e senha (min. 8 caracteres).")

                # Cronograma IA
                if descricao and ia.configurada:
                    with st.spinner("Gerando cronograma com IA..."):
                        cronograma = ia.gerar_cronograma(descricao, nome)
                    st.markdown("**Cronograma sugerido pela IA**")
                    st.markdown(cronograma)

    with aba_lista:
        obras = obras_svc.listar_obras()
        if not obras:
            st.info("Nenhuma obra cadastrada.")
        for o in obras:
            status_map = {"em_andamento": "Em andamento", "paralisada": "Paralisada", "finalizada": "Finalizada"}
            with st.expander(f"{o.nome} — {o.endereco}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Proprietario:** {o.proprietario or '—'}")
                    st.write(f"**Responsavel:** {o.responsavel or '—'}")
                with c2:
                    st.write(f"**Status:** {status_map.get(o.status, o.status)}")
                    st.write(f"**Orcamento:** R$ {o.orcamento_total:,.2f}")
                if o.descricao:
                    st.write(f"**Descricao:** {o.descricao}")


# ── DIARIO ────────────────────────────────────────────────────────────
elif pag == "diario" and u.tipo in ("admin", "construtor"):
    from src.services.diario_service import DiarioService
    if "diario_svc" not in st.session_state:
        st.session_state.diario_svc = DiarioService()
    diario_svc = st.session_state.diario_svc

    st.markdown("<h2 style='color:#f1f5f9;'>Diario da Obra</h2>", unsafe_allow_html=True)

    obras = obras_svc.listar_obras()
    if not obras:
        st.warning("Cadastre uma obra primeiro.")
        st.stop()

    obra_map = {o.id: o.nome for o in obras}
    obra_id = st.selectbox("Obra", options=list(obra_map.keys()), format_func=lambda x: obra_map[x])
    obra = obras_svc.obter_obra(obra_id)

    aba_reg, aba_hist = st.tabs(["Novo registro", "Historico"])

    with aba_reg:
        with st.form("form_diario"):
            texto = st.text_area("O que foi feito hoje? *", height=150,
                                 placeholder="Descreva atividades, materiais usados, equipe presente...")
            arquivos = st.file_uploader("Fotos / Videos / Audios",
                                        accept_multiple_files=True,
                                        type=["jpg","jpeg","png","mp4","mov","mp3","wav","ogg"])
            salvar = st.form_submit_button("Salvar registro", use_container_width=True)

        if salvar:
            if texto:
                entrada = diario_svc.criar_registro(id_obra=obra_id, registro_texto=texto)

                # Upload real para disco + tabela midia
                if arquivos and entrada.id:
                    from src.utils.file_handler import salvar_upload
                    salvos, erros = 0, 0
                    for arq in arquivos:
                        resultado = salvar_upload(arq, id_obra=obra_id, id_diario=entrada.id)
                        if resultado:
                            salvos += 1
                        else:
                            erros += 1
                    if salvos:
                        st.success(f"Registro salvo com {salvos} arquivo(s).")
                    if erros:
                        st.warning(f"{erros} arquivo(s) nao foram salvos (formato nao suportado).")
                else:
                    st.success("Registro salvo.")

                if ia.configurada:
                    with st.spinner("IA analisando o registro..."):
                        analise = ia.analisar_registro(texto, obra.nome, id_usuario=u.id)
                    st.markdown("**Analise da IA**")
                    st.markdown(analise)
                else:
                    st.info("Configure a IA no .env para receber analise automatica.")
            else:
                st.error("Escreva o registro antes de salvar.")

    with aba_hist:
        entradas = diario_svc.listar_por_obra(obra_id)
        if not entradas:
            st.info("Nenhum registro ainda.")
        else:
            if ia.configurada and st.button("Gerar resumo da obra com IA"):
                textos = [e.registro_texto or "" for e in entradas if e.registro_texto]
                with st.spinner("Gerando resumo..."):
                    resumo = ia.resumir_obra(textos, obra.nome)
                st.markdown("**Resumo executivo**")
                st.markdown(resumo)
                st.divider()
            from src.utils.file_handler import listar_midias_diario
            for e in reversed(entradas):
                data_fmt = str(e.data_registro)[:16] if e.data_registro else "Sem data"
                with st.expander(data_fmt):
                    st.write(getattr(e, "registro_texto", None) or "—")
                    midias = listar_midias_diario(e.id) if e.id else []
                    if midias:
                        fotos  = [m for m in midias if m["tipo"] == "foto"]
                        videos = [m for m in midias if m["tipo"] == "video"]
                        audios = [m for m in midias if m["tipo"] == "audio"]
                        if fotos:
                            cols = st.columns(min(len(fotos), 4))
                            for i, foto in enumerate(fotos):
                                with cols[i % 4]:
                                    try:
                                        st.image(foto["caminho"], width=180,
                                                 caption=foto["nome_arquivo"])
                                    except Exception:
                                        st.write(foto["nome_arquivo"])
                        for v in videos:
                            try:
                                st.video(v["caminho"])
                            except Exception:
                                st.write(f"Video: {v['nome_arquivo']}")
                        for a in audios:
                            try:
                                st.audio(a["caminho"])
                            except Exception:
                                st.write(f"Audio: {a['nome_arquivo']}")


# ── ORCAMENTO ─────────────────────────────────────────────────────────
elif pag == "orcamento" and u.tipo in ("admin", "construtor"):
    from src.services.orcamento_service import OrcamentoService
    if "orcamento_svc" not in st.session_state:
        st.session_state.orcamento_svc = OrcamentoService()
    orc_svc = st.session_state.orcamento_svc

    st.markdown("<h2 style='color:#f1f5f9;'>Orcamento</h2>", unsafe_allow_html=True)

    obras = obras_svc.listar_obras()
    if not obras:
        st.warning("Cadastre uma obra primeiro.")
        st.stop()

    obra_map = {o.id: o.nome for o in obras}
    obra_id = st.selectbox("Obra", options=list(obra_map.keys()), format_func=lambda x: obra_map[x])

    aba_add, aba_ver, aba_preco = st.tabs(["Adicionar item", "Orcamento", "Pesquisar preco com IA"])

    with aba_add:
        with st.form("form_orc"):
            c1, c2 = st.columns(2)
            with c1:
                mat = st.text_input("Material / servico *")
                qtd = st.number_input("Quantidade", min_value=0.0, step=1.0)
            with c2:
                uni = st.text_input("Unidade (m2, kg, un...)")
                pu  = st.number_input("Preco unitario (R$)", min_value=0.0, step=0.01)
            if st.form_submit_button("Adicionar", use_container_width=True) and mat:
                orc_svc.adicionar_material(id_obra=obra_id, material=mat, quantidade=qtd, unidade=uni, preco_unitario=pu)
                st.success(f"'{mat}' adicionado.")

    with aba_ver:
        itens = orc_svc.listar_por_obra(obra_id)
        if not itens:
            st.info("Nenhum item ainda.")
        else:
            st.metric("Total", f"R$ {orc_svc.calcular_total_obra(obra_id):,.2f}")
            for i in itens:
                st.write(f"• **{i.material}** — {i.quantidade} {i.unidade} x R$ {i.preco_unitario:.2f} = R$ {i.preco_total:.2f}")

    with aba_preco:
        st.caption("Estimativa gerada por IA para referencia. Confirme sempre com fornecedores "
                   "ou tabelas oficiais (SINAPI/CUB) antes de fechar o orcamento.")
        mat_p = st.text_input("Material", placeholder="cimento CP-II 50kg")
        reg_p = st.text_input("Regiao", value="Brasil")
        if st.button("Pesquisar", use_container_width=True) and mat_p:
            if ia.configurada:
                with st.spinner("Consultando IA..."):
                    st.markdown(ia.consultar_precos(mat_p, reg_p, id_usuario=u.id))
                st.info("Valores aproximados — nao use como preco oficial sem validar.")
            else:
                st.warning("Configure OPENROUTER_API_KEY no .env.")


# ── SOBRAS ────────────────────────────────────────────────────────────
elif pag == "sobras" and u.tipo in ("admin", "construtor"):
    from src.services.sobras_service import SobrasService
    if "sobras_svc" not in st.session_state:
        st.session_state.sobras_svc = SobrasService()
    sobras_svc = st.session_state.sobras_svc

    st.markdown("<h2 style='color:#f1f5f9;'>Mercado de Sobras</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#374151;'>Publique materiais sobrando ou encontre o que precisa.</p>", unsafe_allow_html=True)

    aba_pub, aba_mrc, aba_min = st.tabs(["Publicar material", "Mercado geral", "Meus anuncios"])

    with aba_pub:
        obras = obras_svc.listar_obras()
        if not obras:
            st.warning("Cadastre uma obra primeiro.")
        else:
            obra_map = {o.id: o.nome for o in obras}
            with st.form("form_sobra"):
                obra_id_s = st.selectbox("Obra de origem", list(obra_map.keys()),
                                         format_func=lambda x: obra_map[x])
                c1, c2 = st.columns(2)
                with c1:
                    mat_s  = st.text_input("Material *")
                    qtd_s  = st.number_input("Quantidade", min_value=0.0, step=1.0)
                with c2:
                    uni_s  = st.text_input("Unidade (m², kg, un...)")
                    preco_s = st.number_input("Preco (R$)", min_value=0.0, step=1.0)
                desc_s = st.text_area("Descricao (opcional)", height=80)
                if st.form_submit_button("Publicar", use_container_width=True) and mat_s:
                    sobras_svc.publicar(id_obra=obra_id_s, id_vendedor=u.id,
                                        material=mat_s, quantidade=qtd_s,
                                        unidade=uni_s, preco=preco_s, descricao=desc_s)
                    st.success(f"'{mat_s}' publicado no mercado.")

    with aba_mrc:
        disponiveis = sobras_svc.listar_disponiveis()
        if not disponiveis:
            st.info("Nenhum material disponivel no momento.")
        else:
            for s in disponiveis:
                with st.expander(f"{s['material']} — R$ {s['preco']:.2f}/{s['unidade']} — {s['nome_vendedor']}"):
                    st.write(f"Quantidade: {s['quantidade']} {s['unidade']}")
                    if s["descricao"]:
                        st.write(s["descricao"])
                    if s["id_vendedor"] != u.id:
                        st.info("Entre em contato com o vendedor para negociar.")

    with aba_min:
        meus = [s for obra in obras_svc.listar_obras()
                for s in sobras_svc.listar_por_obra(obra.id)
                if s["id_vendedor"] == u.id]
        if not meus:
            st.info("Voce nao tem anuncios publicados.")
        else:
            for s in meus:
                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    status_cor = "#10b981" if s["status"] == "disponivel" else "#64748b"
                    st.markdown(f"**{s['material']}** — {s['quantidade']} {s['unidade']} — "
                                f"R$ {s['preco']:.2f} — "
                                f"<span style='color:{status_cor};'>{s['status']}</span>",
                                unsafe_allow_html=True)
                with c2:
                    if s["status"] == "disponivel" and st.button("Vendido", key=f"vnd_{s['id']}"):
                        sobras_svc.marcar_vendido(s["id"])
                        st.rerun()
                with c3:
                    if st.button("Remover", key=f"rmv_{s['id']}"):
                        sobras_svc.deletar(s["id"])
                        st.rerun()


# ── ESTUDOS ───────────────────────────────────────────────────────────
elif pag == "estudos" and u.tipo in ("admin", "construtor"):
    st.markdown("<h2 style='color:#f1f5f9;'>Estudos com IA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#374151;'>Tire duvidas sobre construcao civil com o assistente especialista.</p>", unsafe_allow_html=True)

    if not ia.configurada:
        st.warning("Configure OPENROUTER_API_KEY no .env para usar o chat.")
        st.stop()

    if "chat_hist" not in st.session_state:
        st.session_state.chat_hist = []

    # CSS do chat customizado
    st.markdown("""
    <style>
    .msg-wrap { margin-bottom: 12px; }
    .msg-nome { font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
                letter-spacing: 0.08em; margin-bottom: 4px; }
    .msg-user .msg-nome { color: #64748b; text-align: right; }
    .msg-ia .msg-nome   { color: #c2410c; }
    .msg-bubble { padding: 12px 16px; border-radius: 10px;
                  font-size: 0.9rem; line-height: 1.6; color: #cbd5e1; }
    .msg-user .msg-bubble { background: #111827; border: 1px solid #1e2433;
                            margin-left: 15%; text-align: left; }
    .msg-ia .msg-bubble   { background: #0d1117; border: 1px solid #1e2433;
                            margin-right: 15%; }
    </style>
    """, unsafe_allow_html=True)

    # Historico
    for msg in st.session_state.chat_hist:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-wrap msg-user">
                <div class="msg-nome">{u.nome}</div>
                <div class="msg-bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-wrap msg-ia">
                <div class="msg-nome">IAOBRA</div>
                <div class="msg-bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)

    # Input
    pergunta = st.chat_input("Pergunte sobre construcao civil, normas NBR, materiais, tecnicas...")
    if pergunta:
        st.session_state.chat_hist.append({"role": "user", "content": pergunta})
        st.markdown(f"""
        <div class="msg-wrap msg-user">
            <div class="msg-nome">{u.nome}</div>
            <div class="msg-bubble">{pergunta}</div>
        </div>""", unsafe_allow_html=True)

        with st.spinner("IAOBRA esta pensando..."):
            resp = ia.chat_estudos(pergunta, st.session_state.chat_hist[:-1], id_usuario=u.id)

        st.session_state.chat_hist.append({"role": "assistant", "content": resp})
        st.markdown(f"""
        <div class="msg-wrap msg-ia">
            <div class="msg-nome">IAOBRA</div>
            <div class="msg-bubble">{resp}</div>
        </div>""", unsafe_allow_html=True)

    if st.session_state.chat_hist and st.button("Limpar conversa"):
        st.session_state.chat_hist = []
        st.rerun()


# ── PAINEL ADMIN ──────────────────────────────────────────────────────
elif pag == "admin_panel" and u.tipo == "admin":
    st.markdown("<h2 style='color:#f1f5f9;'>Painel do Administrador</h2>", unsafe_allow_html=True)

    aba_c, aba_k, aba_u, aba_pag = st.tabs(["Criar construtor", "Criar cliente", "Usuarios", "Pagamentos PIX"])

    with aba_c:
        st.markdown("<p style='color:#475569;font-size:0.85rem;'>Construtores tem acesso completo as ferramentas da plataforma.</p>", unsafe_allow_html=True)
        with st.form("form_construtor"):
            nc = st.text_input("Nome completo *")
            uc = st.text_input("Usuario *", help="Apenas letras, numeros, _ ou . (3-30 caracteres)")
            sc = st.text_input("Senha *", type="password", help="Minimo 8 caracteres")
            if st.form_submit_button("Criar construtor", use_container_width=True):
                if nc and uc and sc:
                    try:
                        auth.criar_construtor(nome=nc, username=uc, senha=sc)
                        st.success(f"Construtor '{nc}' criado. Login: {uc}")
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.error("Preencha todos os campos.")

    with aba_k:
        obras = obras_svc.listar_obras()
        st.markdown("<p style='color:#475569;font-size:0.85rem;'>Clientes tem acesso somente leitura as obras vinculadas.</p>", unsafe_allow_html=True)
        with st.form("form_cliente_admin"):
            nk = st.text_input("Nome completo *")
            uk = st.text_input("Usuario *")
            sk = st.text_input("Senha *", type="password")
            obras_opts = {o.id: o.nome for o in obras}
            obras_sel = st.multiselect("Obras que pode acompanhar", options=list(obras_opts.keys()),
                                       format_func=lambda x: obras_opts[x])
            if st.form_submit_button("Criar cliente", use_container_width=True):
                if nk and uk and sk:
                    try:
                        auth.criar_cliente(nome=nk, username=uk, senha=sk, obras_ids=obras_sel)
                        st.success(f"Cliente '{nk}' criado. Login: {uk}")
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.error("Preencha todos os campos.")

    with aba_u:
        todos = auth.listar_todos()
        if not todos:
            st.info("Nenhum usuario cadastrado.")
        else:
            st.markdown(f"Total: {len(todos)} usuarios")
            st.divider()
            for usr in todos:
                tipo_br = {"construtor": "Construtor", "cliente": "Cliente"}.get(usr.tipo, usr.tipo)
                status = "Ativo" if usr.ativo else "Inativo"
                bloq = " — Bloqueado" if usr.bloqueado else ""
                obras_nomes = [obras_svc.obter_obra(oid).nome for oid in usr.obras_ids if obras_svc.obter_obra(oid)]
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{usr.nome}** ({usr.username}) — {tipo_br} — {status}{bloq}")
                    if obras_nomes:
                        st.write(f"Obras: {', '.join(obras_nomes)}")
                with col2:
                    if usr.bloqueado and st.button("Desbloquear", key=f"desbloq_{usr.username}"):
                        auth.desbloquear(usr.username)
                        st.rerun()

    with aba_pag:
        st.markdown("<p style='color:#475569;font-size:0.85rem;'>Confirme os pagamentos PIX e libere os creditos.</p>", unsafe_allow_html=True)
        pendentes = cred_svc.pagamentos_pendentes()
        if not pendentes:
            st.info("Nenhum pagamento aguardando confirmacao.")
        else:
            for p in pendentes:
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.write(f"**{p['nome']}** ({p['username']}) — R$ {p['valor_brl']:.2f} — {str(p['criado_em'])[:16]}")
                with c2:
                    if st.button("Confirmar", key=f"conf_{p['id']}"):
                        if cred_svc.confirmar_pagamento(p["id"]):
                            st.success("Creditos liberados.")
                            st.rerun()
                with c3:
                    if st.button("Recusar", key=f"rec_{p['id']}"):
                        with db() as cur:
                            cur.execute("UPDATE transacoes SET confirmado = TRUE, descricao = 'Recusado' WHERE id = %s", (p["id"],))
                        st.rerun()

        st.divider()
        st.markdown("<p style='color:#475569;font-size:0.85rem;'>Adicionar creditos manualmente</p>", unsafe_allow_html=True)
        todos_usr = auth.listar_todos()
        with st.form("form_creditos_manual"):
            usr_sel = st.selectbox("Usuario", options=[u.username for u in todos_usr])
            qtd_cr  = st.number_input("Quantidade de creditos", min_value=1, value=500)
            desc_cr = st.text_input("Descricao", value="Creditos adicionados pelo admin")
            if st.form_submit_button("Adicionar creditos", use_container_width=True):
                usr_obj = next((x for x in todos_usr if x.username == usr_sel), None)
                if usr_obj and cred_svc.adicionar(usr_obj.id, qtd_cr, desc_cr):
                    st.success(f"+{qtd_cr} creditos para {usr_sel}.")

# ── PLANOS ────────────────────────────────────────────────────────────
elif pag == "planos" and u.tipo in ("admin", "construtor"):
    from src.ui.pages.planos_page import render_planos
    render_planos(u, cred_svc)

# ── CONTATO ───────────────────────────────────────────────────────────
elif pag == "contato":
    from src.ui.pages.contato_page import render_contato
    render_contato(usuario=u, is_admin=(u.tipo == "admin"))

# ── ACOMPANHAR (cliente) ──────────────────────────────────────────────
elif pag == "acompanhar" and u.tipo == "cliente":
    from src.services.diario_service import DiarioService
    from src.services.orcamento_service import OrcamentoService
    if "diario_svc" not in st.session_state:
        st.session_state.diario_svc = DiarioService()
    if "orcamento_svc" not in st.session_state:
        st.session_state.orcamento_svc = OrcamentoService()
    from src.ui.pages.cliente_page import render_cliente_dashboard
    render_cliente_dashboard(
        usuario=u,
        obra_service=obras_svc,
        diario_service=st.session_state.diario_svc,
        orcamento_service=st.session_state.orcamento_svc,
    )

else:
    st.session_state.pagina = "home"
    st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center;color:#1f2937;font-size:0.75rem;'>IAOBRA v0.2.0 — Plataforma de gestao de obras com IA</p>",
    unsafe_allow_html=True,
)
