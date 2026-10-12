# Analytical methods and interpretation

## Primary outcome and sample

The binary outcome is E. coli detection (>0 CFU/100 mL = 1; 0 CFU/100 mL = 0), independently established by laboratory measurement. The ML analysis includes 1,200 municipal tap and tube-well samples, of which 849 are positive. The 600 river-water samples are excluded from ML. The analysis concerns two fixed monitoring sites, not spatial generalisation to new sites.

## Predictors and classifiers

The primary models use 17 measured physicochemical parameters: pH, temperature, turbidity, total dissolved solids, hardness, chloride, sulphate, phosphate, ammonium, dissolved oxygen, BOD5, COD, alkalinity, TOC, UV254, chlorophyll-a and oxidation–reduction potential. Water source is binary encoded, and season uses three indicator columns with Winter as reference. The full design has 21 encoded predictor columns. Nitrate and total nitrogen are excluded from the primary model. Microbiological measurements, outcome-derived flags and index-derived classes are not predictors. Censored COD is replaced by 2/sqrt(2) in memory; the recorded detection-limit convention requires laboratory confirmation.

Four model families are examined: L2 logistic regression, random forest, XGBoost and RBF SVM. The four prespecified baselines are B1 (source), B2 (source and season), B3 (source, season, turbidity, BOD5 and ammonium), and B4 (depth-three decision tree). Candidate parameter grids and the fixed seed of 42 are in the source code.

## Nested rolling-origin evaluation

For each evaluation year Y in 2016–2023, model fitting and tuning use years before Y only. The inner fit uses years earlier than Y minus two years, inner validation uses the two immediately preceding years, and the outer fit is refitted using all observations before Y. This yields 584 out-of-time observations.

The separate 2024 evaluation has 76 observations (53 positive, 23 negative). The 2024 records were examined in earlier development and must not be described as an untouched independent test. All prediction and threshold metrics preserve the observed class prevalence.

Reported evaluation includes ROC-AUC, average precision, Brier score, sensitivity, specificity and confusion matrices. Thresholds target at least 80% sensitivity on past-only validation records; this does not guarantee future sensitivity. Primary confidence intervals use 2,000 resamples of entire evaluation years (eight distinct years). Paired differences against B2 should not be interpreted as equivalence when intervals include zero.

## Secondary analyses and interpretation

SMOTE-NC is a training-only sensitivity experiment; primary fitting uses unresampled data. Exploratory nitrogen-feature scenarios, historical QA/QC exclusions and label permutation checks are not primary predictive evaluations. Following laboratory clarification that nitrate was reported as NO3 ion, the historical total-nitrogen QC flag must be reassessed. SHAP explanations apply to XGBoost training-period model predictions and indicate associations rather than causal mechanisms.

## Scope of the package

The scripts in this repository address the machine-learning component only. They do not reproduce water-quality indices (CF, PLI, WQI), PCA, Mann–Kendall trends, or corrections to original laboratory records. Reproducibility of the entire manuscript requires separate verified implementations and authorization to release the underlying data.
