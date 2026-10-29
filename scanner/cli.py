"""python -m scanner.cli <url-or-html-file> [--screenshot] [--clean]

--clean prints only the verdict and the exorcised page text an agent should read.
"""
import json
import sys
from pathlib import Path

from exorcist import exorcise
from scanner.scan import ScanError, scan


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and choke on emoji
    if not argv:
        print(__doc__)
        return 2
    target = argv[0]
    try:
        if Path(target).is_file():
            result = scan(html=Path(target).read_text(encoding="utf-8"), screenshot="--screenshot" in argv)
        else:
            result = scan(url=target, screenshot="--screenshot" in argv)
    except ScanError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    result = exorcise(result)
    if "--clean" in argv:
        print(f"verdict: {result['verdict']}  ({len(result['exorcised'])} ghosts exorcised)\n")
        print(result["clean_text"])
    else:
        result.pop("reading")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
