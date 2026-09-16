# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static academic portfolio site for Golam Murad, served by GitHub Pages from the
`main` branch root (`murad-geoAi/murad-geoAi.github.io`). Plain HTML5, CSS3,
vanilla JS — no build step, no npm, no framework, no Jekyll (`.nojekyll` is
present). What's in the repo is exactly what gets served.

## Commands

Preview locally (required — `file://` breaks GitHub star counts via CORS and
changes clipboard behavior):

```bash
python3 -m http.server 8000      # Windows: py -m http.server 8000
```

Regenerate the interactive demo map (`demos/spatial-cv-demo.html`) after
changing its data or model — the seed is pinned and folium's element ids are
rewritten to sequential ones, so reruns are byte-identical and a diff means
something real changed:

```bash
py -m pip install -r scripts/requirements.txt
py scripts/make_demo_map.py
```

If the demo's data/model changes, the two AUC figures it prints must also be
updated by hand in the `#demo` section of `index.html`, or the prose and the
map will disagree.

There is no test suite, linter, or CI. Verification is manual: load the page
at 375px/768px/1280px, reload with JavaScript disabled, and tab through it to
check focus rings.

Deploy = push to `main`. Don't commit or push unless asked.

## Architecture

- `index.html` — the entire page, all sections in order.
- `assets/js/main.js` — holds the `NEWS` and `PUBLICATIONS` data arrays plus
  all page interactions (filtering, abstract/bibtex toggles, "show more",
  GitHub star fetch).
- `assets/css/style.css` — all styling, CSS custom properties at the top.
- `demos/spatial-cv-demo.html` — generated (not hand-edited) by
  `scripts/make_demo_map.py`; embedded via iframe in `#demo`.
- `demos/vendor/` — Leaflet 1.9.4, self-hosted so the demo makes zero CDN
  calls.
- `scripts/` — build-time only, never runs in production; the live site needs
  nothing installed.

### The one rule that spans files: JS-disabled parity

The site must read correctly with JavaScript disabled. News and publications
render from the `NEWS`/`PUBLICATIONS` arrays in `assets/js/main.js`, but
`index.html` also carries a `<noscript>` block with a plain static copy of
both lists. **Any change to either array must be mirrored in the matching
`<noscript>` block by hand** — nothing keeps them in sync automatically.

### Publications data shape

Each entry in `PUBLICATIONS` (`assets/js/main.js`) is grouped by `year`
automatically (newest year first; within a year, array order = display
order, so new papers go at the top of the array). Key conventions:

- `authors` must use the `ME` constant for the site owner's name — that's
  what renders it bold. Never hardcode `<strong>` into the data.
- `status`, `teaser`, `teaserAlt`, `abstract`, `bibtex`, and each `links` key
  are all optional; omitting one simply omits the corresponding UI element
  (e.g. no `abstract` → no Abstract button).
- `links` render in a fixed order: `paper, code, doi, arxiv, slides, poster,
  video, data`. A new link kind needs an entry in `LINK_LABELS` too.
- PDFs live in `assets/papers/`, lowercase-hyphenated.
- Teasers need three files: `foo.jpg` plus `foo-480.webp` and `foo-960.webp`
  (browsers load the WebP; a missing resized copy shows as a broken image).
  Full convention and a Pillow one-liner are in `README.md`.

### Design constraints

- ASCE palette: deep navy `#253a6e`, medium blue `#0273ba`, bright cyan
  `#059bd6`. Keep text contrast at WCAG AA (4.5:1) or better.
- Respect `prefers-reduced-motion` — any animation must be disabled under it.
- Teaching and Talks & Service sections exist as commented-out blocks near
  the bottom of `index.html`; enabling one also requires adding its link to
  the sticky `<nav>`.

See `README.md` for the full publication/news-item recipes and `TODO.md` for
open/unverified content items.
