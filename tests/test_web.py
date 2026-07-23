from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen

from clinical_demo.web import build_server


class LocalWebTests(unittest.TestCase):
    def setUp(self) -> None:
        runtime_root = Path(__file__).resolve().parent.parent / "runtime"
        runtime_root.mkdir(exist_ok=True)
        self.temp_directory = tempfile.TemporaryDirectory(dir=runtime_root)
        database_path = Path(self.temp_directory.name) / "web-test.sqlite3"
        self.server = build_server("127.0.0.1", 0, database_path)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp_directory.cleanup()

    def test_dashboard_and_run_are_available_locally(self) -> None:
        with urlopen(f"{self.base_url}/api/dashboard", timeout=2) as response:
            initial = json.load(response)
        self.assertIsNone(initial["latest"])

        request = Request(
            f"{self.base_url}/api/run",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=2) as response:
            report = json.load(response)
        self.assertEqual(report["summary"]["total_cases"], 5)

    def test_home_page_is_served(self) -> None:
        with urlopen(self.base_url, timeout=2) as response:
            content = response.read().decode("utf-8")
        self.assertIn("Clinical Nutrition Automation", content)


if __name__ == "__main__":
    unittest.main()
