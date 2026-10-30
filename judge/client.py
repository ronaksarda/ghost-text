"""Judge client: label(ghost) -> (label, reason). Any OpenAI-compatible /chat/completions endpoint serving an
open-weight model: Groq (openai/gpt-oss-20b), llama.cpp, Ollama. Set JUDGE_URL, JUDGE_MODEL, JUDGE_KEY, and
JUDGE_REASONING (low|medium|high) for reasoning models.

Raises on network failure, so exorcise() fails closed. Never returns a verdict: only a label.
"""
import json
import os
import time
import urllib.error
import urllib.request

from judge.prompt import SYSTEM, parse, user_message

TIMEOUT = 10
_probe = {"at": 0.0, "ok": False}


def configured() -> bool:
    return bool(os.environ.get("JUDGE_URL") and os.environ.get("JUDGE_MODEL"))


def alive() -> bool:
    """One tiny request, cached 30 s. A judge that is down or still loading means rules-only mode (PRD 9.5)."""
    if time.monotonic() - _probe["at"] > 30:
        try:
            chat([{"role": "user", "content": "Reply with ok."}], max_tokens=64, timeout=8)
            _probe["ok"] = True
        except Exception:
            _probe["ok"] = False
        _probe["at"] = time.monotonic()
    return _probe["ok"]


def chat(messages: list[dict], max_tokens: int = 400, timeout: float = TIMEOUT, prefix: str = "JUDGE") -> str:
    """prefix picks the endpoint settings: JUDGE_* here, VICTIM_* for eval/victim.py."""
    body = {"model": os.environ[f"{prefix}_MODEL"], "messages": messages, "max_tokens": max_tokens, "temperature": 0}
    if os.environ.get(f"{prefix}_REASONING"):
        body["reasoning_effort"] = os.environ[f"{prefix}_REASONING"]  # reasoning tokens count against max_tokens
    req = urllib.request.Request(os.environ[f"{prefix}_URL"].rstrip("/") + "/chat/completions", method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "ghost-text/1.0",
                                          "Authorization": f"Bearer {os.environ.get(f'{prefix}_KEY', '')}"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                out = json.load(r)
            break
        except urllib.error.HTTPError as e:
            # Free tiers rate-limit: wait as told, but never longer than the caller's budget allows.
            if e.code != 429 or attempt == 2:
                raise
            time.sleep(min(float(e.headers.get("retry-after") or 2), 5))
    text = out["choices"][0]["message"].get("content") or ""
    return text.split("</think>")[-1].strip()  # some servers inline the reasoning block


def label(ghost: dict) -> tuple[str, str]:
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_message(ghost["text"], ghost["technique"], ghost.get("context", ""))}]
    return parse(chat(messages))
