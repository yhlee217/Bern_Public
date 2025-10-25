from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    # Server configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    debug_mode: bool = False

    # Model configuration
    model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model_cache_dir: str = "/tmp/models"
    max_text_length: int = 512

    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "json"

    # API configuration
    api_title: str = "AI Sentiment Analysis Service"
    api_version: str = "1.0.0"
    api_description: str = "Real-time text sentiment analysis API"

    # Performance configuration
    max_workers: int = 4
    request_timeout: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()