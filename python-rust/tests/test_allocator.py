import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parking_allocator import ParkingBay, ParkingStation, Spacecraft, SpacecraftSize


def make_station():
    bays = [
        ParkingBay("B1", SpacecraftSize.SHUTTLE),
        ParkingBay("B2", SpacecraftSize.FREIGHTER),
        ParkingBay("B3", SpacecraftSize.INTERSTELLAR),
    ]
    return ParkingStation(bays)


def test_assigns_smallest_fitting_bay():
    station = make_station()
    craft = Spacecraft("S1", SpacecraftSize.SHUTTLE)
    bay = station.request_parking(craft)
    assert bay is not None
    assert bay.id == "B1"  # best-fit, not the oversized B3


def test_falls_back_to_larger_bay_when_smaller_ones_taken():
    station = make_station()
    station.request_parking(Spacecraft("S1", SpacecraftSize.SHUTTLE))
    bay = station.request_parking(Spacecraft("S2", SpacecraftSize.SHUTTLE))
    assert bay.id == "B2"  # B1 taken, next smallest that fits is B2


def test_queues_when_no_bay_fits():
    station = make_station()
    station.request_parking(Spacecraft("S1", SpacecraftSize.INTERSTELLAR))
    bay = station.request_parking(Spacecraft("S2", SpacecraftSize.INTERSTELLAR))
    assert bay is None
    assert station.waiting_count() == 1


def test_release_seats_next_waiting_craft():
    station = make_station()
    station.request_parking(Spacecraft("S1", SpacecraftSize.INTERSTELLAR))
    station.request_parking(Spacecraft("S2", SpacecraftSize.INTERSTELLAR))
    assert station.waiting_count() == 1

    departing = station.release("B3")
    assert departing.id == "S1"
    assert station.waiting_count() == 0
    assert station.bays["B3"].occupied_by.id == "S2"


def test_priority_is_served_first():
    station = make_station()
    station.request_parking(Spacecraft("S1", SpacecraftSize.INTERSTELLAR))
    station.request_parking(Spacecraft("LOW", SpacecraftSize.INTERSTELLAR, priority=0, arrival_time=1))
    station.request_parking(Spacecraft("HIGH", SpacecraftSize.INTERSTELLAR, priority=10, arrival_time=2))

    station.release("B3")
    assert station.bays["B3"].occupied_by.id == "HIGH"
