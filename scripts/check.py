#!/usr/bin/env python3
"""Check the built site in _site/.

- every in-page anchor (#id) resolves to an element id;
- every local asset is served under the site's base path (via a local HTTP server);
- every URL in content/site.toml appears in the page;
- with --external, every external URL is requested and its HTTP status reported
  (a redirect to a sign-in page is not treated as broken).

Usage: python3 scripts/check.py [--external]
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import sys
import tempfile
import threading
import tomllib
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src", "poster"):
            if a.get(key):
                self.refs.append(a[key])


def content_urls(c) -> list[str]:
    found: list[str] = []

    def walk(v, key=""):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x, k)
        elif isinstance(v, list):
            for x in v:
                walk(x, key)
        elif isinstance(v, str) and (key == "url" or key.endswith("_url")) and key != "base_url":
            found.append(v)

    walk(c)
    return found


def serve(base: str):
    """Serve _site at base (e.g. /adityasissodiya/) on a random local port."""
    tmp = tempfile.TemporaryDirectory()
    target = Path(tmp.name) / base.strip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(SITE, target_is_directory=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=tmp.name)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, tmp


def fetch(url: str, method: str = "GET") -> tuple[int, str]:
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (site link check)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as err:
        return err.code, url
    except Exception as err:  # network errors
        return 0, f"{type(err).__name__}: {err}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", action="store_true", help="also request external URLs")
    args = ap.parse_args()

    with (ROOT / "content" / "site.toml").open("rb") as f:
        c = tomllib.load(f)
    base = urlparse(c["site"]["base_url"]).path
    errors: list[str] = []

    index = (SITE / "index.html").read_text(encoding="utf-8")
    col = Collector()
    col.feed(index)

    # 1. anchors
    for ref in col.refs:
        if ref.startswith("#") or ref.startswith(base + "#"):
            frag = ref.split("#", 1)[1]
            if frag not in col.ids:
                errors.append(f"broken anchor: {ref}")

    # 2. every content URL is in the page, unchanged
    page_hrefs = {r.replace("&amp;", "&") for r in col.refs}
    for url in content_urls(c):
        if url not in page_hrefs:
            errors.append(f"content URL missing from page: {url}")
    if f"mailto:{c['profile']['email']}" not in page_hrefs:
        errors.append("email link missing")

    # 3. local resources served under the base path
    httpd, tmp = serve(base)
    origin = f"http://127.0.0.1:{httpd.server_address[1]}"
    local = {r.split("#")[0] for r in col.refs if r.startswith("/") or not re.match(r"^[a-z]+:", r)}
    local = {r for r in local if r} | {base, base + "404.html"}
    for path in sorted(local):
        if not path.startswith(base):
            errors.append(f"local link outside base path {base}: {path}")
            continue
        status, _ = fetch(origin + path, "HEAD")
        print(f"  local {status} {path}")
        if status != 200:
            errors.append(f"local resource not served: {path} ({status})")
    httpd.shutdown()
    tmp.cleanup()

    # 4. optional external check
    if args.external:
        # The site's own URL is checked after deployment, not before.
        for url in sorted({r for r in col.refs if r.startswith("http") and r != c["site"]["base_url"]}):
            status, final = fetch(url)
            note = "" if final == url else f" -> {final}"
            print(f"  external {status} {url}{note}")
            if status == 404 or status == 410 or status == 0:
                errors.append(f"external link failed: {url} ({status} {final})")

    if errors:
        print("\n".join(["FAILED:"] + [f"  - {x}" for x in errors]))
        return 1
    print(f"OK: {len(col.ids)} ids, {len(col.refs)} links checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
