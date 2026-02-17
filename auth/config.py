"""Configuration settings for the authentication system"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars-"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./auth_system.db"
    
    # Application Configuration
    APP_NAME: str = "Nexus Auth API"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
