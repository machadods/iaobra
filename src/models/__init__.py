"""
MODELS - Entidades do domínio
Define as classes que representam os dados do sistema.
"""

from .obra import Obra
from .diario import Diario
from .orcamento import Orcamento
from .sobras import Sobras
from .timeline import Timeline

__all__ = ["Obra", "Diario", "Orcamento", "Sobras", "Timeline"]
