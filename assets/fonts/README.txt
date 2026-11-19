Fonts of this website
=====================

The text font is New Computer Modern 5.1 by Antonis Tsolomitis (the modern form of
Donald Knuth's Computer Modern, the default font of LaTeX), taken from the TeX Live
package "newcomputermodern" and released under the GUST Font License, a form of the
LaTeX Project Public License 1.3c; see GUST-FONT-LICENSE.txt.

The files here are derived from it: tools/make_fonts.py reduced each font to the
characters a Latin-script website needs (Latin with accents, basic Greek, punctuation,
common symbols and the f-ligatures), converted it to WOFF2, and renamed it "NewCM Web",
as the GUST Font License requests for modified fonts.

  File                         Made from              Used for
  newcm-web-book.woff2         NewCM10-Book.otf       normal text
  newcm-web-bookitalic.woff2   NewCM10-BookItalic.otf italic text
  newcm-web-bold.woff2         NewCM10-Bold.otf       bold text
  newcm-web-bolditalic.woff2   NewCM10-BoldItalic.otf bold italic text
  newcm-web-math.woff2         NewCMMath-Book.otf     symbols such as ℝ, ℤ, ≤ in the text

assets/site.css also draws one glyph of NewCMMath-Book.otf, the maps-to arrow (U+21A6),
as an SVG mask: the mark beside the current page in the menu (same licence).

Formulas are typeset by MathJax (assets/mathjax/), which brings its own New Computer
Modern math font.
