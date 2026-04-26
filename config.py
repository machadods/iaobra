"""
CONFIGURAÇÕES GLOBAIS DO IAOBRAS v0.2.0
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(ENV_FILE)

# ============================================================
# DATABASE
# ============================================================
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:musashi@127.0.0.1:5434/iaobras_db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# ============================================================
# IA - OpenRouter / Gemini (gratuito)
# Crie sua chave em: https://openrouter.ai/keys
# ============================================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# ============================================================
# AUTENTICAÇÃO
# ============================================================
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "iaobras2024")
SECRET_KEY     = os.getenv("SECRET_KEY", "dev_insecure_key")

# ============================================================
# PIX — pagamento do plano Pro
# ============================================================
PIX_CHAVE = os.getenv("PIX_CHAVE", "")
PIX_NOME  = os.getenv("PIX_NOME",  "IAOBRA")
PIX_BANCO = os.getenv("PIX_BANCO", "")

# ============================================================
# STREAMLIT
# ============================================================
STREAMLIT_CONFIG = {
    "page_title": "IAOBRA - Mestre Digital",
    "page_icon": "🧱",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================
# APP
# ============================================================
APP_NAME = os.getenv("APP_NAME", "IAOBRA")
APP_VERSION = os.getenv("APP_VERSION", "0.2.0")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Diretórios
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "src"
DATABASE_DIR = BASE_DIR / "database"
UPLOADS_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"

UPLOADS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
