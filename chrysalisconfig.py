"""
Configuration management for Chrysalis
"""
import os
from typing import Optional
from pydantic import BaseSettings, validator
import logging

logger = logging.getLogger(__name__)


class ChrysalisConfig(BaseSettings):
    """Configuration settings for Chrysalis system"""
    
    # API Keys
    anthropic_api_key: str = ""
    deepseek_api_key: str = ""
    
    # Firebase
    firebase_credentials_path: str = "./firebase-credentials.json"
    firebase_project_id: Optional[str] = None
    
    # Trading
    ccxt_exchange: str = "binance"
    ccxt_api_key: str = ""
    ccxt_secret: str = ""
    
    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    # System Parameters
    max_position_size: int = 100
    safety_circuit_failure_threshold: int = 3
    reflection_vector_model: str = "all-MiniLM-L6-v2"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "chrysalis.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @validator("firebase_credentials_path")
    def validate_firebase_creds(cls, v):
        if not os.path.exists(v):
            logger.error(f"Firebase credentials file not found: {v}")
            raise FileNotFoundError(f"Firebase credentials file not found: {v}")
        return v
    
    @validator("anthropic_api_key", "deepseek_api_key", "ccxt_api_key", "ccxt_secret")
    def validate_api_keys(cls, v, field):
        if not v and field.name in ["anthropic_api_key", "deepseek_api_key"]:
            logger.warning(f"{field.name} not set - LLM functionality will be limited")
        return v


# Global configuration instance
config = ChrysalisConfig()