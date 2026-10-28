# Submitted manuscript v18: machine-learning audit and repository alignment

**Manuscript:** EW-ART-05-2026-000506  
**Submission package reviewed:** 28 October 2026  
**Scope:** machine-learning (ML) component only

## Source and status

The authors' final submission package included an audit workbook,
a clean and marked-up manuscript, a reviewer-response letter,
Supplementary Information and the exported supplementary tables.
The accompanying audit workbook reports 37 of 37 data checks passed
and a seeded rerun (seed 42; scikit-learn 1.9, XGBoost 3.4, SHAP 0.54).
These are **claims recorded in the submitted audit**, not a new,
independent execution by this repository.

The submission ZIP did **not** contain the final analysis-ready
1,800-row workbook, the final seeded Python ML script or the
sample-level outputs and figures from that rerun. Consequently,
the older repository results, version record and integrity hash
must not be described as reproducing the final submitted v18 results.
The existing archived numeric outputs remain unchanged pending
deposit of a complete, coherent rerun package.

## Final submitted v18 ML results

Primary temporal evaluation: nested rolling-origin 2016–2023,
n = 584 out-of-time predictions. The separate 2024 evaluation
(n = 76) had previously been examined during model development.

| Model | Final 2016–2023 AUC | Final 2024 AUC |
| --- | ---: | ---: |
| Logistic regression | 0.697 | 0.694 |
| Random forest | 0.681 | 0.696 |
| XGBoost | 0.672 | 0.687 |
| SVM (RBF) | 0.663 | 0.544 |
| B1: source only | 0.635 | 0.671 |
| B2: source and season | 0.688 | 0.676 |
| B3: reduced-feature LR | 0.686 | 0.687 |
| B4: depth-3 decision tree | 0.628 | 0.691 |
| B5: WQI score only | 0.577 | 0.690 |

The final logistic-regression versus B2 paired AUC difference was
+0.009 (95% year-block bootstrap CI: -0.009 to +0.022).
For XGBoost, the final 2024 confusion-matrix counts were
TN 6, FP 17, FN 7 and TP 46.

The final submission reports XGBoost AUC variability across
six random seeds: 0.664–0.682 for the rolling evaluation and
0.604–0.706 for the separate 2024 assessment.

## Differences from the earlier archived package

- XGBoost rolling AUC: 0.670 -> 0.672; 2024 AUC: 0.704 -> 0.687.
- SVM rolling AUC: 0.662 -> 0.663.
- B5 (WQI-only logistic-regression baseline) added.
- 2024 SMOTE-NC AUCs in final Table S14(b):
  LR 0.687, RF 0.638, XGBoost 0.652.
- Top mean absolute SHAP value for source:
  0.370 -> 0.386, with other SHAP values also revised.
- Hyperparameter selections, some confidence intervals and
  calibration/figure outputs were updated in the final run.

All figures and metrics above are **reported by the final
submission documents**. They have not been added to the archived
`results/` directory because the corresponding complete source
run was not supplied.

## Files needed for full repository alignment

1. The final v4 analysis-ready workbook with confirmed metadata
   and the accompanying data dictionary.
2. The exact seeded final ML script, including B5 and updated
   sensitivity analyses, or the complete reproducible environment.
3. Final numerical results (fold settings, per-sample predictions,
   metrics, QC/SMOTE/SHAP tables) and figures from that run.
4. Updated package-version record and dataset checksum, followed
   by execution of the integrity and results tests.

The README, archived results and test assertions should then be
updated **together** to avoid mixing two different analysis runs.
The index calculations and other non-ML analyses are outside the
scope of this alignment document.
