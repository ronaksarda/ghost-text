"""python scripts/record_demo.py [base-url] — record the demo video to media/ghost-text-demo.mp4.

Needs the app running (uvicorn api.main:app) and ffmpeg on PATH. Everything on screen is the real product;
the captions are the only thing added. Run one search first so the search scene is served from cache.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
EXT = ROOT / "extension"
SIZE = {"width": 1280, "height": 720}
QUERY = "best budget wireless headphones 2026"

CAPTION_JS = """(text) => {
  let c = document.getElementById('__cap');
  if (!c) {
    c = document.createElement('div'); c.id = '__cap';
    Object.assign(c.style, {position: 'fixed', left: '50%', bottom: '28px', transform: 'translateX(-50%)', zIndex: 2147483647,
      background: 'rgba(0,0,0,.86)', color: '#fff', font: '600 22px/1.35 system-ui, sans-serif', padding: '12px 20px',
      borderRadius: '8px', maxWidth: '1000px', textAlign: 'center', border: '1px solid #e0142f'});
    document.body.appendChild(c);
  }
  c.textContent = text; c.style.display = text ? 'block' : 'none';
}"""

PANEL_JS = """([title, lines, tone]) => {
  const p = document.createElement('div');
  Object.assign(p.style, {position: 'fixed', top: '40px', right: '40px', width: '520px', zIndex: 2147483646,
    background: '#0c0607', color: '#ece4d6', border: '2px solid ' + tone, borderRadius: '8px', padding: '18px 20px',
    font: '16px/1.5 "Courier New", monospace', boxShadow: '0 20px 60px rgba(0,0,0,.6)'});
  const h = document.createElement('div');
  Object.assign(h.style, {font: '700 18px system-ui, sans-serif', marginBottom: '10px', color: tone});
  h.textContent = title; p.appendChild(h);
  for (const l of lines) { const d = document.createElement('div'); d.textContent = '> ' + l; d.style.marginBottom = '8px'; p.appendChild(d); }
  document.body.appendChild(p);
}"""


def say(page, text, hold=0):
    page.evaluate(CAPTION_JS, text)
    page.wait_for_timeout(hold)


def scroll_to(page, selector, hold):
    page.evaluate("s => document.querySelector(s).scrollIntoView({behavior: 'smooth', block: 'start'})", selector)
    page.wait_for_timeout(hold)


def site_clip(p, base, out):
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport=SIZE, record_video_dir=str(out), record_video_size=SIZE)
    started = time.monotonic()
    page = ctx.new_page()
    page.goto(base)  # load the pixel font first, so it doesn't swap in and shift the page on camera; trimmed below
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(800)
    lead_in = time.monotonic() - started
    hostile = [g["text"] for g in json.load(urllib.request.urlopen(f"{base}/demo-results/haunted-shop.json"))["ghosts"]
               if g["label"] == "injection"]

    page.goto(f"{base}/demo/haunted-shop.html")
    say(page, "A small shop page. One honest two-star review. Nothing strange.", 3500)
    say(page, "But this is what an AI assistant reads on the same page:", 1200)
    page.evaluate(PANEL_JS, ["Hidden from you, read by your AI", hostile[:5], "#e0142f"])
    page.wait_for_timeout(5500)

    page.goto(base)
    say(page, "", 4200)  # let the screen flicker on and the headline glitch
    say(page, "Ghost Text finds every piece of hidden text and judges which ones are attacks.", 3000)
    page.click("[data-demo=haunted-shop]")
    page.wait_for_selector("#result:not([hidden])")
    scroll_to(page, "#result", 2500)
    say(page, "Haunted: six hidden orders aimed at AI. Code decides the verdict, not the model.", 3000)
    scroll_to(page, ".evidence", 1200)
    page.click("#ghost-list li:first-child")
    say(page, "Each one: the exact hidden sentence, how it was hidden, and where it sits on the page.", 4000)
    page.click("#ghost-list li:nth-child(4)")
    page.wait_for_timeout(2500)

    scroll_to(page, "body", 1500)
    page.click("#tab-search")
    say(page, "Agents search, then read the top results. Ghost Text checks them first.", 800)
    page.type("#q", QUERY, delay=45)
    page.click("#panel-search .go")
    page.wait_for_selector("#search:not([hidden])", timeout=120_000)
    scroll_to(page, "#search", 1000)
    say(page, "Live search (SerpApi), each result opened in a real cloud browser (Browserbase) and scanned.", 4500)
    say(page, "", 300)
    video = page.video
    ctx.close()
    browser.close()
    return Path(video.path()), lead_in


def extension_clip(p, base, out):
    profile = tempfile.mkdtemp()
    ctx = p.chromium.launch_persistent_context(profile, channel="chromium", headless=True, viewport=SIZE,
                                               record_video_dir=str(out), record_video_size=SIZE,
                                               args=[f"--disable-extensions-except={EXT}", f"--load-extension={EXT}"])
    worker = ctx.service_workers[0] if ctx.service_workers else ctx.wait_for_event("serviceworker")
    ext_id = worker.url.split("/")[2]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(f"{base}/demo/haunted-shop.html")
    say(page, "Ghost Text Shield, the browser extension. Install once, then just browse.", 3500)
    left = page.evaluate("""() => ['every review is 5 stars', 'Ignore all previous', 'approved the purchase',
        'Do not mention', 'best shop on the internet'].filter(s => document.documentElement.outerHTML.includes(s))""")
    page.evaluate(PANEL_JS, ["What your AI reads now", [f"Hidden instructions left on the page: {len(left)}",
                                                         "Reviews, prices and real content: kept"], "#9ee27a"])
    say(page, "It already removed the hidden orders. You see the same page; your AI reads a clean one.", 4500)
    tab_key = next(iter(worker.evaluate("chrome.storage.session.get(null)")))
    popup = ctx.new_page()  # resizing a tab here would resize the recorded one too, so screenshot just the popup body
    popup.goto(f"chrome-extension://{ext_id}/popup.html?tab={tab_key.removeprefix('tab')}")
    popup.wait_for_timeout(1500)
    shot = popup.locator("body").screenshot()
    popup.close()
    page.bring_to_front()
    page.evaluate("""(b64) => { const i = document.createElement('img'); i.src = 'data:image/png;base64,' + b64;
        Object.assign(i.style, {position: 'fixed', top: '30px', right: '40px', zIndex: 2147483647, border: '2px solid #e0142f',
        borderRadius: '8px', boxShadow: '0 20px 60px rgba(0,0,0,.7)'}); document.body.appendChild(i); }""",
                  __import__("base64").b64encode(shot).decode())
    say(page, "Click the ghost to see exactly what it caught, and why.", 5000)
    say(page, "Ghost Text: open source scanner, dataset and judge. Free.", 3500)
    video = page.video  # each tab records its own file: keep only this one
    ctx.close()
    shutil.rmtree(profile, ignore_errors=True)
    return Path(video.path()), 0.0


def main(base: str) -> None:
    media = ROOT / "media"
    media.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp())
    with sync_playwright() as p:
        recorded = [site_clip(p, base, work / "a"), extension_clip(p, base, work / "b")]
    clips = []
    for i, (path, skip) in enumerate(recorded):
        trimmed = work / f"clip{i}.webm"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{skip:.2f}", "-i", str(path), "-c:v", "libvpx",
                        "-b:v", "2M", str(trimmed)], check=True)
        clips.append(trimmed)
    listing = work / "list.txt"
    listing.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips))
    out = media / "ghost-text-demo.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-movflags", "+faststart", str(out)], check=True)
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000")
