"""
PLANOS PAGE — creditos, assinatura e pagamento via PIX
"""

import streamlit as st
from config import PIX_CHAVE, PIX_NOME, PIX_BANCO
from src.services.creditos_service import CreditosService, VALOR_PLANO_PRO, CREDITOS_PLANO_PRO


def render_planos(usuario, creditos_svc: CreditosService):
    saldo = creditos_svc.saldo(usuario.id)

    st.markdown("<h2 style='color:#f1f5f9;'>Planos e Creditos</h2>", unsafe_allow_html=True)

    # ── Saldo atual ───────────────────────────────────────────────────
    cor_saldo = "#10b981" if saldo > 50 else "#f59e0b" if saldo > 10 else "#ef4444"
    st.markdown(f"""
    <div style='background:#0d1117;border:1px solid #1e2433;border-radius:10px;
                padding:1.4rem;margin-bottom:1.5rem;'>
        <div style='font-size:0.75rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.1em;color:#475569;margin-bottom:6px;'>
            Seu saldo atual
        </div>
        <div style='font-size:2.8rem;font-weight:900;color:{cor_saldo};letter-spacing:-1px;'>
            {saldo}
        </div>
        <div style='color:#374151;font-size:0.85rem;margin-top:4px;'>
            creditos de IA disponíveis &nbsp;·&nbsp; 1 credito = 1 chamada a IA
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Planos ────────────────────────────────────────────────────────
    st.markdown("<h3 style='color:#94a3b8;font-size:1rem;'>Planos disponiveis</h3>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style='background:#0d1117;border:1px solid #1e2433;border-radius:10px;padding:1.4rem;'>
            <div style='font-weight:700;color:#94a3b8;margin-bottom:8px;'>Gratuito</div>
            <div style='font-size:1.6rem;font-weight:800;color:#f1f5f9;'>10 creditos</div>
            <div style='color:#374151;font-size:0.82rem;margin-top:4px;margin-bottom:12px;'>para teste da plataforma</div>
            <div style='color:#475569;font-size:0.82rem;'>
                Analise de registro<br>
                Consulta de precos<br>
                Chat de estudos
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style='background:#0d1117;border:2px solid #c2410c;border-radius:10px;padding:1.4rem;'>
            <div style='font-weight:700;color:#ea580c;margin-bottom:8px;'>Plano Pro</div>
            <div style='font-size:1.6rem;font-weight:800;color:#f1f5f9;'>
                R$ {VALOR_PLANO_PRO:.2f}<span style='font-size:1rem;font-weight:400;color:#475569;'>/mes</span>
            </div>
            <div style='color:#374151;font-size:0.82rem;margin-top:4px;margin-bottom:12px;'>
                {CREDITOS_PLANO_PRO} creditos por mes
            </div>
            <div style='color:#475569;font-size:0.82rem;'>
                Tudo do gratuito<br>
                Cronograma automatico com IA<br>
                Analise e auditoria ilimitada<br>
                Suporte prioritario
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Como pagar via PIX ────────────────────────────────────────────
    st.markdown("<h3 style='color:#94a3b8;font-size:1rem;'>Como assinar o Plano Pro</h3>", unsafe_allow_html=True)

    if not PIX_CHAVE:
        st.warning("Chave PIX nao configurada. Contate o administrador.")
    else:
        st.markdown(f"""
        <div style='background:#0d1117;border:1px solid #1e2433;border-radius:10px;padding:1.4rem;'>
            <div style='font-size:0.75rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.1em;color:#475569;margin-bottom:12px;'>
                Dados para pagamento PIX
            </div>
            <table style='width:100%;border-collapse:collapse;'>
                <tr>
                    <td style='color:#475569;font-size:0.82rem;padding:4px 0;width:120px;'>Valor</td>
                    <td style='color:#f1f5f9;font-weight:700;'>R$ {VALOR_PLANO_PRO:.2f}</td>
                </tr>
                <tr>
                    <td style='color:#475569;font-size:0.82rem;padding:4px 0;'>Chave PIX</td>
                    <td style='color:#ea580c;font-weight:700;font-family:monospace;'>{PIX_CHAVE}</td>
                </tr>
                <tr>
                    <td style='color:#475569;font-size:0.82rem;padding:4px 0;'>Favorecido</td>
                    <td style='color:#f1f5f9;'>{PIX_NOME}</td>
                </tr>
                <tr>
                    <td style='color:#475569;font-size:0.82rem;padding:4px 0;'>Banco</td>
                    <td style='color:#f1f5f9;'>{PIX_BANCO}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:12px;background:rgba(194,65,12,0.06);border:1px solid rgba(194,65,12,0.15);
                    border-radius:8px;padding:12px 16px;font-size:0.84rem;color:#6b7280;line-height:1.7;'>
            <strong style='color:#94a3b8;'>Como ativar:</strong><br>
            1. Faca o PIX com o valor exato de R$ 39,90<br>
            2. Envie o comprovante via WhatsApp para o numero da chave PIX<br>
            3. Em ate 24h seus creditos serao liberados<br>
            4. Voce receberá 500 creditos validos por 31 dias
        </div>
        """, unsafe_allow_html=True)

        # Botao de aviso de pagamento
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Ja fiz o PIX — avisar o administrador", use_container_width=True):
            tid = creditos_svc.registrar_pagamento_pendente(usuario.id)
            if tid:
                st.success(f"Pagamento registrado (ID {tid}). Aguarde a confirmacao do admin.")
            else:
                st.error("Erro ao registrar. Tente novamente ou entre em contato.")

    st.divider()

    # ── Historico ─────────────────────────────────────────────────────
    st.markdown("<h3 style='color:#94a3b8;font-size:1rem;'>Historico de creditos</h3>", unsafe_allow_html=True)

    hist = creditos_svc.historico(usuario.id, limite=15)
    if not hist:
        st.info("Nenhuma transacao ainda.")
    else:
        for h in hist:
            tipo = h["tipo"]
            sinal = "+" if tipo in ("credito","pagamento") else "-"
            cor   = "#10b981" if sinal == "+" else "#ef4444"
            conf  = "" if h["confirmado"] else " (pendente)"
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:6px 0;"
                f"border-bottom:1px solid #1e2433;font-size:0.84rem;'>"
                f"<span style='color:#64748b;'>{str(h['criado_em'])[:16]}&nbsp;&nbsp;{h['descricao'] or tipo}{conf}</span>"
                f"<span style='color:{cor};font-weight:700;'>{sinal}{abs(h['creditos'])} cr</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
