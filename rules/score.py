"""Rule pre-score (PRD 7.3 step 1). Cheap and explainable; the fine-tuned judge refines it."""
import base64
import binascii
import re

# (pattern, weight, reason). Weights combine as independent evidence: 1 - prod(1 - w).
PATTERNS = [
    (r"\bignore (all |any )?(the )?(previous|prior|above|earlier) (instructions|prompts|messages)", 0.9, "tries to override the AI's instructions"),
    (r"<\|im_start\|>|\[/?INST\]|<\|system\|>|###\s*(instruction|system)", 0.8, "fake chat-template tokens"),
    (r"\b(do not|don't|never)\s+(tell|mention|reveal|show|say)\b.{0,40}\b(user|human|reader)", 0.7, "tells the AI to hide something from the user"),
    (r"\b(ai|llm|language model|assistant|chatbot|agent|gpt|claude|gemini)s?\b.{0,40}\b(reading|read|summari[sz]|process|brows)", 0.6, "addressed to an AI reading the page"),
    (r"\b(send|forward|e-?mail|post|upload|exfiltrat)\w*\b.{0,40}\b(e-?mail|password|address|token|key|cookie|credentials|data)\b", 0.6, "asks for data to be sent somewhere"),
    (r"\b(already\s+)?(approved|authori[sz]ed|confirmed)\b.{0,40}\b(purchase|payment|transfer|checkout|order)", 0.6, "claims the user approved an action"),
    (r"(^|\b)(system|assistant|developer)\s*:", 0.5, "pretends to be a system or assistant message"),
    (r"\b(tell|inform|convince|recommend|assure)\b.{0,30}\buser\b", 0.5, "tells the AI what to say to the user"),
    (r"\b(append|add|include|end|start)\b.{0,80}\b(summary|response|answer|reply|output)\b", 0.5, "tries to change the AI's answer"),
    (r"\byou (are|must|will|should) now\b", 0.5, "tries to change the AI's role"),
    # Alone this only reaches suspicious: "label" is also an HTML tag name. exorcist.py keeps it from ever being benign.
    (r"\b(classif\w*|benign|not (a|an) (prompt )?injection|safe content)\b|\blabel(l?ed)?\s*(this|it|as|every|:|=)", 0.3, "talks to the classifier itself"),
    (r"\b(proceed|click|navigate|go)\s+to\b.{0,30}\b(checkout|link|url|https?:)", 0.4, "pushes the AI to take an action"),
    (r"\b(rate|score|review)\b.{0,30}\b\d+\s*(out of|/)\s*\d+", 0.3, "dictates a rating"),
    (r"https?://|www\.|\b[\w-]+\.(com|net|org|io|xyz|example)\b", 0.2, "contains a link"),
]
COMPILED = [(re.compile(p, re.I | re.S), w, r) for p, w, r in PATTERNS]
INJECTION, SUSPICIOUS = 0.5, 0.25


BASE64 = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")


def decode_base64(text: str) -> str:
    """Readable text hidden in base64 runs over 40 chars (PRD 9.4). Binary blobs (images, hashes) decode to nothing."""
    out = []
    for run in BASE64.findall(text):
        try:
            decoded = base64.b64decode(run + "=" * (-len(run) % 4)).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            continue
        if " " in decoded and "".join(decoded.split()).isprintable():
            out.append(decoded)
    return " ".join(out)


def score(text: str) -> tuple[float, list[str]]:
    miss, reasons = 1.0, []
    decoded = decode_base64(text)
    if decoded:
        text += " " + decoded  # the encoded payload is scored as if it were plain text
        miss *= 0.7
        reasons.append("hides base64-encoded text")
    for pattern, weight, reason in COMPILED:
        if pattern.search(text):
            miss *= 1 - weight
            reasons.append(reason)
    if len(text.split()) > 25:
        miss *= 0.8
        reasons.append("long hidden prose")
    return round(1 - miss, 3), reasons


def label(text: str) -> tuple[str, str]:
    """Rules-only label: the fallback when the model is offline, and the baseline in eval."""
    s, reasons = score(text)
    if s >= INJECTION:
        return "injection", "; ".join(reasons)
    if s >= SUSPICIOUS:
        return "suspicious", "; ".join(reasons)
    return "benign", "no instruction aimed at an AI"
