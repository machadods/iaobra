"""
MODEL: Obra
Define a estrutura de uma obra de construção.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Obra:
    """Representa uma obra de construção."""
    
    id: Optional[int] = None
    nome: str = ""
    endereco: str = ""
    descricao: str = ""
    status: str = "em_andamento"  # em_andamento, paralisada, finalizada
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    proprietario: str = ""
    responsavel: str = ""
    orcamento_total: float = 0.0
    
    def __repr__(self):
        return f"Obra(id={self.id}, nome='{self.nome}', status='{self.status}')"
