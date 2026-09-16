# murad-geoAi.github.io

Personal academic site for Golam Murad — <https://murad-geoAi.github.io>

Plain HTML, CSS and vanilla JavaScript. No build step, no npm, no Jekyll, no
framework. What is in the repository is exactly what GitHub Pages serves.

## Layout

```
.
├── index.html              the whole page — all sections, in order
├── .nojekyll               tells GitHub Pages to serve files as-is
├── assets/
│   ├── css/style.css       all styling; CSS variables at the top
│   ├── js/main.js          NEWS and PUBLICATIONS data + all interactions
│   ├── img/
│   │   ├── avatar.webp     330×330 head-and-shoulders crop for the header (served first)
│   │   ├── avatar.jpg      same crop (fallback)
│   │   ├── profile.jpg     600×600 full photo, used as the social-preview image
│   │   ├── favicon.svg
│   │   └── teasers/        per-paper images: foo.jpg + foo-480.webp + foo-960.webp
│   ├── papers/             PDFs linked from the Publications section
│   └── cv/golam-murad-cv.pdf
├── demos/
│   ├── spatial-cv-demo.html  generated map embedded in the #demo section
│   └── vendor/             Leaflet 1.9.4, self-hosted — the demo makes no CDN calls
├── scripts/                build-time only; the site itself needs nothing installed
│   ├── make_demo_map.py    regenerates demos/spatial-cv-demo.html (see scripts/README.md)
│   └── requirements.txt
├── README.md
└── TODO.md                 open items and things to verify
```

## The one thing to know before editing

The site must read correctly with JavaScript disabled. News and publications are
rendered from JavaScript arrays, so `index.html` also carries a `<noscript>`
block with a plain static copy of both lists.

**When you add a publication or a news item, update it in two places:**

1. the array in `assets/js/main.js` — this is what visitors see
2. the matching `<noscript>` block in `index.html` — a one-line fallback

The fallback lines are deliberately short; a title, authors, venue and links is
enough. If you forget one, the site still works for everyone with JavaScript on.

## Add a publication

Add one object to the `PUBLICATIONS` array near the top of `assets/js/main.js`.
Entries are grouped by `year` automatically, newest year first, and within a year
they appear in array order — so put new papers at the top.

```js
{
  year: 2027,
  title: 'Title of the paper, sentence or title case as published',
  authors: ['Some Coauthor', ME, 'Another Coauthor'],   // ME renders bold
  venue: 'Journal or conference name, location',
  status: 'Under review at Journal Name',   // or 'Preprint', 'Accepted at X', or null
  teaser: 'assets/img/teasers/my-figure.jpg',    // or null for a placeholder box
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

Notes:

- `authors` must use the constant `ME` for your own name — that is what makes it
  bold. Do not write `<strong>` into the data.
- Any of `status`, `teaser`, `abstract`, `bibtex` and each key in `links` may be
  omitted or set to `null`; the corresponding button or element is simply not
  rendered. A paper with no `abstract` gets no Abstract button.
- `links` keys are rendered in a fixed order: `paper, code, doi, arxiv, slides,
  poster, video, data`. Adding a new kind of link means adding it to the
  `LINK_LABELS` object.
- Put the PDF in `assets/papers/` with a lowercase, hyphenated filename.
- Put a 16:9 teaser JPG in `assets/img/teasers/` **and** two resized WebP copies
  beside it named `-480.webp` and `-960.webp` (e.g. `my-figure.jpg`,
  `my-figure-480.webp`, `my-figure-960.webp`). Browsers load the WebP files, and
  a missing one shows as a broken image. With Pillow installed:

  ```
  py -c "from PIL import Image as I; im=I.open('assets/img/teasers/my-figure.jpg'); [im.resize((w, round(im.height*w/im.width)), I.LANCZOS).save(f'assets/img/teasers/my-figure-{w}.webp', quality=78, method=6) for w in (480, 960)]"
  ```

  Teasers are captioned "Illustration". Without one you get a neutral "Figure
  coming soon" box and the layout is unchanged.

## Add a news item

Add one object to the top of the `NEWS` array in `assets/js/main.js`. Newest
first — the order in the array is the order on the page.

```js
{
  date: 'Mar 2027',
  html: 'Short, one sentence. <a href="https://example.org" rel="noopener">Links are allowed</a>.'
}
```

`NEWS_VISIBLE` just below the array controls how many entries show before the
"Show more" button (currently 6).

## Enable the Teaching or Talks & Service sections

Both exist as commented-out blocks near the bottom of `index.html`. Uncomment the
one you want, fill it in, and add a matching link to the `<nav>` list at the top
of the file so it appears in the sticky nav.

## Preview locally

From this directory:

```bash
python3 -m http.server 8000      # Windows: py -m http.server 8000
```

Then open <http://localhost:8000>.

Use a server rather than opening `index.html` directly — over `file://` the
GitHub star counts will not load (the API call is blocked by CORS) and clipboard
behaviour differs.

Things worth checking after an edit:

- the page at 375px, 768px and 1280px wide
- the same page with JavaScript disabled — publications and news must still list
- tab through the page; every link and button should show a focus ring

## Deploy

The site is served from the `main` branch root of
`murad-geoAi/murad-geoAi.github.io`. Pushing to `main` publishes it; GitHub Pages
usually reflects the change within a minute or two.

```bash
git add -A
git commit -m "Describe the change"
git push
```

`.nojekyll` is required — without it GitHub Pages runs the files through Jekyll,
which ignores directories beginning with an underscore and can rewrite content
unexpectedly.
