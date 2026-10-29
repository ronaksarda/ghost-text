"""python -m eval.harvest — scan every site in eval/sites.txt and save its ghost candidates to eval/raw/<host>.jsonl.

Real-site ghosts are the benign half of the dataset (PRD 11). Never accepts consent banners, logs in, or
works around bot checks: a site that blocks us is skipped and logged.
"""
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

from exorcist import contexts
from scanner.scan import scan

HERE = Path(__file__).parent


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    raw = HERE / "raw"
    raw.mkdir(exist_ok=True)
    for url in (HERE / "sites.txt").read_text().split():
        host = urlsplit(url).hostname
        try:
            result = scan(url=url)
        except Exception as e:  # ScanError or a browser crash: one broken site must not stop the harvest
            print(f"skip {host}: {e}")
            continue
        ctx = contexts(result["reading"])
        with open(raw / f"{host}.jsonl", "w", encoding="utf-8") as f:
            for g in result["ghosts"]:
                f.write(json.dumps({"text": g["text"], "technique": g["technique"], "context": ctx.get(g["id"], ""),
                                    "source": host}, ensure_ascii=False) + "\n")
        print(f"{host}: {len(result['ghosts'])} ghosts{' (partial)' if result['partial'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
