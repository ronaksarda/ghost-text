"""Auth0: who is calling. People sign in on the site; agents use an Auth0 access token (client credentials).

Why: search checks (SerpApi) and AI summaries (Ultramarine) cost money per call, and an agent hammering the API
could mass-scan someone's site. Signed-in callers get those features and a higher rate limit; anonymous callers
can still scan, slowly. Set AUTH0_DOMAIN, AUTH0_AUDIENCE and AUTH0_CLIENT_ID (the site's SPA app) to turn it on.
"""
import os

import jwt
from fastapi import HTTPException, Request

_jwks: dict[str, jwt.PyJWKClient] = {}


def configured() -> bool:
    return bool(os.environ.get("AUTH0_DOMAIN") and os.environ.get("AUTH0_AUDIENCE"))


def public_config() -> dict | None:
    if not (configured() and os.environ.get("AUTH0_CLIENT_ID")):
        return None
    return {"domain": os.environ["AUTH0_DOMAIN"], "clientId": os.environ["AUTH0_CLIENT_ID"], "audience": os.environ["AUTH0_AUDIENCE"]}


def caller(request: Request) -> dict | None:
    """Verified token claims, or None for an anonymous caller. A bad token is an error, never anonymous."""
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer ") or not configured():
        return None
    domain = os.environ["AUTH0_DOMAIN"]
    client = _jwks.setdefault(domain, jwt.PyJWKClient(f"https://{domain}/.well-known/jwks.json", cache_keys=True))
    token = header[7:].strip()
    try:
        key = client.get_signing_key_from_jwt(token).key
        return jwt.decode(token, key, algorithms=["RS256"], audience=os.environ["AUTH0_AUDIENCE"],
                          issuer=f"https://{domain}/", options={"require": ["exp", "sub"]})
    except jwt.PyJWTError:
        raise HTTPException(401, "Sign-in expired or invalid. Sign in again.")


def require(request: Request) -> dict:
    who = caller(request)
    if who:
        return who
    if not configured():
        return {"sub": "local"}  # local dev without Auth0: paid features still have daily caps
    raise HTTPException(401, "Sign in to use this.")
