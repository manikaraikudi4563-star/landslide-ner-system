"""
Configuration management for NER-LEWS application.
Loads settings from environment variables with fallback defaults.
"""

import os
from typing import List

class Settings:
    PROJECT_NAME: str = "NER-LEWS: AI-Based Landslide Early Warning & Risk Monitoring System"
    VERSION: str = "2.6.0"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    IS_DEMO_MODE: bool = os.getenv("IS_DEMO_MODE", "true").lower() in ["true", "1", "yes"]
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Database
    _default_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "landslide_ner.db")
    if os.getenv("VERCEL"):
        import shutil
        _tmp_db = "/tmp/landslide_ner.db"
        if os.path.exists(_default_db) and not os.path.exists(_tmp_db):
            try:
                shutil.copy2(_default_db, _tmp_db)
            except Exception:
                pass
        DATABASE_URL: str = os.getenv("DATABASE_URL", _tmp_db)
    else:
        DATABASE_URL: str = os.getenv("DATABASE_URL", _default_db)
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Security & Auth (Demo configuration)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ner-lews-demo-insecure-secret-key-change-in-prod")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # Static directory
    STATIC_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static")

settings = Settings()
