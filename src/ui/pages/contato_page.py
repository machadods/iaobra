"""
CONTATO PAGE — Fale com os desenvolvedores da solucao.
Salva as mensagens na tabela 'contatos' e permite ao admin visualizar.
"""

import re
import logging
import streamlit as st
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.contato")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

DEV_NOME = "Wagner Machado dos Santos"
DEV_EMAIL = "machadinho94@hotmail.com"


def _salvar_contato(nome: str, email: str, assunto: str, mensagem: str) -> bool:
    try:
        with db() as cur:
            cur.execute(
                """
                INSERT INTO contatos (nome, email, assunto, mensagem)
                VALUES (%s, %s, %s, %s)
                """,
                (nome.strip()[:150], email.strip()[:150],
                 (assunto or "").strip()[:200], mensagem.strip()),
            )
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar contato: {e}")
        return False


def render_contato(usuario=None, is_admin: bool = False):
    st.markdown("<h2 style='color:#f1f5f9;'>Fale Conosco</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#374151;'>Dúvidas, sugestões ou problemas? Envie uma mensagem "
        "para a equipe de desenvolvimento da plataforma.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='color:#64748b;font-size:0.85rem;'>Desenvolvedor: "
        f"<strong style='color:#e8590c;'>{DEV_NOME}</strong> — {DEV_EMAIL}</p>",
        unsafe_allow_html=True,
    )

    nome_padrao = getattr(usuario, "nome", "") if usuario else ""

    with st.form("form_contato"):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome *", value=nome_padrao)
        with c2:
            email = st.text_input("Email *", placeholder="voce@exemplo.com")
        assunto = st.text_input("Assunto", placeholder="Sobre o que você quer falar?")
        mensagem = st.text_area("Mensagem *", height=150,
                                placeholder="Escreva sua mensagem para os desenvolvedores...")
        enviar = st.form_submit_button("Enviar mensagem", use_container_width=True)

    if enviar:
        if not nome or not email or not mensagem:
            st.error("Preencha nome, email e mensagem.")
        elif not _EMAIL_RE.match(email.strip()):
            st.error("Informe um email válido.")
        elif _salvar_contato(nome, email, assunto, mensagem):
            st.success("Mensagem enviada! Obrigado pelo contato — responderemos em breve.")
        else:
            st.error("Não foi possível enviar agora. Tente novamente mais tarde.")

    # Admin vê as mensagens recebidas
    if is_admin:
        st.divider()
        st.markdown("<h3 style='color:#f1f5f9;'>Mensagens recebidas</h3>", unsafe_allow_html=True)
        try:
            with db() as cur:
                cur.execute(
                    "SELECT nome, email, assunto, mensagem, criado_em "
                    "FROM contatos ORDER BY criado_em DESC LIMIT 50"
                )
                msgs = cur.fetchall()
        except Exception:
            msgs = []

        if not msgs:
            st.info("Nenhuma mensagem recebida ainda.")
        else:
            for m in msgs:
                titulo = m["assunto"] or "(sem assunto)"
                with st.expander(f"{titulo} — {m['nome']} ({str(m['criado_em'])[:16]})"):
                    st.write(f"**De:** {m['nome']} — {m['email']}")
                    st.write(m["mensagem"])
