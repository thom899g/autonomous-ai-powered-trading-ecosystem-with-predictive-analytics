"""
Configuration management for the trading ecosystem.
Uses Pydantic for validation and environment variable handling.
"""
import os
from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

load_dotenv()

class TradingConfig(BaseSettings):
    """Trading system configuration with validation."""
    
    # Firebase Configuration
    firebase_project_id: str = Field(..., env="FIREBASE_PROJECT_ID")
    firebase_service_account_path: str = Field(
        default="./service-account-key.json", 
        env="FIREBASE_SERVICE_ACCOUNT_PATH"
    )
    firebase_database_url: str = Field(..., env="FIREBASE_DATABASE_URL")
    
    # Exchange Configuration
    exchange_name: str = "binance"
    binance_api_key: Optional[str] = Field(None, env="BINANCE_API_KEY")
    binance_api_secret: Optional[str] = Field(None, env="BINANCE_API_SECRET")
    exchange_timeout: int = 30000  # ms
    
    # Trading Parameters
    max_position_size: float = Field(0.1, ge=0.01, le=1.0, env="MAX_POSITION_SIZE")
    max_daily_loss: float = Field(0.05, ge=0.01, le=0.5, env="MAX_DAILY_LOSS")
    risk_per_trade: float = Field(0.02, ge=0.001, le=0.1, env="RISK_PER_TRADE")
    
    # Model Configuration
    model_retrain_hours: int = Field(24, ge=1, env="MODEL_RETRAIN_HOURS")
    prediction_confidence_threshold: float = Field(
        0.7, ge=0.5, le=0.95, env="PREDICTION_CONFIDENCE_THRESHOLD"
    )
    
    # Data Configuration
    data_update_interval: int = 60  # seconds
    max_data_points: int = 10000
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/trading_system.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @validator("firebase_service_account_path")
    def validate_service_account_path(cls, v):
        """Ensure Firebase service account file exists."""
        if not os.path.exists(v):
            raise FileNotFoundError(
                f"Firebase service account file not found: {v}"
            )
        return v
    
    @validator("binance_api_key", "binance_api_secret")
    def validate_exchange_credentials(cls, v, values):
        """Validate exchange credentials if exchange is configured."""
        if values.get("exchange_name") == "binance" and not v:
            raise ValueError(
                "Binance API credentials required when using binance exchange"
            )
        return v

# Global configuration instance
config = TradingConfig()