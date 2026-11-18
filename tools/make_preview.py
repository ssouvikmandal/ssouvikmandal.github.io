#!/usr/bin/env python3
"""Draw the link-preview picture (images/og-image.png) with one of the motifs.

    python tools/make_preview.py hopf      (or torus, or knot)

The picture (1200 x 630 pixels) is shown when a link to the site is shared: the motif and
the name. It is drawn by a headless Chromium through Playwright, which plain Python does not
have (on the author's server: ~/venvs/web/bin/python tools/make_preview.py hopf).

The browser-tab and phone icons are made by tools/draw_favicon.py.
"""
import argparse
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOTIFS = ROOT / "source" / "motifs"
BG = "#fcfbf8"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    names = sorted(p.stem for p in MOTIFS.glob("*.svg") if not p.stem.endswith("-icon"))
    ap.add_argument("motif", choices=names, help="motif for the link-preview picture")
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright

    images = ROOT / "images"
    with open(ROOT / "site.toml", "rb") as f:
        name = tomllib.load(f)["person"]["name"]
    fonts = (ROOT / "assets" / "fonts").as_uri()
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        browser = pw.chromium.launch()

        def shot(html, width, height):
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            file = Path(tmp) / "shot.html"
            file.write_text(html, encoding="utf-8")
            page.goto(file.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            data = page.screenshot()
            page.close()
            return data

        draw_preview(shot, MOTIFS / f"{args.motif}.svg", name, fonts, images)
        browser.close()
    print(f"images/og-image.png: {(images / 'og-image.png').stat().st_size // 1024 + 1} KB")


def draw_preview(shot, header_svg, name, fonts, images):
    """The 1200 x 630 picture shown when a link to the site is shared."""
    motif = header_svg.read_text().replace("<svg ", '<svg style="width:340px;height:340px;flex:none" ', 1)
    card = f"""<html><head><style>
      @font-face {{ font-family: NewCM; src: url("{fonts}/newcm-web-book.woff2"); }}
      body {{ margin: 0; width: 1200px; height: 630px; background: {BG};
              display: flex; align-items: center; gap: 72px; padding: 0 100px;
              box-sizing: border-box; font-family: NewCM, serif; color: #1c1c1c; }}
      .name {{ font-size: 84px; line-height: 1.05; letter-spacing: .01em; white-space: nowrap; }}
      .rule {{ width: 120px; height: 2px; background: #2e4a68; margin: 34px 0 30px; }}
      .what {{ font-size: 40px; color: #595d63; font-variant-caps: all-small-caps;
               letter-spacing: .06em; }}
    </style></head><body>{motif}<div><div class="name">{name}</div>
    <div class="rule"></div><div class="what">Mathematics</div></div></body></html>"""
    (images / "og-image.png").write_bytes(shot(card, 1200, 630))

if __name__ == "__main__":
    main()
