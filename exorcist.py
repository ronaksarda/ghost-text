"""Label every ghost, decide the verdict in code, and rebuild the page text without the hostile ones."""
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from rules import score

Labeler = Callable[[dict], tuple[str, str]]
MAX_JUDGED = 60  # shortcut: PRD 9.5 says 200; a CPU-served 8B model can't do 200 in 15 s. Raise on a GPU.
MIN_WORDS = 4  # "Menu", "Search", "Skip to content": rules alone are right, and the model is the slow part


def rules_labeler(ghost: dict) -> tuple[str, str]:
    return score.label(ghost["text"])


def contexts(reading: list[dict], width: int = 100) -> dict[str, str]:
    """Visible text just before and after each ghost, for the judge (PRD 7.3). Attribute and comment ghosts get none."""
    out, before = {}, ""
    for i, piece in enumerate(reading):
        if not piece["ghost"]:
            before = (before + " " + piece["text"])[-width:]
        elif piece["ghost"] not in out:
            after = " ".join(p["text"] for p in reading[i + 1:i + 6] if not p["ghost"])[:width]
            out[piece["ghost"]] = f"{before.strip()} … {after.strip()}".strip(" …")
    return out


def _safe(labeler: Labeler, g: dict) -> tuple[str, str]:
    try:
        return labeler(g)
    except Exception as e:  # judge offline or broken: fail closed, never open
        return "suspicious", f"judge unavailable ({type(e).__name__})"


def exorcise(scan_result: dict, labeler: Labeler = rules_labeler, max_judged: int = MAX_JUDGED) -> dict:
    ghosts = scan_result["ghosts"]
    ctx = contexts(scan_result["reading"])
    reasons = {}
    for g in ghosts:
        g["rule_score"], reasons[g["id"]] = score.score(g["text"])
        g.setdefault("context", ctx.get(g["id"], ""))
    # The judge sees the top ghosts by rule score, in parallel (PRD 9.5); the rest keep their rules label.
    ranked = sorted(ghosts, key=lambda g: -g["rule_score"])
    judged = [g for g in ranked if len(g["text"].split()) >= MIN_WORDS][:max_judged]
    picked = {id(g) for g in judged}
    rest = [g for g in ranked if id(g) not in picked]
    with ThreadPoolExecutor(8) as pool:
        for g, result in zip(judged, pool.map(lambda g: _safe(labeler, g), judged)):
            g["label"], g["reason"] = result
    for g in rest:
        g["label"], g["reason"] = rules_labeler(g)
    for g in ghosts:
        if g["label"] not in ("benign", "suspicious", "injection"):
            g["label"] = "suspicious"
        # A ghost that talks about its own classification is never let through as benign (PRD 7.4).
        if g["label"] == "benign" and "talks to the classifier itself" in reasons[g["id"]]:
            g["label"] = "suspicious"

    labels = {g["id"]: g for g in ghosts}
    if any(g["label"] == "injection" for g in ghosts):
        verdict = "haunted"
    elif any(g["label"] == "suspicious" for g in ghosts):
        verdict = "uneasy"
    else:
        verdict = "clean"

    parts = []
    for piece in scan_result["reading"]:
        g = labels.get(piece["ghost"]) if piece["ghost"] else None
        # Unknown ghost ids (truncated) are dropped. Smuggled text keeps its visible half; the hidden half is already stripped.
        if piece["ghost"] and (g is None or (g["label"] != "benign" and "visible_text" not in g)):
            continue
        if piece["text"].strip():
            parts.append((piece["sep"] if parts else "") + piece["text"].strip())

    return {
        **scan_result,
        "verdict": verdict,
        "clean_text": "".join(parts),
        "exorcised": [g["id"] for g in ghosts if g["label"] != "benign"],
    }
