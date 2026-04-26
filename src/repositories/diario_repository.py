"""
DIARIO REPOSITORY
CRUD de registros diários no banco de dados.
"""

from typing import List, Optional
from src.models.diario import Diario
from .base_repository import BaseRepository

class DiarioRepository(BaseRepository[Diario]):
    """Acesso a dados de Diários."""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.registros = []  # Simulando BD em memória (Fase 1)
    
    def create(self, diario: Diario) -> Diario:
        """Cria um novo registro diário."""
        diario.id = len(self.registros) + 1
        self.registros.append(diario)
        return diario
    
    def find_by_id(self, id: int) -> Optional[Diario]:
        """Busca um registro pelo ID."""
        for reg in self.registros:
            if reg.id == id:
                return reg
        return None
    
    def find_by_obra(self, id_obra: int) -> List[Diario]:
        """Busca todos os registros de uma obra."""
        return [r for r in self.registros if r.id_obra == id_obra]
    
    def list_all(self) -> List[Diario]:
        """Lista todos os registros."""
        return self.registros
    
    def update(self, id: int, diario: Diario) -> bool:
        """Atualiza um registro."""
        for i, r in enumerate(self.registros):
            if r.id == id:
                self.registros[i] = diario
                return True
        return False
    
    def delete(self, id: int) -> bool:
        """Deleta um registro."""
        self.registros = [r for r in self.registros if r.id != id]
        return True
