"""
CREDITOS SERVICE
Gerencia saldo de IA, debitos por uso e creditos por pagamento PIX.

Modelo de negocio:
  Plano gratuito  : 10 creditos para teste
  Plano Pro       : 500 creditos/mes — R$ 39,90 via PIX
  Admin           : creditos ilimitados (999999)
  1 credito       = 1 chamada a IA
"""

import logging
from typing import List, Optional
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.creditos")

CUSTO_POR_CHAMADA = 1
CREDITOS_PLANO_PRO = 500
VALOR_PLANO_PRO = 39.90


class CreditosService:

    # ------------------------------------------------------------------
    # Consulta de saldo
    # ------------------------------------------------------------------
    def saldo(self, id_usuario: int) -> int:
        try:
            with db() as cur:
                cur.execute("SELECT creditos FROM usuarios WHERE id = %s", (id_usuario,))
                row = cur.fetchone()
                return int(row["creditos"]) if row else 0
        except Exception:
            return 0

    def tem_creditos(self, id_usuario: int) -> bool:
        return self.saldo(id_usuario) > 0

    # ------------------------------------------------------------------
    # Debito (uso da IA)
    # ------------------------------------------------------------------
    def debitar(self, id_usuario: int, descricao: str = "Chamada IA") -> bool:
        """
        Debita 1 credito. Retorna False se sem saldo.
        Admin nunca e debitado.
        """
        try:
            with db() as cur:
                cur.execute("SELECT creditos, tipo FROM usuarios WHERE id = %s", (id_usuario,))
                row = cur.fetchone()
                if not row:
                    return False
                if row["tipo"] == "admin":
                    return True
                if row["creditos"] <= 0:
                    return False

                cur.execute("""
                    UPDATE usuarios SET creditos = creditos - %s WHERE id = %s
                """, (CUSTO_POR_CHAMADA, id_usuario))

                cur.execute("""
                    INSERT INTO transacoes (id_usuario, tipo, creditos, descricao, confirmado)
                    VALUES (%s, 'debito', %s, %s, TRUE)
                """, (id_usuario, -CUSTO_POR_CHAMADA, descricao))

            return True
        except Exception as e:
            logger.error(f"Erro ao debitar credito: {e}")
            return False

    # ------------------------------------------------------------------
    # Credito (pagamento confirmado pelo admin)
    # ------------------------------------------------------------------
    def adicionar(self, id_usuario: int, quantidade: int,
                  descricao: str = "Creditos adicionados") -> bool:
        try:
            with db() as cur:
                cur.execute("""
                    UPDATE usuarios
                    SET creditos = creditos + %s,
                        plano = CASE WHEN %s >= %s THEN 'pro' ELSE plano END,
                        validade_plano = NOW() + INTERVAL '31 days'
                    WHERE id = %s
                """, (quantidade, quantidade, CREDITOS_PLANO_PRO, id_usuario))

                cur.execute("""
                    INSERT INTO transacoes (id_usuario, tipo, creditos, valor_brl, descricao, confirmado)
                    VALUES (%s, 'credito', %s, %s, %s, TRUE)
                """, (id_usuario, quantidade, VALOR_PLANO_PRO, descricao))

            logger.info(f"Creditos adicionados: usuario {id_usuario} +{quantidade}")
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar creditos: {e}")
            return False

    # ------------------------------------------------------------------
    # Solicitacao de pagamento (pendente de confirmacao admin)
    # ------------------------------------------------------------------
    def registrar_pagamento_pendente(self, id_usuario: int) -> int:
        """Cria transacao pendente. Retorna ID da transacao."""
        try:
            with db() as cur:
                cur.execute("""
                    INSERT INTO transacoes
                        (id_usuario, tipo, creditos, valor_brl, descricao, confirmado)
                    VALUES (%s, 'pagamento', %s, %s, 'Plano Pro — aguardando confirmacao PIX', FALSE)
                    RETURNING id
                """, (id_usuario, CREDITOS_PLANO_PRO, VALOR_PLANO_PRO))
                return cur.fetchone()["id"]
        except Exception as e:
            logger.error(f"Erro ao registrar pagamento: {e}")
            return 0

    def confirmar_pagamento(self, id_transacao: int) -> bool:
        """Admin confirma PIX e libera creditos."""
        try:
            with db() as cur:
                cur.execute("""
                    SELECT id_usuario, creditos, confirmado
                    FROM transacoes WHERE id = %s
                """, (id_transacao,))
                t = cur.fetchone()
                if not t or t["confirmado"]:
                    return False

                cur.execute("""
                    UPDATE transacoes SET confirmado = TRUE WHERE id = %s
                """, (id_transacao,))
                cur.execute("""
                    UPDATE usuarios
                    SET creditos = creditos + %s,
                        plano = 'pro',
                        validade_plano = NOW() + INTERVAL '31 days'
                    WHERE id = %s
                """, (t["creditos"], t["id_usuario"]))

            logger.info(f"Pagamento confirmado: transacao {id_transacao}")
            return True
        except Exception as e:
            logger.error(f"Erro ao confirmar pagamento: {e}")
            return False

    # ------------------------------------------------------------------
    # Historico
    # ------------------------------------------------------------------
    def historico(self, id_usuario: int, limite: int = 20) -> List[dict]:
        try:
            with db() as cur:
                cur.execute("""
                    SELECT tipo, creditos, valor_brl, descricao, confirmado, criado_em
                    FROM transacoes
                    WHERE id_usuario = %s
                    ORDER BY criado_em DESC
                    LIMIT %s
                """, (id_usuario, limite))
                return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

    def pagamentos_pendentes(self) -> List[dict]:
        """Usado pelo admin para ver PIX aguardando confirmacao."""
        try:
            with db() as cur:
                cur.execute("""
                    SELECT t.id, t.id_usuario, u.nome, u.username,
                           t.valor_brl, t.criado_em
                    FROM transacoes t
                    JOIN usuarios u ON u.id = t.id_usuario
                    WHERE t.tipo = 'pagamento' AND t.confirmado = FALSE
                    ORDER BY t.criado_em
                """)
                return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []
