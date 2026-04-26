"""
ORCAMENTO SERVICE — PostgreSQL
preco_total e calculado pelo banco (GENERATED ALWAYS AS).
"""

import logging
from typing import List, Optional
from src.models.orcamento import Orcamento
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.orcamento")


def _row(r) -> Orcamento:
    return Orcamento(
        id=r["id"],
        id_obra=r["id_obra"],
        material=r["material"],
        quantidade=float(r.get("quantidade") or 0),
        unidade=r.get("unidade") or "",
        preco_unitario=float(r.get("preco_unitario") or 0),
        preco_total=float(r.get("preco_total") or 0),
        loja=r.get("loja") or "",
        observacoes=r.get("observacoes") or "",
    )


class OrcamentoService:
    def adicionar_material(self, id_obra: int, material: str,
                           quantidade: float, unidade: str,
                           preco_unitario: float, loja: str = "",
                           observacoes: str = "") -> Orcamento:
        with db() as cur:
            cur.execute("""
                INSERT INTO orcamento
                    (id_obra, material, quantidade, unidade, preco_unitario, loja, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (id_obra, material, quantidade, unidade,
                  preco_unitario, loja, observacoes))
            return _row(cur.fetchone())

    def listar_por_obra(self, id_obra: int) -> List[Orcamento]:
        try:
            with db() as cur:
                cur.execute(
                    "SELECT * FROM orcamento WHERE id_obra = %s ORDER BY criado_em",
                    (id_obra,)
                )
                return [_row(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao listar orcamento: {e}")
            return []

    def calcular_total_obra(self, id_obra: int) -> float:
        try:
            with db() as cur:
                cur.execute(
                    "SELECT COALESCE(SUM(preco_total), 0) AS total FROM orcamento WHERE id_obra = %s",
                    (id_obra,)
                )
                return float(cur.fetchone()["total"])
        except Exception:
            return 0.0

    def deletar_material(self, id_material: int) -> bool:
        try:
            with db() as cur:
                cur.execute("DELETE FROM orcamento WHERE id = %s", (id_material,))
            return True
        except Exception:
            return False
