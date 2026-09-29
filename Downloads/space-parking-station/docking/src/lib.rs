//! Docking approach evaluation and collision checking for Space Parking
//! Station. Pure `std`, no external dependencies.

pub mod collision;
pub mod docking;
pub mod vector;

pub use collision::{check_collisions, is_collision};
pub use docking::{ApproachState, ApproachStatus, DockingBay};
pub use vector::Vec3;
