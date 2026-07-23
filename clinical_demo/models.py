from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class NutritionCase:
    case_id: str
    display_name: str
    age_band: str
    care_area: str
    room_label: str
    nutrition_route: str
    texture: str
    risk_level: str
    follow_up_required: bool
    note: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NutritionCase":
        return cls(
            case_id=str(data["case_id"]),
            display_name=str(data["display_name"]),
            age_band=str(data["age_band"]),
            care_area=str(data["care_area"]),
            room_label=str(data["room_label"]),
            nutrition_route=str(data["nutrition_route"]),
            texture=str(data["texture"]),
            risk_level=str(data["risk_level"]),
            follow_up_required=bool(data["follow_up_required"]),
            note=str(data["note"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

