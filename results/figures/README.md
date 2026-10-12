# Reproducible ML diagnostic figures

The following four PNG files were **successfully regenerated and committed**
by a GitHub Actions run on 12 October 2026, using the frozen
sample-level result tables in `results/`.

| Figure file | Content |
| --- | --- |
| `roc_rolling_2016_2023.png` | ROC curves from out-of-time 2016–2023 predictions (n=584) |
| `calibration_rolling.png` | Calibration curves from 2016–2023 predictions |
| `roc_test_2024.png` | ROC curves from separately examined 2024 observations (n=76) |
| `shap_XGBoost_train_only.png` | Training-only XGBoost global SHAP importance summary |

To reproduce these figures from the existing result tables, run
`python src/plot_archived_ml_figures.py` at repository root after installing
the plotting dependencies. The GitHub Actions workflow
`.github/workflows/render-figures.yml` runs the same program.

**Important provenance distinction:** These plots are accurate renderings
from the archived result tables, **not byte-for-byte copies of the original
9 October 2026 images**. The original raster figures remain in the separate
author-reviewed upload ZIP; layout and styling may differ.

The 2024 data were inspected during prior model development and must not be
called an untouched independent holdout. SHAP importance indicates model
associations, not causal effects.
