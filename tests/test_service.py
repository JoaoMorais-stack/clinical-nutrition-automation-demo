from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from clinical_demo.adapters import SyntheticCaseAdapter
from clinical_demo.repository import SQLiteRunRepository
from clinical_demo.service import NutritionWorkflowService


class NutritionWorkflowServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        runtime_root = Path(__file__).resolve().parent.parent / "runtime"
        runtime_root.mkdir(exist_ok=True)
        self.temp_directory = tempfile.TemporaryDirectory(dir=runtime_root)
        database_path = Path(self.temp_directory.name) / "test.sqlite3"
        repository = SQLiteRunRepository(database_path)
        self.service = NutritionWorkflowService(SyntheticCaseAdapter(), repository)

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_full_run_creates_summary_and_history(self) -> None:
        report = self.service.run()

        self.assertEqual(report["summary"]["total_cases"], 5)
        self.assertEqual(report["summary"]["alerts"], 2)
        self.assertIn("Oral", report["distribution"])
        self.assertEqual(len(self.service.dashboard()["history"]), 1)

    def test_focused_run_filters_cases(self) -> None:
        report = self.service.run("North Wing")

        self.assertEqual(report["mode"], "Focused review: North Wing")
        self.assertTrue(report["cases"])
        self.assertTrue(all(item["care_area"] == "North Wing" for item in report["cases"]))

    def test_runs_rotate_between_synthetic_scenarios(self) -> None:
        first = self.service.run()
        second = self.service.run()

        self.assertNotEqual(first["scenario"], second["scenario"])
        self.assertEqual(second["summary"]["total_cases"], 4)

    def test_reset_clears_local_history(self) -> None:
        self.service.run()
        self.service.reset()

        dashboard = self.service.dashboard()
        self.assertIsNone(dashboard["latest"])
        self.assertEqual(dashboard["history"], [])


if __name__ == "__main__":
    unittest.main()
