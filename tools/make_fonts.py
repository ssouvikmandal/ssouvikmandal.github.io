#!/usr/bin/env python3
"""Make the web fonts in assets/fonts/ from New Computer Modern (TeX Live).

You only need this script to change the character set or the font; the finished .woff2
files are already in assets/fonts/. It needs fontTools and brotli, which are not part of
plain Python (on the author's server: ~/venvs/web/bin/python tools/make_fonts.py).

Source: New Computer Modern 5.1 by Antonis Tsolomitis (TeX Live package "newcomputermodern"),
GUST Font License. The subsets get new font and file names ("NewCM Web"), as the GUST Font
License requests for derived fonts; see assets/fonts/README.txt.
"""
import argparse
import subprocess
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "assets" / "fonts"

# Latin with accents (for names of co-authors and places), basic Greek, punctuation,
# common symbols and the f-ligatures.
TEXT_RANGES = [
    (0x0020, 0x007E), (0x00A0, 0x00FF), (0x0100, 0x017F), (0x0180, 0x024F),
    (0x02B9, 0x02DD), (0x0300, 0x036F), (0x0391, 0x03A9), (0x03B1, 0x03C9),
    (0x03D1, 0x03D6), (0x1E00, 0x1EFF), (0x2000, 0x206F), (0x20AC, 0x20AC),
    (0x2116, 0x2116), (0x2122, 0x2122), (0x2190, 0x2193), (0x2212, 0x2212),
    (0xFB00, 0xFB06),
]
# Mathematical letters and symbols that the text fonts lack (e.g. ℝ), taken from the
# math font and used through unicode-range.
MATH_CODEPOINTS = [0x2102, 0x2115, 0x2119, 0x211A, 0x211D, 0x2124, 0x2200, 0x2202, 0x2203,
                   0x2205, 0x2207, 0x2208, 0x2209, 0x220F, 0x2211, 0x2218, 0x221A, 0x221E,
                   0x2227, 0x2228, 0x2229, 0x222A, 0x222B, 0x2243, 0x2245, 0x2248, 0x2260,
                   0x2261, 0x2264, 0x2265, 0x2282, 0x2283, 0x2286, 0x2287, 0x2295, 0x2297,
                   0x22C5, 0x27E8, 0x27E9]

FACES = [  # (source file, output name, style name)
    ("NewCM10-Book.otf", "newcm-web-book", "Book"),
    ("NewCM10-BookItalic.otf", "newcm-web-bookitalic", "Book Italic"),
    ("NewCM10-Bold.otf", "newcm-web-bold", "Bold"),
    ("NewCM10-BoldItalic.otf", "newcm-web-bolditalic", "Bold Italic"),
    ("NewCMMath-Book.otf", "newcm-web-math", "Math"),
]
FAMILY = "NewCM Web"
NOTE = ("Subset of New Computer Modern 5.1 by Antonis Tsolomitis, renamed and converted "
        "to WOFF2 for the web. GUST Font License (LPPL 1.3c or later).")


def find_source(name):
    return Path(subprocess.run(["kpsewhich", name], capture_output=True, text=True,
                               check=True).stdout.strip())


def unicodes(ranges):
    return [c for a, b in ranges for c in range(a, b + 1)]


def rename(font, style):
    name = font["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17):
            name.removeNames(nameID=rec.nameID)
    ps = (FAMILY + "-" + style).replace(" ", "")
    for nid, value in [(1, FAMILY + " " + style), (2, "Regular"), (3, ps), (4, FAMILY + " " + style),
                       (6, ps), (16, FAMILY), (17, style), (10, NOTE)]:
        name.setName(value, nid, 3, 1, 0x409)
        name.setName(value, nid, 1, 0, 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for src, out, style in FACES:
        path = find_source(src)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]          # keep ligatures, kerning, small caps, old-style figures
        opts.name_IDs = ["*"]
        opts.name_languages = ["*"]
        opts.notdef_outline = True
        opts.hinting = False
        opts.desubroutinize = True
        font = TTFont(path)
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=MATH_CODEPOINTS if style == "Math" else unicodes(TEXT_RANGES))
        sub.subset(font)
        rename(font, style)
        target = OUT / f"{out}.woff2"
        font.flavor = "woff2"
        font.save(target)
        print(f"{target.relative_to(HERE)}: {target.stat().st_size // 1024} KB "
              f"({len(font.getBestCmap())} characters)")


if __name__ == "__main__":
    main()
