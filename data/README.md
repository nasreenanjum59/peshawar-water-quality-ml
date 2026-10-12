# Peshawar water-quality analysis-ready dataset

**File:** `WQ_Peshawar_2009-2024_analysis_ready.xlsx`

This workbook is the input used in the 9 October 2026 archived machine-learning
analysis. Its SHA-256 checksum is:

`e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`

The workbook has three sheets: `analysis_data` (1,800 observations;
40 columns), `data_dictionary` (40 variable descriptions) and
`notes_for_analysis`. There are 600 river-water, 600 municipal tap-water and
600 tube-well samples from 2009–2024. The ML subset includes the tap-water
and tube-well observations (n = 1,200), of which 849 are positive for measured
`E. coli` detection.

## Dataset provenance and reuse

The workbook retains collection dates, sampling locations and laboratory
register identifiers to enable traceability. Anyone redistributing the dataset
should ensure that the institutional data owner has authorised these metadata
and the distribution terms. Cite the study and this dataset as appropriate.

Nitrate concentrations were subsequently confirmed to be expressed as
mg/L NO3 ion, not NO3-N. The ammonium reporting basis and legacy total-nitrogen
quality-control flags require separate interpretation; see `docs/METHODS.md`.
This does not affect the primary ML predictor set, which excludes nitrate and
total nitrogen.

## Check data integrity

```bash
sha256sum data/WQ_Peshawar_2009-2024_analysis_ready.xlsx
python -m unittest discover -s tests -p 'test_*.py' -v
```

The automated checks verify the workbook hash, cohort sizes and selected
archived results; they do not establish laboratory QA/QC validity or reproduce
the paper's physicochemical indices, PCA or trend analyses.
