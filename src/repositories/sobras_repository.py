"""
SOBRAS REPOSITORY
CRUD de sobras (Mercado de Sobras) no banco de dados.
"""

from typing import List, Optional
from src.models.sobras import Sobras
from .base_repository import BaseRepository

class SobrasRepository(BaseRepository[Sobras]):
    """Acesso a dados de Sobras."""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.sobras = []
    
    def create(self, sobra: Sobras) -> Sobras:
        """Publica uma nova sobra."""
        sobra.id = len(self.sobras) + 1
        self.sobras.append(sobra)
        return sobra
    
    def find_by_id(self, id: int) -> Optional[Sobras]:
        """Busca uma sobra pelo ID."""
        for sob in self.sobras:
            if sob.id == id:
                return sob
        return None
    
    def find_by_obra(self, id_obra: int) -> List[Sobras]:
        """Lista sobras de uma obra."""
        return [s for s in self.sobras if s.id_obra == id_obra]
    
    def list_disponivel(self) -> List[Sobras]:
        """Lista sobras disponíveis para venda."""
        return [s for s in self.sobras if s.status == "disponivel"]
    
    def list_all(self) -> List[Sobras]:
        """Lista todas as sobras."""
        return self.sobras
    
    def update(self, id: int, sobra: Sobras) -> bool:
        """Atualiza uma sobra."""
        for i, s in enumerate(self.sobras):
            if s.id == id:
                self.sobras[i] = sobra
                return True
        return False
    
    def delete(self, id: int) -> bool:
        """Deleta uma sobra."""
        self.sobras = [s for s in self.sobras if s.id != id]
        return True
