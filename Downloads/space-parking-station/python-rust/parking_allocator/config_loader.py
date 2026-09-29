"""Load a ParkingStation and a list of Spacecraft arrivals from JSON config files."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ParkingBay, Spacecraft, SpacecraftSize


def load_station_config(path: str | Path) -> list[ParkingBay]:
    data = json.loads(Path(path).read_text())
    return [
        ParkingBay(id=b["id"], max_size=SpacecraftSize[b["max_size"]])
        for b in data["bays"]
    ]


def load_arrivals_config(path: str | Path) -> list[Spacecraft]:
    data = json.loads(Path(path).read_text())
    return [
        Spacecraft(
            id=a["id"],
            size=SpacecraftSize[a["size"]],
            priority=a.get("priority", 0),
            arrival_time=a.get("arrival_time", 0.0),
        )
        for a in data["arrivals"]
    ]
