"""Small checks of the temporal design and frozen manuscript results."""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "peshawar_ml.py"
RESULTS = ROOT / "results"

spec = importlib.util.spec_from_file_location("peshawar_ml", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_operating_threshold_targets_validation_sensitivity():
    observed = np.array([1, 1, 1, 1, 1, 0, 0])
    probs = np.array([0.97, 0.83, 0.71, 0.63, 0.49, 0.5, 0.1])
    threshold = module.sens_threshold(observed, probs, 0.8)
    result = module.operating_point(observed, probs, threshold)
    assert threshold == 0.63
    assert result["sensitivity"] == 0.8
    assert result["TN"] + result["FP"] + result["FN"] + result["TP"] == 7


def test_every_rolling_year_has_past_only_inner_validation():
    with (RESULTS / "02_fold_hyperparameters.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 9 * 8
    for row in rows:
        year = int(row["prediction_year"])
        assert 2016 <= year <= 2024
        assert int(row["inner_train_end_year"]) == year - 3
        assert int(row["inner_validation_start"]) == year - 2
        assert int(row["inner_validation_end"]) == year - 1


def test_archived_headline_results_match_manuscript():
    with (RESULTS / "05_main_aggregated_results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 16
    by_key = {(r["period"], r["model"]): r for r in rows}
    wanted = {
        ("rolling_2016_2023", "Logistic regression"): 0.6967712802,
        ("rolling_2016_2023", "B2 source and season"): 0.6879515692,
        ("rolling_2016_2023", "XGBoost"): 0.6696489049,
        ("previously_inspected_2024", "XGBoost"): 0.7038556194,
    }
    for key, auc in wanted.items():
        assert abs(float(by_key[key]["AUC"]) - auc) < 1e-8
    assert int(by_key[("rolling_2016_2023", "Logistic regression")]["n"]) == 584
    assert int(by_key[("previously_inspected_2024", "XGBoost")]["n"]) == 76
