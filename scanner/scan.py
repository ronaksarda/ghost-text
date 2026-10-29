"""Load a page in a real browser and return its ghost candidates (PRD 5.1 steps 3-5)."""
import base64
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

from rules.unicode import decode_tags, strip_invisibles, suspicious_invisibles
from scanner.guard import is_public_url, route_guard

EXTRACT_JS = (Path(__file__).parent / "extract.js").read_text(encoding="utf-8")
MAX_HTML = 2_000_000
MAX_GHOSTS = 500


class ScanError(Exception):
    pass


def _origin(url: str) -> tuple[str, str]:
    parts = urlsplit(url)
    return parts.scheme, parts.netloc


def _clean(ghost: dict) -> dict | None:
    """Apply the Python side of H9, drop visible text whose only 'invisibles' are legitimate."""
    text = ghost["text"]
    if "H9" in ghost["technique"]:
        hidden = decode_tags(text)
        if hidden:
            ghost["decoded_from"] = "unicode_tags"
            ghost["visible_text"] = strip_invisibles(text).strip()
            text = hidden
        elif not suspicious_invisibles(text):
            ghost["technique"].remove("H9")
            if not ghost["technique"]:
                return None
        ghost["text"] = strip_invisibles(text).strip() or text
    return ghost


def scan(url: str | None = None, html: str | None = None, *, screenshot: bool = False,
         timeout_ms: int = 20_000, cdp_url: str | None = None) -> dict:
    """Scan a URL or pasted HTML. cdp_url connects to a remote browser (Browserbase) instead of local Chromium."""
    if (url is None) == (html is None):
        raise ValueError("pass exactly one of url or html")
    if url is not None and (len(url) > 2000 or not url.startswith(("http://", "https://")) or not is_public_url(url)):
        raise ScanError("Only public http(s) URLs can be scanned.")
    if html is not None and len(html) > MAX_HTML:
        raise ScanError("Pasted HTML is larger than 2 MB.")

    started = time.monotonic()
    partial = False
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url) if cdp_url else p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.route("**/*", route_guard)
            try:
                if url:
                    response = page.goto(url, wait_until="load", timeout=timeout_ms)
                    if response and response.status >= 400:
                        raise ScanError(f"The page answered with HTTP {response.status}.")
                    if response and "html" not in response.headers.get("content-type", "html"):
                        raise ScanError("That URL is not an HTML page.")
                else:
                    page.set_content(html, wait_until="load", timeout=timeout_ms)
            except PlaywrightTimeout:
                partial = True
            except PlaywrightError as e:
                raise ScanError(f"Could not load the page: {e.message.splitlines()[0]}") from e
            try:
                page.wait_for_load_state("networkidle", timeout=3000)
            except PlaywrightTimeout:
                pass
            # One pass to the bottom wakes lazy-loaded content, then back so boxes match the screenshot.
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_timeout(300)
            page.evaluate("window.scrollTo(0, 0)")

            ghosts, reading, unscannable = [], [], []
            stats = {"elements": 0, "text_nodes": 0, "shadow_roots": 0}
            origin = _origin(page.main_frame.url)
            for frame in page.frames:
                # PRD H16: same-origin frames are scanned, cross-origin ones (ads, embeds) are reported, not read.
                if frame is not page.main_frame and not frame.url.startswith("about:") and _origin(frame.url) != origin:
                    unscannable.append({"kind": "cross_origin_iframe", "src": frame.url})
                    continue
                try:
                    result = frame.evaluate(EXTRACT_JS)
                except PlaywrightError:
                    unscannable.append({"kind": "frame", "src": frame.url})
                    continue
                ids = []
                for g in result["ghosts"]:
                    g["id"] = f"g{len(ghosts) + 1}"
                    ids.append(g["id"])
                    if frame is not page.main_frame:
                        g["frame"], g["box"] = frame.url, None
                    ghosts.append(g)
                for piece in result["reading"]:
                    piece["ghost"] = ids[piece["ghost"]] if piece["ghost"] >= 0 else None
                    reading.append(piece)
                unscannable += result["unscannable"]
                for k in stats:
                    stats[k] += result["stats"][k]

            shot = None
            if screenshot:
                shot = "data:image/png;base64," + base64.b64encode(page.screenshot(full_page=True)).decode()
        finally:
            browser.close()

    kept = {g["id"] for g in map(_clean, ghosts) if g}
    ghosts = [g for g in ghosts if g["id"] in kept]
    for piece in reading:
        if piece["ghost"] and piece["ghost"] not in kept:
            piece["ghost"] = None  # its invisible characters are legitimate (emoji, RTL), so keep them
        elif piece["ghost"]:
            piece["text"] = strip_invisibles(piece["text"])
    truncated = len(ghosts) > MAX_GHOSTS
    stats.update(candidates=len(ghosts), ms=round((time.monotonic() - started) * 1000))
    return {
        "url": url,
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "partial": partial,
        "truncated": truncated,
        "screenshot": shot,
        "ghosts": ghosts[:MAX_GHOSTS],
        "reading": reading,
        "unscannable": unscannable,
        "stats": stats,
    }
