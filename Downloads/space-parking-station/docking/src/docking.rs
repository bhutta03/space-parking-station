//! Evaluates whether a spacecraft's approach to a docking bay is safe.

use crate::vector::Vec3;

#[derive(Debug, Clone, Copy)]
pub struct DockingBay {
    pub position: Vec3,
    pub approach_radius: f64,
    pub max_approach_speed: f64,
    pub docking_radius: f64,
}

#[derive(Debug, Clone, Copy)]
pub struct ApproachState {
    pub position: Vec3,
    pub velocity: Vec3,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ApproachStatus {
    Docked,
    OnCourse,
    TooFast,
    OffCorridor,
}

impl DockingBay {
    pub fn speed_limit_at(&self, distance: f64) -> f64 {
        let ratio = (distance / self.approach_radius).max(0.1);
        self.max_approach_speed * ratio
    }

    pub fn evaluate_approach(&self, craft: &ApproachState) -> ApproachStatus {
        let distance = self.position.distance(&craft.position);

        if distance <= self.docking_radius {
            return ApproachStatus::Docked;
        }
        if distance > self.approach_radius {
            return ApproachStatus::OffCorridor;
        }

        let speed = craft.velocity.magnitude();
        if speed > self.speed_limit_at(distance) {
            ApproachStatus::TooFast
        } else {
            ApproachStatus::OnCourse
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn test_bay() -> DockingBay {
        DockingBay {
            position: Vec3::new(0.0, 0.0, 0.0),
            approach_radius: 100.0,
            max_approach_speed: 10.0,
            docking_radius: 2.0,
        }
    }

    #[test]
    fn test_docked_when_within_docking_radius() {
        let bay = test_bay();
        let craft = ApproachState {
            position: Vec3::new(1.0, 0.0, 0.0),
            velocity: Vec3::zero(),
        };
        assert_eq!(bay.evaluate_approach(&craft), ApproachStatus::Docked);
    }

    #[test]
    fn test_off_corridor_when_too_far() {
        let bay = test_bay();
        let craft = ApproachState {
            position: Vec3::new(200.0, 0.0, 0.0),
            velocity: Vec3::zero(),
        };
        assert_eq!(bay.evaluate_approach(&craft), ApproachStatus::OffCorridor);
    }

    #[test]
    fn test_on_course_within_speed_limit() {
        let bay = test_bay();
        let craft = ApproachState {
            position: Vec3::new(50.0, 0.0, 0.0),
            velocity: Vec3::new(1.0, 0.0, 0.0),
        };
        assert_eq!(bay.evaluate_approach(&craft), ApproachStatus::OnCourse);
    }

    #[test]
    fn test_too_fast_near_bay() {
        let bay = test_bay();
        let craft = ApproachState {
            position: Vec3::new(5.0, 0.0, 0.0),
            velocity: Vec3::new(5.0, 0.0, 0.0),
        };
        assert_eq!(bay.evaluate_approach(&craft), ApproachStatus::TooFast);
    }
}
