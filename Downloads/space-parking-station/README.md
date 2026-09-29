# Space Parking Station

A simulation and allocation engine for docking and parking spacecraft at a
space station, built with Python (allocation logic, orchestration) and Rust
(docking safety checks), with an interactive dashboard for demonstration.

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
  traffic (`config/arrivals.json`) are plain JSON.
- **Docking safety checks (Rust)** — evaluates whether an approach is safe
  (on course, too fast, off corridor, or docked) and detects collisions
  between spacecraft.
- **Interactive dashboard** — visualizes bay occupancy, the waiting queue,
  and a live event log; lets you send new arrivals and release bays.
- **Tested** — Python core has full unit test coverage; Rust has unit tests
  written (see EVALUATION.md for verification status).

## Project structure

```
python-rust/
├── config/
│   ├── bays.json
│   └── arrivals.json
├── parking_allocator/
│   ├── __init__.py
│   ├── models.py
│   ├── allocator.py
│   └── config_loader.py
├── tests/
│   └── test_allocator.py
├── demo.py
└── requirements.txt

docking/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── vector.rs
│   ├── docking.rs
│   └── collision.rs
└── examples/
    └── demo.rs

dashboard/
└── index.html      # interactive dashboard, open directly in a browser
```

## Installation & usage — Python

```bash
cd python-rust
pip install -r requirements.txt
python demo.py
pytest tests/
```

## Installation & usage — Rust

```bash
cd docking
cargo test
cargo run --example demo
```

## Dashboard

Open `dashboard/index.html` directly in any browser — no build step or
server required. It ports the same best-fit + priority-queue logic to
JavaScript for a live, clickable demo: send new arrivals, release bays, and
watch the queue drain.

## Using the allocator in your own code

```python
from parking_allocator import ParkingBay, ParkingStation, Spacecraft, SpacecraftSize

station = ParkingStation([
    ParkingBay("B1", SpacecraftSize.SHUTTLE),
    ParkingBay("B2", SpacecraftSize.INTERSTELLAR),
])

craft = Spacecraft("Shuttle-1", SpacecraftSize.SHUTTLE)
bay = station.request_parking(craft)
station.release("B1")
station.status_report()
```

## Architecture / roadmap

- **`python-rust/`** (Python) — parking allocation, mission planning.
- **`docking/`** (Rust) — docking-approach evaluation and collision checks.
- **`dashboard/`** (JS) — standalone visual demo of the allocation logic.

These three currently run independently. The next step is a PyO3 bridge so
the Python allocator can call into the Rust docking checks directly. See
`EVALUATION.md` for a full status report and known gaps.

## Contributing

Contributions are welcome. Please open an issue or pull request describing
the change. Run the relevant test suite before submitting a PR.

## License

MIT — see [LICENSE](LICENSE).
