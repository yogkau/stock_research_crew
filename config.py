"""Configuration management for stock research crew."""
from pathlib import Path
from typing import Optional
import os

class Config:
    # Paths
    BASE_DIR = Path(__file__).parent
    CACHE_DIR = BASE_DIR / ".cache"
    CACHE_FILE = CACHE_DIR / "cache.json"
    PROFILE_FILE = CACHE_DIR / "profile.json"
    
    # LLM Settings
    LLM_MODEL = os.getenv("LLM_MODEL", "ollama/mistral")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "120"))
    
    # Cache Settings
    CACHE_EXPIRY_HOURS = int(os.getenv("CACHE_EXPIRY_HOURS", "24"))
    MAX_CACHE_SIZE_MB = int(os.getenv("MAX_CACHE_SIZE_MB", "100"))
    
    # Performance
    ENABLE_PARALLEL_TASKS = os.getenv("ENABLE_PARALLEL_TASKS", "true").lower() == "true"
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Search
    SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
