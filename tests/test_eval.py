import json
from pathlib import Path

from eval import asr
from eval.run import metrics

DATA = Path(__file__).parent.parent / "eval" / "data.jsonl"


def test_dataset_shape():
    rows = [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines()]
    assert len(rows) >= 350
    assert {r["split"] for r in rows} == {"train", "val", "test"}
    assert {r["label"] for r in rows} == {"benign", "suspicious", "injection"}
    assert len({" ".join(r["text"].lower().split()) for r in rows}) == len(rows)  # no duplicates across splits
    assert any(r["adversarial"] and r["split"] == "test" for r in rows)


def test_metrics():
    rows = [{"label": "injection", "source": "written", "adversarial": True, "lang": "en"},
            {"label": "benign", "source": "bbc.com", "adversarial": False, "lang": "en"}]
    m = metrics(rows, ["injection", "suspicious"], 1.0)
    assert m["per_class"]["injection"]["f1"] == 1.0
    assert m["real_site_fp_rate"] == 1.0 and m["adversarial_caught"] == 1.0


def test_asr_harness_with_obedient_fake_model():
    # A "model" that repeats its input obeys every canary it can see.
    result = asr.run(lambda text: text, limit=3)
    assert result["n"] == 3 and result["asr_raw"] == 1.0
    assert result["asr_exorcised"] <= result["asr_raw"]
