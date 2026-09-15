/* =========================================================================
   Golam Murad — personal site
   Vanilla JS, no dependencies, no build step.

   TO ADD A NEWS ITEM        add one object to the NEWS array below.
   TO ADD A PUBLICATION      add one object to the PUBLICATIONS array below.

   The page must also read correctly with JavaScript disabled, so index.html
   carries a <noscript> copy of both lists. If you add an entry here, add a
   matching line to the <noscript> block in index.html. See README.md.
   ========================================================================= */

/* ===========================================================================
   NEWS — newest first. `date` is the label shown on the left.
   =========================================================================== */

const NEWS = [
  {
    date: 'Aug 2026',
    html: 'Started my PhD in River-Coastal Science and Engineering at Tulane University, ' +
          'joining the Hydroinformatics Lab as a Graduate Research Assistant.'
  },
  {
    date: 'Jun 2026',
    html: 'Our paper on stochastic physics-informed neural networks for consolidation ' +
          'parameter estimation was accepted at <a href="#publications">APMCE 2026</a> (IEB, Dhaka).'
  },
  {
    date: '2026',
    html: 'Preprint on spatial sparsity-aware explainable deep learning for landslide ' +
          'susceptibility mapping posted to ' +
          '<a href="https://doi.org/10.31223/X52J42" rel="noopener">EarthArXiv</a>; ' +
          'under review at Canadian Geotechnical Journal.'
  },
  {
    date: '2026',
    html: 'Preprint on uncertainty-aware Bayesian machine learning for landslide susceptibility ' +
          'in the Chattogram metropolitan hill system posted to ' +
          '<a href="https://doi.org/10.31223/X55J40" rel="noopener">EarthArXiv</a>.'
  },
  {
    date: '2026',
    html: 'Paper on machine learning and explainable AI for vegetation dynamics under review ' +
          'at Environmental Monitoring and Assessment.'
  },
  {
    date: 'Dec 2025',
    html: 'Presented our landslide inventory and hotspot analysis of the Chittagong Hill Tracts ' +
          'at ICCERI 2025, RUET, Rajshahi.'
  },
  {
    date: 'Dec 2025',
    html: 'Joined Soil Profile as a Research Engineer, working on landslide and liquefaction ' +
          'assessment for the Chittagong Metropolitan Area.'
  },
  {
    date: 'Jul 2025',
    html: 'Completed my B.Sc. in Civil Engineering at Chittagong University of Engineering &amp; Technology.'
  },
  {
    date: '2025',
    html: 'Presented deep learning-based landslide susceptibility assessment of Rangamati Hill ' +
          'District at ICERIE 2025, SUST, Sylhet.'
  },
  {
    date: 'Dec 2024',
    html: 'Industrial internship at the Bangladesh Water Development Board.'
  }
];

const NEWS_VISIBLE = 6;   // how many entries show before "Show more"

/* ===========================================================================
   PUBLICATIONS — newest first; grouped by `year` automatically.

   One object per paper:
     year      number, used for grouping
     title     string
     authors   array of names, exactly as published. Use ME for your own name
               so it renders bold.
     venue     string
     status    optional — 'Preprint', 'Under review at X', 'Accepted at X'
     teaser    optional — path to a figure, e.g. 'assets/img/teasers/foo.webp'.
               Leave null for a placeholder box.
     teaserAlt alt text for the teaser; required whenever `teaser` is set.
     links     optional — { paper, code, doi, arxiv, slides, ... }
     abstract  optional string
     bibtex    optional string
   =========================================================================== */

const ME = 'Golam Murad';

