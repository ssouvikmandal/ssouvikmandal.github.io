# Website of Souvik Mandal

Source and published files of <https://ssouvikmandal.github.io>, moved from the Google Site
<https://sites.google.com/view/souvik-mandal> on 18 November 2026. The text of the pages is
the Google Site's text, with a few typing errors corrected; the Publications page was added
from arXiv.

The published site is plain HTML and CSS with relative links. Fonts, icons and MathJax are
stored here, and the site uses no cookies and no trackers. The only scripts are MathJax (on
pages with formulas), a few lines in `assets/email.js` that protect the email addresses,
and, when it is switched on, GoatCounter's small visitor counter, the one outside service
(see [Visitor statistics](#visitor-statistics)); everything works without them. A page is only regenerated
when you run `python3 build.py`, which needs Python 3.11 or later and nothing else.

## Contents

- [The files](#the-files)
- [Everyday changes](#everyday-changes): position, email, address · CV · photo · a
  teaching entry · a paper · a talk · a new section · formulas
- [Publishing](#publishing)
- [Search engines](#search-engines): what the site does · what only you can do
- [Visitor statistics](#visitor-statistics) (GoatCounter)
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
images/orcid-id.svg, images/scholar.svg, images/researchgate.svg, images/email.svg
                          ← the ORCID, Google Scholar, ResearchGate and email icons at
                          the top of every page
favicon.ico, images/favicon-192.png, images/apple-touch-icon.png
                          ← the browser and phone icons (a shaded teal torus)
images/og-image.png       ← the link-preview picture (Hopf fibration)
images/LICENSES.txt       ← where the ORCID, Google Scholar, ResearchGate and email icons and the logo come from
images/bg-*.svg           ← the faint drawings in the page margins (computers only)
assets/site.css           ← the design: colours, fonts, spacing (colours at the top)
assets/email.js           ← turns the protected email links into mailto: links
assets/goatcounter/count.v5.js ← GoatCounter's visitor counter (used when switched on)
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
institution_full_name = "Example University"               # for search engines
institution_url = "https://www.example.edu/"
department_url = "https://math.example.edu/"
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
page; `institution_full_name`, `institution_url` and `department_url` appear only in that
structured data (see [Search engines](#search-engines)). `institution_logo` is the small logo shown beside that line: put the new logo (a
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
        <li><strong class="role">PMRF TA</strong> for the NPTEL course <em>Course Name</em>. Course instructor: Prof. Name, Department of Mathematics, Institute.</li>
        <li><strong class="role">Institute TA</strong> for MA1234 <em>Course Name</em> under Dr. Name, Department of Mathematics, IIT Madras.</li>
      </ul></td>
    </tr>
    <tr>
      <th scope="row" class="session">January–April</th>
      <td><strong class="role">Institute TA</strong> for MA5678 <em>Course Name</em> under Dr. Name, Department of Mathematics, IIT Madras.</td>
    </tr>
  </tbody>
```

- A new year: copy a whole `<tbody> … </tbody>` block and put it first, right after
  `</thead>`. `rowspan="2"` on the year is the number of sessions in that year; with only
  one session, leave out `rowspan="2"` and the second `<tr>`.
- One position in a session: write it straight into the `<td>`. Several positions: put
  each in an `<li>` of a `<ul class="ta">`, as above; the page divides them by a thin line.
- `<strong class="role">` sets "PMRF TA" or "Institute TA" in bold, and `<em>` the course
  name in italics. When a position's
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

## Search engines

### What the site does

Search engines find the site by following links to it and by reading `sitemap.xml` (named
in `robots.txt`). `build.py` writes everything they use, from `site.toml` and the page
headers, so nothing here needs editing by hand:

- **Titles.** The home page's title is set in `source/pages/index.html`
  ("Souvik Mandal – Mathematics (Topology and Geometry), IIT Madras"); every other page's
  title gets "– Souvik Mandal, IIT Madras" added, so each result shows which Souvik Mandal
  this is. Titles and `description:` lines (the text under a result) should name you and
  keep to the facts on the pages.
- **The name as the home page's heading.** On the home page the name at the top is the
  main heading (`<h1>`); "About" is a second-level heading styled like a page title
  (`class="page-title"`). On the other pages the name links to the home page.
- **A description of you for search engines** (schema.org, as JSON-LD, on the home page
  only, not shown on the page): the site's name (`WebSite`, which Google uses as the site
  name in results) and a `ProfilePage` about you (`Person`): name, photo, position,
  institution and department with their web addresses, places studied (`studied_at`),
  awards (`awards`), research areas (`research_areas`), ORCID iD, and the ORCID, Google
  Scholar and ResearchGate profiles as the same person (`sameAs`). All of it comes from `site.toml`; keep it
  in line with the pages. The ORCID, Google Scholar and ResearchGate icons also carry `rel="me"`. The
  profile also says when the site was first published (`created` in `site.toml`) and when
  the home page last changed (kept in `source/last-updated.json`), both as date, time and
  time zone, e.g. `2026-11-18T10:31:41+00:00`: Google marks plain dates there as invalid.
- **Other tags:** a canonical address on every page but the 404 page (the home page is
  `https://ssouvikmandal.github.io/`, not `.../index.html`), `max-image-preview:large` (so
  results may show the photo in full size), link-preview tags, `noindex` on the 404 page,
  and `sitemap.xml` with each page's last-updated date. `robots.txt` keeps search engines
  out of `source/` and `tools/`. The browser icon (`favicon.ico`, `images/favicon-192.png`)
  is also the icon Google shows beside results; keep its file names.

### What only you can do

These steps need your own accounts; they matter more than anything in the code.

1. **Google Search Console** (<https://search.google.com/search-console>): add a property
   of type "URL prefix" with `https://ssouvikmandal.github.io/` (the "Domain" type does not
   work for a `github.io` address). The site is verified with the method "HTML file": the
   file's name is `google_verification_file` under `[search]` in `site.toml`, and
   `build.py` writes the file (`google59317c9659984622.html`, one line naming itself) at
   the top of the site. (The method "HTML tag" also works: put only the code inside
   `content="…"` in `google_site_verification`.) After a change, run
   `python3 build.py --check`, publish, wait a minute and press "Verify". Then, in Search
   Console: Sitemaps → enter `sitemap.xml` → Submit; and URL inspection → enter the home
   page address → "Request indexing". Keep the file (or code): removing it ends the
   verification.
2. **Bing Webmaster Tools** (<https://www.bing.com/webmasters>), which also serves
   DuckDuckGo and Yahoo: sign in and choose "Import from Google Search Console", or verify
   with its HTML tag (`bing_site_verification`, the code from `msvalidate.01`).
3. **Links to the site** from pages that already rank for your name: the "Homepage" field
   of the Google Scholar profile, "Websites & social links" on the ORCID record, the
   department's page about you if it has one, GitHub and other profiles, and your CV and
   email signature.
4. **The old Google Site** has the same text and an older place in search results. Replace
   its content with one line saying that the site has moved, with a link to
   `https://ssouvikmandal.github.io`, and leave it published for some months, so that
   visitors and search engines follow the link.

New sites usually appear in Google within days to a few weeks after these steps; the
position in results for a given search cannot be set from the site itself.

## Visitor statistics

Visits are counted with GoatCounter (<https://www.goatcounter.com>), free for personal
sites, when `[analytics] goatcounter` in `site.toml` holds the account name (the part
before `.goatcounter.com` in the dashboard's address); `""` switches it off. After a
change run `python3 build.py --check` and publish. Switching it on or off does not change
the "Last updated" dates.

- **What you see** in the dashboard (`https://ACCOUNT.goatcounter.com`, after logging in):
  visits per page and per day, where visitors came from (Google, Google Scholar, ORCID,
  ResearchGate, …), countries, browsers, systems and screen sizes. Clicks are counted as
  "events": `download: cv.pdf`, `link: arxiv.org/abs/…` (the paper links),
  `link: orcid.org/…`, `link: scholar.google.com/…`, `link: researchgate.net/…`, `email`
  (the main address) and `email: IIT Madras`. Visits to an address that does not exist
  show that address with the title "Page not found", which helps to find broken links.
  The home page counts as `/`, whether it was opened as `/` or `/index.html`.
- **What it does not do**: no cookies, nothing stored in the visitor's browser, no
  personal data; GoatCounter keeps only totals (it does not keep IP addresses), so no
  cookie banner is needed (GoatCounter's explanation: <https://www.goatcounter.com/help/gdpr>).
  `build.py` gives every counted link its own name and title (`count_clicks()`), so the
  email addresses are never sent to GoatCounter. Visits from `localhost`, from the
  author's checks (`tools/screenshots.py` stops them) and from programs that identify as
  automated browsers are not counted. Ad blockers stop the counter for some visitors, so
  the real numbers are somewhat higher.
- **Your own visits**: open `https://ssouvikmandal.github.io/#toggle-goatcounter` once in
  each browser you use (on each computer and phone) and confirm; that browser is then no
  longer counted. Doing it again counts it again.
- **The script** `assets/goatcounter/count.v5.js` is GoatCounter's `count.v5.js` (ISC
  licence, see its first lines), stored here unchanged and checked against the SHA-384
  checksum GoatCounter publishes (<https://www.goatcounter.com/help/countjs-versions>). It
  sends each visit to `https://ACCOUNT.goatcounter.com/count`. A stored copy never changes
  by itself, and GoatCounter promises that this address keeps working with it.

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
location without changes. Only `sitemap.xml`, `robots.txt`, the canonical, link-preview
and search-engine tags and the 404 page contain the full address, and all of them come from
one line in `site.toml`. After a move, add the new address to Google Search Console as
well and submit its sitemap (see [Search engines](#search-engines)).

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

At the top of every page, to the left of the name (beside it on phones), are four icons,
one below the other: the official ORCID iD icon, linking to the ORCID record (`orcid` in
`site.toml`); the Google Scholar icon, linking to the Google Scholar profile
(`google_scholar`); the ResearchGate icon, linking to the ResearchGate profile
(`researchgate`); and an email icon that writes to the main address (see
[Email addresses and spam](#email-addresses-and-spam)). Each has a tooltip and a label for
screen readers, and the pages themselves carry no separate ORCID or Google Scholar text
links. The ORCID icon must be used as ORCID provides it (green, unaltered). The Google
Scholar icon is Google's Scholar mark (shape from Simple Icons) in white on a circle in
Google's blue; the ResearchGate icon is ResearchGate's "RG" mark (shape from
Simple Icons) in white on a circle in a slightly deeper ResearchGate teal (`#00A396`, for
a contrast of at least 3:1); the email icon is the Feather Icons "mail" icon (MIT licence)
on a circle in the accent colour. Leaving `orcid`, `google_scholar` or `researchgate` empty
in `site.toml` removes that icon. On phones the icons get smaller below 390 pixels of
screen width, so that all four stay beside the name (`assets/site.css`, "Phones"). See
`images/LICENSES.txt`.

The browser-tab icon (and the icon on phone home screens) is a **torus**, smoothly shaded
in a soft teal: `favicon.ico` (16, 32 and 48 pixels), `images/favicon-192.png` and
`images/apple-touch-icon.png`. It is computed by `tools/draw_favicon.py` from the torus's
equation (each pixel follows a ray to the surface and is lit from the upper left), with
numpy and Pillow; the 512-pixel original is `source/motifs/torus-shaded.png`. The teal is a
mid tone, so the icon shows on light and dark tab bars alike. To change its colour, edit
`DARK` and `LIGHT` at the top of `tools/draw_favicon.py` and run

```bash
~/venvs/math/bin/python tools/draw_favicon.py
```

The link-preview picture shows the **Hopf fibration**: seven of its fibres (circles in
$S^3$, stereographically projected to $\mathbb{R}^3$), linked with each other, as an
over/under diagram. Two more motifs, a **torus** in outline and a **trefoil knot**, are
ready in `source/motifs/`. All of them are computed by `tools/draw_motifs.py` (Python with
numpy); no image was copied from anywhere. To draw the preview picture with another motif,
run (with Playwright installed)

```bash
~/venvs/web/bin/python tools/make_preview.py hopf      # or torus, or knot
```

Browsers keep tab icons for a long time. After changing them, raise the number in `?v=3`
on the three icon lines in `source/template.html` (to `?v=4`, and so on) and rebuild, so
that browsers fetch the new icons.

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
| `tools/draw_favicon.py` | draws the shaded torus and writes the browser and phone icons | numpy, Pillow |
| `tools/make_preview.py NAME` | draws the link-preview picture with a motif | Playwright |
| `tools/make_fonts.py` | makes `assets/fonts/*.woff2` from TeX Live's New Computer Modern | fontTools, brotli, TeX Live |
| `tools/screenshots.py DIR [--url URL]` | opens every page (of this folder, or of the published site with `--url`) at phone and computer width in headless Chromium, saves screenshots, reports outside requests, broken images, missing alt text and overflowing pages | Playwright |

`python3 build.py --external` also tests the links to other websites. ResearchGate answers
every program with "403 Forbidden", so its link is skipped there (listed in
`REFUSES_LINK_CHECKS` in `build.py`); open it in a browser instead.

Licences of what is included: the fonts are New Computer Modern by Antonis Tsolomitis
(GUST Font License, see `assets/fonts/`); MathJax 4.1.3 and its New Computer Modern math
font are under the Apache License 2.0 (see `assets/mathjax/`); GoatCounter's `count.v5.js`
is under the ISC licence (see its first lines). The texts, the photo and
the CV are © Souvik Mandal. The IIT Madras logo belongs to IIT Madras; it is the logo
file used on the old Google Site, reduced from 1200 to 128 pixels (shape and colours
unchanged).
