"""python scripts/post_images.py [base-url] — screenshots and a GIF for the DEV post, all from the running product.

Writes media/*.png and media/demo.gif. Needs the app running, ffmpeg, and media/ghost-text-demo.mp4 for the GIF.
"""
import base64
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

from record_demo import EXT, PANEL_JS, QUERY

MEDIA = Path(__file__).parent.parent / "media"


def site_shots(p, base):
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1.5)

    page.goto(base)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(4500)  # flicker, glitch and the hidden line surfacing
    page.screenshot(path=MEDIA / "cover.png", clip={"x": 140, "y": 110, "width": 1000, "height": 420})

    hostile = [g["text"] for g in json.load(urllib.request.urlopen(f"{base}/demo-results/haunted-shop.json"))["ghosts"]
               if g["label"] == "injection"]
    page.goto(f"{base}/demo/haunted-shop.html")
    page.screenshot(path=MEDIA / "shop.png", clip={"x": 0, "y": 0, "width": 1280, "height": 520})  # what a person sees
    page.evaluate(PANEL_JS, ["What your AI reads on this page", hostile[:5], "#e0142f"])
    page.screenshot(path=MEDIA / "what-ai-reads.png", clip={"x": 0, "y": 0, "width": 1280, "height": 520})

    page.goto(base)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.click("[data-demo=haunted-shop]")
    page.wait_for_selector("#result:not([hidden])")
    page.wait_for_timeout(1200)
    page.evaluate("window.scrollTo(0, document.querySelector('#result').offsetTop - 10)")
    page.locator("#ghost-list li").first.click()
    page.wait_for_timeout(900)
    page.evaluate("window.scrollTo(0, document.querySelector('#result').offsetTop - 10)")
    page.wait_for_timeout(600)
    page.screenshot(path=MEDIA / "verdict.png")

    page.goto(base)
    page.click("#tab-search")
    page.fill("#q", QUERY)
    page.click("#panel-search .go")
    page.wait_for_selector("#search:not([hidden])", timeout=180_000)
    page.wait_for_timeout(800)
    page.evaluate("window.scrollTo(0, document.querySelector('#search').offsetTop - 10)")
    page.wait_for_timeout(600)
    page.screenshot(path=MEDIA / "search.png")
    browser.close()


def shield_shot(p, base):
    profile = tempfile.mkdtemp()
    ctx = p.chromium.launch_persistent_context(profile, channel="chromium", headless=True,
                                               viewport={"width": 1280, "height": 720}, device_scale_factor=1.5,
                                               args=[f"--disable-extensions-except={EXT}", f"--load-extension={EXT}"])
    worker = ctx.service_workers[0] if ctx.service_workers else ctx.wait_for_event("serviceworker")
    ext_id = worker.url.split("/")[2]
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(f"{base}/demo/haunted-shop.html")
    page.wait_for_timeout(2500)
    tab = next(iter(worker.evaluate("chrome.storage.session.get(null)"))).removeprefix("tab")
    popup = ctx.new_page()
    popup.goto(f"chrome-extension://{ext_id}/popup.html?tab={tab}")
    popup.wait_for_timeout(1200)
    shot = base64.b64encode(popup.locator("body").screenshot()).decode()
    popup.close()
    page.bring_to_front()
    page.evaluate("""(b64) => { const i = document.createElement('img'); i.src = 'data:image/png;base64,' + b64;
        Object.assign(i.style, {position: 'fixed', top: '24px', right: '40px', width: '340px', border: '2px solid #e0142f',
        borderRadius: '8px', boxShadow: '0 20px 60px rgba(0,0,0,.5)'}); document.body.appendChild(i); }""", shot)
    page.wait_for_timeout(600)
    page.screenshot(path=MEDIA / "shield.png")
    ctx.close()


def gif():
    """The first 30 s of the demo video: the shop, what the AI reads, the verdict."""
    palette = Path(tempfile.mkdtemp()) / "palette.png"
    clip = ["-ss", "0", "-t", "30", "-i", str(MEDIA / "ghost-text-demo.mp4")]
    filters = "fps=8,scale=760:-1:flags=lanczos"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *clip, "-vf", f"{filters},palettegen=max_colors=96", str(palette)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *clip, "-i", str(palette), "-lavfi",
                    f"{filters}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4", str(MEDIA / "demo.gif")], check=True)


def main(base):
    MEDIA.mkdir(exist_ok=True)
    with sync_playwright() as p:
        site_shots(p, base)
        shield_shot(p, base)
    gif()
    for f in sorted(MEDIA.glob("*.png")) + [MEDIA / "demo.gif"]:
        print(f"{f.name:20} {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000")
