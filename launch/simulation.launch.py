"""Start an empty Gazebo Classic simulation for waypoint-development demos."""

from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():
    """Launch Gazebo Classic with ROS 2 factory support."""
    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=[
                    "gazebo",
                    "--verbose",
                    "-s",
                    "libgazebo_ros_factory.so",
                ],
                output="screen",
            )
        ]
    )
