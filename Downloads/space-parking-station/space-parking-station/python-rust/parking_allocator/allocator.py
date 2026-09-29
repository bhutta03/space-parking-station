"""Parking allocation logic for the Space Parking Station.

Strategy:
- Best-fit: when a spacecraft requests a bay, assign the SMALLEST free bay
  that can still fit it. This avoids wasting a large interstellar-class bay
  on a small shuttle when a smaller bay would do.
- If no bay fits, the spacecraft is placed in a waiting queue, ordered by
  (priority desc, arrival_time asc) so higher-priority and earlier arrivals
  are served first once a bay frees up.
"""

from __future__ import annotations

import heapq
import itertools

from .models import ParkingBay, Spacecraft, SpacecraftSize


class ParkingStation:
    def __init__(self, bays: list[ParkingBay]):
        self.bays: dict[str, ParkingBay] = {bay.id: bay for bay in bays}
        self._waiting: list[tuple[int, float, int, Spacecraft]] = []
        self._counter = itertools.count()  # stable tie-breaker for heapq

    def request_parking(self, craft: Spacecraft) -> ParkingBay | None:
        """Try to park `craft`. Returns the assigned bay, or None if it had
        to be queued (call `process_queue` later, e.g. after a bay frees up)."""
        bay = self._best_fit_bay(craft)
        if bay is not None:
            bay.occupied_by = craft
            return bay

        # No bay available right now: queue it (min-heap, so negate priority
        # to get "highest priority first").
        heapq.heappush(
            self._waiting, (-craft.priority, craft.arrival_time, next(self._counter), craft)
        )
        return None

    def release(self, bay_id: str) -> Spacecraft | None:
        """Free a bay and immediately try to fill it from the waiting queue.
        Returns the spacecraft that just departed."""
        bay = self.bays[bay_id]
        departing = bay.occupied_by
        bay.occupied_by = None
        self.process_queue()
        return departing

    def process_queue(self) -> list[tuple[Spacecraft, ParkingBay]]:
        """Try to seat as many waiting spacecraft as current free bays allow.
        Returns the list of (spacecraft, bay) pairs that got seated."""
        seated = []
        still_waiting: list[tuple[int, float, int, Spacecraft]] = []

        # Process in priority order; re-queue anything that still doesn't fit.
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
        """Fraction of bays currently occupied, from 0.0 to 1.0."""
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
