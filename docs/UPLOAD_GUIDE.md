# GitHub and Zenodo release workflow

## Current GitHub repository

Repository: https://github.com/nasreenanjum59/peshawar-water-quality-ml

The repository is **private** pending author approval. It now contains the machine-learning source code, tests, figures, run metadata, numerical results **and the exact analysis-ready workbook** under `data/`. The workbook must remain private until the data owners and all co-authors authorize release, dates and laboratory identifiers are reviewed, the required scientific checks are completed, and double-anonymised peer-review implications are considered.

## Public-release review and optional DOI workflow

1. Co-authors and the data-owning institution review the analysis-ready workbook, its metadata dictionary and any sensitive fields.
2. Confirm that the code and frozen results reproduce the final manuscript in the recorded software environment.
3. After approval, make an audited GitHub release public if a public GitHub repository is the chosen journal repository. Confirm all files and histories are appropriate for disclosure before changing visibility.
4. **Optional:** Sign in at https://zenodo.org and prepare a dataset or software deposit. Enter verified creators, ORCIDs, version, related article, abstract, license, access conditions and keywords.
5. If Zenodo is used, reserve and publish a DOI only after final approval. Cite only the actual DOI after it has been assigned. GitHub alone does not require a Zenodo DOI.
6. If an archived software release is desired, Zenodo can be linked to GitHub; a separate dataset record may be preferable for original data.

Official resources:
- https://help.zenodo.org/docs/deposit/create-new-upload/
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/

The manuscript's Data Availability Statement and reviewer response must reflect what reviewers can actually access. The included dataset and ML code facilitate reanalysis of this ML component, but the current archive does not reproduce the manuscript's CF, PLI, WQI, temporal trend tests or PCA. The manuscript and reviewer response must not imply full-paper reproducibility until those workflows are also deposited and verified.
