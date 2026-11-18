# Website of Souvik Mandal

Source and published files of <https://ssouvikmandal.github.io>, moved from the Google Site
<https://sites.google.com/view/souvik-mandal> on 18 November 2026. The text of the pages is
the Google Site's text, with a few typing errors corrected; the Publications page was added
from arXiv.

The published site is plain HTML and CSS with relative links. Fonts, icons and MathJax are
stored here, and the site uses no outside services, trackers or cookies. The only scripts
are MathJax (on pages with formulas) and a few lines in `assets/email.js` that protect the
email addresses; everything works without them. A page is only regenerated
when you run `python3 build.py`, which needs Python 3.11 or later and nothing else.

## Contents

- [The files](#the-files)
- [Everyday changes](#everyday-changes): position, email, address · CV · photo · a
  teaching entry · a paper · a talk · a new section · formulas
- [Publishing](#publishing)
- [Email addresses and spam](#email-addresses-and-spam)
- [Placeholders](#placeholders)
- [Moving the site](#moving-the-site): your own domain · a university server
- [The icons, the motif and the drawings in the margins](#the-icons-the-motif-and-the-drawings-in-the-margins)
- [Tools and licences](#tools-and-licences)

## The files

```
site.toml                 ← your name, position, affiliation, emails, address, profiles, menu
source/pages/*.html       ← the text of each page (edit these)
source/template.html      ← the frame around every page: head, header, menu, footer
build.py                  ← turns the two above into the published pages
index.html, cv.html, …    ← the published pages (generated: do not edit by hand)
cv.pdf                    ← your CV (at present a placeholder, see "Placeholders")
images/photo.jpg          ← your photo
images/logo-iit-madras.png ← the institution's logo beside the affiliation (set in site.toml)
images/orcid-id.svg, images/scholar.svg, images/email.svg ← the ORCID, Google Scholar and
                          email icons at the top of every page
images/favicon.svg, favicon.ico, images/apple-touch-icon.png,
images/og-image.png       ← the browser icons (a Hopf link) and the link preview
images/LICENSES.txt       ← where the ORCID, Google Scholar and email icons and the logo come from
images/bg-*.svg           ← the faint drawings in the page margins (computers only)
assets/site.css           ← the design: colours, fonts, spacing (colours at the top)
assets/email.js           ← turns the protected email links into mailto: links
assets/fonts/             ← the text font (New Computer Modern), see its README.txt
assets/mathjax/, assets/mathjax-config.js   ← MathJax for formulas, see README-SITE.txt
sitemap.xml, robots.txt   ← for search engines (generated)
404.html                  ← the "page not found" page (generated)
source/last-updated.json  ← the "last updated" date of each page (kept by build.py)
source/motifs/            ← the three motif drawings (torus, Hopf fibration, trefoil knot)
source/placeholders/      ← the LaTeX source of the CV placeholder
source/archive/           ← earlier versions of pages, not published (see its README.md)
tools/                    ← optional helpers; they need extra Python packages, build.py does not
```

Page addresses never change: `index.html`, `cv.html`, `research.html`,
`publications.html`, `achievements.html`, `teaching.html`, `conferences.html` and
`contact.html`, and the CV is always `cv.pdf`. When you update a file, keep its name, so that old links keep working.

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
institution_logo = "images/logo-example-university.png"   # or "" for no logo
email = "your.name [at] example.org"                      # main address, written with [at]
other_emails = [["Example University", "s.mandal [at] example.edu"]]
address = [
  "Souvik Mandal",
  "Department of Mathematics, Example University",
  "City, Postcode",
  "Country",
]
```

`position`, `department` and `institution` appear under your name on every page, in the
page descriptions for search engines and in the structured data (schema.org) on the home
page. `institution_logo` is the small logo shown beside that line: put the new logo (a
square PNG, about 128 × 128 pixels) in `images/` and give its name here, or write `""` to
show none. Keep the old logo file only if some page still uses it. `email` is the main
address: the email icon at the top of every page opens it, and it comes first on the
Contact page; `other_emails` are further addresses listed there with a label (write `[]`
for none). Write every address with ` [at] ` instead of `@` (see
[Email addresses and spam](#email-addresses-and-spam)). `address` is the postal address on
the Contact page. Then rebuild. The introduction on
the home page is ordinary text: edit it in `source/pages/index.html`.

### The CV

Replace `cv.pdf` with the new file (same name) and run `python3 build.py`. Every link to the
CV points to `cv.pdf`, so nothing else changes. (At present `cv.pdf` is a placeholder; see
[Placeholders](#placeholders).) Everything committed here stays public in the repository's
history, even after it is replaced, so check a CV for private details (date of birth, phone
number, home address) before committing it.

### The photo

Replace `images/photo.jpg` with the new photo (same name; JPEG, about 400 × 500 pixels,
under 100 KB) and run `python3 build.py`. The build reads the photo's size, so a photo with
different proportions is still shown undistorted.

### A teaching entry

The Teaching page (`source/pages/teaching.html`) is a table with three columns, Year,
Session and Teaching, newest year first. Each year is one `<tbody>` block with up to two
sessions, July–November and January–April:

```html
  <tbody>
    <tr>
      <th scope="rowgroup" class="year" rowspan="2">2026</th>
      <th scope="row" class="session">July–November</th>
      <td><ul class="ta">
        <li><strong class="role">PMRF TA</strong> for Course Name course at NPTEL. Course Instructor: Prof. Name, Department of Mathematics, Institute.</li>
        <li><strong class="role">Institute TA</strong> for MA1234 (Course Name) under Dr. Name, Department of Mathematics, IIT Madras.</li>
      </ul></td>
    </tr>
    <tr>
      <th scope="row" class="session">January–April</th>
      <td><strong class="role">Institute TA</strong> for MA5678 (Course Name) under Dr. Name, Department of Mathematics, IIT Madras.</td>
    </tr>
  </tbody>
```

- A new year: copy a whole `<tbody> … </tbody>` block and put it first, right after
  `</thead>`. `rowspan="2"` on the year is the number of sessions in that year; with only
  one session, leave out `rowspan="2"` and the second `<tr>`.
- One position in a session: write it straight into the `<td>`. Several positions: put
  each in an `<li>` of a `<ul class="ta">`, as above; the page divides them by a thin line.
- `<strong class="role">` sets "PMRF TA" or "Institute TA" in bold. When a position's
  months differ from its session, add them after the role, e.g.
  `<strong class="role">PMRF TA</strong> (June–October) for …`.
- The sentence common to all PMRF TA positions is in the last row of the table
  (`<tfoot>`); change it there.

On phones the same table is shown as a list (year, session, positions). The earlier list
version of this page is kept in `source/archive/` (see its README).

### A paper

Papers are listed in `source/pages/publications.html`, newest first. For a new preprint,
copy the first `<li>…</li>` block, put the copy at the top of the list, and fill it in
exactly as arXiv shows the paper (the year is that of the first version):

```html
  <li>
    <span class="authors">Souvik Mandal, A. Coauthor</span>.
    <span class="title">Title of the paper</span>.
    <span class="nowrap"><a href="https://arxiv.org/abs/2701.01234">arXiv:2701.01234</a> <span class="meta">[math.AT]</span>, 2027.</span>
  </li>
```

`reversed` on the list makes the numbers count down, so the oldest paper stays number 1.
When a paper is published, start a second list above the preprints and move its entry
there, adding the journal and the DOI:

```html
<h2>Published papers</h2>
<ol class="entries" reversed>
  <li>
    <span class="authors">Souvik Mandal, A. Coauthor</span>.
    <span class="title">Title of the paper</span>.
    <span class="meta">Journal Name <b>12</b> (2027), no. 3, 1–20.</span>
    <span class="links"><a href="https://doi.org/10.xxxx/xxxxx">DOI</a> <a href="https://arxiv.org/abs/2601.01234">arXiv</a> <a href="papers/short-name.pdf">PDF</a></span>
  </li>
</ol>
```

Keep every entry in the same order: authors, title (`<span class="title">`, set in italics),
journal data (`<span class="meta">`), links. Put PDFs of your own papers in a folder
`papers/` with short, permanent names (e.g. `papers/surgery-cayley.pdf`).

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

Any new page works like the Talks page: create `source/pages/NAME.html` beginning
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
Commits are made as "Souvik Mandal" with the GitHub no-reply address
`325233884+ssouvikxyz@users.noreply.github.com` (set in this repository's `.git/config`), so
no real email address appears in the public history. `.git/hooks/pre-commit` runs `~/.local/bin/work-backup pre-commit`, the same check as in
`~/work`: it leaves files larger than 70 MB out of a commit (listing them at the end of
`.gitignore`) and refuses to commit text files that contain a private key or an access
token. Git hooks are not copied by `git clone`; `~/work/server-config/README.md` says how to
set them up again.

## Email addresses and spam

Programs that collect addresses for spam read web pages and public repositories looking for
text of the form `name@domain`. On this site no address appears in that form anywhere:

- In `site.toml` (which is public, in the repository and on the site) addresses are written
  as `name [at] domain`; `build.py` turns them back into `name@domain`.
- In the pages, the visible address is written with HTML character codes and contains a
  hidden decoy (`nospam.` after the `@`, in a `<span hidden>`). Browsers show and copy the
  real address, and screen readers read it, but a program that strips the HTML gets an
  address at a non-existent `nospam.` domain.
- The link target is not in the HTML at all: the link carries a scrambled copy of the
  address (backwards, each character moved one place on) in `data-mail`, and
  `assets/email.js` turns it into a working link when the page loads. Without JavaScript
  the links lead to the Contact page, where the address can still be read and copied.

Where the email links lead:

- **Phones and tablets** (Android, iPhone, iPad): a `mailto:` link, which opens the email
  app (for example the Gmail app) with a new message to the address.
- **Computers**: Gmail's "new message" window in a new browser tab
  (`https://mail.google.com/mail/?view=cm&fs=1&to=…`), with the address already filled
  in; a visitor who is not signed in to Gmail signs in first and then gets the same
  window. A `mailto:` link is not used on computers, because it only works when an email
  program is set up there; when none is, Windows offers a list of browsers and nothing
  happens. Visitors who do not use Gmail can copy the address from the Contact page.

Which kind of device a visitor uses is read from the browser's description of itself
(`navigator.userAgent`), in the first lines of `assets/email.js`.

Never write an address in plain form in any file of this repository, including the README
and commit messages: everything here is public.

## Placeholders

| File | Placeholder for | Replace it by |
|---|---|---|
| `cv.pdf` | the CV (the October 2024 CV from the Google Site is deliberately not published) | overwriting `cv.pdf` with the new CV, then `python3 build.py`, commit, push |

The placeholder is one page saying that the CV will be added soon; its source is
`source/placeholders/cv-placeholder.tex` (`lualatex cv-placeholder.tex`). Every link already
points to `cv.pdf`, so replacing the file is enough. When the real CV is in place, delete
this row.

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

## The icons, the motif and the drawings in the margins

At the top of every page, to the left of the name (beside it on phones), are three icons,
one below the other: the official ORCID iD icon, linking to the ORCID record (`orcid` in
`site.toml`); the Google Scholar icon, linking to the Google Scholar profile
(`google_scholar`); and an email icon that writes to the main address (see
[Email addresses and spam](#email-addresses-and-spam)). Each has a tooltip and a label for
screen readers, and the pages themselves carry no separate ORCID or Google Scholar text
links. The ORCID icon must be used as ORCID provides it (green, unaltered). The Google
Scholar icon is Google's Scholar mark (shape from Simple Icons) in white on a circle in
Google's blue; the email icon is the Feather Icons "mail" icon (MIT licence) on a circle
in the accent colour. Leaving `orcid` or `google_scholar` empty in `site.toml` removes that
icon. See `images/LICENSES.txt`.

The browser icon and the link-preview picture show the **Hopf fibration**: the preview
shows seven of its fibres (circles in $S^3$, stereographically projected to
$\mathbb{R}^3$), linked with each other, as an over/under diagram; the browser icon shows
two fibres, a Hopf link.
Two other variants are ready in `source/motifs/`: a **torus** with meridians and parallels
(hidden lines removed) and a **trefoil knot**. All of them are computed by
`tools/draw_motifs.py` (Python with numpy); no image was copied from anywhere.

To switch to another variant, run (with Playwright installed)

```bash
~/venvs/web/bin/python tools/make_icons.py torus     # or knot, or hopf
```

which installs the browser icons and the link-preview picture. Without Playwright, copy
`source/motifs/torus-icon.svg` to `images/favicon.svg`; the PNG icons and the preview
picture then keep the old motif.

On computer screens (at least 60em, about 960 pixels, wide) the empty parts of the page carry
very faint drawings, also computed by `tools/draw_motifs.py`: a torus behind the menu and in
the left margin (`images/bg-torus.svg`), a cinquefoil knot lower in the left margin
(`images/bg-knot.svg`) and Hopf fibres on two nested tori in the right margin
(`images/bg-hopf.svg`, only on screens at least 80em, about 1280 pixels, wide). Their areas
end 1rem before the text column and start 1rem after it, so they never lie behind the text;
phones and tablets do not show them. Their faintness is `--drawing-opacity: .16` at the top
of `assets/site.css`. At that value even the darkest point of a line leaves a contrast of
12.7:1 for the menu text (at least 4.5:1 is required); keep it at .25 or below.

The accent colour (links, menu, drawings, email icon) is `--accent: #2e4a68` at the top of
`assets/site.css`; if you change it, change `ACCENT` in `tools/draw_motifs.py` and the
circle colour in `images/email.svg` too, and redraw the drawings.

## Tools and licences

Rebuilding the site needs only Python 3.11+ (`build.py`). The helpers in `tools/` are
needed only for the tasks they name. On the author's server they run with the virtual
environments `~/venvs/math` (numpy) and `~/venvs/web` (Playwright with headless Chromium,
fontTools):

| Tool | Does | Needs |
|---|---|---|
| `tools/draw_motifs.py` | draws the motif variants into `source/motifs/` and the margin drawings into `images/bg-*.svg` | numpy |
| `tools/make_icons.py NAME` | installs a motif as the browser icons and in the link preview | Playwright |
| `tools/make_fonts.py` | makes `assets/fonts/*.woff2` from TeX Live's New Computer Modern | fontTools, brotli, TeX Live |
| `tools/screenshots.py DIR [--url URL]` | opens every page (of this folder, or of the published site with `--url`) at phone and computer width in headless Chromium, saves screenshots, reports outside requests, broken images, missing alt text and overflowing pages | Playwright |

`python3 build.py --external` also tests the links to other websites.

Licences of what is included: the fonts are New Computer Modern by Antonis Tsolomitis
(GUST Font License, see `assets/fonts/`); MathJax 4.1.3 and its New Computer Modern math
font are under the Apache License 2.0 (see `assets/mathjax/`). The texts, the photo and
the CV are © Souvik Mandal. The IIT Madras logo belongs to IIT Madras; it is the logo
file used on the old Google Site, reduced from 1200 to 128 pixels (shape and colours
unchanged).
