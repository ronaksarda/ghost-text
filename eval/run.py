"""python -m eval.run <labeler> [--split val|test] — score a labeler on eval/data.jsonl.

Labels go through exorcise(), so eval measures the same code path production uses (rules floor included).
Writes eval/results/<labeler>-<split>.json. Every number in README and the post comes from these files.
"""
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import envfile
from exorcist import exorcise, rules_labeler
from judge.client import label as judge_label

HERE = Path(__file__).parent
LABELS = ("benign", "suspicious", "injection")
LABELERS = {"rules": lambda: rules_labeler, "model": lambda: judge_label}  # model: the open-weight judge in .env


def load(split: str) -> list[dict]:
    rows = [json.loads(line) for line in (HERE / "data.jsonl").read_text(encoding="utf-8").splitlines()]
    return [r for r in rows if r["split"] == split]


def predict(rows: list[dict], labeler) -> tuple[list[str], float]:
    preds, started = [], time.monotonic()
    for r in rows:
        ghost = {"id": r["id"], "text": r["text"], "technique": r["technique"], "context": r["context"]}
        preds.append(exorcise({"ghosts": [ghost], "reading": []}, labeler)["ghosts"][0]["label"])
    return preds, (time.monotonic() - started) * 1000 / max(len(rows), 1)


def metrics(rows: list[dict], preds: list[str], ms: float) -> dict:
    per_class = {}
    for c in LABELS:
        tp = sum(p == c and r["label"] == c for r, p in zip(rows, preds))
        fp = sum(p == c and r["label"] != c for r, p in zip(rows, preds))
        fn = sum(p != c and r["label"] == c for r, p in zip(rows, preds))
        prec, rec = tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn) if tp + fn else 0.0
        per_class[c] = {"precision": prec, "recall": rec, "f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0,
                        "support": tp + fn}
    real = [p for r, p in zip(rows, preds) if r["source"] != "written" and r["label"] == "benign"]
    adv = [p for r, p in zip(rows, preds) if r["adversarial"]]
    by_lang = defaultdict(list)
    for r, p in zip(rows, preds):
        by_lang[r["lang"]].append(p == r["label"])
    return {
        "n": len(rows),
        "accuracy": sum(p == r["label"] for r, p in zip(rows, preds)) / len(rows),
        "per_class": per_class,
        "real_site_fp_rate": sum(p != "benign" for p in real) / len(real) if real else None,
        "real_site_benign_n": len(real),
        "adversarial_caught": sum(p != "benign" for p in adv) / len(adv) if adv else None,
        "adversarial_as_injection": sum(p == "injection" for p in adv) / len(adv) if adv else None,
        "adversarial_n": len(adv),
        "accuracy_by_lang": {k: {"accuracy": sum(v) / len(v), "n": len(v)} for k, v in sorted(by_lang.items())},
        "confusion": dict(Counter(f"{r['label']}->{p}" for r, p in zip(rows, preds))),
        "ms_per_ghost": round(ms, 2),
    }


def table(name: str, split: str, m: dict) -> str:
    pct = lambda x: "n/a" if x is None else f"{x:.1%}"
    lines = [f"### {name} on {split} (n={m['n']})", "", "| class | precision | recall | F1 | support |", "|---|---|---|---|---|"]
    lines += [f"| {c} | {pct(v['precision'])} | {pct(v['recall'])} | {pct(v['f1'])} | {v['support']} |"
              for c, v in m["per_class"].items()]
    lines += ["", f"- accuracy: {pct(m['accuracy'])}",
              f"- real-site false-positive rate: {pct(m['real_site_fp_rate'])} (n={m['real_site_benign_n']})",
              f"- adversarial caught (not benign): {pct(m['adversarial_caught'])}, as injection: "
              f"{pct(m['adversarial_as_injection'])} (n={m['adversarial_n']})",
              "- accuracy by language: " + ", ".join(f"{k} {pct(v['accuracy'])} (n={v['n']})"
                                                     for k, v in m["accuracy_by_lang"].items()),
              f"- latency: {m['ms_per_ghost']} ms per ghost"]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    envfile.load()
    sys.stdout.reconfigure(encoding="utf-8")
    if not argv or argv[0] not in LABELERS:
        print(f"usage: python -m eval.run {{{'|'.join(LABELERS)}}} [--split val|test]")
        return 2
    split = argv[argv.index("--split") + 1] if "--split" in argv else "val"
    rows = load(split)
    preds, ms = predict(rows, LABELERS[argv[0]]())
    m = metrics(rows, preds, ms)
    (HERE / "results").mkdir(exist_ok=True)
    out = {"labeler": argv[0], "split": split, **m,
           "predictions": [{"id": r["id"], "label": r["label"], "pred": p} for r, p in zip(rows, preds)]}
    (HERE / "results" / f"{argv[0]}-{split}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(table(argv[0], split, m))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
