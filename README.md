# Website of Souvik Mandal

Source and published files of <https://ssouvikmandal.github.io>, moved from the Google Site
<https://sites.google.com/view/souvik-mandal> on 18 November 2026.

The published site is plain HTML and CSS with relative links. Fonts and MathJax are stored
here, and the site uses no outside services, trackers or cookies. A page is only regenerated
when you run `python3 build.py`, which needs Python 3.11 or later and nothing else.

## Contents

- [The files](#the-files)
- [Everyday changes](#everyday-changes): position, email, address · CV · photo · a
  teaching entry · a paper · a talk · a new section · formulas
- [Publishing](#publishing)
- [Placeholders](#placeholders)
- [Moving the site](#moving-the-site): your own domain · a university server
- [The motif](#the-motif)
- [Tools and licences](#tools-and-licences)

## The files

```
site.toml                 ← your name, position, affiliation, email, address, profiles, menu
source/pages/*.html       ← the text of each page (edit these)
source/template.html      ← the frame around every page: head, header, menu, footer
build.py                  ← turns the two above into the published pages
index.html, cv.html, …    ← the published pages (generated: do not edit by hand)
cv.pdf                    ← your CV
images/photo.jpg          ← your photo
images/motif.svg, images/favicon.svg, favicon.ico, images/apple-touch-icon.png,
images/og-image.png       ← the motif in the header, the browser icons, the link preview
assets/site.css           ← the design: colours, fonts, spacing (colours at the top)
assets/fonts/             ← the text font (New Computer Modern), see its README.txt
assets/mathjax/, assets/mathjax-config.js   ← MathJax for formulas, see README-SITE.txt
sitemap.xml, robots.txt   ← for search engines (generated)
404.html                  ← the "page not found" page (generated)
source/last-updated.json  ← the "last updated" date of each page (kept by build.py)
source/motifs/            ← the three motif drawings (torus, Hopf fibration, trefoil knot)
tools/                    ← optional helpers; they need extra Python packages, build.py does not
```

Page addresses never change: `index.html`, `cv.html`, `research.html`,
`achievements.html`, `teaching.html`, `conferences.html` and `contact.html`, and the CV is
always `cv.pdf`. When you update a file, keep its name, so that old links keep working.

## Everyday changes

Each change follows the same three steps:

1. Edit `site.toml`, a file in `source/pages/`, or replace a file.
2. Run `python3 build.py --check` in this folder. It regenerates the pages and checks every
   link between them. A page whose content changed gets today's date in its footer.
3. Look at the result: open `index.html` in a browser, or run
   `python3 -m http.server 8000` and open <http://localhost:8000>. Then publish
   (see [Publishing](#publishing)).

### Position, affiliation, email, address (a new job)

Everything that changes with a job is in `site.toml`, under `[person]`:

```toml
position = "Postdoctoral Fellow"
department = "Department of Mathematics"
institution = "Example University"
email = "new.address@example.edu"
address = [
  "Souvik Mandal",
  "Department of Mathematics, Example University",
  "City, Postcode",
  "Country",
]
```

`position`, `department` and `institution` appear under your name on every page, in the
page descriptions for search engines and in the structured data (schema.org) on the home
page. `email` and `address` appear on the Contact page. Then rebuild. The introduction on
the home page is ordinary text: edit it in `source/pages/index.html`.

### The CV

Replace `cv.pdf` with the new file (same name) and run `python3 build.py`. Every link to the
CV points to `cv.pdf`, so nothing else changes.

### The photo

Replace `images/photo.jpg` with the new photo (same name; JPEG, about 400 × 500 pixels,
under 100 KB) and run `python3 build.py`. The build reads the photo's size, so a photo with
different proportions is still shown undistorted.

### A teaching entry

In `source/pages/teaching.html`, copy one `<li>…</li>` line, put it at the top of the list
(newest first) and change the text. Example:

```html
  <li><span class="lead">Institute TA (Jan-April 2027)</span> for MA1234 (Course Name) under Dr. Name, Department of Mathematics, IIT Madras.</li>
```

The part in `<span class="lead">` is set in small capitals. For a course you teach
yourself you might later start a second list under a heading, e.g.
`<h2>Courses taught</h2>`, followed by `<ul class="entries"> … </ul>`.

### A paper

There is no Publications page yet. To start one, create
`source/pages/publications.html`:

```html
<!--
title: Publications
description: Publications and preprints of {{name}}, {{department}}, {{institution}}.
-->
<h1>Publications</h1>

<h2>Preprints</h2>
<ol class="entries" reversed>
  <li>
    <span class="title">Title of the paper</span>, with A. Coauthor.
    <span class="meta">Preprint, 2027.</span>
    <span class="links"><a href="https://arxiv.org/abs/2701.01234">arXiv</a></span>
  </li>
</ol>

<h2>Published papers</h2>
<ol class="entries" reversed>
  <li>
    <span class="title">Title of the paper</span>.
    <span class="meta">Journal Name <b>12</b> (2027), no. 3, 1–20.</span>
    <span class="links"><a href="https://doi.org/10.xxxx/xxxxx">DOI</a> <a href="https://arxiv.org/abs/2601.01234">arXiv</a> <a href="papers/short-name.pdf">PDF</a></span>
  </li>
</ol>
```

and add it to the menu in `site.toml`, at the place where it should appear:

```toml
[[nav]]
label = "Publications"
file = "publications.html"
```

New papers go at the top of their list; `reversed` makes the numbers count down, so the
oldest paper stays number 1. When a preprint is published, move its `<li>` to the second
list and add the journal and DOI. Keep the format of every entry the same:
title in `<span class="title">`, coauthors after "with", journal data in
`<span class="meta">`, links in `<span class="links">`. Put PDFs of your own papers in a
folder `papers/` with short, permanent names (e.g. `papers/surgery-cayley.pdf`).

### A talk

Create `source/pages/talks.html` in the same way (and add it to `[[nav]]`):

```html
<!--
title: Talks
description: Talks given by {{name}}.
-->
<h1>Talks</h1>
<ul class="dated">
  <li>
    <span class="date">March 2027</span>
    <span><span class="title">Title of the talk</span>. Topology Seminar, University, City.
      <span class="links"><a href="slides/2027-03-city.pdf">Slides</a></span></span>
  </li>
</ul>
```

Each `<li>` has two parts: the date, and everything else in one `<span>`. On a computer the
dates form a column on the left; on a phone they sit above each entry. Put slides in a
folder `slides/`.

### A new section (News, Students, …)

Any new page works like Publications and Talks: create `source/pages/NAME.html` beginning
with the comment that holds `title:` and `description:` (both should contain `{{name}}`,
so that search engines see your name), write the text in HTML, add the page to `[[nav]]`
in `site.toml`, and rebuild. The menu has room for more entries: on a computer it is a
column on the left, on a phone it wraps onto more lines. For a News page use the dated
list of the Talks example; for Students use `<ul class="entries">` with one `<li>` per
student. Do not create a page before it has content.

The placeholders that `build.py` fills in are listed at the top of `build.py`, for example
`{{name}}`, `{{email_link}}`, `{{address}}`, `{{photo}}` and `{{profile_links}}`.

### Formulas

Write TeX between `$…$` or `\(…\)` (inline) or `$$…$$` or `\[…\]` (displayed); write `\$`
for a dollar sign. `build.py` notices the formulas and adds MathJax to that page only.
Commutative diagrams work with the `CD` environment of amscd:

```tex
\[ \begin{CD} \pi_n(F) @>>> \pi_n(E) @>>> \pi_n(B) \\ @VVV @VVV @VVV \\ \pi_n(F') @>>> \pi_n(E') @>>> \pi_n(B') \end{CD} \]
```

MathJax cannot read TikZ (tikz-cd). For a diagram that needs it, make an SVG with LaTeX
(`latex` + `dvisvgm`) and include it as an image with a short `alt` text.

## Publishing

The site is published by GitHub Pages from the branch `main` of
`github.com/ssouvikmandal/ssouvikmandal.github.io`, folder `/` (root). After a change:

```bash
python3 build.py --check
git add -A
git commit -m "Add paper on ..."
git push
```

GitHub publishes the new version within a minute or two. The empty file `.nojekyll` tells
GitHub to publish the files exactly as they are, without processing them.

On the server, the remote is `git@github-website:ssouvikmandal/ssouvikmandal.github.io.git`,
where `github-website` is an SSH alias (in `~/.ssh/config`) that uses the deploy key
`~/.ssh/id_ed25519_github_website`, which can write to this one repository only.
`.git/hooks/pre-commit` runs `~/.local/bin/work-backup pre-commit`, the same check as in
`~/work`: it leaves files larger than 70 MB out of a commit (listing them at the end of
`.gitignore`) and refuses to commit text files that contain a private key or an access
token. Git hooks are not copied by `git clone`; `~/work/server-config/README.md` says how to
set them up again.

## Placeholders

None at present: the photo (`images/photo.jpg`) and the CV (`cv.pdf`, the file
"CV(UPDATED_OCT2024).pdf" linked from the Google Site) were both downloaded from the Google
Site. If a file ever has to be replaced by a placeholder, give the placeholder the final
name, list it here, and later just overwrite it with the real file (same name) and rebuild.

## Moving the site

The pages link to each other with relative links, so the published files work in any
location without changes. Only `sitemap.xml`, `robots.txt`, the link-preview tags and the
404 page contain the full address, and all of them come from one line in `site.toml`.

### Your own domain (e.g. `www.souvikmandal.com`) on GitHub Pages

1. In `site.toml`, set `url = "https://www.souvikmandal.com"` and run `python3 build.py`.
2. Create a file `CNAME` in this folder containing the single line `www.souvikmandal.com`,
   commit and push.
3. At your domain registrar, add a DNS record `CNAME` for `www` pointing to
   `ssouvikmandal.github.io` (for the bare domain `souvikmandal.com`, the `A` records listed
   in GitHub's documentation "Managing a custom domain for your GitHub Pages site").
4. In the repository on GitHub: Settings → Pages → Custom domain, enter the domain, and
   tick "Enforce HTTPS" once it is offered.

The old address `ssouvikmandal.github.io` then redirects to the new domain automatically.

### A university server

1. In `site.toml`, set `url` to the new address, e.g.
   `url = "https://www.math.example.edu/~smandal"`, and run `python3 build.py`.
2. Copy the published files to the web folder you are given (often `~/public_html`):
   every `*.html` file, `cv.pdf`, `favicon.ico`, `sitemap.xml`, `robots.txt` and the folders
   `assets/` and `images/` (and `papers/`, `slides/` if you have them). The sources
   (`source/`, `tools/`, `build.py`, `site.toml`, `README.md`) need not be copied.
   For example:
   `rsync -av --exclude={.git,.gitignore,.nojekyll,source,tools,build.py,site.toml,README.md} ./ user@server:public_html/`
3. Ask the administrators whether you may use your own 404 page; on Apache servers this
   is a line `ErrorDocument 404 /~smandal/404.html` in a file `.htaccess`.

Keep this repository as the master copy, so that you can later move again.

## The motif

The line drawing in the header and the browser icon show the **Hopf fibration**: seven of
its fibres (circles in $S^3$, stereographically projected to $\mathbb{R}^3$), linked
with each other, as an over/under diagram. The icon shows two fibres, a Hopf link.
Two other variants are ready in `source/motifs/`: a **torus** with meridians and parallels
(hidden lines removed) and a **trefoil knot**. All of them are computed by
`tools/draw_motifs.py` (Python with numpy); no image was copied from anywhere.

To switch to another variant, run (with Playwright installed)

```bash
~/venvs/web/bin/python tools/make_icons.py torus     # or knot, or hopf
```

which installs the header drawing, the icons and the link-preview picture. Without
Playwright, copy `source/motifs/torus.svg` to `images/motif.svg` and
`source/motifs/torus-icon.svg` to `images/favicon.svg`; the PNG icons and the preview
picture then keep the old motif.

The accent colour (links, menu, motif) is `--accent: #2e4a68` at the top of
`assets/site.css`; if you change it, change `ACCENT` in `tools/draw_motifs.py` too and
redraw the motif.

## Tools and licences

Rebuilding the site needs only Python 3.11+ (`build.py`). The helpers in `tools/` are
needed only for the tasks they name. On the author's server they run with the virtual
environments `~/venvs/math` (numpy) and `~/venvs/web` (Playwright with headless Chromium,
fontTools):

| Tool | Does | Needs |
|---|---|---|
| `tools/draw_motifs.py` | draws the motif variants into `source/motifs/` | numpy |
| `tools/make_icons.py NAME` | installs a motif: header image, icons, link preview | Playwright |
| `tools/make_fonts.py` | makes `assets/fonts/*.woff2` from TeX Live's New Computer Modern | fontTools, brotli, TeX Live |
| `tools/screenshots.py DIR` | opens every page at phone and computer width in headless Chromium, saves screenshots, reports outside requests, broken images, missing alt text and overflowing pages | Playwright |

`python3 build.py --external` also tests the links to other websites.

Licences of what is included: the fonts are New Computer Modern by Antonis Tsolomitis
(GUST Font License, see `assets/fonts/`); MathJax 4.1.3 and its New Computer Modern math
font are under the Apache License 2.0 (see `assets/mathjax/`). The texts, the photo and
the CV are © Souvik Mandal.
