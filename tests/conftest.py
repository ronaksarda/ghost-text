import os

import pytest

LIVE = ("JUDGE_URL", "JUDGE_MODEL", "JUDGE_KEY", "VICTIM_URL", "VICTIM_MODEL", "BROWSERBASE_API_KEY", "SERPAPI_KEY",
        "AUTH0_DOMAIN", "AUTH0_AUDIENCE", "AUTH0_CLIENT_ID")


@pytest.fixture(scope="session", autouse=True)
def no_live_services():
    """Tests fake every outside service. Without this, keys in .env make results depend on someone's free-tier quota."""
    import api.main  # noqa: F401  loads .env first, so the keys it sets are the ones removed here
    saved = {k: os.environ.pop(k) for k in LIVE if k in os.environ}
    yield
    os.environ.update(saved)


@pytest.fixture(autouse=True)
def stats_in_tmp(monkeypatch, tmp_path):
    """Tests never write to the real usage log."""
    monkeypatch.setattr("api.main.STATS", tmp_path / "stats.jsonl")
