# scripts

Build-time only. **The website has no runtime dependencies** — these scripts
generate files that are committed, and GitHub Pages serves the output verbatim.
You never need Python to view or deploy the site.

## make_demo_map.py

Generates `demos/spatial-cv-demo.html`, the interactive map embedded in the
`#demo` section of `index.html`.

```sh
py -m pip install -r scripts/requirements.txt
py scripts/make_demo_map.py
```

It prints the mean AUC under each cross-validation scheme and the output file
size. The seed is pinned and folium's random element ids are rewritten to
sequential ones, so **reruns are byte-identical** — a diff means something
actually changed.

If you change the data or the model, the two AUC figures are also written in
prose in the `#demo` section of `index.html`. Update them there too, or the
page and the map will disagree.

On first run it downloads Leaflet 1.9.4 into `demos/vendor/` (skipped if already
present). Those files are committed so the demo makes no CDN requests.
