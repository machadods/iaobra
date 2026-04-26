"""
MIGRATION RUNNER
Roda automaticamente ao subir o app.
- Cria tabela _migrations se nao existir
- Escaneia database/migrations/*.sql em ordem numerica
- Aplica apenas as migrations novas
- Registra cada migration aplicada com timestamp
"""

import psycopg2
import logging
from pathlib import Path

logger = logging.getLogger("iaobras.migrate")

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _conn(database_url: str):
    return psycopg2.connect(database_url)


def _garantir_tabela_controle(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id         SERIAL PRIMARY KEY,
            nome       VARCHAR(255) NOT NULL UNIQUE,
            aplicada_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)


def _migrations_aplicadas(cur) -> set:
    cur.execute("SELECT nome FROM _migrations")
    return {row[0] for row in cur.fetchall()}


def _listar_arquivos() -> list[Path]:
    """Retorna arquivos .sql numerados em ordem crescente."""
    arquivos = sorted(
        [f for f in MIGRATIONS_DIR.glob("*.sql") if f.stem[0].isdigit()],
        key=lambda f: f.stem,
    )
    return arquivos


def rodar(database_url: str) -> list[str]:
    """
    Aplica todas as migrations pendentes.
    Retorna lista de migrations aplicadas nesta execucao.
    """
    aplicadas_agora = []

    try:
        conn = _conn(database_url)
        conn.autocommit = False
        cur = conn.cursor()

        _garantir_tabela_controle(cur)
        conn.commit()

        ja_aplicadas = _migrations_aplicadas(cur)
        arquivos = _listar_arquivos()

        for arquivo in arquivos:
            nome = arquivo.stem  # ex: 001_schema_completo

            if nome in ja_aplicadas:
                logger.debug(f"Migration ja aplicada: {nome}")
                continue

            logger.info(f"Aplicando migration: {nome}")
            sql = arquivo.read_text(encoding="utf-8")

            try:
                cur.execute(sql)
                cur.execute(
                    "INSERT INTO _migrations (nome) VALUES (%s)", (nome,)
                )
                conn.commit()
                aplicadas_agora.append(nome)
                logger.info(f"Migration aplicada com sucesso: {nome}")
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro na migration {nome}: {e}")
                raise RuntimeError(f"Falha na migration '{nome}': {e}") from e

        cur.close()
        conn.close()

    except psycopg2.OperationalError as e:
        logger.error(f"Sem conexao com o banco: {e}")
        # Nao impede o app de subir — banco pode estar offline
        return []

    return aplicadas_agora


def status(database_url: str) -> dict:
    """Retorna status das migrations para exibir no painel admin."""
    try:
        conn = _conn(database_url)
        cur = conn.cursor()
        _garantir_tabela_controle(cur)
        conn.commit()

        cur.execute("SELECT nome, aplicada_em FROM _migrations ORDER BY aplicada_em")
        aplicadas = [{"nome": r[0], "em": str(r[1])} for r in cur.fetchall()]

        arquivos = [f.stem for f in _listar_arquivos()]
        pendentes = [a for a in arquivos if a not in {m["nome"] for m in aplicadas}]

        cur.close()
        conn.close()
        return {"aplicadas": aplicadas, "pendentes": pendentes}
    except Exception as e:
        return {"erro": str(e), "aplicadas": [], "pendentes": []}
