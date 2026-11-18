#!/usr/bin/env python3
"""Build the website: turn site.toml, source/template.html and source/pages/*.html into the
published pages, sitemap.xml and robots.txt.

    python3 build.py             build everything
    python3 build.py --check     build, then check every link and image between the pages
    python3 build.py --external  as --check, and also test the links to other websites

Needs only Python 3.11 or later; nothing to install. See README.md for how to edit the site.

How a page is made: each file in source/pages/ starts with a comment holding its title and
description, followed by the page text in HTML. The text may contain these placeholders,
which are filled in from site.toml:

    {{name}} {{position}} {{department}} {{institution}} {{email}}
    {{institution_logo}}  the logo given by `institution_logo` (header of every page)
    {{email_link}}     the main email address as a protected mailto: link (see below)
    {{email_rows}}     the Email rows of the Contact page: main address, then other_emails
    {{address}}        the postal address, one line per entry of `address`
    {{photo}}          the photo images/photo.jpg, with its size and alt text
    {{orcid_link}}     link to the ORCID profile
    {{scholar_link}}   link to the Google Scholar profile
    {{profile_links}}  a line with the link to the CV (ORCID, Google Scholar and email are
                       icons at the top of every page)

Pages that contain a formula ($...$, \\(...\\), $$...$$ or \\[...\\]) automatically load
MathJax from assets/mathjax/.

For search engines (README.md, "Search engines"): titles other than the home page's get
"– <name>, <institution>" added; the name at the top is the <h1> of the home page and a
link elsewhere; the home page carries a schema.org description of the site and its owner
(home_jsonld) and the Search Console / Bing codes from [search] in site.toml.

Email addresses never appear whole in the HTML, which keeps them away from the programs
that collect addresses for spam: the visible text contains a hidden decoy ("nospam." after
the @, which visitors neither see nor copy), and the mailto: link is assembled from a
scrambled copy by assets/email.js when the page loads. Without JavaScript the links lead
to the Contact page, where the address can be read and copied. On phones and tablets the
links are mailto: links (they open the email app); on computers they open Gmail's "new
message" window in a new browser tab.

The footer shows "© <years> <name>" on the left (the years run from `since` in site.toml to
the year of the page's last update) and "Last updated <date>" on the right.

"Last updated" in the footer is the date on which a page's content last changed: the build
keeps a fingerprint of every page in source/last-updated.json and only moves the date
forward when the page really changes. The file also keeps the time of that change, which
the home page gives search engines as dateModified.
"""
import argparse
import datetime
import hashlib
import html
import json
import re
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit("build.py needs Python 3.11 or later (for tomllib).")
import tomllib

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
PAGES = SOURCE / "pages"
DATES = SOURCE / "last-updated.json"
PHOTO = "images/photo.jpg"
CV = "cv.pdf"
OG_IMAGE = "images/og-image.png"
MATH_PATTERN = re.compile(r"(?<!\\)\$|\\\(|\\\[")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def fail(message):
    sys.exit(f"build.py: {message}")


# --- reading the sources ----------------------------------------------------------------

def load_config():
    try:
        with open(ROOT / "site.toml", "rb") as f:
            cfg = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        fail(f"site.toml has a syntax error: {e}")
    for key in ("site", "person", "nav"):
        if key not in cfg:
            fail(f"site.toml has no [{key}] section")
    for key in ("name", "position", "department", "institution", "email", "address"):
        if key not in cfg["person"]:
            fail(f"site.toml: [person] has no `{key}`")
    cfg["site"]["url"] = cfg["site"]["url"].rstrip("/")
    return cfg


