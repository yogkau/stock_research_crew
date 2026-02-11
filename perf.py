"""Improved performance wrappers with error handling and retries."""
import time
import logging
from typing import Any, Optional
from functools import wraps
from config import Config

logger = logging.getLogger(__name__)


class TimingLLM:
    """Wrapper to time LLM calls and log performance."""
    
    def __init__(self, llm, model_name: str = ""):
        self._llm = llm
        self.model_name = model_name
        self._log_callback = None
    
    def set_log_callback(self, callback):
        """Set callback for logging profile data."""
        self._log_callback = callback
    
    def __getattr__(self, name: str) -> Any:
        return getattr(self._llm, name)
    
    def _record(self, prompt: str, duration: float, response: str, caller: str = None):
        """Record timing information."""
        info = {
            "time": time.time(),
            "duration_s": round(duration, 3),
            "model": self.model_name,
            "caller": caller,
            "prompt_preview": prompt[:200],
            "response_len": len(str(response))
        }
        
        if self._log_callback:
            try:
                self._log_callback(info)
            except Exception as e:
                logger.error(f"Failed to log profile: {e}")
    
    def _execute_with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic."""
        last_error = None
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(f"LLM call failed (attempt {attempt + 1}/{Config.MAX_RETRIES}): {e}")
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error(f"LLM call failed after {Config.MAX_RETRIES} attempts")
        raise last_error
    
    def __call__(self, prompt: str, *args, caller: str = None, **kwargs):
        start = time.time()
        try:
            result = self._execute_with_retry(self._llm, prompt, *args, **kwargs)
            duration = time.time() - start
            self._record(prompt, duration, result, caller=caller)
            return result
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def generate(self, prompt: str, *args, caller: str = None, **kwargs):
        start = time.time()
        try:
            if hasattr(self._llm, "generate"):
                result = self._execute_with_retry(self._llm.generate, prompt, *args, **kwargs)
            else:
                result = self._execute_with_retry(self._llm, prompt, *args, **kwargs)
            
            duration = time.time() - start
            self._record(prompt, duration, result, caller=caller)
            return result
        except Exception as e:
            logger.error(f"LLM generate failed: {e}")
            raise


class CachingLLM:
    """Wrapper to cache LLM responses."""
    
    def __init__(self, timing_llm: TimingLLM, model_name: str = "", cache_manager=None):
        self._llm = timing_llm
        self.model_name = model_name
        self._cache_manager = cache_manager
    
    def __getattr__(self, name: str) -> Any:
        return getattr(self._llm, name)
    
    def _get_cached(self, prompt: str) -> Optional[str]:
        """Get cached response if available."""
        if self._cache_manager:
            return self._cache_manager.get_prompt_cache(
                prompt, self.model_name, Config.LLM_TEMPERATURE
            )
        return None
    
    def _save_cached(self, prompt: str, response: str):
        """Save response to cache."""
        if self._cache_manager:
            try:
                self._cache_manager.save_prompt_cache(
                    prompt, self.model_name, Config.LLM_TEMPERATURE, response
                )
            except Exception as e:
                logger.error(f"Failed to save to cache: {e}")
    
    def __call__(self, prompt: str, *args, caller: str = None, **kwargs):
        cached = self._get_cached(prompt)
        if cached:
            logger.info(f"Using cached response for prompt (caller: {caller})")
            return cached
        
        result = self._llm(prompt, *args, caller=caller, **kwargs)
        text = str(result) if not isinstance(result, str) else result
        self._save_cached(prompt, text)
        return result
    
    def generate(self, prompt: str, *args, caller: str = None, **kwargs):
        cached = self._get_cached(prompt)
        if cached:
            logger.info(f"Using cached response for generate (caller: {caller})")
            return cached
        
        if hasattr(self._llm, "generate"):
            result = self._llm.generate(prompt, *args, caller=caller, **kwargs)
        else:
            result = self._llm(prompt, *args, caller=caller, **kwargs)
        
        text = str(result) if not isinstance(result, str) else result
        self._save_cached(prompt, text)
        return result
