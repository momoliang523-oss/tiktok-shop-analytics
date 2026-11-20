"""
Application configuration management
"""
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "TikTok Shop Analytics"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tiktok_analytics"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_EXTENSIONS: list[str] = [".xlsx", ".xls", ".csv"]

    # TikTok API (Optional)
    TIKTOK_API_KEY: Optional[str] = None
    TIKTOK_API_SECRET: Optional[str] = None
    TIKTOK_SHOP_ID: Optional[str] = None
    TIKTOK_API_BASE_URL: str = "https://open-api.tiktokglobalshop.com"

    # Email (Optional for reports)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None

    # AWS S3 (Optional for file storage)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None

    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    # Data Directories
    DATA_DIR: str = "./data"
    IMPORTS_DIR: str = "./data/imports"
    EXPORTS_DIR: str = "./data/exports"
    TEMP_DIR: str = "./data/temporary"

    # US Market Configuration
    DEFAULT_CURRENCY: str = "USD"
    DEFAULT_TIMEZONE: str = "America/New_York"
    US_REGIONS: list[str] = ["west", "east", "midwest", "south"]
    US_GENERATIONS: list[str] = ["gen_z", "millennial", "gen_x", "boomer"]

    # Analysis Configuration
    MIN_DATA_POINTS_FOR_ANALYSIS: int = 10
    CLUSTERING_DEFAULT_N_CLUSTERS: int = 3
    RFM_SCORE_WEIGHTS: dict = {"recency": 0.2, "frequency": 0.3, "monetary": 0.5}

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
