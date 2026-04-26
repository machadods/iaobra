"""
FILE HANDLER
Salva uploads em disco e registra na tabela midia do PostgreSQL.
Estrutura: uploads/<id_obra>/<tipo>/<timestamp>_<nome>
"""

import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import UPLOADS_DIR
from src.utils.db_connection import db

logger = logging.getLogger("iaobras.files")

EXTENSOES_FOTO  = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
EXTENSOES_VIDEO = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
EXTENSOES_AUDIO = {".mp3", ".wav", ".ogg", ".m4a", ".aac"}
EXTENSOES_VALIDAS = EXTENSOES_FOTO | EXTENSOES_VIDEO | EXTENSOES_AUDIO


def _tipo_por_extensao(nome: str) -> Optional[str]:
    ext = Path(nome).suffix.lower()
    if ext in EXTENSOES_FOTO:  return "foto"
    if ext in EXTENSOES_VIDEO: return "video"
    if ext in EXTENSOES_AUDIO: return "audio"
    return None


def salvar_upload(arquivo, id_obra: int, id_diario: int) -> Optional[dict]:
    """
    Salva arquivo de upload no disco e registra na tabela midia.
    Retorna dict com info do arquivo ou None se falhar.
    """
    tipo = _tipo_por_extensao(arquivo.name)
    if not tipo:
        logger.warning(f"Extensao nao permitida: {arquivo.name}")
        return None

    # Pasta: uploads/<id_obra>/<tipo>/
    pasta = Path(UPLOADS_DIR) / str(id_obra) / tipo
    pasta.mkdir(parents=True, exist_ok=True)

    # Nome unico com timestamp para evitar colisoes
    ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome  = f"{ts}_{arquivo.name}"
    caminho = pasta / nome

    conteudo = arquivo.getbuffer()
    tamanho  = len(conteudo)

    with open(caminho, "wb") as f:
        f.write(conteudo)

    # Registra na tabela midia
    try:
        with db() as cur:
            cur.execute("""
                INSERT INTO midia (id_diario, id_obra, tipo, nome_arquivo, caminho, tamanho_bytes)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (id_diario, id_obra, tipo, nome, str(caminho), tamanho))
            midia_id = cur.fetchone()["id"]

        logger.info(f"Arquivo salvo: {caminho} (midia.id={midia_id})")
        return {"id": midia_id, "nome": nome, "tipo": tipo,
                "caminho": str(caminho), "tamanho": tamanho}
    except Exception as e:
        logger.error(f"Erro ao registrar midia no banco: {e}")
        caminho.unlink(missing_ok=True)
        return None


def listar_midias_diario(id_diario: int) -> list:
    """Retorna arquivos de um registro do diario."""
    try:
        with db() as cur:
            cur.execute("""
                SELECT id, tipo, nome_arquivo, caminho, tamanho_bytes, criado_em
                FROM midia WHERE id_diario = %s ORDER BY criado_em
            """, (id_diario,))
            return [dict(r) for r in cur.fetchall()]
    except Exception:
        return []


def deletar_midia(id_midia: int) -> bool:
    """Remove arquivo do disco e do banco."""
    try:
        with db() as cur:
            cur.execute("SELECT caminho FROM midia WHERE id = %s", (id_midia,))
            row = cur.fetchone()
            if not row:
                return False
            Path(row["caminho"]).unlink(missing_ok=True)
            cur.execute("DELETE FROM midia WHERE id = %s", (id_midia,))
        return True
    except Exception as e:
        logger.error(f"Erro ao deletar midia {id_midia}: {e}")
        return False
