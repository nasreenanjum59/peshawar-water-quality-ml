# Dataset and code publication checklist

Use this checklist to confirm a complete and reproducible public release.

- [ ] Confirm author and data-owning institution permissions for redistribution of the 1,800-sample workbook, including exact dates, locations and laboratory register identifiers.
- [ ] Check source-data metadata for confidentiality, privacy and site-security concerns. Document redactions or restrictions if required.
- [ ] Reconcile nitrate as mg/L NO3 ion (not nitrate-N); verify ammonium basis and revisit historical TN quality-control flags.
- [ ] Confirm laboratory methods, relevant detection limits, non-detect and missing-data handling, and original record exclusion criteria.
- [ ] Re-run the full script in the recorded dependency environment and compare archived outputs with the final manuscript.
- [ ] If full-manuscript reproducibility is claimed, add separately verified code for CF, PLI, WQI, PCA and temporal trend statistics.
- [ ] Confirm the original rule-based WQI classification and learning-curve analyses are not misrepresented as validation of the revised E. coli outcome.
- [ ] Agree on separate data and software licenses, creators, author order, ORCIDs, acknowledgements and citation metadata.
- [ ] Confirm journal double-anonymised review compatibility, considering the author-identifying GitHub account.
- [ ] Verify public GitHub accessibility using a signed-out browser before stating that the data are publicly available.
- [ ] Optionally decide whether Zenodo archival and a DOI are useful; cite only a DOI actually issued.

## Workbook integrity

The deposited analysis-ready workbook is
`data/WQ_Peshawar_2009-2024_analysis_ready.xlsx`.
Its SHA-256 matches `results/01_input_sha256.txt`. The repository includes
the full ML analysis source, results and software checks. GitHub can serve
as the primary distribution platform; a Zenodo DOI is optional.

Changing repository visibility should occur only once distribution rights,
sensitive metadata and submission requirements have been reviewed.
