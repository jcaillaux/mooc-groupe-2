import os
from pathlib import Path
from dotenv import load_dotenv


# Path
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)
POSTGRES_URI = os.getenv("POSTGRES_URI")
DB_SCHEMA = os.getenv("DB_SCHEMA")

# PostgreSQL configuration Cyril
DATABASE_URL = os.getenv("url")
SCHEMA = os.getenv("SCHEMA")

#MongoDB configuration Cyril
MONGO_URL = os.getenv("urlmongoDB")

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Mistral API configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")



VECTOR_DIMENSION = 3072

# FastAPI configuration
HOST = "localhost"
PORT = 8000
RELOAD = True
