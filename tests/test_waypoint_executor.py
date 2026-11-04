import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import yaml

from src.waypoint_executor import WaypointExecutor


class TestWaypointValidation(unittest.TestCase):
    def setUp(self):
        self.valid_config = {
            "joint_names": ["joint1", "joint2"],
            "trajectory_duration_sec": 2.5,
            "waypoints": [[0.0, 1.0], [0.5, -0.5]],
        }

    def validate_config(self, config):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "waypoints.yaml"
            path.write_text(
                yaml.safe_dump(config), encoding="utf-8"
            )
            return WaypointExecutor.load_and_validate(path)

    def test_valid_configuration(self):
        names, waypoints, duration = self.validate_config(
            self.valid_config
        )
        self.assertEqual(names, ["joint1", "joint2"])
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(duration, 2.5)

    def test_rejects_duplicate_joint_names(self):
        config = dict(self.valid_config)
        config["joint_names"] = ["joint1", "joint1"]
        with self.assertRaises(ValueError):
            self.validate_config(config)

    def test_rejects_wrong_waypoint_length(self):
        config = dict(self.valid_config)
        config["waypoints"] = [[0.0]]
        with self.assertRaises(ValueError):
            self.validate_config(config)

    def test_rejects_non_finite_values(self):
        config = dict(self.valid_config)
        config["waypoints"] = [[float("nan"), 1.0]]
        with self.assertRaises(ValueError):
            self.validate_config(config)

    def test_rejects_non_positive_duration(self):
        config = dict(self.valid_config)
        config["trajectory_duration_sec"] = 0
        with self.assertRaises(ValueError):
            self.validate_config(config)


if __name__ == "__main__":
    unittest.main()
