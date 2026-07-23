from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from clinical_demo.adapters import ClinicalSource
from clinical_demo.models import NutritionCase
from clinical_demo.repository import SQLiteRunRepository


ACTION_BY_RISK = {
    "low": "Routine review",
    "moderate": "Review within the next cycle",
    "high": "Priority dietitian review",
    "critical": "Immediate specialist review",
}


class NutritionWorkflowService:
    def __init__(self, source: ClinicalSource, repository: SQLiteRunRepository) -> None:
        self.source = source
        self.repository = repository

    def _evaluate(self, item: NutritionCase) -> dict[str, Any]:
        case = item.to_dict()
        case["recommended_action"] = ACTION_BY_RISK[item.risk_level]
        case["alert"] = item.risk_level in {"high", "critical"}
        return case

    def run(self, care_area: str | None = None) -> dict[str, Any]:
        scenarios = self.source.scenario_names()
        scenario_name = scenarios[self.repository.count() % len(scenarios)]
        cases = self.source.fetch(scenario_name)
        if care_area:
            cases = [item for item in cases if item.care_area == care_area]

        evaluated = [self._evaluate(item) for item in cases]
        distribution = Counter(item["nutrition_route"] for item in evaluated)
        alerts = sum(1 for item in evaluated if item["alert"])
        follow_ups = sum(1 for item in evaluated if item["follow_up_required"])
        mode = f"Focused review: {care_area}" if care_area else "Full review"
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

        report = {
            "run_id": uuid4().hex[:8].upper(),
            "created_at": created_at,
            "mode": mode,
            "scenario": scenario_name,
            "summary": {
                "total_cases": len(evaluated),
                "alerts": alerts,
                "follow_ups": follow_ups,
                "care_areas": len({item["care_area"] for item in evaluated}),
            },
            "distribution": dict(sorted(distribution.items())),
            "cases": evaluated,
            "events": [
                f"Loaded {len(evaluated)} fictional cases",
                "Applied deterministic nutrition review rules",
                f"Flagged {alerts} priority cases",
                "Stored the run in the local demo database",
            ],
        }
        self.repository.save(report)
        return report

    def dashboard(self) -> dict[str, Any]:
        preview = self.source.fetch(self.source.scenario_names()[0])
        return {
            "latest": self.repository.latest(),
            "history": self.repository.history(),
            "care_areas": sorted({item.care_area for item in preview}),
        }

    def reset(self) -> dict[str, bool]:
        self.repository.reset()
        return {"ok": True}