const PUBLICATIONS = [
  {
    year: 2026,
    title: 'Spatial Sparsity-Aware Explainable Deep Learning-Based Landslide Susceptibility ' +
           'Mapping: Application to a Hill District, Bangladesh',
    authors: [ME, 'Md. Aftabur Rahman', 'Hideaki Yasuhara'],
    venue: 'EarthArXiv preprint',
    status: 'Under review at Canadian Geotechnical Journal',
    teaser: 'assets/img/teasers/sparsity-aware-lsm-rangamati-2026.jpg',
    teaserAlt: 'Spatial sparsity-aware landslide susceptibility mapping figure for Rangamati, Bangladesh.',
    links: {
      paper: 'assets/papers/sparsity-aware-lsm-rangamati-2026.pdf',
      doi: 'https://doi.org/10.31223/X52J42',
      code: 'https://github.com/murad-geoAi/DL_Application_for_Landslide_Susceptibility_Mapping'
    },
    abstract:
      'Landslide susceptibility mapping is a critical disaster risk management tool in mountainous ' +
      'regions, particularly in developing countries and in regions where development is ongoing or ' +
      'planned. This research introduces an approach that addresses the persistent challenge of spatial ' +
      'sparsity in landslide datasets, where strong monitoring of hill slopes is seldom available. The ' +
      'framework first quantifies spatial sparsity through Voronoi-based clustering and spatial ' +
      'autocorrelation metrics (Getis-Ord Gi* and Moran’s I), then implements sparsity mitigation ' +
      'using DBSCAN clustering and spatial density analysis. Twelve landslide conditioning factors ' +
      'derived from remote sensing data are examined, spanning topographic, hydrological and ' +
      'environmental variables. Three deep learning architectures — DNN, 1D-CNN and LSTM — ' +
      'are implemented on both the original and sparsity-mitigated datasets for Rangamati, the largest ' +
      'district of Bangladesh and part of the Chittagong Hill Tracts. The 1D-CNN applied to the ' +
      'sparsity-free dataset achieved an AUC of 0.9625, accuracy of 0.89, precision of 0.914 and an ' +
      'F1-score of 0.853. SHAP analysis provides insight into feature importance, demonstrating the ' +
      'contribution of spatial context features. The study shows that addressing spatial sparsity before ' +
      'applying deep learning substantially improves prediction reliability, while XAI techniques keep ' +
      'the model transparent enough for operational use in disaster risk management.',
    bibtex:
`@article{murad2026sparsity,
  title   = {Spatial Sparsity-Aware Explainable Deep Learning-Based Landslide
             Susceptibility Mapping: Application to a Hill District, Bangladesh},
  author  = {Murad, Golam and Rahman, Md. Aftabur and Yasuhara, Hideaki},
  journal = {EarthArXiv preprint},
  year    = {2026},
  doi     = {10.31223/X52J42},
  note    = {Under review at Canadian Geotechnical Journal}
}`
  },

  {
    year: 2026,
    title: 'Uncertainty-Aware Bayesian Machine Learning for Landslide Susceptibility Mapping in ' +
           'the Chattogram Metropolitan Hill System, Bangladesh',
    authors: [ME, 'Shotabdy Chowdhury Srabony', 'Shafiq Mahmud', 'Md. Aftabur Rahman'],
    venue: 'EarthArXiv preprint',
    status: 'Preprint',
    teaser: 'assets/img/teasers/bayesian-lsm-chattogram-2026.jpg',
    teaserAlt: 'Bayesian machine learning landslide susceptibility mapping figure for Chattogram, Bangladesh.',
    links: {
      paper: 'assets/papers/bayesian-lsm-chattogram-2026.pdf',
      doi: 'https://doi.org/10.31223/X55J40',
      code: 'https://github.com/murad-geoAi/LSM_ChittagongMetropolitonArea'
    },
    abstract:
      'Landslide-prone hilly regions experiencing rapid urban expansion need susceptibility models ' +
      'that provide both robust predictive performance and transparent uncertainty estimates. This ' +
      'study develops an uncertainty-aware probabilistic framework for landslide susceptibility mapping ' +
      'in Bangladesh’s Chattogram metropolitan hill system, incorporating 14 geomorphological, ' +
      'hydrological, environmental and anthropogenic conditioning factors. Multicollinearity analysis ' +
      '(VIF and tolerance) verified the statistical stability of the predictors. Four classifiers were ' +
      'compared within a standardized preprocessing pipeline — Bayesian logistic regression, ' +
      'Gaussian process classifier, L2-regularized logistic regression and random forest — and ' +
      'evaluated using cross-validation, holdout testing and spatial block validation. Random forest ' +
      'gave the strongest discrimination (ROC-AUC = 0.866; MCC = 0.611) on the holdout set, while the ' +
      'Gaussian process classifier showed better probability calibration (ECE = 0.084) with competitive ' +
      'discrimination (ROC-AUC = 0.821). Susceptibility and uncertainty were combined in a 3×3 ' +
      'scheme to visualize hazard alongside confidence: 78.71% of landslides fell in the Very High ' +
      'class, covering only 9.47% of the area (SCAI = 0.12).',
    bibtex:
`@article{murad2026bayesian,
  title   = {Uncertainty-Aware Bayesian Machine Learning for Landslide Susceptibility
             Mapping in the Chattogram Metropolitan Hill System, Bangladesh},
  author  = {Murad, Golam and Srabony, Shotabdy Chowdhury and Mahmud, Shafiq
             and Rahman, Md. Aftabur},
  journal = {EarthArXiv preprint},
  year    = {2026},
  doi     = {10.31223/X55J40}
}`
  },

  {
    year: 2026,
    title: 'Advanced Machine Learning and Explainable AI for Predicting Vegetation Dynamics: ' +
           'A Case Study for Chittagong Division, Bangladesh',
    authors: [ME, 'Md. Aftabur Rahman', 'S. Das'],
    venue: 'Environmental Monitoring and Assessment',
    status: 'Under review at Environmental Monitoring and Assessment',
    teaser: 'assets/img/teasers/vegetation-dynamics-xai-2026.jpg',
    teaserAlt: 'Explainable AI deep neural network figure for NDVI vegetation dynamics prediction, Chittagong Division, Bangladesh.',
    links: {
      code: 'https://github.com/murad-geoAi/Soft_Computing_for_NDVI_Prediction'
    },
    // No manuscript PDF available yet — abstract omitted rather than invented.
    abstract: null,
    bibtex:
`@unpublished{murad2026vegetation,
  title  = {Advanced Machine Learning and Explainable AI for Predicting Vegetation
            Dynamics: A Case Study for Chittagong Division, Bangladesh},
  author = {Murad, Golam and Rahman, Md. Aftabur and Das, S.},
  year   = {2026},
  note   = {Under review at Environmental Monitoring and Assessment}
}`
  },

  {
    year: 2026,
    title: 'Stochastic Physics-Informed Neural Network with MC Dropout for Estimating ' +
           'Consolidation Parameters',
    authors: [ME, 'Shotabdy Chowdhury Srabony', 'Debajit Das Gupta', 'Md. Aftabur Rahman'],
    venue: '6th Annual Paper Meet of the Civil Engineering Division, Institution of Engineers, ' +
           'Bangladesh (APMCE 2026), Dhaka',
    status: 'Accepted at APMCE 2026',
    teaser: 'assets/img/teasers/stochastic-pinn-consolidation-apmce-2026.jpg',
    teaserAlt: 'Stochastic physics-informed neural network for consolidation parameter estimation figure.',
    links: {
      paper: 'assets/papers/stochastic-pinn-consolidation-apmce-2026.pdf'
    },
    abstract:
      'Reliable estimation of the coefficient of consolidation is essential for settlement prediction, ' +
      'pore-pressure dissipation analysis and staged construction planning in soft ground engineering. ' +
      'Conventional oedometer-based methods and inverse back-analysis are costly, time-consuming and ' +
      'difficult to update when only sparse field measurements are available. This study develops a ' +
      'stochastic physics-informed neural network that embeds Terzaghi’s one-dimensional ' +
      'consolidation equation into the training loss and integrates Monte Carlo dropout for uncertainty ' +
      'quantification. The model estimates the coefficient of consolidation from only 50 synthetic ' +
      'sensor readings with added Gaussian noise, representing field-like monitoring constraints. The ' +
      'inverse PINN recovered the consolidation coefficient with high accuracy (1.2093 against a true ' +
      'value of 1.20; relative error 0.78%). Evaluation on a dense spatiotemporal grid yielded an MSE ' +
      'of 0.0088, RMSE of 0.0938 and MAE of 0.0679, and the Monte Carlo dropout intervals achieved ' +
      '94.67% coverage for nominal 95% bounds, indicating well-calibrated predictive uncertainty. The ' +
      'framework is a step toward GeoAI-assisted geotechnical monitoring and digital twin systems for ' +
      'soft ground engineering.',
    bibtex:
`@inproceedings{murad2026pinn,
  title     = {Stochastic Physics-Informed Neural Network with MC Dropout for
               Estimating Consolidation Parameters},
  author    = {Murad, Golam and Srabony, Shotabdy Chowdhury and Gupta, Debajit Das
               and Rahman, Md. Aftabur},
  booktitle = {Proceedings of the 6th Annual Paper Meet of the Civil Engineering
               Division, Institution of Engineers, Bangladesh (APMCE 2026)},
  address   = {Dhaka, Bangladesh},
  year      = {2026}
}`
  },

  {
    year: 2026,
    title: 'Enhancing the Generalization of Flood Susceptibility Models: A Leakage-Aware ' +
           'Ensemble Framework for Deltaic Landscapes',
    authors: ['Shafiq Mahmud', ME, 'Md. Aftabur Rahman'],
    venue: 'EarthArXiv preprint',
    status: 'Preprint',
    teaser: 'assets/img/teasers/leakage-aware-flood-susceptibility-2026.jpg',
    teaserAlt: 'Leakage-aware ensemble flood susceptibility mapping figure for the Greater Noakhali region, Bangladesh.',
    links: {
      paper: 'assets/papers/leakage-aware-flood-susceptibility-2026.pdf',
      code: 'https://github.com/murad-geoAi/ml_flood_susceptibility_mapping'
    },
    abstract:
      'Flood susceptibility mapping is a cornerstone of disaster risk reduction in low-lying deltaic ' +
      'regions, yet conventional machine learning applications frequently suffer from spatial data ' +
      'leakage, producing inflated performance metrics and unreliable hazard predictions. This study ' +
      'develops a leakage-aware machine learning framework for the Greater Noakhali region of ' +
      'Bangladesh. Using a flood inventory derived from Sentinel-1 SAR imagery of the catastrophic ' +
      'August 2024 event, twelve spatially explicit topographic, hydrological and anthropogenic ' +
      'conditioning factors were integrated, and eight ensemble algorithms were evaluated under a ' +
      '10-fold blocked spatial cross-validation strategy. The spatially constrained evaluation gave ' +
      'realistic performance estimates in contrast to the optimistic ROC-AUC values typical of random ' +
      'splits, with random forest showing the highest generalization (ROC-AUC = 0.627) and XGBoost the ' +
      'best precision-recall balance (F1 = 0.451). SHAP analysis identified land use, vegetation ' +
      'density (NDVI) and drainage density as the primary drivers of flood susceptibility in this ' +
      'coastal tract.',
    bibtex:
`@article{mahmud2026flood,
  title   = {Enhancing the Generalization of Flood Susceptibility Models: A
             Leakage-Aware Ensemble Framework for Deltaic Landscapes},
  author  = {Mahmud, Shafiq and Murad, Golam and Rahman, Md. Aftabur},
  journal = {EarthArXiv preprint},
  year    = {2026}
}`
  },

  {
    year: 2025,
    title: 'Comprehensive Landslide Inventory and Hotspot Analysis in the Chittagong Hill Tracts ' +
           'of Southeastern Bangladesh',
    authors: [ME, 'Nawrin Nawar', 'Hamim Ashrafi', 'Debajit Das Gupta', 'Md. Aftabur Rahman'],
    venue: 'International Conference on Civil Engineering Research &amp; Innovations (ICCERI 2025), ' +
           'RUET, Rajshahi, Bangladesh',
    status: null,
    teaser: 'assets/img/teasers/landslide-inventory-hotspot-icceri-2025.jpg',
    teaserAlt: 'Landslide inventory and hotspot analysis map of the Chittagong Hill Tracts, Bangladesh.',
    links: {
      paper: 'assets/papers/landslide-inventory-hotspot-icceri-2025.pdf'
    },
    abstract:
      'The Chittagong Hill Tracts of southeastern Bangladesh — the districts of Chittagong, ' +
      'Rangamati, Bandarban, Cox’s Bazar and Khagrachari — are acutely vulnerable to ' +
      'landslides due to rugged topography, intense precipitation and anthropogenic disturbances such ' +
      'as deforestation and unregulated hill cutting. This study develops a comprehensive landslide ' +
      'inventory map of 1,005 documented occurrences, integrating NASA’s global landslide ' +
      'inventory, peer-reviewed literature, field reports and UAV drone surveys. Using Getis-Ord Gi* ' +
      'within a GIS environment, the analysis delineates landslide hotspots and cold spots, revealing ' +
      'critical spatial heterogeneity in landslide distribution and indicating where field survey ' +
      'effort should be concentrated to collect further inventory points. The outputs support disaster ' +
      'risk reduction strategies, land-use regulation and resilient infrastructure planning in this ' +
      'high-risk region.',
    bibtex:
`@inproceedings{murad2025inventory,
  title     = {Comprehensive Landslide Inventory and Hotspot Analysis in the
               Chittagong Hill Tracts of Southeastern Bangladesh},
  author    = {Murad, Golam and Nawar, Nawrin and Ashrafi, Hamim and
               Gupta, Debajit Das and Rahman, Md. Aftabur},
  booktitle = {Proceedings of the International Conference on Civil Engineering
               Research and Innovations (ICCERI 2025)},
  address   = {Rajshahi, Bangladesh},
  year      = {2025}
}`
  },

  {
    year: 2025,
    title: 'Landslide Susceptibility Assessment of Rangamati Hill District Using Deep Learning Method',
    authors: [ME, 'Md. Aftabur Rahman'],
    venue: '8th International Conference on Engineering Research, Innovation and Education ' +
           '(ICERIE 2025), SUST, Sylhet, Bangladesh',
    status: null,
    teaser: 'assets/img/teasers/rangamati-dnn-lsm-icerie-2025.jpg',
    teaserAlt: 'Deep learning landslide susceptibility map of Rangamati Hill District, Bangladesh.',
    links: {
      paper: 'assets/papers/rangamati-dnn-lsm-icerie-2025.pdf',
      code: 'https://github.com/murad-geoAi/DL_Application_for_Landslide_Susceptibility_Mapping'
    },
    abstract:
      'Landslides are a major geological hazard in mountainous regions, and with roughly 10% of the ' +
      'land area of Bangladesh being hilly terrain, landslide-induced disasters are prominent there ' +
      'as well. As urbanization pushes development into hilly areas, susceptible regions need to be ' +
      'identified for safe and economical growth. This research develops a landslide susceptibility ' +
      'map for Rangamati district in the Chittagong Hill Tracts. Geologic and geotechnical parameters ' +
      'extracted through remote sensing form the initial dataset, and NASA landslide inventory maps ' +
      'are used to prepare synthesized datasets for validation. A deep neural network trained on 80% ' +
      'of the data and tested on the remaining 20% produced a susceptibility map with an accuracy of ' +
      '88% in terms of its statistical distribution, and the inventory map converges well with the ' +
      'susceptibility map, substantiating the developed procedure.',
    bibtex:
`@inproceedings{murad2025rangamati,
  title     = {Landslide Susceptibility Assessment of Rangamati Hill District
               Using Deep Learning Method},
  author    = {Murad, Golam and Rahman, Md. Aftabur},
  booktitle = {Proceedings of the 8th International Conference on Engineering
               Research, Innovation and Education (ICERIE 2025)},
  address   = {Sylhet, Bangladesh},
  year      = {2025}
}`
  }
];

