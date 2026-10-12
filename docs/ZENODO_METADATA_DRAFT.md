# Zenodo deposit draft — **do not publish yet**

**Status:** Metadata draft for co-author and data-owner review. No Zenodo record or DOI
has been created. The code repository is private.

## Recommended deposit

- **Upload type:** Dataset (data and computational analysis)
- **Working title:** Temporal machine-learning reanalysis of E. coli detection in
  municipal tap and tube-well water, Peshawar, Pakistan (2009–2024)
- **Version:** To be agreed before publication
- **Publication date:** Actual date of Zenodo publication (do not predate)
- **Creators, affiliations, ORCIDs:** Complete only after author approval,
  in the agreed author order
- **Related manuscript:** Environmental Science: Water Research & Technology,
  manuscript EW-ART-05-2026-000506. Confirm linking and double-anonymised
  review requirements before release.
- **Keywords:** E. coli; microbiological water quality; municipal tap water;
  tube-well groundwater; temporal validation; machine learning; Peshawar; Pakistan
- **Licenses:** Select code and dataset licenses *separately* with consent
  from all rightsholders; do not assume a license.
- **Access:** Keep draft unpublished while permissions, possible personal data,
  analytical units, and laboratory quality-assurance checks remain open.

## Proposed description

This planned archive documents the machine-learning component of a 2009–2024
retrospective water-quality study in Peshawar, Pakistan. The complete
analysis-ready workbook contains 1,800 observations spanning three water
sources. The ML analysis uses 1,200 tap-water and tube-well observations;
the independently measured outcome is laboratory E. coli detection
(>0 vs 0 CFU/100 mL). The primary comparison consists of 584 nested
rolling-origin out-of-time predictions from 2016–2023, supplemented by
76 separately reported observations from 2024 that had been previously
inspected during model development and are not a strictly untouched holdout.

The archived model outputs include performance and uncertainty summaries,
temporal folds, individual predictions, baseline comparisons, sensitivity
analyses, and training-only global SHAP summaries. Associated scripts
document preprocessing, fitting, assessment, and graphical rendering.
The analysis does not establish real-time deployment, causality, or
generalisation to new water sampling locations.

## Materials under review

1. Separate dataset review ZIP containing the original analysis-ready
   workbook, Python code, results, and documentation.
2. Private version-controlled GitHub repository containing scripts and
   de-identified ML analysis outputs. Review whether even sample identifiers
   in model-output CSVs are suitable for release.
3. Journal-specific supplementary information, distinct from the repository.

## Mandatory checks before pressing Publish

- Written author/institution approval for data and software distribution.
- Site names, exact dates, original register identifiers, and any sensitive
  sampling metadata reviewed; redact or restrict only with documented changes.
- Laboratory-confirmed nitrate/ammonium reporting basis and QA/QC checked.
- Complete original-software-environment re-run and manuscript/SI reconciliation.
- Appropriate authorship, ORCIDs, funding, licenses, and release version.
- Double-anonymised peer-review compatibility and data citation agreed.

## Suggested Data Availability Statement after approval (not for use yet)

The analysis-ready data and Python code underlying the machine-learning
component are archived at Zenodo (DOI: [insert DOI only after assignment]).
The versioned analysis code is also available at [approved public GitHub URL].
Methods and supplementary tables for the other analyses are described in the
article and Supplementary Information. Any access restrictions and exclusions
are explained in the Zenodo record.

No data archive is represented as publicly available until it genuinely is.
