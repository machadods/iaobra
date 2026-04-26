"""
MODEL: Usuario
Tipos: admin | construtor | cliente
"""

import re
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Usuario:
    id: Optional[int] = None
    nome: str = ""
    username: str = ""
    senha_hash: str = ""
    tipo: str = "cliente"           # "admin" | "construtor" | "cliente"
    obras_ids: List[int] = field(default_factory=list)
    tentativas_login: int = 0       # controle de brute force
    bloqueado: bool = False
    ativo: bool = True

    # Compatibilidade com codigo antigo
    @property
    def perfil(self) -> str:
        return self.tipo

    def is_admin(self) -> bool:
        return self.tipo == "admin"

    def is_construtor(self) -> bool:
        return self.tipo == "construtor"

    def is_cliente(self) -> bool:
        return self.tipo == "cliente"

    # Manter compatibilidade
    def is_mestre(self) -> bool:
        return self.tipo in ("admin", "construtor")

    def pode_ver_obra(self, obra_id: int) -> bool:
        if self.tipo in ("admin", "construtor"):
            return True
        return obra_id in self.obras_ids

    @staticmethod
    def validar_username(username: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_\.]{3,30}$', username))

    @staticmethod
    def validar_senha(senha: str) -> bool:
        return len(senha) >= 8
