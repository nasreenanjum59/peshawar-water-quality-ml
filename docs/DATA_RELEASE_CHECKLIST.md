# Data and code release checklist

Complete all items before any public deposit or GitHub visibility change.

- [ ] Obtain consent from all co-authors and the data-owning laboratory or institution for distribution of the 1,800-sample analysis-ready workbook.
- [ ] Review sample identifiers, dates, locations, laboratory register references and site information for privacy and security concerns; document any necessary de-identification.
- [ ] Reconcile nitrate reported as NO3 ion (not nitrate-N), clarify ammonium basis and revisit legacy total-nitrogen QA/QC flags.
- [ ] Confirm laboratory methods, detection limits, missing-value handling and records excluded during processing.
- [ ] Run the full script in its recorded dependency environment and verify reproduction of the deposited tables, figures and manuscript results.
- [ ] Coordinate an appropriate archive for CF, PLI, WQI, temporal trend and PCA analysis code if full-manuscript reproducibility is claimed.
- [ ] Resolve reviewer-requested learning curves and any direct WQI-rule baseline if included in the final paper.
- [ ] Confirm software/data licenses, creator names, ORCIDs, affiliations, acknowledgements and repository metadata.
- [ ] Check journal requirements for double-anonymised review and whether public repository authorship could affect anonymous review.
- [ ] Decide whether a public GitHub repository alone is sufficient for the final Data Availability Statement. A Zenodo deposit and DOI are optional; if chosen, cite the DOI only after assignment.

**Private deposit completed:** The original analysis-ready Excel workbook is now stored at `data/WQ_Peshawar_2009-2024_analysis_ready.xlsx` in this private GitHub repository. Its SHA-256 matches `results/01_input_sha256.txt`. This is NOT permission to make the data public.

The separate Zenodo ZIP remains a local review package, not authorization to publish data. Repository visibility, code licensing and underlying dataset release require explicit approval.
