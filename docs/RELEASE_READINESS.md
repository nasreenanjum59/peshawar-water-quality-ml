# Dataset and ML package release verification

## Files available in the repository

- Excel workbook: `data/WQ_Peshawar_2009-2024_analysis_ready.xlsx` with 1,800 observations (600 per source), data dictionary and analysis notes.
- ML subset: 1,200 municipal tap-water and tube-well samples, with 849 laboratory-measured E. coli-positive observations.
- Python ML pipeline, archived prediction tables, baseline comparisons, bootstrap uncertainty summaries and diagnostic PNG figures.
- Automated integrity and archived-output checks:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

The five tests passed locally and on GitHub Actions on 12 October 2026.
These tests verify file integrity and selected headline results; they do not
replace an independently repeated full run in the original software environment.

The workbook SHA-256 is
`e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`.

## Publication and verification notes

1. **Attribution and distribution rights:** Confirm the data owner and
   co-authors have authorised dissemination of the workbook and its detailed
   collection dates, locations and laboratory register identifiers.
2. **Double-anonymised review:** The GitHub account URL may disclose author
   identity. Agree on the manuscript citation method with the journal
   editorial office or consider a review-compatible access route.
3. **Scientific interpretation:** Nitrate is reported as NO3 ion, not NO3-N;
   ammonium basis and historical TN QC flags need separate confirmation.
   The primary ML models exclude nitrate and total nitrogen.
4. **Reproducibility:** The full 2026 analysis has not been independently
   rerun end-to-end in the recorded original package versions.
5. **Attribution and licenses:** Choose and document data and software reuse
   permissions; no license or archival DOI has yet been assigned.
6. **Scope:** The code here supports the ML analysis. CF/PLI/WQI, PCA and
   trend statistics require separate supporting files for full-paper code
   reproducibility.

## GitHub visibility and optional release version

Public access is controlled by GitHub repository visibility. A repository
administrator can set it through **Settings → General → Danger Zone →
Change repository visibility → Public**. Inspect the Git history before
changing visibility; history is also exposed after publication.

After changing visibility, verify the repository using a signed-out browser
and review **Actions → Verify deposited ML package**. A GitHub Release tag
can be created for a versioned software snapshot; Zenodo and a DOI are
optional.

## Suggested Data Availability Statement after public access is verified

> The analysis-ready dataset (1,800 water-quality observations), data
> dictionary, Python machine-learning code and archived model outputs are
> available at https://github.com/nasreenanjum59/peshawar-water-quality-ml.
> The machine-learning analysis uses the municipal tap-water and tube-well
> subset (n = 1,200). The repository documents and supports reproduction of
> the machine-learning component; analyses based on CF, PLI, WQI, PCA and
> temporal trends are described separately in the manuscript and
> Supplementary Information.

Use the statement only after actual public access has been verified.
