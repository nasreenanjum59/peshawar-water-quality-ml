# Optional Zenodo metadata template

Zenodo archiving is optional. The primary dataset and ML code files are
included in the GitHub repository at
https://github.com/nasreenanjum59/peshawar-water-quality-ml.
No Zenodo record or DOI has yet been assigned.

## Suggested Zenodo metadata (if archival DOI is desired)

- **Deposit type:** Dataset and accompanying computational analysis
- **Working title:** Temporal machine-learning reanalysis of E. coli
  detection in municipal tap and tube-well water, Peshawar, Pakistan
  (2009–2024)
- **Version and publication date:** The actual approved release tag and date
- **Creators, ORCIDs and affiliations:** Enter the verified author-approved
  names and contributor order
- **Related article:** Environmental Science: Water Research & Technology,
  manuscript EW-ART-05-2026-000506
- **Keywords:** E. coli; microbiological water quality; municipal tap water;
  tube-well groundwater; temporal validation; machine learning; Peshawar
- **Licenses:** Specify approved data and software reuse terms separately
- **Access:** Select terms consistent with institutional data ownership and
  journal double-anonymised review requirements

## Description for a future deposit

This archive documents the machine-learning component of a retrospective
water-quality study conducted in Peshawar, Pakistan, between 2009 and 2024.
The analysis-ready workbook includes 1,800 records from three water sources.
The ML component uses 1,200 municipal tap-water and tube-well observations
to predict independently measured E. coli detection (>0 versus 0 CFU/100 mL).
The primary analysis uses 584 out-of-time nested rolling-origin predictions
from 2016–2023. A separate evaluation of 76 samples from 2024 is described
as previously examined, not an untouched external test.

Archived outputs include nested validation-fold information, model scores
and uncertainty summaries, predicted probabilities, baseline comparisons,
sensitivity analyses and global training-period SHAP summaries. The
accompanying Python scripts document preprocessing, model fitting, evaluation
and plot generation. The analyses do not demonstrate real-time prediction,
causal inference or spatial generalisability beyond the two monitoring sites.

## Suggested references

Use the GitHub URL for the primary deposited dataset and ML code.
If an optional Zenodo archive is created, cite only a DOI formally issued
by Zenodo after the authors have checked licensing and citation metadata.
