"""
MODEL: Orcamento
Define materiais e custos de uma obra.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Orcamento:
    """Representa um item de orçamento."""
    
    id: Optional[int] = None
    id_obra: int = 0
    material: str = ""
    quantidade: float = 0.0
    unidade: str = "un"  # un, m², m³, kg, sacos, etc
    preco_unitario: float = 0.0
    preco_total: float = 0.0
    loja: str = ""
    data_cotacao: Optional[str] = None
    observacoes: str = ""
    
    def calcular_total(self):
        """Calcula o preço total do item."""
        self.preco_total = self.quantidade * self.preco_unitario
        return self.preco_total
    
    def __repr__(self):
        return f"Orcamento(material='{self.material}', qtd={self.quantidade}, total=R${self.preco_total:.2f})"
