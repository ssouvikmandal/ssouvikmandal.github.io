MathJax on this website
=======================

This folder is a copy of MathJax 4.1.3 (https://www.mathjax.org, Apache License 2.0,
see LICENSE), taken from the npm package "mathjax" 4.1.3; fonts/mathjax-newcm-font/ is the
npm package "@mathjax/mathjax-newcm-font" 4.1.3 (the New Computer Modern math font for
MathJax). Both tarballs were checked against the sha512 checksums published by the npm
registry on 2026-11-18.

Only the parts a web page needs were copied: tex-chtml.js (the TeX-to-HTML component that
pages load), the extensions it loads on demand (input/, output/, a11y/, ui/, sre/ for
screen-reader speech) and the CommonHTML font files.

The settings are in ../mathjax-config.js. They point MathJax at this local font copy;
MathJax 4 would otherwise download its fonts from a CDN. build.py adds the two script
tags only to pages that contain a formula.

To update MathJax later: download the two packages from https://registry.npmjs.org (or
with `npm pack mathjax @mathjax/mathjax-newcm-font`), replace the same files, and check
a page with formulas in a browser with the network inspector open: every request must go
to this site.
