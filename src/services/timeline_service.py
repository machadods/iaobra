"""
TIMELINE SERVICE
Simulação temporal da obra (Fase 4+).
Placeholder para futuras implementações.
"""

from typing import List, Optional
from datetime import datetime
from src.models.timeline import Timeline

class TimelineService:
    """Serviço para gerenciar timeline temporal da obra."""
    
    def __init__(self):
        """Inicializa serviço de timeline."""
        self.snapshots = []
        self.enabled = False  # Será habilitado na Fase 4
    
    def criar_snapshot(
        self,
        id_obra: int,
        fase: str,
        progresso_percentual: float,
        imagens: List[str] = None,
        video_360: str = None,
    ) -> Timeline:
        """Cria um snapshot no tempo (Fase 4+)."""
        # TODO: Implementar na Fase 4
        timeline = Timeline(
            id_obra=id_obra,
            fase=fase,
            progresso_percentual=progresso_percentual,
            imagens=imagens or [],
            video_360=video_360,
            timestamp=datetime.now(),
        )
        return timeline
    
    def listar_timeline(self, id_obra: int) -> List[Timeline]:
        """Lista timeline de uma obra (Fase 4+)."""
        # TODO: Implementar na Fase 4
        return []
    
    def navegar_tempo(self, id_obra: int, timestamp: datetime) -> Optional[Timeline]:
        """Navega até um ponto específico no tempo (Fase 4+)."""
        # TODO: Implementar na Fase 4
        return None
    
    def gerar_video_simulacao(self, id_obra: int) -> str:
        """Gera vídeo de simulação temporal (Fase 4+)."""
        # TODO: Implementar na Fase 4
        return "Simulação temporal será disponível na Fase 4"
