# TODO

Open items from the initial build (13 September 2026). Everything here is either
unverified, placeholder, or waiting on a file. Nothing on the site was invented —
where a fact was missing it was left out or marked, not guessed.

## Verify — external links

All About-section links were checked before the first deploy and corrected:

- [x] `https://sse.tulane.edu/river` — department (200). The earlier guess
      `/rcse` was a 404 and has been replaced.
- [x] `https://sse.tulane.edu/ibrahim-demir` — Prof. Demir's faculty page (200).
- [x] `https://tulane.edu` (200) and `https://www.cuet.ac.bd` (200, redirects to
      `cuet.ac.bd`).
- [ ] `https://hydroinformatics.tulane.edu/` — Hydroinformatics Lab. The site is
      live and indexed, but it returns 403 to automated requests, so it could not
      be confirmed programmatically. **Open it once in a browser** to be sure.

## Verify — facts that came from the prompt, not from a file

Your CV (`assets/cv/golam-murad-cv.pdf`) contains no mention of Tulane; it ends
with "Research Engineer, Soil Profile, Dec 2025 – Present, Chittagong". So all of
the following is on the site on your word alone and should be double-checked:

- [ ] **PhD start date is written as "Aug 2026"** in the news list — confirm the
      actual month, and correct it in `NEWS` in `main.js` *and* in the `<noscript>`
      block in `index.html`.
- [ ] Position title: "first-year PhD student" and "Graduate Research Assistant,
      Hydroinformatics Lab, advised by Prof. Ibrahim Demir".
- [ ] **Consider updating the CV itself** — the PDF now linked from the site
      predates Tulane and still lists a Bangladesh address and phone number.
      Replace `assets/cv/golam-murad-cv.pdf` when you have a current version.

## Missing content

- [x] **Teaser figures.** All seven papers now have illustrative teasers
      (captioned "Illustration"). They are AI-generated graphics with some garbled
      text inside the images; consider swapping in real figures from the papers.
      See README for the JPG + WebP file convention. Originally: drop figures into
      `assets/img/teasers/`, then
      set `teaser` and `teaserAlt` on the matching object in `PUBLICATIONS`. The
      layout does not change when you do — only the image appears.
- [ ] **Vegetation dynamics paper has no abstract and no PDF.** There is no
      manuscript for it in `Paper/`, so the entry has `abstract: null` and no Paper
      button. Add both when available.
- [ ] **No DOI for the flood susceptibility preprint** (Mahmud, Murad, Rahman).
      The PDF states it is an EarthArXiv preprint but carries no DOI. Add a `doi`
      key to its `links` when EarthArXiv assigns one.

## Status labels to confirm

- [ ] **APMCE 2026** is labelled **"Accepted at APMCE 2026"** per your instruction.
      Your CV says "Submitted to". If it is not yet accepted, change `status` to
      `'Under review at APMCE 2026'`.
- [ ] **ICERIE 2025** — the PDF gives no month and its footer still reads
      "Submitted: xx Month, xxxx / Accepted: xx Month, xxxx". The site says 2025 per
      your CV, with no month. Add the month if you have it.

## Data discrepancies between your CV and the PDFs

Resolved in favour of the PDF in each case. Worth fixing in the CV so they agree:

- [ ] The Bayesian LSM paper: your CV lists the third author as **"S. Mahmud"** and
      the region as "Chittagong Metropolitan Hill System". The manuscript says
      **"Shafiq Mahmud"** and **"Chattogram"**. The site uses the manuscript.
- [ ] The vegetation dynamics paper: your CV lists **"S. Das"**. No manuscript was
      available to expand the initial. The site shows "S. Das".
- [ ] Your CV omits the flood susceptibility preprint, on which you are second
      author. It is included on the site at your request — consider adding it to
      the CV.

## Optional

- [ ] **Teaching** and **Talks & Service** sections exist as commented-out stubs at
      the bottom of `index.html`. Uncomment and add a nav link when you have content.
- [ ] **Open Graph image** — social previews currently use your square profile
      photo. A 1200×630 image would look better if you ever share the link.
- [ ] **Custom domain** — if you ever want one, add a `CNAME` file and set the DNS
      records; nothing else in this repo needs to change.
