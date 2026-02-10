from pathlib import Path
import json
from datetime import datetime
import hashlib

CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_FILE = CACHE_DIR / "cache.json"
PROFILE_FILE = CACHE_DIR / "profile.json"


def _ensure():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not CACHE_FILE.exists():
        CACHE_FILE.write_text(json.dumps({}))
    if not PROFILE_FILE.exists():
        PROFILE_FILE.write_text(json.dumps({"calls": []}))


def get_cached(stock: str):
    _ensure()
    data = json.loads(CACHE_FILE.read_text())
    return data.get("final", {}).get(stock)


def save_cache(stock: str, result: str):
    _ensure()
    data = json.loads(CACHE_FILE.read_text())
    finals = data.get("final", {})
    finals[stock] = {
        "result": result,
        "saved_at": datetime.utcnow().isoformat() + "Z"
    }
    data["final"] = finals
    CACHE_FILE.write_text(json.dumps(data, indent=2))


def _prompt_key(prompt: str, model: str = "") -> str:
    key = f"{model}|{prompt}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def get_prompt_cache(prompt: str, model: str = ""):
    _ensure()
    data = json.loads(CACHE_FILE.read_text())
    prompts = data.get("prompts", {})
    return prompts.get(_prompt_key(prompt, model))


def save_prompt_cache(prompt: str, model: str, response: str):
    _ensure()
    data = json.loads(CACHE_FILE.read_text())
    prompts = data.get("prompts", {})
    prompts[_prompt_key(prompt, model)] = {
        "model": model,
        "prompt": prompt,
        "response": response,
        "saved_at": datetime.utcnow().isoformat() + "Z"
    }
    data["prompts"] = prompts
    CACHE_FILE.write_text(json.dumps(data, indent=2))


def log_profile(call_info: dict):
    _ensure()
    data = json.loads(PROFILE_FILE.read_text())
    calls = data.get("calls", [])
    calls.append(call_info)
    data["calls"] = calls
    PROFILE_FILE.write_text(json.dumps(data, indent=2))
