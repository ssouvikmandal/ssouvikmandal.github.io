#!/usr/bin/env python3
"""Install one of the motifs from source/motifs/ as the site's icons and preview picture.

    python tools/make_icons.py hopf      (or torus, or knot)

Writes images/favicon.svg (browser tab), favicon.ico (older
browsers), images/apple-touch-icon.png (phone home screens) and images/og-image.png (the
preview picture shown when a link to the site is shared). The PNG files are drawn by a
headless Chromium through Playwright, which plain Python does not have (on the author's
server: ~/venvs/web/bin/python tools/make_icons.py hopf).

Without Playwright you can still change the browser-tab icon by hand: copy
source/motifs/NAME-icon.svg to images/favicon.svg. The PNG icons and the preview picture
then keep the old motif until this script is run.
"""
import argparse
import shutil
import struct
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOTIFS = ROOT / "source" / "motifs"
BG = "#fcfbf8"


def ico_from_pngs(pngs):
    """An .ico file holding PNG images (supported by every browser since 2009)."""
    header = struct.pack("<HHH", 0, 1, len(pngs))
    offset = 6 + 16 * len(pngs)
    entries, blobs = b"", b""
    for size, data in pngs:
        entries += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), offset)
        blobs += data
        offset += len(data)
    return header + entries + blobs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("motif", choices=sorted(p.stem for p in MOTIFS.glob("*.svg") if not p.stem.endswith("-icon")))
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright

    header_svg = MOTIFS / f"{args.motif}.svg"
    icon_svg = MOTIFS / f"{args.motif}-icon.svg"
    images = ROOT / "images"
    images.mkdir(exist_ok=True)
    shutil.copyfile(icon_svg, images / "favicon.svg")
    with open(ROOT / "site.toml", "rb") as f:
        name = tomllib.load(f)["person"]["name"]
    fonts = (ROOT / "assets" / "fonts").as_uri()

    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        browser = pw.chromium.launch()

        def shot(html, width, height, transparent=False):
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            file = Path(tmp) / "shot.html"
            file.write_text(html, encoding="utf-8")
            page.goto(file.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            data = page.screenshot(omit_background=transparent)
            page.close()
            return data

        icon = icon_svg.read_text()
        pngs = []
        for size in (16, 32, 48):
            pngs.append((size, shot(f'<body style="margin:0"><div style="width:{size}px;height:{size}px">'
                                    f'{icon.replace("<svg ", f"<svg style=\"width:{size}px;height:{size}px;display:block\" ", 1)}'
                                    "</div></body>", size, size, transparent=True)))
        (ROOT / "favicon.ico").write_bytes(ico_from_pngs(pngs))
        touch = shot(f'<body style="margin:0;background:{BG};display:grid;place-items:center;'
                     'width:180px;height:180px">'
                     + icon.replace("<svg ", '<svg style="width:132px;height:132px" ', 1)
                     + "</body>", 180, 180)
        (images / "apple-touch-icon.png").write_bytes(touch)
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
        browser.close()
    for f in ("images/favicon.svg", "favicon.ico",
              "images/apple-touch-icon.png", "images/og-image.png"):
        print(f"{f}: {(ROOT / f).stat().st_size // 1024 + 1} KB")


if __name__ == "__main__":
    main()
