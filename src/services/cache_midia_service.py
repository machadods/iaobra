"""
Serviço de Cache e Compressão de Mídia
Otimiza armazenamento e acesso a grandes volumes de dados
"""

import hashlib
import zlib
import gzip
import pickle
import json
from pathlib import Path
from typing import Any, Optional, Dict, Tuple
from datetime import datetime, timedelta
import diskcache as dc
from functools import wraps
import logging
from loguru import logger

class GerenciadorCache:
    """Gerencia cache de análises e compressão de dados"""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_path = Path(cache_dir)
        self.cache_path.mkdir(exist_ok=True)
        
        # Configurar cache em disco
        self.cache = dc.Cache(str(self.cache_path))
        
        self.logger = logger
        self.logger.add("logs/cache.log", rotation="500 MB")
        
        # Algoritmos de compressão suportados
        self.algoritmos = {
            "zlib": self._comprimir_zlib,
            "gzip": self._comprimir_gzip,
            "none": self._nao_comprimir
        }
    
    # ============================================================
    # COMPRESSÃO
    # ============================================================
    
    def _comprimir_zlib(self, dados: bytes) -> bytes:
        """Compressão com zlib (rápida)"""
        return zlib.compress(dados, level=6)
    
    def _comprimir_gzip(self, dados: bytes) -> bytes:
        """Compressão com gzip (mais compatível)"""
        return gzip.compress(dados, compresslevel=6)
    
    def _nao_comprimir(self, dados: bytes) -> bytes:
        """Sem compressão"""
        return dados
    
    def _descomprimir_zlib(self, dados: bytes) -> bytes:
        """Descompressão com zlib"""
        return zlib.decompress(dados)
    
    def _descomprimir_gzip(self, dados: bytes) -> bytes:
        """Descompressão com gzip"""
        return gzip.decompress(dados)
    
    def comprimir_dados(
        self, 
        dados: Any, 
        algoritmo: str = "zlib"
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Comprime dados e retorna estatísticas
        
        Args:
            dados: Dados a comprimir
            algoritmo: 'zlib', 'gzip' ou 'none'
        
        Returns:
            (dados_comprimidos, metadata)
        """
        # Serializar
        dados_serializados = pickle.dumps(dados)
        tamanho_original = len(dados_serializados)
        
        # Comprimir
        funcao_compressao = self.algoritmos.get(algoritmo, self._comprimir_zlib)
        dados_comprimidos = funcao_compressao(dados_serializados)
        tamanho_comprimido = len(dados_comprimidos)
        
        # Taxa de compressão
        taxa = (tamanho_original - tamanho_comprimido) / tamanho_original * 100 if tamanho_original > 0 else 0
        
        metadata = {
            "algoritmo": algoritmo,
            "tamanho_original": tamanho_original,
            "tamanho_comprimido": tamanho_comprimido,
            "taxa_compressao": round(taxa, 2),
            "data_compressao": datetime.now().isoformat()
        }
        
        self.logger.info(f"Dados comprimidos: {tamanho_original} -> {tamanho_comprimido} bytes ({taxa:.1f}%)")
        
        return dados_comprimidos, metadata
    
    def descomprimir_dados(
        self, 
        dados_comprimidos: bytes, 
        algoritmo: str = "zlib"
    ) -> Any:
        """Descomprime dados"""
        if algoritmo == "zlib":
            dados_serializados = self._descomprimir_zlib(dados_comprimidos)
        elif algoritmo == "gzip":
            dados_serializados = self._descomprimir_gzip(dados_comprimidos)
        else:
            dados_serializados = dados_comprimidos
        
        return pickle.loads(dados_serializados)
    
    # ============================================================
    # CACHE COM TTL
    # ============================================================
    
    def gerar_chave_cache(self, *args, **kwargs) -> str:
        """Gera chave de cache única baseada em argumentos"""
        chave_str = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(chave_str.encode()).hexdigest()
    
    def armazenar_cache(
        self, 
        chave: str, 
        valor: Any, 
        ttl_minutos: int = 60,
        comprimir: bool = True
    ) -> bool:
        """
        Armazena em cache com TTL
        
        Args:
            chave: Chave única de cache
            valor: Valor a cachear
            ttl_minutos: Tempo de vida em minutos
            comprimir: Se deve comprimir
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            valor_final = valor
            metadata = {"comprimido": False}
            
            if comprimir:
                valor_final, metadata = self.comprimir_dados(valor, "zlib")
                metadata["comprimido"] = True
            
            # Armazenar com TTL
            expire_time = datetime.now() + timedelta(minutes=ttl_minutos)
            self.cache.set(chave, valor_final, expire=ttl_minutos * 60)
            self.cache.set(f"{chave}:metadata", metadata, expire=ttl_minutos * 60)
            
            self.logger.info(f"Cache armazenado: {chave} (TTL: {ttl_minutos}min)")
            return True
        
        except Exception as e:
            self.logger.error(f"Erro ao armazenar cache: {e}")
            return False
    
    def recuperar_cache(self, chave: str) -> Optional[Any]:
        """Recupera valor do cache"""
        try:
            if chave not in self.cache:
                self.logger.debug(f"Cache miss: {chave}")
                return None
            
            valor = self.cache[chave]
            metadata = self.cache.get(f"{chave}:metadata", {})
            
            # Descomprimir se necessário
            if metadata.get("comprimido"):
                valor = self.descomprimir_dados(valor, metadata.get("algoritmo", "zlib"))
            
            self.logger.debug(f"Cache hit: {chave}")
            return valor
        
        except Exception as e:
            self.logger.error(f"Erro ao recuperar cache: {e}")
            return None
    
    def limpar_cache_expirado(self) -> int:
        """Remove entradas expiradas do cache"""
        # diskcache já limpa automaticamente, mas podemos forçar
        antes = len(self.cache)
        self.cache.clear_expired()
        depois = len(self.cache)
        removidos = antes - depois
        
        self.logger.info(f"Cache limpo: {removidos} entradas expiradas removidas")
        return removidos
    
    # ============================================================
    # DECORADOR PARA CACHE AUTOMÁTICO
    # ============================================================
    
    def cachear(self, ttl_minutos: int = 60, comprimir: bool = True):
        """
        Decorador para cachear resultado de função automaticamente
        
        Usage:
            @cache_manager.cachear(ttl_minutos=30)
            def minha_funcao(arg1, arg2):
                return resultado_custoso
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Gerar chave
                chave = self.gerar_chave_cache(func.__name__, *args, **kwargs)
                
                # Tentar recuperar do cache
                resultado_cache = self.recuperar_cache(chave)
                if resultado_cache is not None:
                    self.logger.debug(f"Usando resultado cacheado para {func.__name__}")
                    return resultado_cache
                
                # Executar função
                resultado = func(*args, **kwargs)
                
                # Armazenar em cache
                self.armazenar_cache(chave, resultado, ttl_minutos, comprimir)
                
                return resultado
            
            return wrapper
        return decorator
    
    # ============================================================
    # ESTATÍSTICAS DE CACHE
    # ============================================================
    
    def obter_stats_cache(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        return {
            "total_chaves": len(self.cache),
            "tamanho_total_bytes": sum(
                len(self.cache[k]) if isinstance(self.cache[k], bytes) else 0 
                for k in self.cache
            ),
            "cache_info": {
                "hits": self.cache.statistics()[0] if self.cache.statistics() else 0,
                "misses": self.cache.statistics()[1] if self.cache.statistics() else 0
            }
        }
    
    def exibir_stats(self):
        """Exibe estatísticas formatadas"""
        stats = self.obter_stats_cache()
        tamanho_mb = stats["tamanho_total_bytes"] / (1024 * 1024)
        print(f"""
        ============ CACHE STATS ============
        Total de Chaves: {stats['total_chaves']}
        Tamanho Total: {tamanho_mb:.2f} MB
        Cache Hits: {stats['cache_info']['hits']}
        Cache Misses: {stats['cache_info']['misses']}
        ====================================
        """)

# ============================================================
# COMPRESSOR DE MÍDIA
# ============================================================

class CompressorMidia:
    """Compressão otimizada para arquivos de mídia"""
    
    def __init__(self):
        self.logger = logger
        self.qualidade_presets = {
            "maxima": {"taxa_compressao": 1, "qualidade": 100},
            "alta": {"taxa_compressao": 0.8, "qualidade": 85},
            "media": {"taxa_compressao": 0.6, "qualidade": 70},
            "baixa": {"taxa_compressao": 0.4, "qualidade": 55},
        }
    
    def calcular_tamanho_reduzido(
        self, 
        tamanho_original: int, 
        preset: str = "media"
    ) -> int:
        """Calcula tamanho após compressão"""
        config = self.qualidade_presets.get(preset, self.qualidade_presets["media"])
        return int(tamanho_original * config["taxa_compressao"])
    
    def gerar_thumbnail(
        self, 
        caminho_arquivo: str, 
        largura: int = 300,
        altura: int = 200
    ) -> Optional[bytes]:
        """Gera thumbnail comprimido para preview rápido"""
        try:
            from PIL import Image
            
            img = Image.open(caminho_arquivo)
            img.thumbnail((largura, altura), Image.Resampling.LANCZOS)
            
            # Salvar em memória
            import io
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)
            
            return buffer.getvalue()
        
        except Exception as e:
            self.logger.error(f"Erro ao gerar thumbnail: {e}")
            return None
    
    def obter_hash_midia(self, caminho_arquivo: str) -> str:
        """Calcula hash MD5 de arquivo para deduplicação"""
        hash_md5 = hashlib.md5()
        
        try:
            with open(caminho_arquivo, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            
            return hash_md5.hexdigest()
        
        except Exception as e:
            self.logger.error(f"Erro ao calcular hash: {e}")
            return ""

# Instâncias globais
cache_manager = GerenciadorCache()
compressor_midia = CompressorMidia()
