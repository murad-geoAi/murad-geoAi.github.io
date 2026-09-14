# CLAUDE.md

Project notes for working in this repo.

- Static academic portfolio: plain HTML5, CSS3, vanilla JS. No build step, no
  npm, no framework, no Jekyll (`.nojekyll` is present). What's in the repo is
  exactly what GitHub Pages serves.
- The site MUST read correctly with JavaScript disabled. News and publications
  are rendered from JS arrays in `assets/js/main.js` AND mirrored in a
  `<noscript>` block in `index.html`. When either list changes, update BOTH
  places.
- Design system: ASCE palette — deep navy `#253a6e`, medium blue `#0273ba`,
  bright cyan `#059bd6`. Keep text contrast at WCAG AA (4.5:1) or better.
- The site respects `prefers-reduced-motion`. Any animation must be disabled
  under it.
- Preview locally: `python3 -m http.server 8000` (Windows: `py -m http.server
  8000`).
- Deploy = push to `main`. Don't commit or push unless asked.
