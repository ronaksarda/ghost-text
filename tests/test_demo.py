"""The demo gallery (PRD 5.3) must always give the right verdict. Every later change has to keep this green."""
from pathlib import Path

import pytest

from exorcist import exorcise
from scanner.scan import scan

DEMO = Path(__file__).parent.parent / "demo"


@pytest.mark.parametrize("page, verdict", [
    ("haunted-shop", "haunted"),
    ("clean-blog", "clean"),
    ("unicode-smuggling", "haunted"),
    ("benign-heavy", "clean"),
])
def test_demo_verdict(page, verdict):
    result = exorcise(scan(html=(DEMO / f"{page}.html").read_text(encoding="utf-8")))
    assert result["verdict"] == verdict


def test_demo_gallery_is_complete():
    assert len(list(DEMO.glob("*.html"))) == 4


def test_smuggled_recipe_decoded_and_exorcised():
    result = exorcise(scan(html=(DEMO / "unicode-smuggling.html").read_text(encoding="utf-8")))
    texts = [g["text"] for g in result["ghosts"] if g["label"] == "injection"]
    assert any("needs no yeast" in t for t in texts) and any("starter kit" in t for t in texts)
    assert "7 g dry yeast" in result["clean_text"] and "needs no yeast" not in result["clean_text"]
    assert "خبز الموتى" in result["clean_text"]  # legitimate RTL mark kept


def test_closed_details_is_display_hidden():
    ghosts = scan(html=(DEMO / "benign-heavy.html").read_text(encoding="utf-8"))["ghosts"]
    faq = [g for g in ghosts if "lanternignore" in g["text"]]
    assert faq[0]["technique"] == ["H1"]
