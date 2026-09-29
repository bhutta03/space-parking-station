"""Parking allocation logic for the Space Parking Station."""

from __future__ import annotations

import heapq
import itertools

from .models import ParkingBay, Spacecraft, SpacecraftSize


class ParkingStation:
    def __init__(self, bays: list[ParkingBay]):
        self.bays: dict[str, ParkingBay] = {bay.id: bay for bay in bays}
        self._waiting: list[tuple[int, float, int, Spacecraft]] = []
        self._counter = itertools.count()

    def request_parking(self, craft: Spacecraft) -> ParkingBay | None:
        bay = self._best_fit_bay(craft)
        if bay is not None:
            bay.occupied_by = craft
            return bay
        heapq.heappush(
            self._waiting, (-craft.priority, craft.arrival_time, next(self._counter), craft)
        )
        return None

    def release(self, bay_id: str) -> Spacecraft | None:
        bay = self.bays[bay_id]
        departing = bay.occupied_by
        bay.occupied_by = None
        self.process_queue()
        return departing

    def process_queue(self) -> list[tuple[Spacecraft, ParkingBay]]:
        seated = []
        still_waiting: list[tuple[int, float, int, Spacecraft]] = []

        while self._waiting:
            _, _, _, craft = heapq.heappop(self._waiting)
            bay = self._best_fit_bay(craft)
            if bay is not None:
                bay.occupied_by = craft
                seated.append((craft, bay))
            else:
                still_waiting.append((-craft.priority, craft.arrival_time, next(self._counter), craft))

        for item in still_waiting:
            heapq.heappush(self._waiting, item)
        return seated

    def _best_fit_bay(self, craft: Spacecraft) -> ParkingBay | None:
        candidates = [b for b in self.bays.values() if b.can_fit(craft)]
        if not candidates:
            return None
        return min(candidates, key=lambda b: b.max_size)

    def utilization(self) -> float:
        if not self.bays:
            return 0.0
        occupied = sum(1 for b in self.bays.values() if not b.is_free)
        return occupied / len(self.bays)

    def waiting_count(self) -> int:
        return len(self._waiting)

    def status_report(self) -> str:
        lines = [f"Station utilization: {self.utilization():.0%}"]
        for bay in self.bays.values():
            lines.append(f"  {bay}")
        lines.append(f"Waiting: {self.waiting_count()} spacecraft")
        return "\n".join(lines)