def read_page(path):
    """Split a page source into its settings (the leading comment) and its HTML."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    if not m:
        fail(f"{path.relative_to(ROOT)} must start with a <!-- ... --> block holding "
             "its title and description")
    meta = {}
    for line in m.group(1).strip().splitlines():
        if line.strip():
            key, sep, value = line.partition(":")
            if not sep:
                fail(f"{path.relative_to(ROOT)}: line `{line.strip()}` should look like `key: value`")
            meta[key.strip().lower()] = value.strip()
    for key in ("title", "description"):
        if key not in meta:
            fail(f"{path.relative_to(ROOT)}: no `{key}:` line in the comment at the top")
    return meta, text[m.end():].rstrip() + "\n"


def image_size(path):
    """Width and height of a JPEG or PNG file (whatever its extension says)."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + length
    fail(f"{path.relative_to(ROOT)} is not a JPEG or PNG image")


# --- placeholders -----------------------------------------------------------------------

def entities(text):
    """Write every character as an HTML character reference (keeps the email address
    readable for people but hides it from the simplest address-harvesting programs)."""
    return "".join(f"&#{ord(c)};" for c in text)


def real_address(written):
    """site.toml writes addresses as "name [at] domain"; turn that into name@domain."""
    address = re.sub(r"\s*\[at\]\s*", "@", written.strip())
    if address.count("@") != 1 or " " in address:
        fail(f"site.toml: {written!r} is not an email address written as 'name [at] domain'")
    return address


def scramble(address):
    """The address backwards, each character moved one code point on ("@" becomes "A");
    assets/email.js undoes this."""
    return "".join(chr(ord(c) + 1) for c in reversed(address))


def email_text(address):
    """The address as text that reads and copies correctly but holds a hidden decoy."""
    local, _, domain = address.partition("@")
    return f'{entities(local)}&#64;<span hidden>nospam.</span>{entities(domain)}'


def email_link(address, label=""):
    """A link that becomes mailto:address when assets/email.js runs."""
    extra = f' aria-label="{html.escape(label)}" title="{html.escape(label)}"' if label else ""
    return (f'<a class="email" href="contact.html#email" data-mail="{html.escape(scramble(address))}"'
            f'{extra}>')


def placeholders(cfg):
    p = cfg["person"]
    esc = html.escape
    values = {k: esc(str(p[k])) for k in ("name", "position", "department", "institution")}
    main_email = real_address(p["email"])
    values["email"] = email_text(main_email)
    values["email_link"] = email_link(main_email) + email_text(main_email) + "</a>"
    rows = [f'  <dt id="email">Email:</dt>\n  <dd>{values["email_link"]}</dd>']
    for label, written in p.get("other_emails", []):
        address = real_address(written)
        rows.append(f"  <dt>Email ({esc(label)}):</dt>\n  <dd>{email_link(address)}{email_text(address)}</a></dd>")
    values["email_rows"] = "\n".join(rows)
    # The icons at the top of every page: ORCID record, Google Scholar profile, email.
    # rel="me" says that these profiles belong to the owner of this site.
    icons = []
    if p.get("orcid"):
        orcid_id = p["orcid"].rstrip("/").rsplit("/", 1)[-1]
        icons.append(f'<a class="icon" href="{esc(p["orcid"])}" rel="me" title="ORCID record: {esc(orcid_id)}" '
                     f'aria-label="ORCID record of {esc(p["name"])}">'
                     '<img src="images/orcid-id.svg" alt="" width="24" height="24"></a>')
    if p.get("google_scholar"):
        icons.append(f'<a class="icon" href="{esc(p["google_scholar"])}" rel="me" title="Google Scholar profile" '
                     f'aria-label="Google Scholar profile of {esc(p["name"])}">'
                     '<img src="images/scholar.svg" alt="" width="24" height="24"></a>')
    icons.append(email_link(main_email, f'Email {p["name"]}').replace('class="email"', 'class="icon"')
                 + '<img src="images/email.svg" alt="" width="24" height="24"></a>')
    values["header_icons"] = '<div class="header-icons">' + "".join(icons) + "</div>"
    values["address"] = ('<address class="postal">\n'
                         + "<br>\n".join(esc(line) for line in p["address"])
                         + "\n</address>")
    logo = p.get("institution_logo", "")
    if logo:
        if not (ROOT / logo).exists():
            fail(f"site.toml: institution_logo {logo} does not exist")
        lw, lh = image_size(ROOT / logo)
        # Decorative: the institution's name is written right next to it.
        values["institution_logo"] = (f'<img class="inst-logo" src="{esc(logo)}" width="{lw}" '
                                      f'height="{lh}" alt="">')
    else:
        values["institution_logo"] = ""
    w, h = image_size(ROOT / PHOTO)
    values["photo"] = (f'<img class="photo" src="{PHOTO}" width="{w}" height="{h}" '
                       f'alt="Photo of {esc(p["name"])}">')
    if p.get("orcid"):
        orcid_id = p["orcid"].rstrip("/").rsplit("/", 1)[-1]
        values["orcid_link"] = (f'<a href="{esc(p["orcid"])}" title="ORCID iD {esc(orcid_id)}">'
                                "ORCID</a>")
    else:
        values["orcid_link"] = ""
    if p.get("google_scholar"):
        values["scholar_link"] = f'<a href="{esc(p["google_scholar"])}">Google Scholar</a>'
    else:
        values["scholar_link"] = ""
    links = [f'<a href="{CV}">CV</a>'] if (ROOT / CV).exists() else []
    values["profile_links"] = ('<p class="profile-links">'
                               + '<span class="dot" aria-hidden="true">·</span>'.join(links)
                               + "</p>")
    return values


