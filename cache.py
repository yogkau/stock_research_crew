"""Improved caching with expiration and size management."""
from pathlib import Path
import json
from datetime import datetime, timedelta
import hashlib
import logging
from typing import Optional, Dict, Any
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self):
        self._ensure_cache_dir()
        self._cache_data: Optional[Dict] = None
        self._profile_data: Optional[Dict] = None
    
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist."""
        try:
            Config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            if not Config.CACHE_FILE.exists():
                Config.CACHE_FILE.write_text(json.dumps({"final": {}, "prompts": {}}))
            if not Config.PROFILE_FILE.exists():
                Config.PROFILE_FILE.write_text(json.dumps({"calls": []}))
        except Exception as e:
            logger.error(f"Failed to initialize cache: {e}")
    
    def _load_cache(self) -> Dict:
        """Load cache with in-memory caching."""
        if self._cache_data is None:
            try:
                self._cache_data = json.loads(Config.CACHE_FILE.read_text())
            except Exception as e:
                logger.error(f"Failed to load cache: {e}")
                self._cache_data = {"final": {}, "prompts": {}}
        return self._cache_data
    
    def _save_cache(self, data: Dict):
        """Save cache and update in-memory copy."""
        try:
            self._check_cache_size()
            Config.CACHE_FILE.write_text(json.dumps(data, indent=2))
            self._cache_data = data
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def _check_cache_size(self):
        """Remove old entries if cache exceeds size limit."""
        try:
            size_mb = Config.CACHE_FILE.stat().st_size / (1024 * 1024)
            if size_mb > Config.MAX_CACHE_SIZE_MB:
                logger.warning(f"Cache size {size_mb:.2f}MB exceeds limit, cleaning...")
                self._clean_old_entries()
        except Exception as e:
            logger.error(f"Failed to check cache size: {e}")
    
    def _clean_old_entries(self):
        """Remove entries older than expiry time."""
        data = self._load_cache()
        cutoff = datetime.utcnow() - timedelta(hours=Config.CACHE_EXPIRY_HOURS)
        
        # Clean final results
        finals = data.get("final", {})
        data["final"] = {
            k: v for k, v in finals.items()
            if self._is_recent(v.get("saved_at"), cutoff)
        }
        
        # Clean prompt cache
        prompts = data.get("prompts", {})
        data["prompts"] = {
            k: v for k, v in prompts.items()
            if self._is_recent(v.get("saved_at"), cutoff)
        }
        
        self._save_cache(data)
        logger.info(f"Cleaned cache: {len(finals) - len(data['final'])} final, {len(prompts) - len(data['prompts'])} prompt entries removed")
    
    def _is_recent(self, timestamp_str: Optional[str], cutoff: datetime) -> bool:
        """Check if timestamp is more recent than cutoff."""
        if not timestamp_str:
            return False
        try:
            ts = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return ts > cutoff
        except Exception:
            return False
    
    def get_cached_result(self, stock: str) -> Optional[str]:
        """Get cached final result for stock."""
        data = self._load_cache()
        entry = data.get("final", {}).get(stock)
        if entry and self._is_recent(entry.get("saved_at"), 
                                     datetime.utcnow() - timedelta(hours=Config.CACHE_EXPIRY_HOURS)):
            logger.info(f"Cache hit for stock: {stock}")
            return entry.get("result")
        return None
    
    def save_result(self, stock: str, result: str):
        """Save final result for stock."""
        data = self._load_cache()
        finals = data.get("final", {})
        finals[stock] = {
            "result": result,
            "saved_at": datetime.utcnow().isoformat() + "Z"
        }
        data["final"] = finals
        self._save_cache(data)
    
    def _prompt_key(self, prompt: str, model: str, temperature: float) -> str:
        """Generate cache key including temperature."""
        key = f"{model}|{temperature}|{prompt}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()
    
    def get_prompt_cache(self, prompt: str, model: str, temperature: float = 0.2) -> Optional[str]:
        """Get cached prompt response."""
        data = self._load_cache()
        prompts = data.get("prompts", {})
        entry = prompts.get(self._prompt_key(prompt, model, temperature))
        if entry and self._is_recent(entry.get("saved_at"),
                                     datetime.utcnow() - timedelta(hours=Config.CACHE_EXPIRY_HOURS)):
            return entry.get("response")
        return None
    
    def save_prompt_cache(self, prompt: str, model: str, temperature: float, response: str):
        """Save prompt response to cache."""
        data = self._load_cache()
        prompts = data.get("prompts", {})
        prompts[self._prompt_key(prompt, model, temperature)] = {
            "model": model,
            "temperature": temperature,
            "prompt": prompt[:500],  # Truncate for storage
            "response": response,
            "saved_at": datetime.utcnow().isoformat() + "Z"
        }
        data["prompts"] = prompts
        self._save_cache(data)
    
    def log_profile(self, call_info: Dict[str, Any]):
        """Log performance profile."""
        try:
            if self._profile_data is None:
                self._profile_data = json.loads(Config.PROFILE_FILE.read_text())
            
            calls = self._profile_data.get("calls", [])
            calls.append(call_info)
            self._profile_data["calls"] = calls
            
            Config.PROFILE_FILE.write_text(json.dumps(self._profile_data, indent=2))
        except Exception as e:
            logger.error(f"Failed to log profile: {e}")


# Singleton instance
cache_manager = CacheManager()

# Backward compatibility functions
def get_cached(stock: str) -> Optional[str]:
    return cache_manager.get_cached_result(stock)

def save_cache(stock: str, result: str):
    cache_manager.save_result(stock, result)

def get_prompt_cache(prompt: str, model: str = "") -> Optional[str]:
    return cache_manager.get_prompt_cache(prompt, model, Config.LLM_TEMPERATURE)

def save_prompt_cache(prompt: str, model: str, response: str):
    cache_manager.save_prompt_cache(prompt, model, Config.LLM_TEMPERATURE, response)

def log_profile(call_info: Dict[str, Any]):
    cache_manager.log_profile(call_info)
