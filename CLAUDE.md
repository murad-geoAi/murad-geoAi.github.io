# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal academic portfolio site for Golam Murad, served at
`https://murad-geoAi.github.io`. Static HTML5, CSS3, vanilla JS — no build
step, no npm, no framework, no Jekyll (`.nojekyll` is present). What's in the
repo is exactly what GitHub Pages serves from the `main` branch root.

## Layout

- `index.html` — the entire page, all sections in order, plus two `<noscript>`
  fallback blocks (news, publications) mid-file, not at the bottom.
- `assets/cv/index.html` — a second, separate page (a styled CV landing page)
  that also links `assets/css/style.css`. A style change can affect this page
  too — check it alongside `index.html`.
- `assets/css/style.css` — all styling; CSS variables at the top.
- `assets/js/main.js` — `NEWS` and `PUBLICATIONS` data arrays plus all
  interactions (rendering, filtering, "show more", copy-bibtex, GitHub star
  fetch, etc.).
- `assets/img/` — `avatar.jpg`/`avatar.webp` (header photo), `profile.jpg`
  (social-preview image), `favicon.svg`, plus:
  - `assets/img/teasers/` — per-paper figures (optional; falls back to a
    "Figure coming soon" placeholder box if absent). Each figure needs three
    files: `foo.jpg` plus resized `foo-480.webp` and `foo-960.webp` (browsers
    load the WebP; a missing resized copy shows as a broken image). Full
    convention and a Pillow one-liner are in `README.md`.
- `assets/papers/` — PDFs linked from the Publications section.
- `assets/cv/golam-murad-cv.pdf` — linked CV (PDF; distinct from
  `assets/cv/index.html` above).
- `assets/vendor/leaflet/` — vendored Leaflet JS/CSS/marker images, so the
  demo map has no third-party runtime dependency. Not hand-edited; see
  "Regenerating the demo map" below.
- `demos/spatial-cv-demo.html` — generated Folium map, embedded via
  `<iframe>` in the Demo section. Not hand-edited.
- `scripts/make_demo_map.py` — generates `demos/spatial-cv-demo.html`.
  Dev-only (needs `folium`, `numpy`, `scikit-learn`, minimum versions in
  `scripts/requirements.txt`; not shipped to visitors).

## Critical rule: JS-disabled parity

The site must read correctly with JavaScript disabled. News and publications
render from JS arrays in `assets/js/main.js`, and are mirrored in a
`<noscript>` block in `index.html`. **Any change to `NEWS` or `PUBLICATIONS`
must be made in both places** — the JS array (what visitors normally see) and
the matching `<noscript>` fallback (short: title/date, authors, venue, links
only). Forgetting the fallback doesn't break anything for JS users, but it
silently breaks accessibility for everyone else.

## Adding a publication

Add one object to the `PUBLICATIONS` array in `assets/js/main.js`. Entries
auto-group by `year`, newest year first; within a year, they render in array
order, so put new papers at the top of their year.

```js
{
  year: 2027,
  title: 'Title of the paper, sentence or title case as published',
  authors: ['Some Coauthor', ME, 'Another Coauthor'],   // ME renders bold
  venue: 'Journal or conference name, location',
  status: 'Under review at Journal Name',   // or 'Preprint', 'Accepted at X', or null
  teaser: 'assets/img/teasers/my-figure.jpg',   // .jpg — the WebP srcset is derived from this path; or null for a placeholder box
  teaserAlt: 'What the figure shows, for screen readers.',
  links: {
    paper: 'assets/papers/my-paper-2027.pdf',
    code:  'https://github.com/murad-geoAi/my-repo',
    doi:   'https://doi.org/10.xxxxx/yyyyy'
  },
  abstract: 'Plain text. Written as one string, no HTML.',
  bibtex: `@article{key2027,
  title  = {...},
  author = {...},
  year   = {2027}
}`
}
```

- `authors` must use the `ME` constant in `assets/js/main.js` for Golam
  Murad's own name — that's what renders it bold. Never hardcode `<strong>`.
- `status`, `teaser`, `teaserAlt`, `abstract`, `bibtex`, and each key under
  `links` may be omitted or `null` — the corresponding button/element is
  simply not rendered (e.g. no `abstract` → no Abstract button).
- `links` render in a fixed order: `paper, code, doi, arxiv, slides, poster,
  video, data`. A new link kind must be added to the `LINK_LABELS` object in
  `assets/js/main.js`.
- PDFs go in `assets/papers/`, lowercase hyphenated filenames. Teasers go in
  `assets/img/teasers/`, ~1200px wide, **16:9** (see the three-file WebP
  convention above).

## Adding a news item

Add one object to the top of the `NEWS` array in `assets/js/main.js` — array
order is display order, newest first.

```js
{ date: 'Mar 2027', html: 'Short, one sentence. <a href="https://example.org" rel="noopener">Links allowed</a>.' }
```

`NEWS_VISIBLE` (just below the array) controls how many entries show before
the "Show more" toggle.

## Enabling Teaching / Talks & Service sections

Both exist as commented-out blocks near the bottom of `index.html`. Uncomment
the desired one, fill it in, and add a matching link to the `<nav>` list at
the top of the file.

## Design system

Warm, paper-like academic palette — cream background, dark ink text, a
single clay accent. No gradients, no photographic backgrounds. **Light-only —
there is no dark mode or `prefers-color-scheme` handling**, by deliberate
choice (see `REDESIGN-PLAN.md`); don't add one without checking with the site
owner first, since every token below would need a matching dark value.

