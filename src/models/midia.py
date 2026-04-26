"""
Modelo de Mídia - Suporta áudio, vídeo, imagem
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class TipoMidia(str, Enum):
    """Tipos de mídia suportados"""
    IMAGEM = "imagem"
    VIDEO = "video"
    AUDIO = "audio"

@dataclass
class Midia:
    """Representa um arquivo de mídia (imagem, vídeo ou áudio)"""
    id: Optional[int] = None
    id_obra: int = 0
    id_diario: Optional[int] = None
    
    # Metadados Básicos
    tipo_midia: TipoMidia = TipoMidia.IMAGEM
    nome_arquivo: str = ""
    caminho_local: Optional[str] = None
    url_s3: Optional[str] = None
    
    # Metadados Técnicos
    tamanho_bytes: Optional[int] = None
    duracao_segundos: Optional[int] = None
    largura_pixels: Optional[int] = None
    altura_pixels: Optional[int] = None
    formato: Optional[str] = None
    codec_video: Optional[str] = None
    codec_audio: Optional[str] = None
    taxa_bits_video: Optional[int] = None
    taxa_bits_audio: Optional[int] = None
    fps: Optional[int] = None
    resolucao: Optional[str] = None
    
    # Processamento
    hash_md5: Optional[str] = None
    processada: bool = False
    data_processamento: Optional[datetime] = None
    metadata_ia: Optional[Dict[str, Any]] = None
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    data_captura: Optional[datetime] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
    
    def __post_init__(self):
        if self.criado_em is None:
            self.criado_em = datetime.now()
        if self.atualizado_em is None:
            self.atualizado_em = datetime.now()

@dataclass
class ExtrAcaoAudio:
    """Resultado da extração e análise de áudio"""
    id: Optional[int] = None
    id_midia: int = 0
    
    # Arquivo
    caminho_audio: Optional[str] = None
    url_s3_audio: Optional[str] = None
    tamanho_bytes: Optional[int] = None
    
    # Análise
    transcricao: Optional[str] = None
    idioma: Optional[str] = None
    confianca_transcricao: Optional[float] = None
    emocoes: Optional[Dict[str, Any]] = None
    palavras_chave: List[str] = field(default_factory=list)
    duracao_segundos: Optional[int] = None
    
    # Processamento
    processada: bool = False
    data_processamento: Optional[datetime] = None
    criado_em: Optional[datetime] = None

@dataclass
class AnaliseImagem:
    """Análise detalhada de imagem via IA"""
    id: Optional[int] = None
    id_midia: int = 0
    
    # Detecções
    objetos_detectados: Optional[Dict[str, Any]] = None
    pessoas_detectadas: Optional[int] = None
    facial_landmarks: Optional[Dict[str, Any]] = None
    qualidade_imagem: Optional[float] = None
    iluminacao: Optional[float] = None
    
    # Progressão da Obra
    fase_obra: Optional[str] = None
    progresso_visual: Optional[float] = None
    areas_criticas: Optional[Dict[str, Any]] = None
    
    # Cor
    paleta_cores: Optional[Dict[str, Any]] = None
    dominancia_cor: Optional[str] = None
    
    # Confiança
    confianca_geral: Optional[float] = None
    processada: bool = False
    data_processamento: Optional[datetime] = None
    criado_em: Optional[datetime] = None

@dataclass
class AnaliseVideo:
    """Análise detalhada de vídeo via IA"""
    id: Optional[int] = None
    id_midia: int = 0
    
    # Análise Temporal
    quadros_por_segundo: Optional[int] = None
    quadros_totais: Optional[int] = None
    mudanca_cena_timestamp: List[int] = field(default_factory=list)
    
    # Detecções
    objetos_por_frame: Optional[Dict[str, Any]] = None
    atividades_detectadas: List[str] = field(default_factory=list)
    pessoas_por_timestamp: List[int] = field(default_factory=list)
    
    # Resumo
    resumo_frames: Optional[Dict[str, Any]] = None
    thumbnail_timestamp: Optional[int] = None
    cenas_principais: Optional[Dict[str, Any]] = None
    
    # Movimento
    velocidade_media: Optional[float] = None
    areas_movimento: Optional[Dict[str, Any]] = None
    
    # Processamento
    processada: bool = False
    data_processamento: Optional[datetime] = None
    criado_em: Optional[datetime] = None

@dataclass
class StatsObra:
    """Estatísticas agregadas de uma obra"""
    id: Optional[int] = None
    id_obra: int = 0
    
    # Contadores
    total_midias: int = 0
    total_imagens: int = 0
    total_videos: int = 0
    total_audios: int = 0
    
    # Temporal
    data_inicio_obra: Optional[datetime] = None
    progresso_percentual: Optional[float] = None
    dias_passados: Optional[int] = None
    dias_planejados: Optional[int] = None
    atraso_dias: Optional[int] = None
    
    # Distribuição
    imagens_por_dia: Optional[float] = None
    videos_por_dia: Optional[float] = None
    tamanho_total_mb: Optional[float] = None
    
    # Performance
    velocidade_upload_mbps: Optional[float] = None
    tempo_processamento_medio_segundos: Optional[int] = None
    
    # IA
    confianca_progresso_media: Optional[float] = None
    anomalias_detectadas: int = 0
    ultimas_anomalias: Optional[Dict[str, Any]] = None
    
    atualizado_em: Optional[datetime] = None

@dataclass
class TimelineStats:
    """Estatísticas ao longo da timeline da obra"""
    id: Optional[int] = None
    id_obra: int = 0
    
    # Período
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    
    # Métricas Diárias
    midias_por_dia: List[int] = field(default_factory=list)
    progresso_diario: List[float] = field(default_factory=list)
    qualidade_media_diaria: List[float] = field(default_factory=list)
    
    # Velocidade
    velocidade_media_percentual_por_dia: Optional[float] = None
    velocidade_variancia: Optional[float] = None
    velocidade_desvio_padrao: Optional[float] = None
    
    # Padrões
    padrao_atividade: Optional[str] = None
    pico_atividade_hora: Optional[str] = None
    dia_mais_produtivo: Optional[str] = None
    
    # Previsões
    data_conclusao_prevista: Optional[datetime] = None
    confianca_previsao: Optional[float] = None
    
    criado_em: Optional[datetime] = None

@dataclass
class EventoObra:
    """Evento importante detectado na obra"""
    id: Optional[int] = None
    id_obra: int = 0
    id_midia: Optional[int] = None
    
    tipo_evento: str = ""
    descricao: Optional[str] = None
    severidade: Optional[str] = None
    
    timestamp_evento: Optional[datetime] = None
    criado_em: Optional[datetime] = None
    
    confianca: Optional[float] = None
    recomendacoes: List[str] = field(default_factory=list)
