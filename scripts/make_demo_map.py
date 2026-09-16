#!/usr/bin/env python3
"""Generate demos/spatial-cv-demo.html: a Folium map comparing random vs.
spatial-block 5-fold cross-validation on synthetic, spatially-autocorrelated
point data.

Dev-only. Requires: folium, numpy, scikit-learn (pip install them; not
shipped to site visitors). Run from the repo root:

    py scripts/make_demo_map.py

Regenerates demos/spatial-cv-demo.html and vendors Leaflet locally into
assets/vendor/leaflet/ on first run (skipped if already present).
"""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from pathlib import Path

import folium
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "demos" / "spatial-cv-demo.html"
VENDOR_DIR = REPO_ROOT / "assets" / "vendor" / "leaflet"

RNG_SEED = 7
N_BLOBS = 6
POINTS_PER_BLOB = 30
BLOB_SPREAD_DEG = 0.35   # lat/lon std within a blob
N_SPLITS = 5

# Map center: Chittagong Hill Tracts, Bangladesh — matches the author's
# actual landslide-susceptibility study region rather than an arbitrary spot.
CENTER_LAT, CENTER_LON = 22.6, 92.2
BLOB_EXTENT_DEG = 1.6  # how far blob centers spread from CENTER

# Five colorblind-separable, >=3:1-on-cream colors validated during the
# section-2 planning pass. Reused directly, not re-derived.
FOLD_COLORS = ["#1F3B73", "#2E7D74", "#B8860B", "#7B4B94", "#4A5A63"]

# CARTO's free keyless Positron tier (basemaps.cartocdn.com and its Fastly
# mirror) has been retired — both now serve an "API KEY REQUIRED" watermark
# baked into the tile image itself, verified 2026-09-16. Esri's World Light
# Gray Canvas is a long-standing free, no-auth ArcGIS REST tile service and
# is visually the closer match to what CARTO Positron used to look like:
# flat light grey, minimal labels, no watermark.
TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
TILE_ATTR = "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ"

# Must match the version folium's own template bundles, or the CDN->local
# rewrite silently no-ops and the page keeps loading from jsdelivr.
LEAFLET_VERSION = "1.9.3"
LEAFLET_CSS_URL = f"https://cdn.jsdelivr.net/npm/leaflet@{LEAFLET_VERSION}/dist/leaflet.css"
LEAFLET_JS_URL = f"https://cdn.jsdelivr.net/npm/leaflet@{LEAFLET_VERSION}/dist/leaflet.js"
# Marker images referenced by leaflet.css via relative url(images/...).
LEAFLET_IMAGES = ["marker-icon.png", "marker-icon-2x.png", "marker-shadow.png"]
LEAFLET_IMG_BASE = f"https://cdn.jsdelivr.net/npm/leaflet@{LEAFLET_VERSION}/dist/images/"

# folium's default template also pulls in jQuery, Bootstrap, FontAwesome and
# Leaflet.awesome-markers for features this map never uses (no popups, no
# Bootstrap UI, no awesome-markers icons — just CircleMarkers + a tile
# layer). Strip them rather than vendor libraries that do nothing.
UNUSED_CDN_LINE_PATTERNS = [
    re.compile(r'^\s*<script src="https://code\.jquery\.com/[^"]*"></script>\s*$', re.M),
    re.compile(r'^\s*<script src="https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]*"></script>\s*$', re.M),
    re.compile(r'^\s*<script src="https://cdnjs\.cloudflare\.com/ajax/libs/Leaflet\.awesome-markers/[^"]*"></script>\s*$', re.M),
    re.compile(r'^\s*<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/bootstrap@[^"]*"/>\s*$', re.M),
    re.compile(r'^\s*<link rel="stylesheet" href="https://netdna\.bootstrapcdn\.com/[^"]*"/>\s*$', re.M),
    re.compile(r'^\s*<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/@fortawesome/[^"]*"/>\s*$', re.M),
    re.compile(r'^\s*<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/Leaflet\.awesome-markers/[^"]*"/>\s*$', re.M),
    re.compile(r'^\s*<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/gh/python-visualization/folium/[^"]*"/>\s*$', re.M),
]


def make_synthetic_points(rng: np.random.Generator):
    """Spatially-autocorrelated points: label is a property of which blob
    a point falls in (plus noise), so nearby points share labels and random
    folds leak blob membership across train/test."""
    blob_centers = rng.uniform(-1, 1, size=(N_BLOBS, 2)) * BLOB_EXTENT_DEG
    blob_centers += [CENTER_LAT, CENTER_LON]
    # Alternate base label by blob so classes aren't spatially confounded
    # with a simple north/south split, but blob membership still carries
    # nearly all the signal.
    blob_base_label = (np.arange(N_BLOBS) % 2)

    lats, lons, labels, blob_id = [], [], [], []
    for i, (blat, blon) in enumerate(blob_centers):
        pts_lat = rng.normal(blat, BLOB_SPREAD_DEG, POINTS_PER_BLOB)
        pts_lon = rng.normal(blon, BLOB_SPREAD_DEG, POINTS_PER_BLOB)
        # 85% of points in a blob follow the blob's base label; 15% flip,
        # so the classifier has real (if easy) signal, not a lookup table.
        flip = rng.random(POINTS_PER_BLOB) < 0.15
        base = np.full(POINTS_PER_BLOB, blob_base_label[i])
        lab = np.where(flip, 1 - base, base)
        lats.append(pts_lat)
        lons.append(pts_lon)
        labels.append(lab)
        blob_id.append(np.full(POINTS_PER_BLOB, i))

    return (
        np.concatenate(lats),
        np.concatenate(lons),
        np.concatenate(labels),
        np.concatenate(blob_id),
    )


def run_cv(X: np.ndarray, y: np.ndarray, fold_assignment: np.ndarray, n_splits: int):
    """Given a fold assignment (0..n_splits-1 per point), run leave-one-fold-out
    CV with a RandomForest and return (out-of-fold predictions, auc, fold_id)."""
    oof_pred = np.zeros(len(y))
    for fold in range(n_splits):
        test_mask = fold_assignment == fold
        train_mask = ~test_mask
        clf = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=RNG_SEED)
        clf.fit(X[train_mask], y[train_mask])
        oof_pred[test_mask] = clf.predict_proba(X[test_mask])[:, 1]
    auc = roc_auc_score(y, oof_pred)
    return oof_pred, auc


def spatial_block_folds(lat: np.ndarray, lon: np.ndarray, n_splits: int) -> np.ndarray:
    """KMeans on coordinates gives geographically contiguous folds."""
    coords = np.column_stack([lat, lon])
    km = KMeans(n_clusters=n_splits, random_state=RNG_SEED, n_init=10)
    return km.fit_predict(coords)


def random_folds(n_points: int, n_splits: int, rng: np.random.Generator) -> np.ndarray:
    assignment = np.zeros(n_points, dtype=int)
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=RNG_SEED)
    for fold, (_, test_idx) in enumerate(kf.split(np.arange(n_points))):
        assignment[test_idx] = fold
    return assignment


def build_features(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    # Deliberately weak, spatially-smooth features (not lat/lon directly,
    # to avoid trivially handing the classifier the answer) — coarse
    # sinusoidal terrain-like proxies, consistent with "synthetic" data.
    f1 = np.sin(lat * 3) + np.cos(lon * 2)
    f2 = np.sin(lon * 4) * np.cos(lat * 1.5)
    return np.column_stack([f1, f2, lat, lon])


def vendor_leaflet():
    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    img_dir = VENDOR_DIR / "images"
    img_dir.mkdir(exist_ok=True)

    targets = {
        VENDOR_DIR / "leaflet.css": LEAFLET_CSS_URL,
        VENDOR_DIR / "leaflet.js": LEAFLET_JS_URL,
    }
    for name in LEAFLET_IMAGES:
        targets[img_dir / name] = LEAFLET_IMG_BASE + name

    for dest, url in targets.items():
        if dest.exists():
            continue
        print(f"vendoring {url} -> {dest.relative_to(REPO_ROOT)}")
        with urllib.request.urlopen(url) as resp:
            dest.write_bytes(resp.read())


def rewrite_cdn_to_local(html: str) -> str:
    """Folium/Leaflet emit absolute CDN URLs for leaflet.css/js. Rewrite
    them to the vendored local copies so the page has no third-party
    runtime dependency."""
    html = html.replace(LEAFLET_CSS_URL, "../assets/vendor/leaflet/leaflet.css")
    html = html.replace(LEAFLET_JS_URL, "../assets/vendor/leaflet/leaflet.js")
    for pattern in UNUSED_CDN_LINE_PATTERNS:
        html = pattern.sub("", html)
    return html


def build_toggle_and_auc_html(auc_random: float, auc_spatial: float, map_var: str,
                               fg_random_var: str, fg_spatial_var: str) -> str:
    # Below ~520px of actual rendering width (which includes the case where
    # this page sits inside a narrower embedding iframe, not just a narrow
    # top-level viewport) an absolutely-positioned corner overlay risks
    # covering data points regardless of how small it's shrunk, since points
    # are scattered across the whole map. So at that width the panel becomes
    # part of normal document flow, stacked above the map, guaranteeing zero
    # overlap by construction instead of by hoping a corner stays empty.
    return f"""
<style>
  html, body {{ margin: 0; padding: 0; }}
  body {{ display: flex; flex-direction: column; }}
  #validation-panel {{
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 1000;
    background: #FFFFFF;
    border: 1px solid #E3DDD3;
    border-radius: 4px;
    padding: .65rem .75rem;
    font: 13px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #23211E;
    box-shadow: 0 1px 3px rgba(0,0,0,.12);
    max-width: 190px;
    box-sizing: border-box;
  }}
  #validation-panel h4 {{
    margin: 0 0 .5rem;
    font-size: .7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #6B6862;
  }}
  .vp-toggle {{ display: flex; gap: .35rem; margin-bottom: .6rem; }}
  .vp-btn {{
    flex: 1;
    font: inherit;
    font-size: .72rem;
    padding: .3rem .4rem;
    border: 1px solid #998C77;
    border-radius: 3px;
    background: #FAF7F2;
    color: #A94F32;
    cursor: pointer;
  }}
  .vp-btn[aria-pressed="true"] {{ background: #23211E; color: #FFFFFF; border-color: #23211E; }}
  .vp-auc {{ display: flex; justify-content: space-between; font-variant-numeric: tabular-nums; }}
  .vp-auc + .vp-auc {{ margin-top: .2rem; }}
  .vp-auc-label {{ color: #6B6862; }}
  .vp-auc-value {{ font-weight: 700; }}

  /* Narrow: panel leaves the map and becomes a full-width bar above it,
     so it can never overlap a data point. */
  @media (max-width: 520px) {{
    body {{ display: flex; flex-direction: column; }}
    #validation-panel {{
      position: static;
      width: 100%;
      max-width: none;
      border-width: 0 0 1px 0;
      border-radius: 0;
      box-shadow: none;
      padding: .6rem .75rem;
      order: -1;
    }}
    .vp-toggle {{ max-width: 260px; }}
    .folium-map {{ flex: 1 1 auto; }}
  }}
</style>
<div id="validation-panel">
  <h4>Validation scheme</h4>
  <div class="vp-toggle">
    <button type="button" class="vp-btn" id="vp-btn-random" aria-pressed="true">Random 5-fold</button>
    <button type="button" class="vp-btn" id="vp-btn-spatial" aria-pressed="false">Spatial block</button>
  </div>
  <div class="vp-auc"><span class="vp-auc-label">Random AUC</span><span class="vp-auc-value">{auc_random:.3f}</span></div>
  <div class="vp-auc"><span class="vp-auc-label">Spatial-block AUC</span><span class="vp-auc-value">{auc_spatial:.3f}</span></div>
</div>
<script>
(function() {{
  function whenReady(fn) {{
    if (window.{map_var} && window.{fg_random_var} && window.{fg_spatial_var}) {{ fn(); }}
    else {{ setTimeout(function() {{ whenReady(fn); }}, 50); }}
  }}
  whenReady(function() {{
    var map = window.{map_var};
    var fgRandom = window.{fg_random_var};
    var fgSpatial = window.{fg_spatial_var};
    map.removeLayer(fgSpatial);  // random scheme visible by default
    var btnRandom = document.getElementById('vp-btn-random');
    var btnSpatial = document.getElementById('vp-btn-spatial');
    function showRandom() {{
      if (!map.hasLayer(fgRandom)) map.addLayer(fgRandom);
      if (map.hasLayer(fgSpatial)) map.removeLayer(fgSpatial);
      btnRandom.setAttribute('aria-pressed', 'true');
      btnSpatial.setAttribute('aria-pressed', 'false');
    }}
    function showSpatial() {{
      if (!map.hasLayer(fgSpatial)) map.addLayer(fgSpatial);
      if (map.hasLayer(fgRandom)) map.removeLayer(fgRandom);
      btnSpatial.setAttribute('aria-pressed', 'true');
      btnRandom.setAttribute('aria-pressed', 'false');
    }}
    btnRandom.addEventListener('click', showRandom);
    btnSpatial.addEventListener('click', showSpatial);
  }});
}})();
</script>
"""


def main():
    rng = np.random.default_rng(RNG_SEED)
    lat, lon, y, blob_id = make_synthetic_points(rng)
    X = build_features(lat, lon)

    rand_fold = random_folds(len(y), N_SPLITS, rng)
    spatial_fold = spatial_block_folds(lat, lon, N_SPLITS)

    _, auc_random = run_cv(X, y, rand_fold, N_SPLITS)
    _, auc_spatial = run_cv(X, y, spatial_fold, N_SPLITS)

    print(f"Random 5-fold AUC:        {auc_random:.3f}")
    print(f"Spatial-block 5-fold AUC: {auc_spatial:.3f}")
    print(f"Gap:                      {auc_random - auc_spatial:.3f}")

    m = folium.Map(
        location=[CENTER_LAT, CENTER_LON],
        zoom_start=8,
        tiles=None,
        control_scale=False,
    )
    folium.TileLayer(tiles=TILE_URL, attr=TILE_ATTR, name="CARTO Positron", control=False).add_to(m)

    fg_random = folium.FeatureGroup(name="Random 5-fold", show=True)
    fg_spatial = folium.FeatureGroup(name="Spatial block 5-fold", show=False)

    for lat_i, lon_i, fold_i in zip(lat, lon, rand_fold):
        folium.CircleMarker(
            location=[lat_i, lon_i],
            radius=4,
            color=FOLD_COLORS[fold_i],
            fill=True,
            fill_color=FOLD_COLORS[fold_i],
            fill_opacity=0.85,
            weight=1,
        ).add_to(fg_random)

    for lat_i, lon_i, fold_i in zip(lat, lon, spatial_fold):
        folium.CircleMarker(
            location=[lat_i, lon_i],
            radius=4,
            color=FOLD_COLORS[fold_i],
            fill=True,
            fill_color=FOLD_COLORS[fold_i],
            fill_opacity=0.85,
            weight=1,
        ).add_to(fg_spatial)

    fg_random.add_to(m)
    fg_spatial.add_to(m)

    panel_html = build_toggle_and_auc_html(
        auc_random, auc_spatial,
        map_var=m.get_name(),
        fg_random_var=fg_random.get_name(),
        fg_spatial_var=fg_spatial.get_name(),
    )
    m.get_root().html.add_child(folium.Element(panel_html))

    html = m.get_root().render()
    html = rewrite_cdn_to_local(html)

    vendor_leaflet()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")

    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
