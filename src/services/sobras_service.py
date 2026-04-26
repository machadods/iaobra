"""
SOBRAS SERVICE — PostgreSQL
Marketplace de materiais sobrando entre mestres e clientes.
"""

import logging
from typing import List
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.sobras")


def _row(r) -> dict:
    return {
        "id":              r["id"],
        "id_obra":         r["id_obra"],
        "id_vendedor":     r.get("id_vendedor"),
        "nome_vendedor":   r.get("nome_vendedor") or "—",
        "material":        r["material"],
        "quantidade":      float(r.get("quantidade") or 0),
        "unidade":         r.get("unidade") or "",
        "preco":           float(r.get("preco") or 0),
        "descricao":       r.get("descricao") or "",
        "status":          r.get("status") or "disponivel",
        "data_publicacao": r.get("data_publicacao"),
    }


class SobrasService:
    def publicar(self, id_obra: int, id_vendedor: int, material: str,
                 quantidade: float, unidade: str, preco: float,
                 descricao: str = "") -> dict:
        with db() as cur:
            cur.execute("""
                INSERT INTO sobras
                    (id_obra, id_vendedor, material, quantidade, unidade, preco, descricao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (id_obra, id_vendedor, material, quantidade, unidade, preco, descricao))
            return _row(cur.fetchone())

    def listar_disponiveis(self) -> List[dict]:
        try:
            with db() as cur:
                cur.execute("""
                    SELECT s.*, u.nome AS nome_vendedor
                    FROM sobras s
                    LEFT JOIN usuarios u ON u.id = s.id_vendedor
                    WHERE s.status = 'disponivel'
                    ORDER BY s.data_publicacao DESC
                """)
                return [_row(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao listar sobras: {e}")
            return []

    def listar_por_obra(self, id_obra: int) -> List[dict]:
        try:
            with db() as cur:
                cur.execute("""
                    SELECT s.*, u.nome AS nome_vendedor
                    FROM sobras s
                    LEFT JOIN usuarios u ON u.id = s.id_vendedor
                    WHERE s.id_obra = %s
                    ORDER BY s.data_publicacao DESC
                """, (id_obra,))
                return [_row(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao listar sobras da obra: {e}")
            return []

    def marcar_vendido(self, id_sobra: int) -> bool:
        try:
            with db() as cur:
                cur.execute("""
                    UPDATE sobras SET status = 'vendido', data_venda = NOW()
                    WHERE id = %s
                """, (id_sobra,))
            return True
        except Exception:
            return False

    def deletar(self, id_sobra: int) -> bool:
        try:
            with db() as cur:
                cur.execute("DELETE FROM sobras WHERE id = %s", (id_sobra,))
            return True
        except Exception:
            return False
