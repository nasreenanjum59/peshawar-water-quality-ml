# Analysis-ready workbook (private co-author review)

**File:** `WQ_Peshawar_2009-2024_analysis_ready.xlsx`

This is the exact workbook used as input in the archived 9 October 2026
machine-learning analysis. Its SHA-256 checksum is:

`e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`

The workbook has three sheets: `analysis_data` (1,800 observations,
40 columns), `data_dictionary` (40 variable descriptions) and
`notes_for_analysis`. The observations comprise 600 river, 600 tap,
and 600 tube-well samples from 2009–2024. The ML analysis uses the tap
and tube-well subset (n = 1,200; 849 positive for measured E. coli).

**RELEASE RESTRICTION:** The GitHub repository is private for co-author
review. The workbook contains dates, locations and laboratory register
identifiers; it must not be exposed publicly without data-owner approval,
privacy/site-security checks and agreement on the reporting of historical
analytical units. In particular, nitrate was confirmed in mg/L NO3 ion,
while the ammonium basis and certain legacy TN-based QC flags require
additional clarification. This file is not a certified public-release
dataset. Review any exclusions and proposed redactions with the authors
and keep a record of changes and checksums.

To check file identity, run:

```bash
sha256sum data/WQ_Peshawar_2009-2024_analysis_ready.xlsx
python -m unittest discover -s tests -p 'test_dataset_integrity.py' -v
```

These checks confirm input integrity and headline cohort counts, not
scientific validity, laboratory QA/QC or exact reproduction of every
manuscript table. The current code reproduces the ML workflow only; CF,
PLI, WQI, PCA and temporal trend computations are outside this package.
