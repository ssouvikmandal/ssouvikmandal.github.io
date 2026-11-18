#!/usr/bin/env python3
"""Open every page in headless Chromium at phone and computer widths, save screenshots and
report problems: requests to outside servers, missing files, script errors, images that do
not load, images without alt text, and pages wider than the screen.

    python tools/screenshots.py OUTPUT_FOLDER
    python tools/screenshots.py OUTPUT_FOLDER --url https://ssouvikmandal.github.io   (live site)

Needs Playwright (on the author's server: ~/venvs/web/bin/python tools/screenshots.py ...).
Without --url, the site is served from this folder at http://127.0.0.1:8765/ for the
duration of the run. Either way the browser is not allowed to contact any other server than
the site's own.
"""
import argparse
import functools
import http.server
import re
import sys
import threading
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = 8765
SIZES = {"phone": dict(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                       is_mobile=True, has_touch=True),
         "computer": dict(viewport={"width": 1440, "height": 900}, device_scale_factor=1)}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    ap.add_argument("--pages", nargs="*", help="only these pages (default: all)")
    ap.add_argument("--prefix", default="", help="prefix for the screenshot file names")
    ap.add_argument("--sizes", nargs="*", default=list(SIZES), choices=list(SIZES))
    ap.add_argument("--viewport-only", action="store_true", help="screenshot the first screen only")
    ap.add_argument("--scale", type=float, default=1, help="pixel density of the computer screenshots (phone: 2)")
    ap.add_argument("--url", help="check this published site instead of the local files")
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright

    with open(ROOT / "site.toml", "rb") as f:
        cfg = tomllib.load(f)
    pages = args.pages or [n["file"] for n in cfg["nav"]] + ["404.html", "no-such-page/"]
    args.out.mkdir(parents=True, exist_ok=True)

    class NotFound(Quiet):          # imitate GitHub Pages: unknown addresses get 404.html
        def send_error(self, code, message=None, explain=None):
            if code == 404:
                body = (ROOT / "404.html").read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                super().send_error(code, message, explain)

    if args.url:
        base, server = args.url.rstrip("/") + "/", None
    else:
        base = f"http://127.0.0.1:{PORT}/"
        server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT),
                                                 functools.partial(NotFound, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
    problems = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for size in args.sizes:
            opts = dict(SIZES[size])
            if size == "computer":
                opts["device_scale_factor"] = args.scale
            ctx = browser.new_context(**opts)
            for page_name in pages:
                page = ctx.new_page()
                outside, failed, errors = [], [], []

                def route(r):
                    if r.request.url.startswith(base):
                        r.continue_()
                    else:
                        outside.append(r.request.url)
                        r.abort()
                page.route("**/*", route)
                page.on("response", lambda r: failed.append(f"{r.status} {r.url}")
                        if r.status >= 400 and not r.url.endswith(("404.html", "no-such-page/")) else None)
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("console", lambda m: errors.append(m.text) if m.type == "error"
                        and "404" not in m.text else None)
                page.goto(base + page_name, wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(300)
                info = page.evaluate("""() => ({
                    overflow: document.documentElement.scrollWidth - window.innerWidth,
                    brokenImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src),
                    noAlt: [...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.src),
                    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.style + ' ' + f.weight),
                    title: document.title,
                    h1: [...document.querySelectorAll('h1')].length,
                })""")
                stem = re.sub(r"[^a-z0-9-]+", "-", page_name.replace(".html", "")).strip("-") or "index"
                shot = args.out / f"{args.prefix}{stem}-{size}.png"
                page.screenshot(path=str(shot), full_page=not args.viewport_only)
                label = f"{page_name} ({size})"
                for u in outside:
                    problems.append(f"{label}: tried to contact an outside server: {u}")
                for u in failed:
                    problems.append(f"{label}: request failed: {u}")
                for e in errors:
                    problems.append(f"{label}: script error: {e}")
                for u in info["brokenImages"]:
                    problems.append(f"{label}: image did not load: {u}")
                for u in info["noAlt"]:
                    problems.append(f"{label}: image without alt text: {u}")
                if info["overflow"] > 0:
                    problems.append(f"{label}: page is {info['overflow']} px wider than the screen")
                if info["h1"] != 1:
                    problems.append(f"{label}: {info['h1']} h1 headings (expected 1)")
                print(f"{label}: {info['title']!r}; fonts: {', '.join(sorted(set(info['fonts']))) or 'none'}")
                page.close()
            ctx.close()
        browser.close()
    if server:
        server.shutdown()
    print("no problems" if not problems else f"{len(problems)} problem(s):")
    for p in problems:
        print("  - " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
