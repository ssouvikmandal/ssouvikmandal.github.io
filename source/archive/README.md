# Archived pages

Earlier versions of pages, kept so that they can be shown again. Files in this folder are
not built, linked from the menu or listed in the sitemap (and `robots.txt` asks search
engines not to read `source/`).

| File | What | Archived |
|---|---|---|
| `teaching-list.html` | the Teaching page as a list of entries (text as on the old Google Site, with the typing errors corrected) | 18 November 2026, when the table version replaced it |

To show an archived version again, copy it over the current page and rebuild, for example:

```bash
cp source/archive/teaching-list.html source/pages/teaching.html
python3 build.py --check
```

The page keeps its address (`teaching.html`). To go back to the table, copy the table
version back from the git history (`git log -- source/pages/teaching.html`) or keep a copy
of it here first.
