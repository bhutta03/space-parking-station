"""Runnable demo of the Space Parking Station allocator."""

from pathlib import Path

from parking_allocator import ParkingStation, load_arrivals_config, load_station_config

CONFIG_DIR = Path(__file__).parent / "config"


def main():
    bays = load_station_config(CONFIG_DIR / "bays.json")
    arrivals = load_arrivals_config(CONFIG_DIR / "arrivals.json")
    station = ParkingStation(bays)

    print("=== Arrivals ===")
    for craft in arrivals:
        bay = station.request_parking(craft)
        if bay:
            print(f"{craft.id} -> parked at {bay.id}")
        else:
            print(f"{craft.id} -> no bay available, queued (priority={craft.priority})")

    print("\n=== Station status ===")
    print(station.status_report())

    occupied_bays = [b for b in station.bays.values() if not b.is_free]
    if occupied_bays and station.waiting_count() > 0:
        bay_to_free = occupied_bays[0]
        print(f"\n=== Freeing {bay_to_free.id} ({bay_to_free.occupied_by.id} departs) ===")
        station.release(bay_to_free.id)
        print(station.status_report())


if __name__ == "__main__":
    main()
