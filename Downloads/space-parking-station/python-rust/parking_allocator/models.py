"""Core data models for the Space Parking Station allocator."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class SpacecraftSize(IntEnum):
    """Size classes for spacecraft, ordered smallest to largest."""

    SHUTTLE = 1
    FREIGHTER = 2
    CRUISER = 3
    INTERSTELLAR = 4


@dataclass
class Spacecraft:
    """A spacecraft requesting a parking bay."""

    id: str
    size: SpacecraftSize
    priority: int = 0
    arrival_time: float = 0.0

    def __repr__(self) -> str:
        return f"Spacecraft({self.id}, {self.size.name}, priority={self.priority})"


@dataclass
class ParkingBay:
    """A single parking bay at the station."""

    id: str
    max_size: SpacecraftSize
    occupied_by: Spacecraft | None = field(default=None)

    @property
    def is_free(self) -> bool:
        return self.occupied_by is None

    def can_fit(self, craft: Spacecraft) -> bool:
        return self.is_free and craft.size <= self.max_size

    def __repr__(self) -> str:
        status = "free" if self.is_free else f"occupied by {self.occupied_by.id}"
        return f"Bay({self.id}, max={self.max_size.name}, {status})"
