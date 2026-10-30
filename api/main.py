"""uvicorn api.main:app — POST /scan, /search, /summarize, /judge, the demo gallery, and the website (PRD 5, 8, 9.1)."""
import asyncio
import io
import json
import os
import hashlib
import threading
import time
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import envfile
from api import auth
from eval import victim
from exorcist import exorcise, rules_labeler
from judge import client as judge_client
from scanner.scan import MAX_HTML, ScanError, scan

envfile.load()
ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo"
RATE, RATE_SIGNED_IN, WINDOW = 10, 60, 60.0
DAILY = {"summarize": 300, "search": 100}  # caps spend on paid APIs even if an account is abused
spent: dict[str, list] = {}
cache: dict[str, dict] = {}
busy = threading.BoundedSemaphore(2)  # one Chromium per scan; more than two at once starves a small droplet
hits: dict[str, deque] = defaultdict(deque)
demo_results: dict[str, dict] = {}


class ScanRequest(BaseModel):
    url: str | None = None
    html: str | None = None


def labeler():
    """The fine-tuned judge when JUDGE_URL is set; rules only otherwise (PRD 9.5)."""
    if judge_client.configured() and judge_client.alive():
        return judge_client.label, "online"
    return rules_labeler, "offline"


def browserbase_cdp_url() -> str | None:
    """One Browserbase session per scan (PRD 10). None means use local Chromium."""
    key = os.environ.get("BROWSERBASE_API_KEY")
    if not key:
        return None
    body = {"timeout": 120}  # a scan takes seconds; never leave a paid session running
    if os.environ.get("BROWSERBASE_PROJECT_ID"):
        body["projectId"] = os.environ["BROWSERBASE_PROJECT_ID"]  # optional: Browserbase infers it from the key
    req = urllib.request.Request("https://api.browserbase.com/v1/sessions", method="POST",
                                 data=json.dumps(body).encode(),
                                 headers={"X-BB-API-Key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r)["connectUrl"]
    except Exception:
        return None  # Browserbase down or out of credit: fall back to local Chromium (PRD 9.2)


def run_scan(url: str | None = None, html: str | None = None, screenshot: bool = True) -> dict:
    label_fn, judge = labeler()
    cdp = browserbase_cdp_url() if url else None
    try:
        result = scan(url=url, html=html, screenshot=screenshot, cdp_url=cdp)
    except ScanError:
        raise
    except Exception:
        if not cdp:
            raise
        result = scan(url=url, html=html, screenshot=screenshot)  # remote browser failed mid-scan: retry locally
    result = exorcise(result, label_fn)
    # What a naive agent reads (DOM text, ghosts included): the "before" side of the AI summary comparison.
    result["raw_text"] = "\n".join(p["text"] for p in result.pop("reading"))[:20_000]
    return {**result, "judge": judge, "browser": "browserbase" if cdp else "chromium"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Demo verdicts are computed once at startup, so the gallery works even if the browser backend breaks later.
    for page in sorted(DEMO.glob("*.html")):
        # Playwright's sync API refuses to run on the event loop thread.
        result = await asyncio.to_thread(run_scan, html=page.read_text(encoding="utf-8"))
        demo_results[page.stem] = {**result, "url": f"/demo/{page.name}"}
    yield


app = FastAPI(title="Ghost Text", lifespan=lifespan, docs_url="/api/docs", redoc_url=None)


@app.middleware("http")
async def revalidate(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("Cache-Control", "no-cache")  # small site: always revalidate, so a deploy shows at once
    return response


def client_ip(request: Request) -> str:
    # Behind Caddy, uvicorn --proxy-headers puts the visitor's address here. Only Caddy can reach the app port.
    return request.client.host if request.client else "?"


def check_rate(who: str, limit: int = RATE) -> None:
    now, q = time.monotonic(), hits[who]
    while q and now - q[0] > WINDOW:
        q.popleft()
    if len(q) >= limit:
        retry = int(WINDOW - (now - q[0])) + 1
        raise HTTPException(429, f"Too many scans. Try again in {retry} seconds.", headers={"Retry-After": str(retry)})
    q.append(now)


def limit(request: Request) -> None:
    """Signed-in people and agents get their own, higher limit; everyone else shares a per-IP one."""
    who = auth.caller(request)
    check_rate(f"user:{who['sub']}", RATE_SIGNED_IN) if who else check_rate(client_ip(request))


def spend(kind: str, n: int = 1) -> None:
    day = time.strftime("%Y-%m-%d")
    used = spent.setdefault(kind, [day, 0])
    if used[0] != day:
        used[:] = [day, 0]
    if used[1] + n > DAILY[kind]:
        raise HTTPException(429, "Today's free allowance for this feature is used up. Try again tomorrow.")
    used[1] += n


def validate(body: ScanRequest) -> None:
    if (body.url is None) == (body.html is None):
        raise HTTPException(400, "Send either a URL or HTML, not both.")
    if body.html is not None:
        if len(body.html) > MAX_HTML:
            raise HTTPException(400, "Pasted HTML is larger than 2 MB.")
        return
    url = body.url.strip()
    if len(url) > 2000:
        raise HTTPException(400, "That URL is longer than 2,000 characters.")
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise HTTPException(400, "Only http:// and https:// URLs can be scanned.")
    body.url = url


@app.post("/scan")
def scan_endpoint(body: ScanRequest, request: Request):
    validate(body)
    limit(request)
    if not busy.acquire(timeout=30):
        raise HTTPException(503, "Ghost Text is busy. Try again in a minute.")
    try:
        result = run_scan(url=body.url, html=body.html)
    except ScanError as e:
        raise HTTPException(400 if "public" in str(e) or "2 MB" in str(e) else 422, str(e))
    except Exception:
        raise HTTPException(502, "The browser could not load that page. If it needs a login or blocks bots, use Paste HTML.")
    finally:
        busy.release()
    if body.url:
        host = urlsplit(body.url).hostname or ""
        try:
            result["host"] = host.encode("idna").decode()  # show the punycode form so lookalike domains are visible
        except UnicodeError:
            result["host"] = host
    return result


class Ghost(BaseModel):
    text: str
    technique: list[str] = []
    context: str = ""


class JudgeRequest(BaseModel):
    ghosts: list[Ghost]


@app.post("/judge")
def judge_endpoint(body: JudgeRequest, request: Request):
    """For the browser extension: label hidden sentences it found. Gets ghost text only, never a page; stores nothing."""
    if not (judge_client.configured() and judge_client.alive()):
        raise HTTPException(503, "AI judge offline.")
    if not 1 <= len(body.ghosts) <= 50 or any(len(g.text) > 4000 for g in body.ghosts):
        raise HTTPException(400, "Send 1 to 50 ghosts, each under 4,000 characters.")
    limit(request)
    ghosts = [{"id": f"g{i}", **g.model_dump()} for i, g in enumerate(body.ghosts)]
    exorcise({"ghosts": ghosts, "reading": []}, judge_client.label)  # same floor and fail-closed path as /scan
    return {"labels": [[g["label"], g["reason"]] for g in ghosts]}


class SummarizeRequest(BaseModel):
    raw: str
    clean: str


@app.post("/summarize")
def summarize_endpoint(body: SummarizeRequest, request: Request, who: dict = Depends(auth.require)):
    """Ultramarine summarises the page twice: as a naive agent reads it, and after Ghost Text cleans it."""
    if not victim.configured():
        raise HTTPException(503, "AI summaries are offline.")
    raw, clean = body.raw[:victim.MAX_CHARS], body.clean[:victim.MAX_CHARS]
    key = hashlib.sha256((raw + "\0" + clean).encode()).hexdigest()
    if key not in cache:
        check_rate(f"user:{who['sub']}", RATE_SIGNED_IN)
        spend("summarize", 2)
        before = dict(victim.usage)
        try:
            with ThreadPoolExecutor(2) as pool:
                raw_sum, clean_sum = pool.map(victim.summarize, [raw, clean])
        except Exception:
            raise HTTPException(502, "The AI summary service did not answer. Try again in a minute.")
        run = {k: victim.usage[k] - before[k] for k in before}  # approximate if two requests overlap
        cache[key] = {"raw": raw_sum, "clean": clean_sum, "model": victim.MODEL, "cost_usd": victim.cost_usd(run)}
        if len(cache) > 500:
            cache.pop(next(iter(cache)))
    return cache[key]


class SearchRequest(BaseModel):
    q: str


def serp(q: str) -> list[dict]:
    params = urllib.parse.urlencode({"engine": "google", "q": q, "num": 10, "api_key": os.environ["SERPAPI_KEY"]})
    with urllib.request.urlopen(f"https://serpapi.com/search.json?{params}", timeout=20) as r:
        return [x for x in json.load(r).get("organic_results", []) if x.get("link", "").startswith(("http://", "https://"))]


def check_result(item: dict) -> dict:
    row = {"title": item.get("title", ""), "link": item["link"], "snippet": item.get("snippet", "")}
    try:
        result = run_scan(url=item["link"], screenshot=False)
    except ScanError as e:
        return {**row, "verdict": "unscanned", "error": str(e)}
    except Exception:
        return {**row, "verdict": "unscanned", "error": "The page did not load."}
    hostile = sorted((g for g in result["ghosts"] if g["label"] != "benign"), key=lambda g: g["label"] != "injection")
    return {**row, "verdict": result["verdict"], "hostile": len(hostile), "first": hostile[0]["text"][:200] if hostile else None}


@app.post("/search")
def search_endpoint(body: SearchRequest, request: Request, who: dict = Depends(auth.require)):
    """Search the web (SerpApi) and scan the top results before an agent reads them."""
    q = " ".join(body.q.split())
    if not 1 <= len(q) <= 200:
        raise HTTPException(400, "Type a search of up to 200 characters.")
    if not os.environ.get("SERPAPI_KEY"):
        raise HTTPException(503, "Search is offline.")
    key = "search:" + q.lower()
    hit = cache.get(key)
    if hit and time.time() - hit["at"] < 3600:
        return hit["body"]
    check_rate(f"user:{who['sub']}", RATE_SIGNED_IN)
    spend("search")
    try:
        items = serp(q)[:5]
    except Exception:
        raise HTTPException(502, "The search service did not answer. Try again in a minute.")
    if not busy.acquire(timeout=30):
        raise HTTPException(503, "Ghost Text is busy. Try again in a minute.")
    try:
        with ThreadPoolExecutor(3) as pool:  # results load in parallel; each scan keeps its own 20 s limit
            rows = list(pool.map(check_result, items))
    finally:
        busy.release()
    out = {"q": q, "results": rows}
    cache[key] = {"at": time.time(), "body": out}
    return out


@app.get("/config")
def config():
    """What the site can offer right now, and the public Auth0 settings for sign-in."""
    return {"auth0": auth.public_config(), "summaries": victim.configured(),
            "search": bool(os.environ.get("SERPAPI_KEY")), "judge": labeler()[1]}


@app.get("/demo-results/{name}.json")
def demo_result(name: str):
    if name not in demo_results:
        raise HTTPException(404, "No such demo page.")
    if demo_results[name]["judge"] == "offline" and labeler()[1] == "online":
        # The judge was still loading at startup: redo the demo once it is up, keep the old result if that fails.
        try:
            demo_results[name] = {**run_scan(html=(DEMO / f"{name}.html").read_text(encoding="utf-8")), "url": f"/demo/{name}.html"}
        except Exception:
            pass
    return JSONResponse(demo_results[name])


@app.get("/ghost-text-shield.zip")
def shield_zip(request: Request):
    """The browser extension, zipped from extension/ on request, pointed at the server it was downloaded from."""
    origin = str(request.base_url).rstrip("/")  # needs uvicorn --proxy-headers behind a TLS proxy to read https
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT / "extension").iterdir()):
            if f.suffix == ".png":
                z.write(f, f"ghost-text-shield/{f.name}")
            elif f.suffix in (".js", ".json", ".html"):
                text = f.read_text(encoding="utf-8").replace("http://localhost:8000", origin)
                z.writestr(f"ghost-text-shield/{f.name}", text)
    return Response(buf.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": 'attachment; filename="ghost-text-shield.zip"'})


@app.get("/health")
def health():
    return {"ok": True, "demos": len(demo_results)}


app.mount("/demo", StaticFiles(directory=DEMO), name="demo")
app.mount("/", StaticFiles(directory=ROOT / "web", html=True), name="web")
