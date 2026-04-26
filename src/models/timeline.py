"""
MODEL: Timeline
Define snapshots temporais da obra (Fase 4+).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Timeline:
    """Representa um snapshot no tempo de uma obra."""
    
    id: Optional[int] = None
    id_obra: int = 0
    timestamp: Optional[datetime] = None
    fase: str = ""  # fundação, estrutura, alvenaria, cobertura, etc
    progresso_percentual: float = 0.0
    imagens: List[str] = None  # Lista de caminhos
    video_360: Optional[str] = None  # Caminho do vídeo 360°
    metatags: dict = None  # Metadados customizados
    
    def __post_init__(self):
        if self.imagens is None:
            self.imagens = []
        if self.metatags is None:
            self.metatags = {}
    
    def __repr__(self):
        return f"Timeline(id_obra={self.id_obra}, fase='{self.fase}', progresso={self.progresso_percentual}%)"
