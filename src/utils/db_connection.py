"""
DB CONNECTION
Conexao real com PostgreSQL via psycopg2.
Use get_conn() para obter uma conexao do pool.
"""

import psycopg2
import psycopg2.extras
import logging
from contextlib import contextmanager
from config import DATABASE_URL

logger = logging.getLogger("iaobras.db")


def get_conn():
    """Retorna uma conexao com o banco."""
    return psycopg2.connect(DATABASE_URL)


@contextmanager
def db():
    """
    Context manager para queries com commit automatico.

    Uso:
        with db() as cur:
            cur.execute("SELECT ...")
            rows = cur.fetchall()
    """
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def banco_disponivel() -> bool:
    """Testa se o banco esta acessivel."""
    try:
        conn = get_conn()
        conn.close()
        return True
    except Exception:
        return False
