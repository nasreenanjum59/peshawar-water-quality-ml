# Peshawar water-quality analysis-ready dataset

**File:** `WQ_Peshawar_2009-2024_analysis_ready.xlsx`

This three-sheet workbook contains the final author-confirmed source-data values
(29 October 2026), in the column layout expected by the archived ML script.
Its 1,800 records and measured values are unchanged from the original ML input;
only the data dictionary and analysis notes were clarified. SHA-256 checksum:

`eecf1f7d53ff88c33020862ad0bd585ea85c965cad608b88f38f97f1e2655369`

The workbook has three sheets: `analysis_data` (1,800 observations;
40 columns), `data_dictionary` (40 variable descriptions) and
`notes_for_analysis`. There are 600 river-water, 600 municipal tap-water and
600 tube-well samples from 2009–2024. The ML subset includes the tap-water
and tube-well observations (n = 1,200), of which 849 are positive for measured
`E. coli` detection.

## Dataset provenance and reuse

The workbook retains collection dates, sampling locations and laboratory
register identifiers to support traceability. Please cite the associated
study and repository when using these data.

The final laboratory record confirms nitrate in mg/L as NO3 ion,
original `ammonium_mg_l` concentrations in mg/L as ammonia (NH3), and
`tn_mg_l` in mg/L as N. These source-column names are retained because
the archived ML code expects them. The legacy nitrogen-related QC flag
is preserved, not recalculated. The primary predictor set excludes nitrate
and total nitrogen.

## Check data integrity

```bash
sha256sum data/WQ_Peshawar_2009-2024_analysis_ready.xlsx
python -m unittest discover -s tests -p 'test_*.py' -v
```

The automated checks verify the workbook hash, cohort sizes and selected
archived results; they do not establish laboratory QA/QC validity or reproduce
the paper's physicochemical indices, PCA or trend analyses.
