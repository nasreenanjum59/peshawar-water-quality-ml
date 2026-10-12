# Verification report (11 October 2026)

## Completed checks

- The separate Zenodo review workbook was checked against the original analysis-ready workbook checksum (SHA-256: e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c).
- The archived results contain 16 headline summary rows: eight models evaluated over the primary 2016–2023 rolling period and the separately described 2024 period.
- Primary sample count: 584. Separate 2024 sample count: 76.
- Python source compilation and three package checks passed during the initial packaging.
- On 12 October 2026, after converting the ML checks into standard \`unittest.TestCase\` tests, five checks passed locally against the deposited workbook: two dataset-integrity tests and three ML output/temporal-split tests. These are consistency tests and do not constitute an independent full model rerun.
- GitHub Actions workflow `.github/workflows/verify-repository.yml` ran those five checks successfully on 12 October 2026.
- A complete reduced software smoke test using the full workbook and --quick mode completed, including nested fold generation, benchmarks and exploratory sensitivity checks.

## Deposited workbook integrity (12 October 2026)

- The 1,800-record analysis-ready Excel workbook is deposited at `data/WQ_Peshawar_2009-2024_analysis_ready.xlsx`.
- File SHA-256: `e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`.
- Git blob SHA-1: `ec629c02deccf16109b61ddfa8fc8444e921b291`; the GitHub object matched the SHA-1 calculated on the original bytes.
- The workbook contains `analysis_data`, `data_dictionary` and `notes_for_analysis` sheets; 1,800 data rows are distributed across three source groups (600 each).
- The Git-object integrity check verifies uploaded bytes but does not replace an independent scientific rerun.

## Outstanding checks

The archived model results were generated with Python 3.9.13, NumPy 2.0.2, pandas 2.2.3, scikit-learn 1.6.1 and XGBoost 2.1.4. The smoke test used a different local environment, including XGBoost 3.1.3, and a reduced hyperparameter search. **The smoke test is not an exact reproduction of the archived publication results.**

A complete recorded-environment rerun remains a recommended scientific verification step; independent source-record/laboratory QA/QC verification and review of legacy total-nitrogen flags are also outstanding. Confirm co-author/data-owner distribution authority before enabling public access.
