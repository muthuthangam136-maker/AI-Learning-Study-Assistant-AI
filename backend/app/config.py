import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Determine base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Learning & Study Assistant"
    VERSION: str = "1.0.0"
    
    # Mode
    DEMO_MODE: bool = True
    
    # LLM Settings (OpenAI-compatible)
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: str = ""
    
    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8001
    BACKEND_URL: str = "http://localhost:8001"
    
    # Storage & DB
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'data' / 'app.db'}"
    CHROMA_PATH: str = str(BASE_DIR / "data" / "chroma")
    KNOWLEDGE_BASE_DIR: str = str(BASE_DIR / "data" / "knowledge_base")
    
    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
os.makedirs(Path(settings.CHROMA_PATH), exist_ok=True)
os.makedirs(Path(settings.KNOWLEDGE_BASE_DIR), exist_ok=True)
os.makedirs(Path(settings.DATABASE_URL.replace("sqlite:///", "")).parent, exist_ok=True)
