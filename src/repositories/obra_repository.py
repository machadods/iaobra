"""
OBRA REPOSITORY
CRUD de obras no banco de dados.
"""

from typing import List, Optional
from src.models.obra import Obra
from .base_repository import BaseRepository

class ObraRepository(BaseRepository[Obra]):
    """Acesso a dados de Obras."""
    
    def __init__(self, db_connection=None):
        """Inicializa o repository com uma conexão de BD."""
        self.db = db_connection
        self.obras = []  # Simulando BD em memória (Fase 1)
    
    def create(self, obra: Obra) -> Obra:
        """Cria uma nova obra."""
        # TODO: Implementar com SQLAlchemy quando BD estiver pronta
        obra.id = len(self.obras) + 1
        self.obras.append(obra)
        return obra
    
    def find_by_id(self, id: int) -> Optional[Obra]:
        """Busca uma obra pelo ID."""
        for obra in self.obras:
            if obra.id == id:
                return obra
        return None
    
    def list_all(self) -> List[Obra]:
        """Lista todas as obras."""
        return self.obras
    
    def find_by_status(self, status: str) -> List[Obra]:
        """Busca obras por status."""
        return [o for o in self.obras if o.status == status]
    
    def update(self, id: int, obra: Obra) -> bool:
        """Atualiza uma obra."""
        for i, o in enumerate(self.obras):
            if o.id == id:
                self.obras[i] = obra
                return True
        return False
    
    def delete(self, id: int) -> bool:
        """Deleta uma obra."""
        self.obras = [o for o in self.obras if o.id != id]
        return True