All colors are CSS custom properties on `:root` in `assets/css/style.css`;
there are no hardcoded hex values anywhere else in the stylesheet except: the
print block, which forces literal `#000` regardless of the tokens (print
always renders black); and the nav's scroll-fade `mask-image` gradients,
which use literal `#000`/`transparent` as opaque/transparent mask stops, not
as visible color.

- `--bg` `#FAF7F2`, `--bg-subtle` `#F2EDE4`, `--surface` `#FFFFFF` — page,
  hero/footer band, and card backgrounds.
- `--border` `#E3DDD3` — decorative hairlines only (under 3:1, not a UI
  boundary). `--border-firm` `#998C77` — for anything that must read as a
  UI-component edge (button outlines, nav-hover underline); it's deliberately
  darker so it clears WCAG's 3:1 non-text threshold against `--bg`.
- `--ink` `#23211E` / `--ink-muted` `#6B6862` — body/headings and secondary
  text.
- `--accent` `#C96442` (clay) is **non-text only** — rules, underlines,
  border accents, the decision-boundary motif. At 3.65:1 on `--bg` it clears
  the 3:1 bar for non-text but fails 4.5:1 for text at any size. Link and
  active-nav text uses `--accent-text` `#A94F32` (5.10:1) instead, with
  `--accent-text-hover` `#8F4029` (6.70:1) on hover/focus.
- `--accent-soft` `#F0DDD4` — chip/tag backgrounds. Pair it with `--ink`
  (12.23:1), not `--ink-muted` or `--accent` — both dip under 4.5:1 on it.
- Exactly one accent color in the whole system. If something needs to stand
  out and clay is already used nearby, reach for weight or spacing, not a
  new hue.
- Icons (mail/scholar/orcid/github/linkedin/cv in the `index.html` sprite)
  are single-stroke `fill:none; stroke:currentColor` paths, not brand marks
  — they inherit whatever text color surrounds them and are not exempted
  from the one-accent rule.
- `--focus` `#A94F32` — the focus-ring color. Same value as `--accent-text`
  today, but a separate token; don't assume changing one also changes the
  other.
- Non-color tokens also on `:root`: `--measure` (`46rem`, the readable text
  column width), `--gutter` (`1.25rem`, page-edge padding), and `--sans` /
  `--mono` (system font stacks — **no webfonts**; the site loads nothing from
  Google Fonts or any CDN, by design).

Keep text contrast at WCAG AA (4.5:1) or better, non-text UI boundaries at
3:1 or better — re-verify computed contrast (relative luminance, not eyeballing)
whenever a token value changes. The site respects `prefers-reduced-motion`;
any animation must be disabled under it.

## Regenerating the demo map

`demos/spatial-cv-demo.html` is a static Folium map, embedded via `<iframe>`
in the Demo section of `index.html`. It's generated, not hand-written; see
also `scripts/README.md` for the short version of this workflow. To
regenerate it after changing the fold logic, colors, or panel styling, edit
`scripts/make_demo_map.py` and run:

```bash
python3 -m pip install -r scripts/requirements.txt   # one-time, dev-only
python3 scripts/make_demo_map.py                      # Windows: py scripts/make_demo_map.py
```

The seed is pinned, but Folium still assigns each map/feature-group a random
hash id on every run, so a rerun's diff always shows id-only churn even when
nothing meaningful changed — judge a regeneration by the printed AUC values,
not by the diff. If the demo's underlying data or model changes, the two AUC
figures it prints must also be updated by hand in the `#demo` section of
`index.html`, or the prose and the map will disagree (this has happened
before — see git history).

This also vendors Leaflet into `assets/vendor/leaflet/` on first run (skipped
if already present) so the demo has no third-party runtime dependency —
regenerating never adds a CDN call. The basemap is Esri's free World Light
Gray Canvas (no API key); CARTO's free keyless Positron tier was retired and
now serves a watermarked tile, so don't switch back to it without verifying
by loading an actual tile first.

The generated map is a standalone HTML document and can't read `style.css`'s
`:root` tokens, so `make_demo_map.py` hardcodes `#6B6862` (== `--ink-muted`)
for its own panel CSS. If `--ink-muted` ever changes, update it here too or
the demo's panel text will silently drift from the rest of the page.

## Preview locally

```bash
python3 -m http.server 8000      # Windows: py -m http.server 8000
```

Then open `http://localhost:8000`. Use a server, not `file://` — over
`file://` the GitHub star count widget fails (CORS) and clipboard behavior
differs.

After an edit, check: the page at 375px/768px/1280px width; the same page
with JavaScript disabled (publications and news must still list); and tab
order (every link/button should show a focus ring). There is no test suite,
linter, or CI — verification is manual.

## Deploy

Push to `main` — GitHub Pages (`murad-geoAi/murad-geoAi.github.io`) serves
straight from the branch root and usually reflects changes within a minute or
two. `.nojekyll` must stay present, or GitHub Pages runs files through Jekyll
and ignores underscore-prefixed directories. **Don't commit or push unless
asked.**

## Open items

See `TODO.md` for unverified facts, missing content (teaser figures, some
abstracts/PDFs/DOIs), and status labels pending confirmation from the site
owner — several facts currently on the site (e.g. PhD start date, position
title) came from the prompt rather than a source file and are flagged there
for double-checking. See `README.md` for the full publication/news-item
recipes.

`REDESIGN-PLAN.md` is a **completed** spec, not a live to-do — all three of
its phases have shipped. Its lasting value is as the record of *why* the
design is the way it is: the warm palette rationale, "no dark mode in this
pass," "no new fonts," "no new frameworks," and the one-accent rule all come
from there. Treat it as design rationale to consult, not pending work.
