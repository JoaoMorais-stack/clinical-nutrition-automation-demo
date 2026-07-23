from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from clinical_demo.models import NutritionCase


class ClinicalSource(Protocol):
    def scenario_names(self) -> list[str]: ...

    def fetch(self, scenario_name: str) -> list[NutritionCase]: ...


class SyntheticCaseAdapter:
    """Loads deterministic, fictional cases from a local fixture."""

    def __init__(self, fixture_path: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parent.parent
        self.fixture_path = fixture_path or project_root / "fixtures" / "synthetic_cases.json"

    def _load(self) -> dict:
        with self.fixture_path.open("r", encoding="utf-8") as fixture:
            return json.load(fixture)

    def scenario_names(self) -> list[str]:
        return list(self._load()["scenarios"])

    def fetch(self, scenario_name: str) -> list[NutritionCase]:
        scenarios = self._load()["scenarios"]
        if scenario_name not in scenarios:
            raise ValueError(f"Unknown synthetic scenario: {scenario_name}")
        return [NutritionCase.from_dict(item) for item in scenarios[scenario_name]]