def attr(text):
    """Escape plain text for use in HTML (also inside double-quoted attributes)."""
    return html.escape(text, quote=False).replace('"', "&quot;")


def fill(text, values, where, strict=True):
    """Replace {{key}} by values[key]. In page text an unknown {{key}} (which could be part
    of a formula) is left alone; in the template it is an error."""
    def sub(m):
        key = m.group(1)
        if key not in values:
            if strict:
                fail(f"{where}: unknown placeholder {{{{{key}}}}}")
            print(f"note: {where}: {{{{{key}}}}} is not a placeholder; left as it is")
            return m.group(0)
        return values[key]
    return re.sub(r"\{\{\s*([a-z_]+)\s*\}\}", sub, text)


# --- building ---------------------------------------------------------------------------

def page_url(cfg, file):
    base = cfg["site"]["url"]
    return base + "/" if file == "index.html" else f"{base}/{file}"


def nav_html(cfg, current):
    lines = []
    for item in cfg["nav"]:
        here = ' aria-current="page"' if item["file"] == current else ""
        lines.append(f'      <li><a href="{item["file"]}"{here}>{html.escape(item["label"])}</a></li>')
    return "\n".join(lines)


def date_time(value):
    """An ISO 8601 date and time with its time zone, e.g. "2026-11-18T10:31:41+00:00", as
    Google requires for schema.org dates. Takes a datetime (one without a time zone is taken
    as local time), a date (midnight, local time) or such a value written as text."""
    if isinstance(value, str):
        value = (datetime.datetime.fromisoformat(value) if "T" in value
                 else datetime.date.fromisoformat(value))
    if not isinstance(value, datetime.datetime):
        value = datetime.datetime.combine(value, datetime.time())
    if value.tzinfo is None:
        value = value.astimezone()
    return value.replace(microsecond=0).isoformat()


def name_parts(name):
    """("Souvik", "Mandal") from "Souvik Mandal": given names, then the family name."""
    parts = name.split()
    return (" ".join(parts[:-1]), parts[-1]) if len(parts) > 1 else ("", name)


