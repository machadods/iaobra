"""
BASE REPOSITORY
Classe base com métodos CRUD genéricos.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Classe base para todos os repositories."""
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Cria uma nova entidade."""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        """Busca uma entidade pelo ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[T]:
        """Lista todas as entidades."""
        pass
    
    @abstractmethod
    def update(self, id: int, entity: T) -> bool:
        """Atualiza uma entidade."""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Deleta uma entidade."""
        pass
