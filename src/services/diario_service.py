"""
DIARIO SERVICE — PostgreSQL
"""

import logging
from typing import List, Optional
from datetime import datetime
from src.models.diario import Diario
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.diario")


def _row(r) -> Diario:
    return Diario(
        id=r["id"],
        id_obra=r["id_obra"],
        data_registro=r.get("data_registro"),
        registro_texto=r.get("registro_texto") or "",
        fotos=[],
        videos=[],
        audio=None,
        criado_em=r.get("criado_em"),
    )


class DiarioService:
    def criar_registro(self, id_obra: int, registro_texto: str,
                       fotos: List[str] = None, analise_ia: str = None) -> Diario:
        with db() as cur:
            cur.execute("""
                INSERT INTO diario (id_obra, registro_texto, analise_ia, data_registro)
                VALUES (%s, %s, %s, NOW())
                RETURNING *
            """, (id_obra, registro_texto, analise_ia))
            entrada = _row(cur.fetchone())

        # Salva midias (fotos)
        if fotos and entrada.id:
            self._salvar_midias(entrada.id, id_obra, fotos, "foto")

        return entrada

    def _salvar_midias(self, id_diario: int, id_obra: int,
                       arquivos: List[str], tipo: str):
        try:
            with db() as cur:
                for nome in arquivos:
                    cur.execute("""
                        INSERT INTO midia (id_diario, id_obra, tipo, nome_arquivo)
                        VALUES (%s, %s, %s, %s)
                    """, (id_diario, id_obra, tipo, nome))
        except Exception as e:
            logger.error(f"Erro ao salvar midia: {e}")

    def listar_por_obra(self, id_obra: int) -> List[Diario]:
        try:
            with db() as cur:
                cur.execute("""
                    SELECT * FROM diario
                    WHERE id_obra = %s
                    ORDER BY data_registro ASC
                """, (id_obra,))
                return [_row(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao listar diario: {e}")
            return []

    def obter_registro(self, id_registro: int) -> Optional[Diario]:
        try:
            with db() as cur:
                cur.execute("SELECT * FROM diario WHERE id = %s", (id_registro,))
                row = cur.fetchone()
                return _row(row) if row else None
        except Exception:
            return None

    def deletar_registro(self, id_registro: int) -> bool:
        try:
            with db() as cur:
                cur.execute("DELETE FROM diario WHERE id = %s", (id_registro,))
            return True
        except Exception:
            return False
