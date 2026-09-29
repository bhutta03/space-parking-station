# Space Parking Station

A simulation and allocation engine for docking and parking spacecraft at a
space station, built with Python (allocation logic, orchestration) and
designed to be extended with Rust (performance-critical navigation/docking
checks).

## Overview

Space Parking Station manages a set of parking bays of different sizes and
assigns arriving spacecraft to the best available bay. When the station is
full, spacecraft are queued and served by priority once a bay frees up.

## Features

- **Best-fit allocation** — assigns the smallest bay that still fits the
  spacecraft, so large bays stay free for large spacecraft.
- **Priority queue** — when no bay is free, spacecraft wait in priority order
  (with arrival time as a tiebreaker).
- **Config-driven** — station layout (`config/bays.json`) and simulated
  traffic (`config/arrivals.json`) are plain JSON, no code changes needed to
  try a new scenario.
- **Tested** — core allocation logic has unit test coverage (`tests/`).

## Project structure

```
python-rust/
├── config/
│   ├── bays.json          # station layout: bay IDs and max spacecraft size
│   └── arrivals.json      # simulated spacecraft arrivals
├── parking_allocator/
│   ├── __init__.py
│   ├── models.py           # Spacecraft, ParkingBay, SpacecraftSize
│   ├── allocator.py        # ParkingStation: allocation + queue logic
│   └── config_loader.py    # loads station/arrivals from JSON
├── tests/
│   └── test_allocator.py
├── demo.py                 # runnable simulation
└── requirements.txt
```

## Installation

Requires Python 3.10+.

```bash
cd python-rust
pip install -r requirements.txt
```

## Usage

Run the demo simulation:

```bash
python demo.py
```

Edit `config/bays.json` to change the station's bay layout, or
`config/arrivals.json` to change which spacecraft arrive and when, then
re-run the demo — no code changes required.

Run the test suite:

```bash
pytest tests/
```

## Using it in your own code

```python
from parking_allocator import ParkingBay, ParkingStation, Spacecraft, SpacecraftSize

station = ParkingStation([
    ParkingBay("B1", SpacecraftSize.SHUTTLE),
    ParkingBay("B2", SpacecraftSize.INTERSTELLAR),
])

craft = Spacecraft("Shuttle-1", SpacecraftSize.SHUTTLE)
bay = station.request_parking(craft)  # -> ParkingBay or None if queued

station.release("B1")        # frees the bay and auto-seats the next waiting craft
station.status_report()      # human-readable station summary
```

## Architecture / roadmap

Currently the allocation engine is pure Python. The planned Rust component
will handle performance- and safety-critical work — collision checks,
docking-approach navigation, and real-time telemetry — communicating with
the Python layer via [PyO3](https://pyo3.rs/) bindings. This keeps mission
planning, data analysis, and the allocator itself in Python (fast to
iterate) while safety-critical control logic runs in Rust (fast and
memory-safe at runtime).

## Contributing

Contributions are welcome. Please open an issue or pull request describing
the change. Run the test suite before submitting a PR.

## License

MIT — see [LICENSE](LICENSE).
