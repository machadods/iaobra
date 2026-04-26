"""
LOGGER
Sistema de logging centralizado.
"""

import logging
from pathlib import Path

# Criar diretório de logs
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """Cria e retorna um logger configurado."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.FileHandler(LOG_DIR / "iaobras.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger
