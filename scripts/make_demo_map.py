#!/usr/bin/env python3
"""Build the spatial cross-validation demo map embedded on the homepage.

The point of the demo: on spatially autocorrelated data, random k-fold CV
reports a much better score than it should, because randomly scattered folds
put a held-out point's neighbours in the training set. Contiguous spatial
blocks do not, so they report the score you would actually get somewhere new.

Everything here is synthetic. No study data, no downloads beyond a one-time
fetch of Leaflet into demos/vendor/, no API keys. The seed is pinned, so two
runs produce a byte-identical file.

    py scripts/make_demo_map.py

Writes demos/spatial-cv-demo.html and prints both AUCs and the file size.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

import folium
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold

SEED = 42
N_POINTS = 300
N_FOLDS = 5

# Generic land rectangle near 27.7 N, 85.3 E — roughly 30 x 22 km. It is a
# stand-in for "a study area", not a claim about anywhere in particular.
LON_MIN, LON_MAX = 85.15, 85.45
LAT_MIN, LAT_MAX = 27.62, 27.82

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "demos" / "spatial-cv-demo.html"
VENDOR = REPO / "demos" / "vendor"

LEAFLET_VERSION = "1.9.4"
_LEAFLET_CDN = f"https://cdn.jsdelivr.net/npm/leaflet@{LEAFLET_VERSION}/dist"
LEAFLET_FILES = {
    "leaflet.js": f"{_LEAFLET_CDN}/leaflet.js",
    "leaflet.css": f"{_LEAFLET_CDN}/leaflet.css",
    # leaflet.css references these relatively. Nothing here should render them
    # (CircleMarker, not Marker; the layer control is expanded, so its toggle
    # icon stays hidden) but vendoring them keeps a stray 404 off the console.
    "images/layers.png": f"{_LEAFLET_CDN}/images/layers.png",
    "images/layers-2x.png": f"{_LEAFLET_CDN}/images/layers-2x.png",
    "images/marker-icon.png": f"{_LEAFLET_CDN}/images/marker-icon.png",
}

# Five hues that stay distinguishable as 5px dots on CartoDB Positron and
# survive the common colour-vision deficiencies (Okabe-Ito, minus the pale
# yellow, which disappears on a light basemap).
FOLD_COLORS = ["#0072b2", "#d55e00", "#009e73", "#cc79a7", "#56505f"]

# Correlation ranges in degrees. ~0.01 deg is ~1.1 km here.
COVARIATE_RANGES = (0.10, 0.06, 0.03, 0.015)
LATENT_RANGE = 0.05

# How strongly each observed covariate drives the label, and how strongly the
# unobserved spatial field does. The latent term is the whole mechanism: it is
# real signal the model can only reach by recognising a neighbourhood.
BETAS = np.array([1.1, -0.9, 0.7, 0.5])
LATENT_WEIGHT = 2.6
NOISE_WEIGHT = 0.6


def gaussian_random_field(coords: np.ndarray, rng: np.random.Generator,
                          length_scale: float) -> np.ndarray:
    """Draw one spatially autocorrelated field over `coords`.

    Exponential covariance, exp(-d / length_scale), factored with Cholesky and
    multiplied by white noise. This is the textbook construction; at 300 points
    the 300x300 factorisation is instant.
    """
    d = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    cov = np.exp(-d / length_scale)
    cov[np.diag_indices_from(cov)] += 1e-8   # keep it positive definite
    field = np.linalg.cholesky(cov) @ rng.standard_normal(len(coords))
    return (field - field.mean()) / field.std()


def make_data(rng: np.random.Generator):
    """Synthetic points, covariates and labels with real spatial structure."""
    coords = np.column_stack([
        rng.uniform(LON_MIN, LON_MAX, N_POINTS),
        rng.uniform(LAT_MIN, LAT_MAX, N_POINTS),
    ])

    # Four observed covariates — think elevation, slope, distance to a river,
    # rainfall: each smooth in space, at a different scale.
    X = np.column_stack([
        gaussian_random_field(coords, rng, r) for r in COVARIATE_RANGES
    ])

    # A fifth field that is NEVER shown to the model. Because it is smooth in
    # space, a point's neighbours carry most of its value — which is exactly
    # what random folds leak across the split and spatial blocks do not.
    latent = gaussian_random_field(coords, rng, LATENT_RANGE)

    logit = X @ BETAS + LATENT_WEIGHT * latent
    logit += NOISE_WEIGHT * rng.standard_normal(N_POINTS)
    y = (rng.uniform(size=N_POINTS) < 1.0 / (1.0 + np.exp(-logit))).astype(int)
    return coords, X, y


def cv_auc(X: np.ndarray, y: np.ndarray, folds: np.ndarray) -> tuple[float, float]:
    """Mean and sd of held-out AUC over the given fold assignment."""
    scores = []
    for f in np.unique(folds):
        test = folds == f
        model = RandomForestClassifier(n_estimators=300, random_state=SEED)
        model.fit(X[~test], y[~test])
        proba = model.predict_proba(X[test])[:, 1]
        scores.append(roc_auc_score(y[test], proba))
    return float(np.mean(scores)), float(np.std(scores))


def assign_folds(coords: np.ndarray, rng_seed: int):
    """Both fold layouts over the same points."""
    random_folds = np.empty(N_POINTS, dtype=int)
    kf = KFold(n_splits=N_FOLDS, shuffle=True, random_state=rng_seed)
    for i, (_, test) in enumerate(kf.split(coords)):
        random_folds[test] = i

    # KMeans on the coordinates gives five contiguous Voronoi regions tiling
    # the study area — contiguous blocks, which is what "spatial CV" means.
    spatial_folds = KMeans(
        n_clusters=N_FOLDS, random_state=rng_seed, n_init=10
    ).fit_predict(coords)

    return random_folds, spatial_folds


def fetch_leaflet() -> None:
    """Download Leaflet into demos/vendor/ once, so the demo makes no CDN calls."""
    for name, url in LEAFLET_FILES.items():
        target = VENDOR / name
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"  fetching {name} from {url}")
        with urllib.request.urlopen(url) as response:
            target.write_bytes(response.read())


def point_collection(coords: np.ndarray, folds: np.ndarray) -> dict:
    """One GeoJSON FeatureCollection — far smaller than 300 CircleMarker objects.

    Coordinates are rounded to 5 decimals (~1 m), and fold is the only property.
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(float(lon), 5), round(float(lat), 5)],
                },
                "properties": {"fold": int(fold)},
            }
            for (lon, lat), fold in zip(coords, folds)
        ],
    }


def add_layer(m: folium.Map, name: str, data: dict, show: bool) -> None:
    group = folium.FeatureGroup(name=name, show=show)
    folium.GeoJson(
        data,
        marker=folium.CircleMarker(
            radius=5, weight=1, color="#ffffff", fill=True, fill_opacity=0.95
        ),
        style_function=lambda feat: {
            "fillColor": FOLD_COLORS[feat["properties"]["fold"]],
            "color": "#ffffff",
        },
        tooltip=folium.GeoJsonTooltip(fields=["fold"], aliases=["Fold"]),
    ).add_to(group)
    group.add_to(m)


def legend_html(random_auc, random_sd, spatial_auc, spatial_sd) -> str:
    """The AUC card. Inline styles only, using the site's own type and colours."""
    swatches = "".join(
        f'<span style="display:inline-block;width:11px;height:11px;border-radius:50%;'
        f'background:{c};margin-right:4px;vertical-align:-1px"></span>'
        for c in FOLD_COLORS
    )
    return f"""
<div id="auc-card" style="
     position:absolute; bottom:12px; left:10px; z-index:9999;
     max-width:16rem; padding:.7rem .8rem;
     background:rgba(255,255,255,.95); border:1px solid #cfd6dd; border-radius:3px;
     box-shadow:0 1px 3px rgba(0,0,0,.12);
     font:400 12px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,
          'Helvetica Neue',Arial,'Noto Sans',sans-serif; color:#1a1a1a;">
  <div style="font-weight:700;text-transform:uppercase;letter-spacing:.08em;
              font-size:10px;color:#253a6e;border-bottom:1px solid #e5e8ec;
              padding-bottom:.35rem;margin-bottom:.45rem;">
    Mean AUC, {N_FOLDS}-fold
    <span style="display:block;width:2rem;height:2px;background:#0489c2;
                 margin-top:.35rem;"></span>
  </div>
  <div style="display:flex;justify-content:space-between;gap:.75rem;">
    <span>Random folds</span>
    <strong>{random_auc:.2f} <span style="font-weight:400;color:#5f6a78;">&plusmn;{random_sd:.2f}</span></strong>
  </div>
  <div style="display:flex;justify-content:space-between;gap:.75rem;margin-top:.15rem;">
    <span>Spatial blocks</span>
    <strong>{spatial_auc:.2f} <span style="font-weight:400;color:#5f6a78;">&plusmn;{spatial_sd:.2f}</span></strong>
  </div>
  <div style="margin-top:.5rem;padding-top:.45rem;border-top:1px solid #e5e8ec;
              color:#5f6a78;">
    {swatches}<br>
    Same {N_POINTS} synthetic points, same model &mdash; only the folds differ.
    Use the layer control to switch.
  </div>
</div>
"""


def stabilise_ids(html: str) -> str:
    """Replace folium's random UUID element ids with sequential ones.

    branca names every element `map_<uuid4().hex>`, and uuid4 draws from
    os.urandom, so it cannot be seeded. Without this, regenerating the demo
    rewrites every id and the git diff buries whatever actually changed.
    """
    seen: dict[str, str] = {}

    def rename(match: re.Match) -> str:
        uuid_hex = match.group(1)
        if uuid_hex not in seen:
            seen[uuid_hex] = f"{len(seen) + 1:04d}"
        return "_" + seen[uuid_hex]

    # Anchored on the underscore rather than the owning name, so ids that carry
    # a suffix (geo_json_<uuid>_styler) are rewritten too.
    return re.sub(r"_([0-9a-f]{32})(?![0-9a-f])", rename, html)


def localise_assets(html: str) -> str:
    """Point Leaflet at demos/vendor/ and drop every other CDN tag.

    Folium's template also pulls jQuery, Bootstrap, glyphicons, Font Awesome and
    leaflet.awesome-markers. None are needed here — LayerControl, CircleMarker
    and GeoJsonTooltip are all pure Leaflet — so they go, which removes every
    remaining third-party request except the basemap tiles.
    """
    html = re.sub(
        r'<script[^>]+src="[^"]*leaflet@[^"]*/dist/leaflet\.js"[^>]*></script>',
        '<script src="vendor/leaflet.js"></script>',
        html,
    )
    html = re.sub(
        r'<link[^>]+href="[^"]*leaflet@[^"]*/dist/leaflet\.css"[^>]*/?>',
        '<link rel="stylesheet" href="vendor/leaflet.css"/>',
        html,
    )
    # Anything still pointing off-site, except the Leaflet tags just rewritten.
    html = re.sub(
        r'\s*<(?:script|link)[^>]*(?:src|href)="https?://(?!vendor)[^"]*"[^>]*'
        r'(?:></script>|/?>)',
        "",
        html,
    )

    # Folium hard-codes user-scalable=no, which fails WCAG 1.4.4 for anyone who
    # opens the demo full screen. Leaflet handles pinch on the map itself, so
    # letting the page zoom costs nothing.
    html = html.replace(
        'content="width=device-width,\n                initial-scale=1.0, '
        'maximum-scale=1.0, user-scalable=no"',
        'content="width=device-width, initial-scale=1.0"',
    )

    html = html.replace("<html>", '<html lang="en">', 1)
    html = stabilise_ids(html)
    html = html.replace(
        "<head>",
        "<head>\n    <title>Random vs. spatial cross-validation "
        "&mdash; synthetic demo</title>",
        1,
    )
    return html


def main() -> None:
    rng = np.random.default_rng(SEED)

    coords, X, y = make_data(rng)
    random_folds, spatial_folds = assign_folds(coords, SEED)

    random_auc, random_sd = cv_auc(X, y, random_folds)
    spatial_auc, spatial_sd = cv_auc(X, y, spatial_folds)
    gap = random_auc - spatial_auc

    print(f"  points            {N_POINTS}   positives {int(y.sum())}")
    print(f"  random {N_FOLDS}-fold AUC   {random_auc:.3f} +/- {random_sd:.3f}")
    print(f"  spatial block AUC   {spatial_auc:.3f} +/- {spatial_sd:.3f}")
    print(f"  optimism (gap)      {gap:+.3f}")
    if gap < 0.05:
        print("  WARNING: the gap is too small to read on a map. Widen "
              "LATENT_RANGE or raise LATENT_WEIGHT -- do not touch the scoring.")

    fetch_leaflet()

    m = folium.Map(
        location=[(LAT_MIN + LAT_MAX) / 2, (LON_MIN + LON_MAX) / 2],
        zoom_start=11,
        tiles="CartoDB positron",
        scrollWheelZoom=False,   # the page must stay scrollable over the map
        control_scale=False,
    )
    add_layer(m, f"Random {N_FOLDS}-fold", point_collection(coords, random_folds), show=True)
    add_layer(m, f"Spatial block {N_FOLDS}-fold", point_collection(coords, spatial_folds), show=False)
    folium.LayerControl(collapsed=False).add_to(m)

    m.get_root().html.add_child(folium.Element(
        legend_html(random_auc, random_sd, spatial_auc, spatial_sd)
    ))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(localise_assets(m.get_root().render()), encoding="utf-8")

    size = OUT.stat().st_size
    print(f"  wrote {OUT.relative_to(REPO).as_posix()}  {size / 1024:.1f} KB")
    if size > 3 * 1024 * 1024:
        print("  WARNING: over the 3 MB budget -- reduce N_POINTS.")


if __name__ == "__main__":
    main()
