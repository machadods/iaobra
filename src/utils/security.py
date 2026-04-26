"""
SECURITY — validacoes e hardening
Checklist executado na subida do app.
"""

import os
import re
import logging
from config import SECRET_KEY, OPENROUTER_API_KEY, DATABASE_URL

logger = logging.getLogger("iaobras.security")

ALERTAS = []


def _alerta(msg: str):
    ALERTAS.append(msg)
    logger.warning(f"[SECURITY] {msg}")


def checar_ambiente() -> list[str]:
    """
    Retorna lista de alertas de seguranca.
    Lista vazia = tudo ok.
    """
    ALERTAS.clear()

    # Chave secreta fraca
    if SECRET_KEY in ("dev_insecure_key", "", "iaobra_troque_esta_chave_por_algo_aleatorio_2024"):
        _alerta("SECRET_KEY esta com valor padrao. Troque por uma chave aleatoria no .env")

    # API key exposta em logs (nao logar)
    if OPENROUTER_API_KEY and len(OPENROUTER_API_KEY) > 10:
        pass  # presente e parece valida — nao logar o valor
    elif not OPENROUTER_API_KEY:
        _alerta("OPENROUTER_API_KEY nao configurada. IA desativada.")

    # DATABASE_URL com senha default
    if "password" in DATABASE_URL or "user:pass" in DATABASE_URL:
        _alerta("DATABASE_URL parece ter credenciais de exemplo. Verifique o .env")

    # DEBUG em producao
    if os.getenv("DEBUG", "True").lower() == "true":
        if os.getenv("ENV", "dev") == "prod":
            _alerta("DEBUG=True em ambiente de producao. Desative no .env")

    return list(ALERTAS)


def sanitizar_texto(texto: str, max_len: int = 5000) -> str:
    """Remove caracteres perigosos e limita tamanho."""
    texto = re.sub(r"[<>{}|\\`]", "", texto)
    return texto[:max_len].strip()


def validar_arquivo(nome: str, tipos_permitidos: set = None) -> bool:
    """Valida extensao de arquivo de upload."""
    if tipos_permitidos is None:
        tipos_permitidos = {".jpg", ".jpeg", ".png", ".pdf", ".mp4", ".mp3", ".wav"}
    ext = os.path.splitext(nome.lower())[1]
    return ext in tipos_permitidos


def mascarar_chave(chave: str) -> str:
    """Mascara chave de API para exibicao segura."""
    if not chave or len(chave) < 8:
        return "****"
    return chave[:6] + "..." + chave[-4:]
