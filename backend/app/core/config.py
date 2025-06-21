from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings configuration"""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GitLab GenAI Chatbot"
    VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database
    DATABASE_URL: str = "sqlite:///./chatbot.db"

    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "llama3-8b-8192"
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.7

    # RAG Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    SIMILARITY_THRESHOLD: float = 0.5
    MAX_DOCUMENTS: int = 5

    # Vector Database
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Scraping Configuration
    GITLAB_HANDBOOK_URL: str = "https://about.gitlab.com/handbook/"
    GITLAB_DIRECTION_URL: str = "https://about.gitlab.com/direction/"
    SCRAPING_DELAY: float = 1.0
    MAX_PAGES: int = 100

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
