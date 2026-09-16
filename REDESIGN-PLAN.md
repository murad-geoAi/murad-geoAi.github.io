# Redesign plan — portfolio site

This file is the spec. Read it fully before planning. Do not start coding
until I approve a plan.

Three pieces of work, in this order:
1. Fix two bugs in the existing Folium demo
2. Replace the color system
3. Add a subtle ML/geospatial motif to the design

---

## 1. Fix the demo map (do this first)

### 1a. Basemap shows "API KEY REQUIRED" watermark

The CartoDB Positron tiles currently render with an "API KEY REQUIRED"
watermark repeated across the map. The tile endpoint being used now
requires a CARTO key.

Fix it in `scripts/make_demo_map.py`. Options, in order of preference:

- Pass an explicit keyless tile URL to `folium.TileLayer`, e.g. the plain
  OpenStreetMap standard tiles, with correct attribution
- Or a keyless CARTO basemap CDN URL if one still works — verify by
  actually loading a tile, do not assume

Requirements:
- No API keys, no accounts, no environment variables. This is a static
  site on GitHub Pages.
- Attribution must be correct for whatever tiles are used.
- The basemap must stay light and low-contrast so the colored fold points
  remain the visual focus.
- After the change, regenerate `demos/spatial-cv-demo.html` and confirm by
  loading it that no watermark appears.

### 1b. Layer control is confusing

Right now the control shows the basemap as an option, and the two fold
layers are independent checkboxes — the visitor can enable both at once
(points overlap and the comparison is meaningless) or disable both (empty
map).

Change it to:
- Hide the basemap from the control entirely
- Make "Random 5-fold" and "Spatial block 5-fold" mutually exclusive, so
  exactly one is always visible — either use radio-style overlays or build
  a small custom two-button toggle in the map's HTML
- Default to "Random 5-fold" on load, since the story is "this looks good
  … until you block it spatially"
- Label the control clearly, e.g. a heading that says "Validation scheme"

### 1c. While you are in there

- The AUC box is good. Keep it, but restyle it to the new palette in
  section 2 once that exists.
- Check the box does not overlap the points at 390px width.

---

## 2. Color system

Replace the current blue hero and blue-tinted UI entirely. The new
direction is a warm, paper-like academic palette — cream background, dark
ink text, a single clay accent. No gradients, no photographic background
behind the header.

### Tokens

Define these once as CSS custom properties on `:root` and refactor every
existing hardcoded color in the stylesheets to reference them. Do not
leave stray hex values scattered in the CSS.

```css
:root {
  --bg:            #FAF7F2;  /* page background, warm off-white */
  --bg-subtle:     #F2EDE4;  /* alternating sections, hero band */
  --surface:       #FFFFFF;  /* cards, the map frame */
  --border:        #E3DDD3;  /* hairlines, dividers, card edges */
  --ink:           #23211E;  /* headings and body text */
  --ink-muted:     #6B6862;  /* captions, dates, disclaimers */
  --accent:        #C96442;  /* clay — links, active nav, underline */
  --accent-hover:  #A94F32;
  --accent-soft:   #F0DDD4;  /* accent background washes, tag chips */
}
```

### Rules

- The hero becomes `--bg-subtle` with the motif from section 3 behind it.
  Remove the blue gradient and the photo backdrop.
- Hero text switches to `--ink`. Verify contrast — it must pass WCAG AA at
  the size used.
- The profile photo keeps its circular crop but gets a `--border` ring
  instead of sitting on a dark field.
- The social buttons (Email, Scholar, ORCID, GitHub, LinkedIn, CV) become
  outlined pills: `--surface` fill, `--border` outline, `--ink` label, and
  on hover the outline and label go `--accent`.
- Active nav tab underline uses `--accent`, not blue.
- Exactly one accent color. If something needs to stand out and clay is
  already used nearby, use weight or spacing instead of a new color.
- Update the demo map's fold-point colors to a palette that sits well on
  the cream page. Five categorical colors, colorblind-safe, and none of
  them should clash with `--accent`.

### Dark mode

If the site already has a dark mode, mirror every token. If it does not,
do not add one in this pass — tell me and we will do it separately.

---

## 3. ML / geospatial design motif

I want the design to quietly signal what I work on, without looking like a
tech startup landing page. Subtle, structural, never decorative noise.

Implement these:

### 3a. Hero background — contour + node motif

A single SVG layer behind the hero text, at low opacity, combining:
- Faint topographic contour lines (nested irregular closed curves), which
  read as both terrain and water flow
- A sparse node-and-edge graph overlaid on them — maybe 12–20 small dots
  connected by thin straight lines, irregular, not a neat grid

Constraints:
- Inline SVG or a CSS background, no image files, no external libraries
- Total opacity low enough that it never competes with the text — start
  around 6–8% and show me both ends
- Must not tile visibly or repeat in an obvious pattern
- Static by default. If you add any motion, gate it behind
  `prefers-reduced-motion: no-preference` and keep it almost imperceptible
- Degrades to flat `--bg-subtle` if the SVG fails

### 3b. Section dividers

Replace plain horizontal rules between sections with a very thin contour
line fragment, same motif family, `--border` color.

### 3c. Scatter accent on the Demo section heading

A tiny cluster of dots forming a soft decision boundary, sitting next to
or behind the "Demo" heading. Small — under 60px. Same accent family.

### 3d. Skills section

If skills are currently plain text or generic badges, render them as
`--accent-soft` chips with `--ink` labels.

### Explicitly not wanted

- No animated particle networks
- No glowing neural-net hero graphics
- No matrix/code-rain effects
- No stock "AI brain" imagery
- Nothing that adds a JS dependency

---

## 4. Global constraints

- Static site on GitHub Pages. No server code, no build step that I have
  to remember to run, no API keys.
- No new frameworks. No Tailwind, no Bootstrap, no component library.
- No new fonts unless the current one clashes badly with the warm palette
  — if it does, tell me before switching, and propose one system-safe
  alternative with a full fallback stack.
- Total page weight added by sections 2 and 3 combined must stay under
  50 KB. Report the actual number.
- Must look correct at 1440px, 768px, and 390px.
- Preserve all existing content, links, and section order. This is a
  restyle, not a rewrite.
- Work on a branch. Commit each of the three sections separately so I can
  revert one without losing the others.

---

## 5. Acceptance checks

Before you tell me it is done:

- [ ] Demo map loads with no watermark on any tile
- [ ] Exactly one fold scheme visible at a time; basemap not in the control
- [ ] No blue remains anywhere in the stylesheets
- [ ] Every color in the CSS references a token from section 2
- [ ] Hero text contrast passes WCAG AA
- [ ] Hero motif is visible but does not interfere with reading the name
      and description
- [ ] Page still scrolls normally on mobile when a finger is over the map
- [ ] Nothing overflows horizontally at 390px
- [ ] Reported page weight is under 50 KB added

---

## 6. What I want from you now

Do not write code yet.

Read the repo, then give me a plan covering:
- Every file you will create or modify, with a one-line reason each
- How you will fix the tile watermark, and which tile source you verified
- Your proposed five colors for the fold points, with reasoning
- How you will build the contour motif, and roughly how many bytes of SVG
- Anything in this document you think is a bad idea, and why
