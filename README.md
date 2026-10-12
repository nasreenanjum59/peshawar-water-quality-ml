# Peshawar water-quality ML reanalysis

**Manuscript:** EW-ART-05-2026-000506, *Environmental Science: Water Research & Technology*  
**Status:** preparation for co-author review, not yet a publicly released dataset or software deposit  
**Analysis frozen:** 9 October 2026; explanatory packaging updated 11 October 2026

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
- `results/`: archived outputs generated on 9 October 2026, plus diagnostic
  figures. The output files carry their original column names and run metadata.
- `tests/`: checks for temporal folds, decision thresholds and headline
  metrics in the archived outputs.
- `docs/METHODS.md`: model definitions, analysis choices and known limitations.
- `docs/DATA_RELEASE_CHECKLIST.md`: provenance, licensing and journal checks
  that must be resolved before publication.
- `docs/UPLOAD_GUIDE.md`: instructions for GitHub and Zenodo deposits.
- `data/` is **deliberately absent from the GitHub-ready archive** until
  public-data permissions are confirmed. The separate Zenodo review package
  contains the exact analysis-ready workbook for author inspection.

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

The supplied workbook has SHA-256:

`e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`

Check a local copy with `python -m hashlib` alternatives or `sha256sum`.

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
   warning capability. The direct WQI benchmark and learning-curve request
   remain open until verified and integrated by the authors.

**Release status:** This is a reviewer-response reproducibility draft. Authors
must validate provenance, approvals, model code and deposited artifacts before
public posting or DOI assignment. See `docs/DATA_RELEASE_CHECKLIST.md`.