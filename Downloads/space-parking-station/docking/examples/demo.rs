//! Run with: cargo run --example demo

use docking::{ApproachState, DockingBay, Vec3, check_collisions};

fn main() {
    let bay = DockingBay {
        position: Vec3::new(0.0, 0.0, 0.0),
        approach_radius: 100.0,
        max_approach_speed: 10.0,
        docking_radius: 2.0,
    };

    let ships = vec![
        ("Shuttle-Alpha", ApproachState { position: Vec3::new(80.0, 0.0, 0.0), velocity: Vec3::new(-6.0, 0.0, 0.0) }),
        ("Freighter-01", ApproachState { position: Vec3::new(10.0, 0.0, 0.0), velocity: Vec3::new(-8.0, 0.0, 0.0) }),
        ("Cruiser-Zeta", ApproachState { position: Vec3::new(150.0, 0.0, 0.0), velocity: Vec3::new(-5.0, 0.0, 0.0) }),
        ("Shuttle-Beta", ApproachState { position: Vec3::new(1.0, 0.0, 0.0), velocity: Vec3::zero() }),
    ];

    println!("=== Docking approach evaluation ===");
    for (name, state) in &ships {
        let distance = bay.position.distance(&state.position);
        let speed = state.velocity.magnitude();
        let status = bay.evaluate_approach(state);
        println!("{name}: distance={distance:.1}, speed={speed:.1} -> {status:?}");
    }

    println!("\n=== Collision check (radius 1.5 each) ===");
    let positions: Vec<(Vec3, f64)> = ships.iter().map(|(_, s)| (s.position, 1.5)).collect();
    let collisions = check_collisions(&positions);
    if collisions.is_empty() {
        println!("No collisions detected.");
    } else {
        for (i, j) in collisions {
            println!("Collision risk between {} and {}", ships[i].0, ships[j].0);
        }
    }
}
