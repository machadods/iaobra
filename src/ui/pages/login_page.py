"""
LOGIN PAGE — IAOBRA
"""

import streamlit as st
from src.services.auth_service import AuthService


def render_login(auth_service: AuthService):
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #07090f !important; }
    [data-testid="stMain"] { background: transparent !important; }

    .login-wrap {
        text-align: center;
        padding: 4rem 0 2rem 0;
    }
    .login-badge {
        display: inline-block;
        background: rgba(194,65,12,0.1);
        border: 1px solid rgba(194,65,12,0.2);
        color: #ea580c;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    .login-title {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -2px;
        color: #f1f5f9;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .login-title span { color: #ea580c; }
    .login-sub {
        color: #374151;
        font-size: 0.9rem;
        margin-bottom: 0;
    }
    .login-card {
        background: #0d1117;
        border: 1px solid #1e2433;
        border-radius: 12px;
        padding: 2rem 2rem 1.5rem 2rem;
    }
    .login-card-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .login-hint {
        text-align: center;
        margin-top: 1rem;
        color: #1f2937;
        font-size: 0.76rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrap">
        <div class="login-badge">Plataforma de obras com IA</div>
        <div class="login-title">IA<span>OBRA</span></div>
        <div class="login-sub">Mestre Digital — Gestao inteligente de obras</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-card"><div class="login-card-title">Acesso a plataforma</div>', unsafe_allow_html=True)

        username = st.text_input("Usuario", placeholder="seu.usuario", key="li_user")
        senha = st.text_input("Senha", type="password", placeholder="minimo 8 caracteres", key="li_pass")
        entrar = st.button("Entrar", use_container_width=True, key="btn_login")

        st.markdown('<div class="login-hint">Primeiro acesso: admin / iaobras2024</div></div>', unsafe_allow_html=True)

    if entrar:
        if not username or not senha:
            with col2:
                st.error("Preencha usuario e senha.")
            return

        usuario = auth_service.login(username, senha)
        if usuario:
            st.session_state.usuario = usuario
            st.session_state.pagina = "home"
            st.rerun()
        elif auth_service.buscar_por_username(username) and auth_service.buscar_por_username(username).bloqueado:
            with col2:
                st.error("Conta bloqueada apos multiplas tentativas. Contate o administrador.")
        else:
            with col2:
                st.error("Usuario ou senha invalidos.")
