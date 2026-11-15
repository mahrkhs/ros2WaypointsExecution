# Franka Panda – ROS 2 Waypoint Execution

A Python-based ROS 2 project for configuring, validating and processing joint-space waypoints for a Franka Panda robotic arm.

The project combines waypoint validation, ROS 2 trajectory messages and a Panda robot description prepared for Gazebo simulation.

## Features

- Load robot joint configurations from YAML files.
- Validate joint names, waypoint dimensions and numeric values.
- Generate ROS 2 `JointTrajectory` messages.
- Test waypoint processing in dry-run mode.
- Integrate the Franka Panda URDF model.
- Configure Gazebo and ROS 2 controllers.

## How It Works

1. Load joint names and waypoints from a YAML file.
2. Validate the configuration.
3. Generate ROS 2 trajectory messages.
4. Process waypoints in dry-run mode without moving a robot.


## Project Structure

```text
ros2WaypointsExecution/
├── config/
├── gazebo_panda/
├── launch/
├── resource/
├── tests/
├── urdf/
├── package.xml
├── setup.py
└── README.md
```

## Installation

Build the ROS 2 package:

```bash
colcon build --symlink-install
source install/setup.bash
```

## Run the Waypoint Executor

```bash
ros2 run gazebo_panda waypoint_executor
```

Dry-run mode is enabled by default.

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```

