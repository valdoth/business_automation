from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Version
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Business Process Automation API"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI-Powered Business Process Automation"
    
    # Neo4j Settings
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    
    # MinIO Settings
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str
    MINIO_SECURE: bool = False
    
    # AI Settings
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-3.5-turbo"  # Default model
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 