def home_jsonld(cfg, title, description, modified):
    """The description of the site and of its owner that search engines read from the home
    page (schema.org, in JSON-LD): a WebSite (which gives Google the site's name) and a
    ProfilePage whose main subject is the Person. Everything comes from site.toml."""
    p, site = cfg["person"], cfg["site"]
    home = site["url"] + "/"
    given, family = name_parts(p["name"])
    w, h = image_size(ROOT / PHOTO)
    institution = {"@type": "CollegeOrUniversity",
                   "name": p.get("institution_full_name") or p["institution"]}
    if p.get("institution_full_name") and p["institution_full_name"] != p["institution"]:
        institution["alternateName"] = p["institution"]
    if p.get("institution_url"):
        institution["url"] = p["institution_url"]
    department = {"@type": "Organization", "name": f'{p["department"]}, {p["institution"]}'}
    if p.get("department_url"):
        department["url"] = p["department_url"]
    institution["department"] = department
    person = {
        "@type": "Person",
        "@id": home + "#person",
        "name": p["name"],
        "givenName": given,
        "familyName": family,
        "url": home,
        "image": {"@type": "ImageObject", "url": f'{site["url"]}/{PHOTO}',
                  "width": w, "height": h},
        "description": description,
        "jobTitle": p["position"],
        "affiliation": institution,
    }
    if not given:
        del person["givenName"]
    if p.get("studied_at"):
        person["alumniOf"] = [{"@type": "CollegeOrUniversity", "name": n, "url": u} if u else
                              {"@type": "CollegeOrUniversity", "name": n}
                              for n, u in p["studied_at"]]
    if p.get("awards"):
        person["award"] = p["awards"]
    if p.get("research_areas"):
        person["knowsAbout"] = p["research_areas"]
    same_as = [u for u in (p.get("orcid"), p.get("google_scholar")) if u]
    if same_as:
        person["sameAs"] = same_as
    if p.get("orcid"):
        person["identifier"] = {"@type": "PropertyValue", "propertyID": "ORCID",
                                "value": p["orcid"].rstrip("/").rsplit("/", 1)[-1]}
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": home + "#website", "url": home, "name": p["name"],
             "inLanguage": site.get("language", "en"), "publisher": {"@id": home + "#person"}},
            {"@type": "ProfilePage", "@id": home, "url": home, "name": title,
             "inLanguage": site.get("language", "en"), "isPartOf": {"@id": home + "#website"}},
        ],
    }
    profile = data["@graph"][1]
    # Dates with time and time zone (Google flags plain dates on a ProfilePage as invalid).
    if site.get("created"):
        profile["dateCreated"] = date_time(site["created"])
    profile["dateModified"] = modified
    profile["mainEntity"] = person
    text = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{text}\n</script>\n'


def home_meta(cfg):
    """Extra tags for the home page: first and last name for link previews, and the codes
    that prove ownership to Google Search Console and Bing Webmaster Tools."""
    given, family = name_parts(cfg["person"]["name"])
    tags = ""
    if given:
        tags += f'<meta property="profile:first_name" content="{attr(given)}">\n'
    tags += f'<meta property="profile:last_name" content="{attr(family)}">\n'
    search = cfg.get("search", {})
    for key, name in (("google_site_verification", "google-site-verification"),
                      ("bing_site_verification", "msvalidate.01")):
        code = str(search.get(key, "")).strip()
        if code:
            if not re.fullmatch(r"[A-Za-z0-9_-]+", code):
                fail(f"site.toml: [search] {key} should be only the code from content=\"…\", "
                     f"not the whole tag: {code!r}")
            tags += f'<meta name="{name}" content="{code}">\n'
    return tags


