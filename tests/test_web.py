"""The website in a real browser: what a visitor sees and clicks."""
import socket
import threading
import time

import pytest
import uvicorn
from playwright.sync_api import sync_playwright

from api import main


@pytest.fixture(scope="module")
def site():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    server = uvicorn.Server(uvicorn.Config(main.app, port=port, log_level="error"))
    threading.Thread(target=server.run, daemon=True).start()
    while not server.started:
        time.sleep(0.2)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser.new_page(viewport={"width": 1280, "height": 800}), f"http://127.0.0.1:{port}"
        browser.close()
    server.should_exit = True


def test_hidden_controls_stay_hidden(site):
    page, base = site
    page.goto(base)
    assert not page.locator("#sign").is_visible()  # sign-in is off without Auth0 settings
    page.click("#tab-search")
    assert page.locator("#panel-search").is_visible() and not page.locator("#panel-url").is_visible()
    page.click("#tab-url")
    assert page.locator("#panel-url").is_visible() and not page.locator("#panel-search").is_visible()


@pytest.mark.parametrize("demo, word", [("haunted-shop", "Haunted"), ("benign-heavy", "Clean")])
def test_demo_cards_show_verdict_and_evidence(site, demo, word):
    page, base = site
    page.goto(base)
    page.click(f"[data-demo={demo}]")
    page.wait_for_selector("#result:not([hidden])")
    assert page.text_content("#verdict-word") == word
    if word == "Haunted":
        assert page.locator("#ghost-list li").count() >= 6 and page.locator(".box.hostile").count() >= 3
        page.locator("#ghost-list li").first.click()
        assert page.locator(".ghost-item.on").count() == 1


def test_ghost_text_is_never_html(site):
    page, base = site
    page.goto(base)
    page.evaluate("""() => render({verdict: 'haunted', judge: 'offline', unscannable: [], screenshot: null,
        ghosts: [{id: 'g1', label: 'injection', text: '<img src=x onerror=window.__pwned=1>', technique: ['H1'],
                  views: ['dom_text'], reason: 'test', box: null}]})""")
    assert page.evaluate("window.__pwned") is None
    assert "<img src=x" in page.text_content("#ghost-list")
