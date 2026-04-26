"""
REPOSITORIES - Acesso a Dados (DAO Pattern)
Implementa CRUD para cada entidade.
"""

from .obra_repository import ObraRepository
from .diario_repository import DiarioRepository
from .orcamento_repository import OrcamentoRepository
from .sobras_repository import SobrasRepository

__all__ = [
    "ObraRepository",
    "DiarioRepository",
    "OrcamentoRepository",
    "SobrasRepository",
]
