"""
UTILS - Utilitários e Ferramentas
Funções helper, decoradores, logging, etc.
"""

from .logger import get_logger
from .validators import validar_email, validar_telefone
from .decorators import cache_resultado, require_session

__all__ = [
    "get_logger",
    "validar_email",
    "validar_telefone",
    "cache_resultado",
    "require_session",
]
