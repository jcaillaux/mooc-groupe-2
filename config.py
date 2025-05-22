import os
from pathlib import Path
from dotenv import load_dotenv


# Path
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Loading environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

# PostgreSQL configuration Cyril
DATABASE_URL = "postgresql://postgres:moocproject@localhost:5432/postgres"#os.getenv("url")
SCHEMA = "public"#os.getenv("SCHEMA")

# MongoDB configuration Cyril

#MONGO_URL = os.getenv("urlmongoDB")
MONGO_URL="mongodb://localhost:27017/"
MONGO_DB_NAME = "G2"
MONGO_COLLECTION_ORIGINAL = "forum_original"
MONGO_COLLECTION_CLEANED = "extracted_content"
# MONGO_COLLECTION_CLEANED = "documents"

# Pgvector
VECTOR_DIMENSION = 384

# Paramètres service RAG
NB_MESSAGES_PROPOSES = 10

# FastAPI configuration
HOST = "localhost"
PORT = 7860
RELOAD = True
