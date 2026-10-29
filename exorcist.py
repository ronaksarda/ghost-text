"""Label every ghost, decide the verdict in code, and rebuild the page text without the hostile ones."""
from collections.abc import Callable

from rules import score

Labeler = Callable[[dict], tuple[str, str]]


def rules_labeler(ghost: dict) -> tuple[str, str]:
    return score.label(ghost["text"])


def exorcise(scan_result: dict, labeler: Labeler = rules_labeler) -> dict:
    ghosts = scan_result["ghosts"]
    for g in ghosts:
        g["rule_score"], reasons = score.score(g["text"])
        try:
            g["label"], g["reason"] = labeler(g)
        except Exception as e:  # judge offline or broken: fail closed, never open
            g["label"], g["reason"] = "suspicious", f"judge unavailable ({type(e).__name__})"
        if g["label"] not in ("benign", "suspicious", "injection"):
            g["label"] = "suspicious"
        # A ghost that talks about its own classification is never let through as benign (PRD 7.4).
        if g["label"] == "benign" and "talks to the classifier itself" in reasons:
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
