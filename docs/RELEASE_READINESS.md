# GitHub public-release readiness (12 October 2026)

**Current state: PRIVATE RELEASE CANDIDATE. Do not describe this repository as publicly accessible until its GitHub visibility has actually changed.**

## Already deposited and checked
- The analysis-ready workbook contains 1,800 samples (600 each: river, tap and tube well); the ML analysis uses 1,200 tap and tube-well samples.
- Workbook: `data/WQ_Peshawar_2009-2024_analysis_ready.xlsx`. SHA-256: `e2cbaeb755a37a132caef555abe850fc628f13bc1ed1bea3d2c4f4bbd564b89c`.
- Python workflow, frozen model outputs, four regenerated figures, methods, model tests and data dictionary are present.
- A local verification of the corrected ML test module ran three checks successfully on 12 October 2026. The repository also contains two dataset-integrity tests. The full combined test command is:
  ```bash
  python -m unittest discover -s tests -p 'test_*.py' -v
  ```
  The complete combined suite should be rerun with the exact deposited workbook before public release.

## Public-release gates still needing author confirmation
1. **Release authority:** Obtain explicit permission from the data-owning laboratory/institution as applicable, in addition to co-author approval. Confirm whether exact collection dates, site names, institutional laboratory register references and analysis notes may be disseminated. The workbook is currently **not** de-identified.
2. **Journal double-anonymised review:** The repository URL uses a personally identifying GitHub account. A public citation during double-anonymised peer review could expose authorship. Agree on a review-compatible route (for example, anonymised reviewer supplements, a neutral repository, or an editor-approved approach) before changing visibility. See: https://www.rsc.org/publishing/publish-with-us/publish-a-journal-article/environmental-science-water-research-and-technology
3. **Scientific reconciliation:** Confirm the nitrate basis (reported as NO3 ion, not NO3-N), ammonium basis, historical TN QA flags, censored COD convention and the final manuscript wording. Code for CF/PLI/WQI, PCA and conventional trend statistics is not currently in this ML repository.
4. **Recorded-environment reproducibility:** The October 2026 model outputs have not been independently rerun end-to-end in the original software environment. The quick-mode smoke test does **not** establish numerical reproduction of publication results.
5. **Licenses and attribution:** Agree on an explicit software license, a data reuse license or restrictions, and the creator/citation metadata. No license or registered DOI has been issued in this repository.
6. **Submission alignment:** Verify final figures, SI tables, journal data-availability statement, the frozen primary cohort/results, and that 2024 is identified as a *separate previously examined evaluation*, not an untouched independent test.

## After gates 1–6 are cleared
1. Inspect the entire Git history for any information that should not be public; changing repository visibility exposes its reachable history, not just current files.
2. In GitHub repository **Settings → General → Danger Zone → Change repository visibility**, select **Make public** and complete the GitHub confirmation. (The connected GitHub actions available here do not expose a repository-visibility change.)
3. Open the repository in a signed-out browser, verify that the workbook, code, docs and figure files are downloadable, and run the tests. Check the repository's actual visibility before making any public-access claim.
4. If desired, create a GitHub Release with a version tag after code and data licenses and attribution are agreed. A GitHub Release does not automatically assign a DOI. Zenodo is optional.
5. Once public, update the manuscript's **Data availability** section and response letter with the exact live URL. Specify that this repository reproduces the **ML component**, not all CF/PLI/WQI/PCA/trend calculations unless these are separately provided.

## Data availability statement, only after successful public access check
> The analysis-ready water-quality dataset (1,800 observations), data dictionary, Python code and associated machine-learning results are available at https://github.com/nasreenanjum59/peshawar-water-quality-ml . The machine-learning analysis used the tap-water and tube-well subset (n = 1,200). The deposited code reproduces the machine-learning component; methods and code supporting other analyses are described separately in the manuscript and Supplementary Information.

Do not use this as the manuscript's final Data Availability Statement **until** the repository is publicly accessible and the laboratory/institution and anonymity considerations are resolved. This suggested statement does not claim a DOI, a complete reproducibility rerun, or a full-paper code deposit.
