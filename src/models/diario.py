"""
MODEL: Diario
Define os registros diários de uma obra.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Diario:
    """Representa um registro diário de uma obra."""
    
    id: Optional[int] = None
    id_obra: int = 0
    data_registro: Optional[datetime] = None
    registro_texto: str = ""
    fotos: List[str] = field(default_factory=list)  # Caminhos dos arquivos
    videos: List[str] = field(default_factory=list)
    audio: Optional[str] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def __repr__(self):
        return f"Diario(id={self.id}, id_obra={self.id_obra}, data={self.data_registro})"
