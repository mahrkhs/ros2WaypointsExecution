
#!/usr/bin/env python3
"""Validate and demonstrate joint-space waypoints using ROS 2."""

import math
from pathlib import Path

import rclpy
import yaml
from builtin_interfaces.msg import Duration
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class WaypointExecutor(Node):
    """Load, validate, and process joint-space waypoint configurations."""

    def __init__(self):
        super().__init__("waypoint_executor")

        self.declare_parameter(
            "config_file",
            str(Path.cwd() / "config" / "waypoints.yaml"),
        )
        self.declare_parameter(
            "trajectory_topic",
            "/joint_trajectory_controller/joint_trajectory",
        )
        self.declare_parameter("dry_run", True)

        self.dry_run = bool(self.get_parameter("dry_run").value)
        config_path = Path(self.get_parameter("config_file").value)
        self.topic = self.get_parameter("trajectory_topic").value

        self.joint_names, self.waypoints, self.duration = (
            self.load_and_validate(config_path)
        )

        self.publisher = self.create_publisher(
            JointTrajectory, self.topic, 10
        )
        self.index = 0
        self.timer = self.create_timer(5.0, self.process_next)

        self.get_logger().info(
            f"Loaded {len(self.waypoints)} waypoints for "
            f"{len(self.joint_names)} joints."
        )

        if self.dry_run:
            self.get_logger().info(
                "Dry-run enabled: no trajectory messages will be published."
            )
        else:
            self.get_logger().warning(
                f"Live publishing enabled on {self.topic}. "
                "Verify the robot, controller, and joint limits first."
            )

    @staticmethod
    def load_and_validate(path):
        """Load YAML and validate waypoint dimensions and numeric values."""
        with path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            raise ValueError("Configuration must be a YAML mapping.")

        names = config.get("joint_names")
        waypoints = config.get("waypoints")
        duration = config.get("trajectory_duration_sec")

        if not isinstance(names, list) or not names:
            raise ValueError("joint_names must be a non-empty list.")
        if not all(isinstance(name, str) and name.strip() for name in names):
            raise ValueError("Every joint name must be a non-empty string.")
        if len(set(names)) != len(names):
            raise ValueError("Joint names must be unique.")

        if not isinstance(waypoints, list) or not waypoints:
            raise ValueError("waypoints must be a non-empty list.")

        if isinstance(duration, bool) or not isinstance(
            duration, (int, float)
        ):
            raise ValueError("trajectory_duration_sec must be numeric.")
        duration = float(duration)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("Trajectory duration must be finite and positive.")

        validated_waypoints = []
        for index, waypoint in enumerate(waypoints):
            if not isinstance(waypoint, list):
                raise ValueError(f"Waypoint {index + 1} must be a list.")
            if len(waypoint) != len(names):
                raise ValueError(
                    f"Waypoint {index + 1} has {len(waypoint)} values; "
                    f"expected {len(names)}."
                )

            values = []
            for value in waypoint:
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)
                ):
                    raise ValueError(
                        f"Waypoint {index + 1} contains a non-finite "
                        "or non-numeric value."
                    )
                values.append(float(value))

            validated_waypoints.append(values)

        return names, validated_waypoints, duration

    def process_next(self):
        """Display a waypoint or publish it, depending on dry-run mode."""
        if self.index >= len(self.waypoints):
            status = "Dry-run complete." if self.dry_run else (
                "All waypoint messages published; execution is unconfirmed."
            )
            self.get_logger().info(status)
            self.timer.cancel()
            return

        message = JointTrajectory()
        message.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = self.waypoints[self.index]
        point.time_from_start = Duration(
            sec=int(self.duration),
            nanosec=round(
                (self.duration - int(self.duration)) * 1_000_000_000
            ),
        )
        message.points.append(point)

        waypoint_number = self.index + 1
        total = len(self.waypoints)

        if self.dry_run:
            self.get_logger().info(
                f"[DRY RUN] Waypoint {waypoint_number}/{total}: "
                f"{self.waypoints[self.index]}"
            )
        else:
            self.publisher.publish(message)
            self.get_logger().info(
                f"Published waypoint message {waypoint_number}/{total}; "
                "robot execution has not been confirmed."
            )

        self.index += 1



def main(args=None):
    rclpy.init(args=args)
    node = None

    try:
        node = WaypointExecutor()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Configuration error: {error}")
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

