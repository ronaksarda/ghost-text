"""SSRF guard (PRD 9.1): the browser may only talk to public internet hosts."""
import ipaddress
import socket
from urllib.parse import urlsplit


def is_public_url(url: str) -> bool:
    parts = urlsplit(url)
    if parts.scheme in ("data", "blob", "about"):
        return True  # no network involved
    if parts.scheme not in ("http", "https") or not parts.hostname:
        return False
    try:
        infos = socket.getaddrinfo(parts.hostname, parts.port or 443, proto=socket.IPPROTO_TCP)
    except (socket.gaierror, UnicodeError):
        return False
    # Every address must be public, so a host with one private record can't slip through.
    return all(ipaddress.ip_address(info[4][0].split("%")[0]).is_global for info in infos)


def route_guard(route):
    """Playwright route handler, applied to every request the page makes (redirects and subresources included)."""
    if is_public_url(route.request.url):
        route.continue_()
    else:
        route.abort("blockedbyclient")
