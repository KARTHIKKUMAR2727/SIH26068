import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "WeatherGPT"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    JWT_SECRET: str = "weathergpt-production-secure-jwt-key-2026-supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = "weathergpt"
    
    # Weather Provider ("openmeteo", "demo", "openweather")
    WEATHER_PROVIDER: str = os.getenv("WEATHER_PROVIDER", "openmeteo")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    
    # NWP Provider ("openmeteo_nwp", "gfs", "demo")
    NWP_PROVIDER: str = os.getenv("NWP_PROVIDER", "openmeteo_nwp")
    NWP_API_URL: str = os.getenv("NWP_API_URL", "https://api.open-meteo.com/v1/forecast")
    
    # LLM Configuration ("grounded_local", "openai", "gemini", "ollama")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    
    # Geocoding
    GEOCODING_PROVIDER: str = os.getenv("GEOCODING_PROVIDER", "openmeteo")
    GEOCODING_API_KEY: str = os.getenv("GEOCODING_API_KEY", "")
    
    # Demo Mode: When True or when providers fail, fallback cleanly and mark simulated
    FORCE_DEMO_MODE: bool = os.getenv("FORCE_DEMO_MODE", "false").lower() == "true"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "*"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
