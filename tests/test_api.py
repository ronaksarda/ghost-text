from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import main

DEMO = Path(__file__).parent.parent / "demo"
VERDICTS = {"haunted-shop": "haunted", "clean-blog": "clean", "unicode-smuggling": "haunted", "benign-heavy": "clean"}


@pytest.fixture(scope="module")
def client():
    with TestClient(main.app) as c:
        yield c


@pytest.fixture(autouse=True)
def fresh_rate_limit():
    main.hits.clear()


@pytest.mark.parametrize("page, verdict", VERDICTS.items())
def test_demo_through_api(client, page, verdict):
    r = client.post("/scan", json={"html": (DEMO / f"{page}.html").read_text(encoding="utf-8")})
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] == verdict and "reading" not in body
    assert body["screenshot"].startswith("data:image/png;base64,") and body["judge"] in ("online", "offline")


@pytest.mark.parametrize("page, verdict", VERDICTS.items())
def test_demo_results_cached(client, page, verdict):
    assert client.get(f"/demo-results/{page}.json").json()["verdict"] == verdict


@pytest.mark.parametrize("url", ["http://127.0.0.1/", "http://169.254.169.254/latest/meta-data/",
                                 "http://localhost:8000/", "file:///etc/passwd", "http://10.1.2.3/"])
def test_ssrf_rejected(client, url):
    assert client.post("/scan", json={"url": url}).status_code == 400


@pytest.mark.parametrize("body", [{}, {"url": "https://example.com", "html": "<p>x</p>"},
                                  {"html": "x" * 2_000_001}, {"url": "https://example.com/" + "a" * 2000}])
def test_bad_input_rejected(client, body):
    assert client.post("/scan", json=body).status_code == 400


def test_rate_limit(client):
    for _ in range(10):
        assert client.post("/scan", json={"html": "<p>hi</p>"}).status_code == 200
    r = client.post("/scan", json={"html": "<p>hi</p>"})
    assert r.status_code == 429 and int(r.headers["retry-after"]) > 0


def test_site_serves(client):
    assert client.get("/health").json()["demos"] == 4
    assert "Ghost Text" in client.get("/").text
    assert client.get("/demo/haunted-shop.html").status_code == 200
