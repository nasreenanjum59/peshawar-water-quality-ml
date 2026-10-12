"""Unit checks for temporal design and archived manuscript results.

Run with: python -m unittest discover -s tests -p 'test_*.py' -v
"""
from __future__ import annotations

import csv
import importlib.util
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "peshawar_ml.py"
RESULTS = ROOT / "results"

spec = importlib.util.spec_from_file_location("peshawar_ml", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MLPackageTests(unittest.TestCase):
    def test_operating_threshold_targets_validation_sensitivity(self):
        observed = np.array([1, 1, 1, 1, 1, 0, 0])
        probs = np.array([0.97, 0.83, 0.71, 0.63, 0.49, 0.5, 0.1])
        threshold = module.sens_threshold(observed, probs, 0.8)
        result = module.operating_point(observed, probs, threshold)
        self.assertAlmostEqual(threshold, 0.63)
        self.assertAlmostEqual(result["sensitivity"], 0.8)
        self.assertEqual(result["TN"] + result["FP"] + result["FN"] + result["TP"], 7)

    def test_every_rolling_year_has_past_only_inner_validation(self):
        with (RESULTS / "02_fold_hyperparameters.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 9 * 8)
        for row in rows:
            with self.subTest(prediction_year=row["prediction_year"], model=row["model"]):
                year = int(row["prediction_year"])
                self.assertGreaterEqual(year, 2016)
                self.assertLessEqual(year, 2024)
                self.assertEqual(int(row["inner_train_end_year"]), year - 3)
                self.assertEqual(int(row["inner_validation_start"]), year - 2)
                self.assertEqual(int(row["inner_validation_end"]), year - 1)

    def test_archived_headline_results_match_manuscript(self):
        with (RESULTS / "05_main_aggregated_results.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 16)
        by_key = {(r["period"], r["model"]): r for r in rows}
        wanted = {
            ("rolling_2016_2023", "Logistic regression"): 0.6967712802,
            ("rolling_2016_2023", "B2 source and season"): 0.6879515692,
            ("rolling_2016_2023", "XGBoost"): 0.6696489049,
            ("previously_inspected_2024", "XGBoost"): 0.7038556194,
        }
        for key, auc in wanted.items():
            with self.subTest(model=key):
                self.assertAlmostEqual(float(by_key[key]["AUC"]), auc, delta=1e-8)
        self.assertEqual(int(by_key[("rolling_2016_2023", "Logistic regression")]["n"]), 584)
        self.assertEqual(int(by_key[("previously_inspected_2024", "XGBoost")]["n"]), 76)


if __name__ == "__main__":
    unittest.main()
