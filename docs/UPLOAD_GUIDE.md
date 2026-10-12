# GitHub and Zenodo release workflow

## Current GitHub repository

Repository: https://github.com/nasreenanjum59/peshawar-water-quality-ml

The repository is **private** pending author approval. The machine-learning source code, tests, run metadata and numerical results can be maintained here. Data are intentionally excluded and protected by .gitignore. Do not make the repository public until permission and double-anonymised review implications have been considered.

## Dataset and DOI workflow

1. Co-authors and the data-owning institution review the analysis-ready workbook, its metadata dictionary and any sensitive fields.
2. Confirm that the code and frozen results reproduce the final manuscript in the recorded software environment.
3. Sign in at https://zenodo.org and create a draft deposit. Enter verified creators, ORCIDs, version, related article, abstract, license, access conditions and keywords.
4. Upload the approved dataset and code archive to the draft. Zenodo draft deposits can be reviewed before publication.
5. Reserve a DOI if appropriate, and publish only after all release conditions are satisfied. Cite the actual DOI, not a proposed or hypothetical identifier.
6. Alternatively, link GitHub to Zenodo and archive a software release after approval; a separate dataset record can be used for raw-data files.

Official resources:
- https://help.zenodo.org/docs/deposit/create-new-upload/
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/

The manuscript's Data Availability Statement and reviewer response must reflect what reviewers can actually access. An ML-only archive is not a complete reproducibility package for water-quality indices, temporal trend tests or PCA.
