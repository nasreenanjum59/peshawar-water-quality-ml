# Peshawar water-quality ML reanalysis

**Manuscript:** EW-ART-05-2026-000506, *Environmental Science: Water Research & Technology*  
**Contents:** analysis-ready dataset, reproducible ML code, archived model outputs and supporting documentation. GitHub is the primary distribution platform; no DOI has been assigned.  
**Analysis frozen:** 9 October 2026; repository documentation updated 12 October 2026

## Scope

This repository contains the Python analysis and archived outputs for the
machine-learning component of a retrospective water-quality study in Peshawar,
Pakistan (2009–2024). The machine-learning outcome is laboratory-measured
*E. coli* detection (presence vs absence), not a water-quality-index class.
Only tap and tube-well samples are used for ML (1,200 observations);
600 river-water observations are included in the workbook for the broader paper
but not for the ML prediction task.

The primary comparison uses **584 nested rolling-origin predictions from
2016–2023**. Earlier years are used for tuning and fitting; each evaluation
year is excluded from its own training. The 2024 observations (**n = 76**)
were examined during previous model development and are presented separately.
They are **not** an untouched independent external validation set.

## Files

- `src/peshawar_ml.py`: main analytical workflow, including model tuning,
  temporal validation, baselines, bootstrap intervals, sensitivity analyses
  and descriptive plots.
- `results/`: archived numerical outputs from 9 October 2026 and four diagnostic PNG
  figures regenerated from the frozen numerical tables. The regenerated figures
  are not byte-for-byte copies of the original images; see `results/figures/README.md`.
- `src/plot_archived_ml_figures.py`: regenerates the four figures from archived results.
- `tests/`: checks for temporal folds, decision thresholds and headline
  metrics in the archived outputs.
- `docs/METHODS.md`: model definitions, analysis choices and known limitations.
- `docs/UPLOAD_GUIDE.md`: straightforward instructions for obtaining the
  dataset, running the code and interpreting the analysis outputs.
- `docs/VALIDATION_REPORT.md`: recorded data-integrity and software-test results.
- `data/WQ_Peshawar_2009-2024_analysis_ready.xlsx`: analysis-ready workbook with
  1,800 observations, a data dictionary and analysis notes. This dataset includes
  collection dates, sampling-site names and laboratory register references.
  Consult `data/README.md` for data provenance and interpretation.

## Run the analysis

The original run used Python 3.9.13, NumPy 2.0.2, pandas 2.2.3,
scikit-learn 1.6.1 and XGBoost 2.1.4. See `results/00_versions.json` for
machine-readable run information. Package version changes, especially in
XGBoost, may produce different probabilities or metrics.

```bash
python -m venv .venv
# Activate .venv before proceeding.
python -m pip install -r requirements-recorded.txt
python src/peshawar_ml.py \
    --data data/WQ_Peshawar_2009-2024_analysis_ready.xlsx \
    --out runs/full --with-smote --with-shap --permutations 200
```

For a reduced **software smoke test only**, use `--quick --permutations 0`
and a separate output directory. Do not cite quick-mode statistics. Full
analyses may take substantial CPU time; the `--out` directory must not
already contain files. The script does not modify its input workbook. See `docs/VALIDATION_REPORT.md` for the packaging checks performed and limitations.

Before interpreting the deposited outputs, run the package and data-integrity checks:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

These checks confirm integrity and selected archived results. They do not replace
an independent complete scientific rerun in the recorded environment.

The supplied workbook has SHA-256:

`e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`

Check a local copy with `sha256sum data/WQ_Peshawar_2009-2024_analysis_ready.xlsx`
(or an equivalent SHA-256 utility on your operating system).

## Main results from the archived run

| Model | Rolling 2016–2023 AUC | 2024 AUC (examined previously) |
| --- | ---: | ---: |
| Logistic regression | 0.697 | 0.694 |
| Random forest | 0.681 | 0.696 |
| XGBoost | 0.670 | 0.704 |
| RBF SVM | 0.662 | 0.544 |
| B2 (source and season) | 0.688 | 0.676 |

The logistic-regression-minus-B2 difference in the rolling evaluation was
0.009 (95% year-block bootstrap percentile interval, −0.009 to 0.023).
The analysis does not establish added discrimination over source and season.

## Important interpretation limits

1. The first 2016–2023 model comparison pools eight evaluation years. The
   2,000-draw year-block bootstrap consequently has only eight sampling units
   and provides approximate, potentially unstable uncertainty intervals.
2. The 2024 within-year record bootstrap does not account for all repeated-site
   or temporal dependence. It is descriptive, not external validation.
3. The 17 primary physicochemical predictors exclude nitrate and total nitrogen.
   The laboratory subsequently confirmed nitrate in mg/L **NO3 ion** rather than
   NO3-N, while TN is in mg/L N. Earlier nitrate–TN comparison flags therefore
   need laboratory re-evaluation. The ammonium reporting basis remains to be
   confirmed. Chemical indices are outside this script.
4. Training-only SMOTE-NC is **secondary**. The main comparison retains
   natural class prevalence. SHAP describes the fitted model, not causation.
5. This repository does **not** establish model transportability beyond the
   two fixed drinking-water monitoring sites, clinical risk, or a real-time
   warning capability. The former WQI-class prediction task and its learning curves
   are not used to substantiate the revised, independently measured E. coli outcome.

## Dataset and code availability

The analysis-ready workbook, ML code, archived numerical results and figures are
included in this GitHub repository. The repository documents the **ML analysis**;
CF/PLI/WQI, PCA and temporal-trend calculations are outside the present code package.
The five integrity and archived-output tests passed in GitHub Actions. These checks
do not substitute for an exact end-to-end rerun of the publication environment.

For a reproducible starting point, use the archived input workbook, follow
the commands above, and consult `docs/METHODS.md` for model design and
interpretation. The repository contains the ML analysis and its source data;
the broader study's CF/PLI/WQI, PCA and trend calculations are not part of
this Python package.