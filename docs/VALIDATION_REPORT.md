# Verification report (11 October 2026)

## Completed checks

- The separate Zenodo review workbook was checked against the original analysis-ready workbook checksum (SHA-256: e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c).
- The archived results contain 16 headline summary rows: eight models evaluated over the primary 2016–2023 rolling period and the separately described 2024 period.
- Primary sample count: 584. Separate 2024 sample count: 76.
- Python source compilation and three package tests passed during packaging.
- A complete reduced software smoke test using the full workbook and --quick mode completed, including nested fold generation, benchmarks and exploratory sensitivity checks.

## Outstanding checks

The archived model results were generated with Python 3.9.13, NumPy 2.0.2, pandas 2.2.3, scikit-learn 1.6.1 and XGBoost 2.1.4. The smoke test used a different local environment, including XGBoost 3.1.3, and a reduced hyperparameter search. **The smoke test is not an exact reproduction of the archived publication results.**

Before public release, the full analysis must be rerun in the recorded environment and compared with the manuscript and SI. Independent source-record and laboratory QA/QC verification and review of legacy total-nitrogen flags are also outstanding. The dataset must not be publicly released without co-author and data-owner approval.
