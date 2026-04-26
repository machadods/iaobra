"""
OBRA SERVICE — PostgreSQL
"""

import logging
from datetime import date
from typing import List, Optional
from src.models.obra import Obra
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.obras")


def _row(r) -> Obra:
    return Obra(
        id=r["id"],
        nome=r["nome"],
        endereco=r["endereco"],
        descricao=r.get("descricao") or "",
        status=r.get("status") or "em_andamento",
        data_inicio=r.get("data_inicio"),
        data_fim=r.get("data_fim"),
        proprietario=r.get("proprietario") or "",
        responsavel=r.get("responsavel") or "",
        orcamento_total=float(r.get("orcamento_total") or 0),
    )


class ObraService:
    def criar_obra(self, nome: str, endereco: str, descricao: str = "",
                   proprietario: str = "", responsavel: str = "",
                   orcamento_total: float = 0.0,
                   id_construtor: int = None) -> Obra:
        with db() as cur:
            cur.execute("""
                INSERT INTO obras (nome, endereco, descricao, status, data_inicio,
                                   proprietario, responsavel, orcamento_total, id_construtor)
                VALUES (%s, %s, %s, 'em_andamento', %s, %s, %s, %s, %s)
                RETURNING *
            """, (nome, endereco, descricao, date.today(),
                  proprietario, responsavel, orcamento_total, id_construtor))
            return _row(cur.fetchone())

    def listar_obras(self, id_construtor: int = None) -> List[Obra]:
        try:
            with db() as cur:
                if id_construtor:
                    cur.execute(
                        "SELECT * FROM obras WHERE id_construtor = %s ORDER BY criado_em DESC",
                        (id_construtor,)
                    )
                else:
                    cur.execute("SELECT * FROM obras ORDER BY criado_em DESC")
                return [_row(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao listar obras: {e}")
            return []

    def obter_obra(self, id_obra: int) -> Optional[Obra]:
        try:
            with db() as cur:
                cur.execute("SELECT * FROM obras WHERE id = %s", (id_obra,))
                row = cur.fetchone()
                return _row(row) if row else None
        except Exception:
            return None

    def atualizar_obra(self, id_obra: int, **kwargs) -> bool:
        campos_permitidos = {"nome", "endereco", "descricao", "status",
                             "data_fim", "proprietario", "responsavel", "orcamento_total"}
        updates = {k: v for k, v in kwargs.items() if k in campos_permitidos}
        if not updates:
            return False
        try:
            sets = ", ".join(f"{k} = %s" for k in updates)
            with db() as cur:
                cur.execute(
                    f"UPDATE obras SET {sets}, atualizado_em = NOW() WHERE id = %s",
                    list(updates.values()) + [id_obra]
                )
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar obra: {e}")
            return False

    def deletar_obra(self, id_obra: int) -> bool:
        try:
            with db() as cur:
                cur.execute("DELETE FROM obras WHERE id = %s", (id_obra,))
            return True
        except Exception:
            return False

    def listar_por_status(self, status: str) -> List[Obra]:
        try:
            with db() as cur:
                cur.execute(
                    "SELECT * FROM obras WHERE status = %s ORDER BY criado_em DESC",
                    (status,)
                )
                return [_row(r) for r in cur.fetchall()]
        except Exception:
            return []
