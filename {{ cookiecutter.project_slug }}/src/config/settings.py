import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables desde un archivo .env si existe
BASE_DIR = Path(__file__).resolve().parents[2]
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# === ENTORNO ===
ENV = os.getenv("ENV", "development")

# === BASE PATHS ===
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
MODELS_DIR = Path(os.getenv("MODELS_DIR", BASE_DIR / "models"))
LOGS_DIR = Path(os.getenv("LOGS_DIR", BASE_DIR / "logs"))

# === BASE DE DATOS ===
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dsn": os.getenv("DB_DSN"),
    "lib_dir": os.getenv("DB_LIB_DIR"),

    "host": os.getenv("DB_HOST", "localhost"),
    "name": os.getenv("DB_NAME", "bd_test"),
    "port": os.getenv("DB_PORT", '5432')
}

# === API EXTERNA ===
API_CONFIG = {
    "url": os.getenv("API_URL"),
    "key": os.getenv("API_KEY"),
}

# === NOTIFICACIONES SLACK ===
SLACK_CONFIG = {
    "webhook": os.getenv("SLACK_WEBHOOK"),
    "channel": os.getenv("SLACK_CHANNEL", "#general"),
    "username": os.getenv("SLACK_USERNAME", "bot"),
}
