"""
AUTH SERVICE — usa tabela 'usuarios' no PostgreSQL
LGPD: senhas em hash SHA-256, bloqueio por tentativas, inputs sanitizados.
"""

import hashlib
import re
import logging
from typing import Optional, List
from src.models.usuario import Usuario
from src.utils.db_connection import db, banco_disponivel
from config import ADMIN_USERNAME, ADMIN_PASSWORD

MAX_TENTATIVAS = 5
logger = logging.getLogger("iaobras.auth")


class AuthService:
    def __init__(self):
        self._garantir_admin()

    # ------------------------------------------------------------------
    # Seguranca
    # ------------------------------------------------------------------
    @staticmethod
    def _hash(senha: str) -> str:
        return hashlib.sha256(senha.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def _sanitizar(valor: str) -> str:
        return re.sub(r"[<>&\"';\{\}\(\)\[\]]", "", valor).strip()[:100]

    # ------------------------------------------------------------------
    # Admin padrao
    # ------------------------------------------------------------------
    def _garantir_admin(self):
        if not banco_disponivel():
            return
        try:
            with db() as cur:
                cur.execute("SELECT id FROM usuarios WHERE tipo = 'admin' LIMIT 1")
                if cur.fetchone():
                    return
                cur.execute("""
                    INSERT INTO usuarios (nome, username, senha_hash, tipo)
                    VALUES (%s, %s, %s, 'admin')
                    ON CONFLICT (username) DO NOTHING
                """, ("Administrador", ADMIN_USERNAME, self._hash(ADMIN_PASSWORD)))
            logger.info("Admin padrao criado.")
        except Exception as e:
            logger.error(f"Erro ao garantir admin: {e}")

    # ------------------------------------------------------------------
    # Conversao linha -> Usuario
    # ------------------------------------------------------------------
    @staticmethod
    def _row(r) -> Usuario:
        return Usuario(
            id=r["id"],
            nome=r["nome"],
            username=r["username"],
            senha_hash=r["senha_hash"],
            tipo=r["tipo"],
            obras_ids=[],          # carregado sob demanda via obras_clientes
            tentativas_login=r["tentativas_login"],
            bloqueado=r["bloqueado"],
            ativo=r["ativo"],
        )

    def _obras_do_usuario(self, id_usuario: int) -> List[int]:
        with db() as cur:
            cur.execute(
                "SELECT id_obra FROM obras_clientes WHERE id_cliente = %s",
                (id_usuario,)
            )
            return [r["id_obra"] for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Autenticacao
    # ------------------------------------------------------------------
    def login(self, username: str, senha: str) -> Optional[Usuario]:
        username = self._sanitizar(username).lower()
        if not username or not senha:
            return None
        try:
            with db() as cur:
                cur.execute(
                    "SELECT * FROM usuarios WHERE username = %s AND ativo = TRUE",
                    (username,)
                )
                row = cur.fetchone()
                if not row:
                    return None

                u = self._row(row)
                if u.bloqueado:
                    return None

                if u.senha_hash == self._hash(senha):
                    cur.execute(
                        "UPDATE usuarios SET tentativas_login = 0 WHERE id = %s",
                        (u.id,)
                    )
                    u.obras_ids = self._obras_do_usuario(u.id)
                    logger.info(f"Login OK: {username} ({u.tipo})")
                    return u

                # Senha errada — incrementa tentativas
                novas = row["tentativas_login"] + 1
                bloquear = novas >= MAX_TENTATIVAS
                cur.execute(
                    "UPDATE usuarios SET tentativas_login = %s, bloqueado = %s WHERE id = %s",
                    (novas, bloquear, row["id"])
                )
                if bloquear:
                    logger.warning(f"Conta bloqueada: {username}")
                return None
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            return None

    def desbloquear(self, username: str) -> bool:
        try:
            with db() as cur:
                cur.execute(
                    "UPDATE usuarios SET bloqueado = FALSE, tentativas_login = 0 WHERE username = %s",
                    (username,)
                )
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def criar_usuario(self, nome: str, username: str, senha: str,
                      tipo: str, obras_ids: List[int] = None) -> Usuario:
        nome     = self._sanitizar(nome)
        username = self._sanitizar(username).lower()

        if not Usuario.validar_username(username):
            raise ValueError("Usuario invalido (3-30 chars, apenas letras/numeros/_/.)")
        if not Usuario.validar_senha(senha):
            raise ValueError("Senha muito curta (minimo 8 caracteres).")
        if tipo not in ("admin", "construtor", "cliente"):
            raise ValueError("Tipo invalido.")

        try:
            with db() as cur:
                cur.execute(
                    "SELECT id FROM usuarios WHERE username = %s", (username,)
                )
                if cur.fetchone():
                    raise ValueError(f"Usuario '{username}' ja existe.")

                cur.execute("""
                    INSERT INTO usuarios (nome, username, senha_hash, tipo)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (nome, username, self._hash(senha), tipo))
                novo_id = cur.fetchone()["id"]

                if obras_ids and tipo == "cliente":
                    for oid in obras_ids:
                        cur.execute(
                            "INSERT INTO obras_clientes (id_obra, id_cliente) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            (oid, novo_id)
                        )

            logger.info(f"Usuario criado: {username} ({tipo})")
            return Usuario(id=novo_id, nome=nome, username=username,
                           senha_hash=self._hash(senha), tipo=tipo,
                           obras_ids=obras_ids or [])
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Erro ao criar usuario: {e}") from e

    def criar_construtor(self, nome: str, username: str, senha: str) -> Usuario:
        return self.criar_usuario(nome, username, senha, "construtor")

    def criar_cliente(self, nome: str, username: str, senha: str,
                      obras_ids: List[int] = None) -> Usuario:
        return self.criar_usuario(nome, username, senha, "cliente", obras_ids)

    def listar_construtores(self) -> List[Usuario]:
        return self._listar_por_tipo("construtor")

    def listar_clientes(self) -> List[Usuario]:
        return self._listar_por_tipo("cliente")

    def listar_todos(self) -> List[Usuario]:
        try:
            with db() as cur:
                cur.execute(
                    "SELECT * FROM usuarios WHERE tipo != 'admin' ORDER BY criado_em"
                )
                return [self._row(r) for r in cur.fetchall()]
        except Exception:
            return []

    def _listar_por_tipo(self, tipo: str) -> List[Usuario]:
        try:
            with db() as cur:
                cur.execute(
                    "SELECT * FROM usuarios WHERE tipo = %s ORDER BY criado_em", (tipo,)
                )
                return [self._row(r) for r in cur.fetchall()]
        except Exception:
            return []

    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        try:
            with db() as cur:
                cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
                row = cur.fetchone()
                if not row:
                    return None
                u = self._row(row)
                u.obras_ids = self._obras_do_usuario(u.id)
                return u
        except Exception:
            return None

    def atualizar_obras_cliente(self, username: str, obras_ids: List[int]) -> bool:
        u = self.buscar_por_username(username)
        if not u:
            return False
        try:
            with db() as cur:
                cur.execute("DELETE FROM obras_clientes WHERE id_cliente = %s", (u.id,))
                for oid in obras_ids:
                    cur.execute(
                        "INSERT INTO obras_clientes (id_obra, id_cliente) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (oid, u.id)
                    )
            return True
        except Exception:
            return False

    def desativar_usuario(self, username: str, solicitante_tipo: str) -> bool:
        u = self.buscar_por_username(username)
        if not u or u.tipo == "admin":
            return False
        if solicitante_tipo != "admin" and u.tipo == "construtor":
            return False
        try:
            with db() as cur:
                cur.execute("UPDATE usuarios SET ativo = FALSE WHERE id = %s", (u.id,))
            return True
        except Exception:
            return False