def render(cfg, template, values, file, meta, body, updated, modified):
    """`updated`: the date of the page's last change (footer); `modified`: the same moment
    as date and time with time zone (for search engines)."""
    site, person = cfg["site"], cfg["person"]
    is_home, is_404 = file == "index.html", file == "404.html"
    where = f"source/pages/{file}"
    # Title and description are plain text: fill in the plain values, then escape.
    plain = {k: str(person[k]) for k in ("name", "position", "department", "institution")}
    title = fill(meta["title"], plain, where)
    if not is_home and person["name"] not in title:
        # "Publications – Souvik Mandal, IIT Madras": the name with the institution tells
        # search engines (and readers of a results page) which Souvik Mandal this is.
        title = f'{title} – {person["name"]}, {person["institution"]}'
    description = fill(meta["description"], plain, where)
    head_extra = ""
    if meta.get("math", "auto") == "yes" or (meta.get("math", "auto") == "auto"
                                             and MATH_PATTERN.search(body)):
        head_extra += ('<script src="assets/mathjax-config.js"></script>\n'
                       '<script defer src="assets/mathjax/tex-chtml.js"></script>\n')
    if is_home:
        head_extra += home_meta(cfg) + home_jsonld(cfg, title, description, modified)
    base_path = urllib.parse.urlsplit(site["url"]).path.rstrip("/") + "/"
    since = int(site.get("since", updated.year))
    page_values = dict(values)
    page_values.update({
        "language": html.escape(site.get("language", "en")),
        "title": attr(title),
        "description": attr(description),
        "canonical": page_url(cfg, file),
        "og_type": "profile" if is_home else "website",
        "og_image": f'{site["url"]}/{OG_IMAGE}',
        "nav": nav_html(cfg, file),
        "content": fill(body, values, where, strict=False).rstrip(),
        "head_extra": head_extra,
        # The 404 page is shown at any address, so its links must start from the site root.
        "base": f'<base href="{html.escape(base_path)}">\n' if is_404 else "",
        # Search engines may show the photo and preview images in full size.
        "robots": ('<meta name="robots" content="noindex">\n' if is_404 else
                   '<meta name="robots" content="max-image-preview:large">\n'),
        # The name at the top of every page: the main heading on the home page (so that
        # search engines see the name as its title), a link to the home page elsewhere.
        "name_heading": (f'<h1 class="name">{html.escape(person["name"])}</h1>' if is_home else
                         f'<a class="name" href="index.html">{html.escape(person["name"])}</a>'),
        "updated": f"{updated.day} {MONTHS[updated.month - 1]} {updated.year}",
        # "2026", or "2026–2028" for a page last updated in a later year
        "copyright_years": (str(since) if updated.year <= since else f"{since}–{updated.year}"),
        "updated_iso": updated.isoformat(),
    })
    return fill(template, page_values, "source/template.html")


def build(now):
    """`now`: the date and time (with time zone) recorded for pages that changed."""
    today = now.date()
    cfg = load_config()
    template = (SOURCE / "template.html").read_text(encoding="utf-8")
    values = placeholders(cfg)
    dates = json.loads(DATES.read_text()) if DATES.exists() else {}
    nav_files = [item["file"] for item in cfg["nav"]]
    if len(set(nav_files)) != len(nav_files):
        fail("site.toml: the same file appears twice in [[nav]]")
    files = nav_files + ["404.html"]
    for f in sorted(p.name for p in PAGES.glob("*.html")):
        if f not in files:
            print(f"note: source/pages/{f} is not in the menu (add it to [[nav]] in site.toml "
                  "to publish it)")
    for file in files:
        src = PAGES / file
        if not src.exists():
            fail(f"site.toml lists {file} in the menu, but source/pages/{file} does not exist")
    new_dates, written = {}, []
    for file in files:
        meta, body = read_page(PAGES / file)
        # Fingerprint the page without its date, to tell whether it changed.
        probe = render(cfg, template, values, file, meta, body, datetime.date(2000, 1, 1),
                       "2000-01-01T00:00:00+00:00")
        digest = hashlib.sha256(probe.encode()).hexdigest()
        old = dates.get(file, {})
        if old.get("hash") == digest:
            updated = datetime.date.fromisoformat(old["date"])
            modified = old.get("time") or date_time(updated)
        else:
            updated, modified = today, date_time(now)
        new_dates[file] = {"date": updated.isoformat(), "time": modified, "hash": digest}
        out = render(cfg, template, values, file, meta, body, updated, modified)
        target = ROOT / file
        if not target.exists() or target.read_text(encoding="utf-8") != out:
            target.write_text(out, encoding="utf-8")
            written.append(file)
    DATES.write_text(json.dumps(new_dates, indent=2, sort_keys=True) + "\n")
    # sitemap.xml and robots.txt
    entries = "".join(f"  <url>\n    <loc>{html.escape(page_url(cfg, f))}</loc>\n"
                      f"    <lastmod>{new_dates[f]['date']}</lastmod>\n  </url>\n"
                      for f in nav_files)
    extra = [(ROOT / "sitemap.xml",
              '<?xml version="1.0" encoding="UTF-8"?>\n'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
              + entries + "</urlset>\n"),
             (ROOT / "robots.txt",
              "User-agent: *\nAllow: /\nDisallow: /source/\nDisallow: /tools/\n\n"
              f"Sitemap: {cfg['site']['url']}/sitemap.xml\n"),
             (ROOT / ".nojekyll", "")]
    # Google Search Console's verification file: one line naming the file itself.
    gfile = str(cfg.get("search", {}).get("google_verification_file", "")).strip()
    if gfile:
        if not re.fullmatch(r"google[0-9a-f]+\.html", gfile):
            fail(f"site.toml: [search] google_verification_file should be a file name like "
                 f"google1234abcd.html, not {gfile!r}")
        extra.append((ROOT / gfile, f"google-site-verification: {gfile}"))
    for path, text in extra:
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            written.append(path.name)
    print("written: " + (", ".join(written) if written else "nothing (everything was up to date)"))
    return cfg, files


