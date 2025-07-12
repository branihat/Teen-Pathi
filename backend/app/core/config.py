from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # MongoDB Database
    MONGODB_URL: str
    DATABASE_NAME: str = "betting_db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Payment Gateway
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    
    # Email Configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
    # Application Settings
    APP_NAME: str = "Betting Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Admin Settings
    SUPER_ADMIN_EMAIL: str = "admin@betting.com"
    SUPER_ADMIN_PASSWORD: str = "SuperAdmin123!"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
