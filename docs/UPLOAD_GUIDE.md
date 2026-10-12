# GitHub dataset and Python code release

## Repository

https://github.com/nasreenanjum59/peshawar-water-quality-ml

The GitHub repository contains the 2009–2024 analysis-ready water-quality
workbook (1,800 observations and data dictionary), the Python machine-learning
pipeline, temporal validation outputs, model comparisons, diagnostic figures,
reproducibility instructions and integrity tests.

The ML analysis uses municipal tap-water and tube-well samples (n = 1,200)
to predict laboratory-measured `E. coli` detection. River-water samples are
provided for the wider study but are not included in the ML models.

## Confirm public accessibility

1. Verify data-owner and co-author permission to distribute the workbook,
   including its exact dates, site names and laboratory register references.
2. Verify final results, data metadata, author information, licenses and
   relevant journal double-anonymised review requirements.
3. In GitHub, open **Settings → General → Danger Zone → Change repository
   visibility**, choose **Public** and confirm. Access to Settings requires
   repository administration permission.
4. Open the repository from a signed-out browser to check that the dataset,
   Python files, documentation and results are accessible.
5. Check **Actions → Verify deposited ML package** for the five automated
   integrity and results checks. This verification is not a substitute for an
   independent end-to-end model rerun.
6. Add the verified repository URL to the final manuscript Data Availability
   Statement, clearly limiting the code deposit's scope to the ML component.

**Important:** GitHub public visibility also exposes reachable Git history.
Inspect past commits and uploaded metadata before changing visibility.

## Optional Zenodo DOI

A Zenodo deposit is optional, not a requirement for GitHub access. If an
archival DOI is desired, create a Zenodo record using verified creators,
ORCIDs, affiliations, licenses and version details, then cite the DOI actually
issued. Do not cite a placeholder DOI.

Official resources:
- https://help.zenodo.org/docs/deposit/create-new-upload/
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/

The current GitHub code reproduces the machine-learning workflow only.
Physicochemical indices (CF, PLI, WQI), PCA and temporal trend analyses
require their own verified supporting code or documentation.
