# ROS 2 Joint-Space Waypoint Validation and Demonstration

A project demonstrating how to load, validate, and process joint-space waypoints for a robot using ROS 2 and Python.

## Project Overview

Robotic applications often require a sequence of joint configurations to describe a robot's intended motion. Before sending trajectory messages to a controller, the configuration should be checked for basic errors.

This project loads waypoint data from a YAML configuration file, validates its structure and numeric values, and demonstrates the processing of each waypoint. It defaults to **dry-run mode**, so it does not publish trajectory commands to a robot.

## Key Features

- Load joint names and waypoint configurations from YAML.
- Validate joint names, waypoint dimensions, numeric values, and trajectory duration.
- Create ROS 2 `JointTrajectory` messages.
- Demonstrate waypoint processing in dry-run mode.
- Support optional message publishing when explicitly enabled.
- Include automated unit tests for configuration validation.

## How It Works

1. **Configuration:** Read joint names, waypoint positions, and trajectory duration from `config/waypoints.yaml`.
2. **Validation:** Check that joint names are unique, each waypoint has the correct number of values, and all positions and durations are valid finite numbers.
3. **Message construction:** Build a ROS 2 `JointTrajectory` message for the current waypoint.
4. **Dry-run demonstration:** Log each waypoint without publishing commands.
5. **Optional publishing:** When dry-run is disabled, publish waypoint messages to the configured topic.

## Project Structure

```text
ros2WaypointsExecution/
├── config/
│   └── waypoints.yaml
├── src/
│   └── waypoint_executor.py
├── tests/
│   └── test_waypoint_executor.py
├── .gitignore
├── LICENSE
└── README.md
```

## Requirements

- Python 3
- ROS 2 with the Python client library (`rclpy`)
- ROS 2 message packages providing `builtin_interfaces` and `trajectory_msgs`
- PyYAML

The ROS 2 environment must be sourced before running the node.

## Run the Demonstration

From the project root, with your ROS 2 environment sourced:

```bash
python3 src/waypoint_executor.py
```

Dry-run mode is enabled by default. The node should report the loaded waypoints and finish without publishing trajectory messages.

## Run the Tests

```bash
python3 -m unittest discover -s tests -v
```


## License

See the `LICENSE` file.