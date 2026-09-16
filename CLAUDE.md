# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal academic portfolio site for Golam Murad, served at
`https://murad-geoAi.github.io`. Static HTML5, CSS3, vanilla JS — no build
step, no npm, no framework, no Jekyll (`.nojekyll` is present). What's in the
repo is exactly what GitHub Pages serves from the `main` branch root.

## Layout

- `index.html` — the entire page, all sections in order, plus a `<noscript>`
  fallback block near the bottom.
- `assets/css/style.css` — all styling; CSS variables at the top.
- `assets/js/main.js` — `NEWS` and `PUBLICATIONS` data arrays plus all
  interactions (rendering, filtering, "show more", copy-bibtex, etc.).
- `assets/img/teasers/` — per-paper figures (optional; falls back to a
  "Figure coming soon" placeholder box if absent).
- `assets/papers/` — PDFs linked from the Publications section.
- `assets/cv/golam-murad-cv.pdf` — linked CV.

## Critical rule: JS-disabled parity

The site must read correctly with JavaScript disabled. News and publications
render from JS arrays in `assets/js/main.js`, and are mirrored in a
`<noscript>` block in `index.html`. **Any change to `NEWS` or `PUBLICATIONS`
must be made in both places** — the JS array (what visitors normally see) and
the matching `<noscript>` fallback (short: title/date, authors, venue, links
only). Forgetting the fallback doesn't break anything for JS users, but it
silently breaks accessibility for everyone else.

## Adding a publication

Add one object to the `PUBLICATIONS` array (`assets/js/main.js`, starts at
line 93). Entries auto-group by `year`, newest year first; within a year, they
render in array order, so put new papers at the top of their year.

```js
{
  year: 2027,
  title: 'Title of the paper, sentence or title case as published',
  authors: ['Some Coauthor', ME, 'Another Coauthor'],   // ME renders bold
  venue: 'Journal or conference name, location',
  status: 'Under review at Journal Name',   // or 'Preprint', 'Accepted at X', or null
  teaser: 'assets/img/teasers/my-figure.webp',   // or null for a placeholder box
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

- `authors` must use the `ME` constant (`assets/js/main.js:91`) for Golam
  Murad's own name — that's what renders it bold. Never hardcode `<strong>`.
- `status`, `teaser`, `teaserAlt`, `abstract`, `bibtex`, and each key under
  `links` may be omitted or `null` — the corresponding button/element is
  simply not rendered (e.g. no `abstract` → no Abstract button).
- `links` render in a fixed order: `paper, code, doi, arxiv, slides, poster,
  video, data`. A new link kind must be added to `LINK_LABELS`
  (`assets/js/main.js:420`).
- PDFs go in `assets/papers/`, lowercase hyphenated filenames. Teasers go in
  `assets/img/teasers/`, ~1200px wide, 4:3.

## Adding a news item

Add one object to the top of the `NEWS` array (`assets/js/main.js:17`) —
array order is display order, newest first.

```js
{ date: 'Mar 2027', html: 'Short, one sentence. <a href="https://example.org" rel="noopener">Links allowed</a>.' }
```

`NEWS_VISIBLE` (`assets/js/main.js:71`) controls how many entries show before
the "Show more" toggle.

## Enabling Teaching / Talks & Service sections

Both exist as commented-out blocks near the bottom of `index.html`. Uncomment
the desired one, fill it in, and add a matching link to the `<nav>` list at
the top of the file.

## Design system

Warm, paper-like academic palette — cream background, dark ink text, a
single clay accent. No gradients, no photographic backgrounds. All colors
are CSS custom properties on `:root` in `assets/css/style.css`; there are no
hardcoded hex values anywhere else in the stylesheet (the print block's
literal `#000` is the one intentional exception — print always forces black
regardless of theme).

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

Keep text contrast at WCAG AA (4.5:1) or better, non-text UI boundaries at
3:1 or better — re-verify computed contrast (relative luminance, not eyeballing)
whenever a token value changes. The site respects `prefers-reduced-motion`;
any animation must be disabled under it.

## Preview locally

```bash
python3 -m http.server 8000      # Windows: py -m http.server 8000
```

Then open `http://localhost:8000`. Use a server, not `file://` — over
`file://` the GitHub star count widget fails (CORS) and clipboard behavior
differs.

After an edit, check: the page at 375px/768px/1280px width; the same page
with JavaScript disabled (publications and news must still list); and tab
order (every link/button should show a focus ring).

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
for double-checking.
