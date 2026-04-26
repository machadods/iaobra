"""
VALIDATORS
Funções de validação comuns.
"""

import re

def validar_email(email: str) -> bool:
    """Valida se é um email válido."""
    padrao = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(padrao, email) is not None

def validar_telefone(telefone: str) -> bool:
    """Valida se é um telefone válido (Brasil)."""
    apenas_numeros = re.sub(r'\D', '', telefone)
    return len(apenas_numeros) >= 10

def validar_nome_obra(nome: str) -> bool:
    """Valida nome da obra."""
    return len(nome.strip()) >= 3

def validar_endereco(endereco: str) -> bool:
    """Valida endereço."""
    return len(endereco.strip()) >= 10
