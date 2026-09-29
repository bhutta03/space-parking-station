//! Simple sphere-sphere collision detection between spacecraft.

use crate::vector::Vec3;

pub fn is_collision(pos_a: Vec3, radius_a: f64, pos_b: Vec3, radius_b: f64) -> bool {
    pos_a.distance(&pos_b) < (radius_a + radius_b)
}

pub fn check_collisions(crafts: &[(Vec3, f64)]) -> Vec<(usize, usize)> {
    let mut collisions = Vec::new();
    for i in 0..crafts.len() {
        for j in (i + 1)..crafts.len() {
            let (pos_a, radius_a) = crafts[i];
            let (pos_b, radius_b) = crafts[j];
            if is_collision(pos_a, radius_a, pos_b, radius_b) {
                collisions.push((i, j));
            }
        }
    }
    collisions
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_no_collision_far_apart() {
        let a = (Vec3::new(0.0, 0.0, 0.0), 1.0);
        let b = (Vec3::new(10.0, 0.0, 0.0), 1.0);
        assert!(!is_collision(a.0, a.1, b.0, b.1));
    }

    #[test]
    fn test_collision_when_overlapping() {
        let a = (Vec3::new(0.0, 0.0, 0.0), 2.0);
        let b = (Vec3::new(3.0, 0.0, 0.0), 2.0);
        assert!(is_collision(a.0, a.1, b.0, b.1));
    }

    #[test]
    fn test_check_collisions_finds_pair() {
        let crafts = vec![
            (Vec3::new(0.0, 0.0, 0.0), 1.0),
            (Vec3::new(0.5, 0.0, 0.0), 1.0),
            (Vec3::new(100.0, 0.0, 0.0), 1.0),
        ];
        let collisions = check_collisions(&crafts);
        assert_eq!(collisions, vec![(0, 1)]);
    }

    #[test]
    fn test_no_collisions_when_all_spaced_out() {
        let crafts = vec![
            (Vec3::new(0.0, 0.0, 0.0), 1.0),
            (Vec3::new(50.0, 0.0, 0.0), 1.0),
            (Vec3::new(100.0, 0.0, 0.0), 1.0),
        ];
        assert!(check_collisions(&crafts).is_empty());
    }
}
