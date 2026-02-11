import time
from typing import Any
from functools import wraps
from cache import get_prompt_cache, save_prompt_cache, log_profile


class TimingLLM:
    def __init__(self, llm, model_name: str = ""):
        self._llm = llm
        self.model_name = model_name

    def __getattr__(self, name: str) -> Any:
        return getattr(self._llm, name)

    def _record(self, prompt: str, duration: float, response: str, caller: str = None):
        info = {
            "time": time.time(),
            "duration_s": duration,
            "model": self.model_name,
            "caller": caller,
            "prompt_preview": prompt[:200]
        }
        try:
            info["response_len"] = len(response)
        except Exception:
            pass
        log_profile(info)

    def __call__(self, prompt: str, *args, caller: str = None, **kwargs):
        start = time.time()
        result = self._llm(prompt, *args, **kwargs)
        duration = time.time() - start
        try:
            text = result if isinstance(result, str) else str(result)
        except Exception:
            text = ""
        self._record(prompt, duration, text, caller=caller)
        return result

    def generate(self, prompt: str, *args, caller: str = None, **kwargs):
        start = time.time()
        if hasattr(self._llm, "generate"):
            result = self._llm.generate(prompt, *args, **kwargs)
        else:
            result = self._llm(prompt, *args, **kwargs)
        duration = time.time() - start
        try:
            text = result if isinstance(result, str) else str(result)
        except Exception:
            text = ""
        self._record(prompt, duration, text, caller=caller)
        return result


class CachingLLM:
    def __init__(self, timing_llm: TimingLLM, model_name: str = ""):
        self._llm = timing_llm
        self.model_name = model_name

    def __getattr__(self, name: str) -> Any:
        return getattr(self._llm, name)

    def __call__(self, prompt: str, *args, caller: str = None, **kwargs):
        cached = get_prompt_cache(prompt, self.model_name)
        if cached:
            return cached.get("response")
        result = self._llm(prompt, *args, caller=caller, **kwargs)
        try:
            text = result if isinstance(result, str) else str(result)
        except Exception:
            text = ""
        save_prompt_cache(prompt, self.model_name, text)
        return result

    def generate(self, prompt: str, *args, caller: str = None, **kwargs):
        cached = get_prompt_cache(prompt, self.model_name)
        if cached:
            return cached.get("response")
        if hasattr(self._llm, "generate"):
            result = self._llm.generate(prompt, *args, caller=caller, **kwargs)
        else:
            result = self._llm(prompt, *args, caller=caller, **kwargs)
        try:
            text = result if isinstance(result, str) else str(result)
        except Exception:
            text = ""
        save_prompt_cache(prompt, self.model_name, text)
        return result
