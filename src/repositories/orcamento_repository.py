"""
ORCAMENTO REPOSITORY
CRUD de orçamentos no banco de dados.
"""

from typing import List, Optional
from src.models.orcamento import Orcamento
from .base_repository import BaseRepository

class OrcamentoRepository(BaseRepository[Orcamento]):
    """Acesso a dados de Orçamentos."""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.orcamentos = []
    
    def create(self, orcamento: Orcamento) -> Orcamento:
        """Cria um novo item de orçamento."""
        orcamento.id = len(self.orcamentos) + 1
        orcamento.calcular_total()
        self.orcamentos.append(orcamento)
        return orcamento
    
    def find_by_id(self, id: int) -> Optional[Orcamento]:
        """Busca um item pelo ID."""
        for orc in self.orcamentos:
            if orc.id == id:
                return orc
        return None
    
    def find_by_obra(self, id_obra: int) -> List[Orcamento]:
        """Busca todos os itens de uma obra."""
        return [o for o in self.orcamentos if o.id_obra == id_obra]
    
    def list_all(self) -> List[Orcamento]:
        """Lista todos os itens."""
        return self.orcamentos
    
    def update(self, id: int, orcamento: Orcamento) -> bool:
        """Atualiza um item."""
        for i, o in enumerate(self.orcamentos):
            if o.id == id:
                self.orcamentos[i] = orcamento
                return True
        return False
    
    def delete(self, id: int) -> bool:
        """Deleta um item."""
        self.orcamentos = [o for o in self.orcamentos if o.id != id]
        return True
    
    def calcular_orcamento_total(self, id_obra: int) -> float:
        """Calcula o orçamento total de uma obra."""
        return sum(o.preco_total for o in self.find_by_obra(id_obra))
