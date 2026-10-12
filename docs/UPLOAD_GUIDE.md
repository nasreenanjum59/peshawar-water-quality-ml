# Using the water-quality dataset and Python code

Repository: https://github.com/nasreenanjum59/peshawar-water-quality-ml

## Included materials

- `data/WQ_Peshawar_2009-2024_analysis_ready.xlsx`: 1,800 water-quality
  observations from 2009–2024, a data dictionary and analysis notes.
- `src/peshawar_ml.py`: Python machine-learning pipeline for predicting
  measured *E. coli* detection in municipal tap and tube-well observations
  (n = 1,200).
- `src/plot_archived_ml_figures.py`: figure generation from archived outputs.
- `results/`: nested rolling-origin model predictions, evaluation metrics,
  quality-control sensitivity results and diagnostic figures.
- `tests/`: data integrity and archived-output consistency checks.
- `docs/METHODS.md` and `docs/VALIDATION_REPORT.md`: methods and tests.

## Download and run

Choose **Code → Download ZIP** on GitHub, or clone the repository:

```bash
git clone https://github.com/nasreenanjum59/peshawar-water-quality-ml.git
cd peshawar-water-quality-ml
python -m venv .venv
# Activate the virtual environment for your operating system
python -m pip install -r requirements-recorded.txt
```

Run the five integrity and archived-output consistency tests:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Run the primary analysis workflow:

```bash
python src/peshawar_ml.py \
  --data data/WQ_Peshawar_2009-2024_analysis_ready.xlsx \
  --out runs/full --with-smote --with-shap --permutations 200
```

The archived results were produced with the package versions described in
`results/00_versions.json`. The full analysis can take significant time.
The optional `--quick` mode checks software operation but must not be used
as a substitute for the publication results.

## Interpretation and citation

The ML component predicts *E. coli* detection using nested temporal
validation (2016–2023, n = 584), with 2024 (n = 76) assessed separately.
The 2024 evaluation was previously inspected and is not an untouched
independent external test. The code does not calculate the broader study's
CF/PLI/WQI, PCA or Mann–Kendall trend statistics.

Please cite the associated water-quality study and this repository when
reusing the dataset or software. No Zenodo DOI has been assigned.
