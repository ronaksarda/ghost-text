"""Judge client: label(ghost) -> (label, reason). Talks to any OpenAI-compatible /completions endpoint
(Tinker's, or llama.cpp on a DigitalOcean droplet) set by JUDGE_URL, JUDGE_MODEL and JUDGE_KEY in .env.

Raises on network failure, so exorcise() fails closed. Never returns a verdict: only a label.
"""
import json
import os
import urllib.request

from judge.prompt import parse, render

TIMEOUT = 10


def configured() -> bool:
    return bool(os.environ.get("JUDGE_URL") and os.environ.get("JUDGE_MODEL"))


def complete(prompt: str) -> str:
    body = {"model": os.environ["JUDGE_MODEL"], "prompt": prompt, "max_tokens": 60, "temperature": 0,
            "stop": ["<|im_end|>"]}
    req = urllib.request.Request(os.environ["JUDGE_URL"].rstrip("/") + "/completions", method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {os.environ.get('JUDGE_KEY', '')}"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)["choices"][0]["text"]


def label(ghost: dict) -> tuple[str, str]:
    return parse(complete(render(ghost["text"], ghost["technique"], ghost.get("context", ""))))
