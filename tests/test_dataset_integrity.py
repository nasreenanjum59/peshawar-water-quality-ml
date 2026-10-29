"""Check input-file identity and the ML cohort without altering records."""
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pandas as pd

DATASET = Path(__file__).resolve().parents[1] / "data" / "WQ_Peshawar_2009-2024_analysis_ready.xlsx"
EXPECTED_SHA256 = "eecf1f7d53ff88c33020862ad0bd585ea85c965cad608b88f38f97f1e2655369"


class DatasetIntegrityTests(unittest.TestCase):
    def test_workbook_sha256(self):
        self.assertTrue(DATASET.is_file(), f"Dataset missing: {DATASET}")
        actual = hashlib.sha256(DATASET.read_bytes()).hexdigest()
        self.assertEqual(actual, EXPECTED_SHA256)

    def test_cohort_counts_and_dictionary(self):
        data = pd.read_excel(DATASET, sheet_name="analysis_data")
        dictionary = pd.read_excel(DATASET, sheet_name="data_dictionary")
        self.assertEqual(data.shape, (1800, 40))
        self.assertEqual(len(dictionary), 40)
        self.assertEqual(data["sample_id"].nunique(), 1800)
        self.assertEqual(data["source"].value_counts().to_dict(),
                         {"river": 600, "tap": 600, "tube_well": 600})
        cohort = data.loc[data["source"].isin(["tap", "tube_well"])]
        self.assertEqual(len(cohort), 1200)
        self.assertEqual(int((cohort["ecoli_cfu_100ml"] > 0).sum()), 849)


if __name__ == "__main__":
    unittest.main()