# --- checking ---------------------------------------------------------------------------

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.base = [], set(), None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "base":
            self.base = a.get("href")
        for key in ("href", "src"):
            if a.get(key) and not (tag == "link" and a.get("rel") in ("canonical",)) \
                    and not (tag == "base"):
                self.links.append(html.unescape(a[key]))


def check(cfg, files, external):
    problems, outside = [], set()
    pages = {}
    for file in files:
        parser = Links()
        parser.feed((ROOT / file).read_text(encoding="utf-8"))
        pages[file] = parser
    for file, parser in pages.items():
        for link in parser.links:
            parts = urllib.parse.urlsplit(link)
            if parts.scheme in ("http", "https"):
                outside.add(link)
                continue
            if parts.scheme in ("mailto", "tel") or link.startswith("data:"):
                continue
            if link.startswith("/") and file != "404.html":
                problems.append(f"{file}: {link} starts with / (use a relative link)")
                continue
            path = parts.path.lstrip("/") or file
            target = (ROOT / path) if file == "404.html" else (ROOT / file).parent / path
            if not target.exists():
                problems.append(f"{file}: link to {link}, but {path} does not exist")
            elif parts.fragment and path in pages and parts.fragment not in pages[path].ids:
                problems.append(f"{file}: link to {link}, but {path} has no id {parts.fragment!r}")
    for f in ("favicon.ico", "images/favicon-192.png", "images/apple-touch-icon.png", "assets/email.js", OG_IMAGE, PHOTO):
        if not (ROOT / f).exists():
            problems.append(f"missing file: {f}")
    if external:
        for url in sorted(outside):
            status = fetch_status(url)
            ok = isinstance(status, int) and status < 400
            print(f"  {'ok  ' if ok else 'FAIL'} {status}  {url}")
            if not ok:
                problems.append(f"outside link may be broken ({status}): {url}")
    print(f"checked {len(files)} pages: " + ("no problems" if not problems else
                                             f"{len(problems)} problem(s)"))
    for p in problems:
        print("  - " + p)
    return not problems


def fetch_status(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link check)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return f"error: {getattr(e, 'reason', e)}"


def main():
    ap = argparse.ArgumentParser(description="Build the website (see README.md).")
    ap.add_argument("--check", action="store_true", help="check links and images after building")
    ap.add_argument("--external", action="store_true", help="also test links to other websites")
    ap.add_argument("--date", help="use this date (YYYY-MM-DD, at midnight) instead of now "
                                   "for changed pages")
    args = ap.parse_args()
    now = (datetime.datetime.combine(datetime.date.fromisoformat(args.date), datetime.time())
           if args.date else datetime.datetime.now()).astimezone().replace(microsecond=0)
    cfg, files = build(now)
    if args.check or args.external:
        if not check(cfg, files, args.external):
            sys.exit(1)


if __name__ == "__main__":
    main()
