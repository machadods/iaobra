"""
DECORATORS
Decoradores úteis para a aplicação.
"""

import streamlit as st
from functools import wraps

def cache_resultado(ttl_seconds: int = 3600):
    """Decorator para cachear resultado de função."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Streamlit cache
            cached_func = st.cache_data(ttl=ttl_seconds)(func)
            return cached_func(*args, **kwargs)
        return wrapper
    return decorator

def require_session(chave: str, valor_padrao=None):
    """Decorator que garante que uma chave existe em session_state."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if chave not in st.session_state:
                st.session_state[chave] = valor_padrao
            return func(*args, **kwargs)
        return wrapper
    return decorator
