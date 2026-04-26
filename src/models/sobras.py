"""
MODEL: Sobras
Define materiais que sobraram (Mercado de Sobras).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Sobras:
    """Representa um item de sobra disponível para venda."""
    
    id: Optional[int] = None
    id_obra: int = 0
    material: str = ""
    quantidade: float = 0.0
    unidade: str = "un"
    preco: float = 0.0
    descricao: str = ""
    foto: Optional[str] = None  # Caminho da imagem
    status: str = "disponivel"  # disponivel, vendido
    data_publicacao: Optional[datetime] = None
    data_venda: Optional[datetime] = None
    vendedor: str = ""
    
    def __repr__(self):
        return f"Sobras(material='{self.material}', qtd={self.quantidade}, preco=R${self.preco:.2f})"
