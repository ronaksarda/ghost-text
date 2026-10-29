"""python -m eval.build — merge harvested and written ghosts into eval/data.jsonl with a fixed split.

Harvested ghosts that any rule fires on go to eval/review.jsonl with label "?" for a human to set.
Only reviewed ones (label benign/suspicious/injection) enter the dataset.
The test split is never used for training or prompt tuning: change SEED and every number in the post is void.
"""
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from eval.written import records
from rules.score import score

HERE = Path(__file__).parent
SEED = 2026
PER_SITE = 8  # keeps one ghost-heavy site from drowning the rest
LABELS = ("benign", "suspicious", "injection")


def lang(text: str) -> str:
    if re.search("[ऀ-ॿ]", text):
        return "hi"
    if re.search("[一-鿿]", text):
        return "zh"
    if re.search("[֐-ࣿ]", text):
        return "rtl"
    if re.search("[ñ¿¡]|\\b(el|la|los|las|del|que|una|más)\\b", text, re.I):
        return "es"
    return "en"


def key(text: str) -> str:
    return " ".join(text.lower().split())


def harvested(rng: random.Random) -> list[dict]:
    review_path = HERE / "review.jsonl"
    reviewed = {}
    if review_path.exists():
        for line in review_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            reviewed[key(r["text"])] = r
    out, to_review = [], []
    for path in sorted((HERE / "raw").glob("*.jsonl")):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        rows = [r for r in {key(r["text"]): r for r in rows if 2 <= len(r["text"]) <= 2000}.values()]
        rng.shuffle(rows)
        for r in rows[:PER_SITE]:
            r.update(adversarial=False, label="benign")
            if score(r["text"])[0] > 0:
                r["label"] = reviewed.get(key(r["text"]), {}).get("label", "?")
                to_review.append(r)
            if r["label"] in LABELS:
                out.append(r)
    with open(review_path, "w", encoding="utf-8") as f:
        for r in to_review:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    pending = sum(r["label"] == "?" for r in to_review)
    print(f"{len(to_review)} harvested ghosts need review, {pending} still unlabelled in eval/review.jsonl")
    return out


def main() -> None:
    rng = random.Random(SEED)
    rows = {}
    for r in records() + harvested(rng):
        rows.setdefault(key(r["text"]), r)  # first wins: written labels beat harvested duplicates
    strata = defaultdict(list)
    for r in rows.values():
        r["lang"] = lang(r["text"])
        strata[(r["label"], r["adversarial"], r["source"] == "written")].append(r)
    data = []
    for group in strata.values():
        rng.shuffle(group)
        n = len(group)
        for i, r in enumerate(group):
            r["split"] = "train" if i < round(n * 0.7) else "val" if i < round(n * 0.85) else "test"
        data += group
    data.sort(key=lambda r: (r["split"], r["label"], r["text"]))
    with open(HERE / "data.jsonl", "w", encoding="utf-8") as f:
        for i, r in enumerate(data):
            f.write(json.dumps({"id": f"d{i:04d}", **{k: r[k] for k in (
                "text", "technique", "context", "label", "source", "lang", "adversarial", "split")}},
                ensure_ascii=False) + "\n")
    counts = defaultdict(int)
    for r in data:
        counts[(r["split"], r["label"])] += 1
    print(f"{len(data)} records:", dict(sorted(counts.items())))


if __name__ == "__main__":
    main()