/* ===========================================================================
   Everything below is rendering and interaction. You should not need to edit it.
   =========================================================================== */

(function () {
  'use strict';

  /** Escape text destined for an HTML context. */
  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  let uid = 0;
  const nextId = (prefix) => prefix + '-' + (++uid);

  /* ------------------------------ news ------------------------------ */

  function renderNews() {
    const list = document.getElementById('news-list');
    const toggle = document.getElementById('news-toggle');
    if (!list) return;

    list.innerHTML = NEWS.map(function (item, i) {
      return '<li' + (i >= NEWS_VISIBLE ? ' class="news-extra" hidden' : '') + '>' +
               '<span class="news-date">' + esc(item.date) + '</span>' +
               '<span class="news-body">' + item.html + '</span>' +
             '</li>';
    }).join('');

    if (!toggle || NEWS.length <= NEWS_VISIBLE) return;

    toggle.hidden = false;
    toggle.addEventListener('click', function () {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      list.querySelectorAll('.news-extra').forEach(function (li) {
        li.hidden = expanded;
      });
      toggle.setAttribute('aria-expanded', String(!expanded));
      toggle.textContent = expanded ? 'Show more' : 'Show less';
    });
  }

  /* -------------------------- publications -------------------------- */

  function authorLine(authors) {
    return authors.map(function (name) {
      return name === ME
        ? '<span class="me">' + esc(name) + '</span>'
        : esc(name);
    }).join(', ');
  }

  function teaserMarkup(pub) {
    if (pub.teaser) {
      return '<img class="pub-teaser" src="' + esc(pub.teaser) + '" alt="' +
             esc(pub.teaserAlt || '') + '" loading="lazy" decoding="async">';
    }
    // No figure yet: a labelled box that keeps the layout final.
    return '<div class="pub-teaser is-placeholder" aria-hidden="true">Figure<br>coming soon</div>';
  }

  const LINK_LABELS = {
    paper:  'Paper',
    code:   'Code',
    doi:    'DOI',
    arxiv:  'arXiv',
    slides: 'Slides',
    poster: 'Poster',
    video:  'Video',
    data:   'Data'
  };

  function renderPublication(pub) {
    const absId = nextId('abstract');
    const bibId = nextId('bibtex');
    const parts = [];

    parts.push('<article class="pub" data-reveal>');
    parts.push(teaserMarkup(pub));
    parts.push('<div class="pub-body">');

    // Title links to the paper when there is one.
    const titleHtml = esc(pub.title);
    parts.push('<h3 class="pub-title">' +
      (pub.links && pub.links.paper
        ? '<a href="' + esc(pub.links.paper) + '">' + titleHtml + '</a>'
        : titleHtml) +
      '</h3>');

    parts.push('<p class="pub-authors">' + authorLine(pub.authors) + '</p>');

    // `venue` may contain entities such as &amp;, so it is not escaped here.
    parts.push('<p class="pub-venue">' + pub.venue + ', ' + pub.year +
      (pub.status ? '<span class="tag">' + esc(pub.status) + '</span>' : '') + '</p>');

    // Action row
    const actions = [];
    if (pub.links) {
      Object.keys(LINK_LABELS).forEach(function (key) {
        if (!pub.links[key]) return;
        const external = /^https?:/.test(pub.links[key]);
        actions.push('<a class="btn" href="' + esc(pub.links[key]) + '"' +
          (external ? ' rel="noopener"' : '') + '>' + LINK_LABELS[key] + '</a>');
      });
    }
    if (pub.abstract) {
      actions.push('<button type="button" class="btn js-toggle" aria-expanded="false" ' +
        'aria-controls="' + absId + '">Abstract</button>');
    }
    if (pub.bibtex) {
      actions.push('<button type="button" class="btn js-toggle" aria-expanded="false" ' +
        'aria-controls="' + bibId + '">BibTeX</button>');
    }
    if (actions.length) {
      parts.push('<div class="pub-actions">' + actions.join('') + '</div>');
    }

    if (pub.abstract) {
      parts.push('<div class="panel panel-abstract" id="' + absId + '" hidden>' +
        esc(pub.abstract) + '</div>');
    }
    if (pub.bibtex) {
      parts.push('<div class="panel panel-bibtex" id="' + bibId + '" hidden>' +
        '<button type="button" class="btn copy-btn">Copy</button>' +
        '<pre><code>' + esc(pub.bibtex) + '</code></pre></div>');
    }

    parts.push('</div></article>');
    return parts.join('');
  }

  function renderPublications() {
    const host = document.getElementById('publication-list');
    if (!host) return;

    // Group by year, newest first, preserving in-year order.
    const years = [];
    const byYear = {};
    PUBLICATIONS.forEach(function (pub) {
      if (!byYear[pub.year]) { byYear[pub.year] = []; years.push(pub.year); }
      byYear[pub.year].push(pub);
    });
    years.sort(function (a, b) { return b - a; });

    host.innerHTML = years.map(function (year) {
      return '<h3 class="pub-year">' + year + '</h3>' +
             byYear[year].map(renderPublication).join('');
    }).join('');
  }

  /* ----------------------- toggles and clipboard ----------------------- */

  function wireToggles() {
    document.addEventListener('click', function (ev) {
      const toggle = ev.target.closest('.js-toggle');
      if (toggle) {
        const panel = document.getElementById(toggle.getAttribute('aria-controls'));
        if (!panel) return;
        const open = toggle.getAttribute('aria-expanded') === 'true';
        panel.hidden = open;
        toggle.setAttribute('aria-expanded', String(!open));
        return;
      }

      const copy = ev.target.closest('.copy-btn');
      if (copy) {
        const code = copy.parentElement.querySelector('code');
        if (code) copyText(code.textContent, copy);
      }
    });
  }

  function copyText(text, button) {
    function done(ok) {
      button.textContent = ok ? 'Copied' : 'Press Ctrl+C';
      button.setAttribute('data-copied', String(ok));
      setTimeout(function () {
        button.textContent = 'Copy';
        button.removeAttribute('data-copied');
      }, 2000);
    }

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); },
                                              function () { done(fallbackCopy(text)); });
    } else {
      done(fallbackCopy(text));
    }
  }

  // execCommand path for file:// and other non-secure contexts.
  function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  /* --------------------------- scroll-spy nav --------------------------- */

  function wireNav() {
    const links = Array.prototype.slice.call(
      document.querySelectorAll('.site-nav a[href^="#"]'));
    if (!links.length) return;

    const sections = links
      .map(function (a) { return document.querySelector(a.getAttribute('href')); })
      .filter(Boolean);
    if (!sections.length) return;

    function setCurrent(id) {
      links.forEach(function (a) {
        if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }

    if (!('IntersectionObserver' in window)) return;

    const visible = new Set();
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) visible.add(entry.target.id);
        else visible.delete(entry.target.id);
      });
      // Highlight the topmost section currently in the reading band.
      for (let i = 0; i < sections.length; i++) {
        if (visible.has(sections[i].id)) { setCurrent(sections[i].id); return; }
      }
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ------------------------------ reveal ------------------------------ */

  function wireReveal() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) {
      // CSS hides [data-reveal] under .js; with no observer, show everything now.
      document.querySelectorAll('[data-reveal]').forEach(function (el) {
        el.classList.add('is-visible');
      });
      return;
    }

    // threshold 0: any sliver on screen counts, so a tall block can't stay hidden.
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0 });

    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ------------------------- GitHub star counts ------------------------- */

  function loadStars() {
    const spans = document.querySelectorAll('.stars[data-repo]');
    if (!spans.length) return;

    fetch('https://api.github.com/users/murad-geoAi/repos?per_page=100')
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (repos) {
        if (!Array.isArray(repos)) return;
        const stars = {};
        repos.forEach(function (r) { stars[r.name] = r.stargazers_count; });
        spans.forEach(function (span) {
          const n = stars[span.getAttribute('data-repo')];
          if (typeof n === 'number') span.textContent = '★ ' + n;
        });
      })
      // Rate-limited or offline: the cards simply show no star count.
      .catch(function () { /* no-op */ });
  }

  /* ------------------------------- init ------------------------------- */

  function init() {
    renderNews();
    renderPublications();
    wireToggles();
    wireNav();
    wireReveal();
    loadStars();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
