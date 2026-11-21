import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    package_share = get_package_share_directory("gazebo_panda")
    moveit_share = get_package_share_directory(
        "moveit_resources_panda_moveit_config"
    )

    # Reuse the existing Gazebo Panda simulation.
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                package_share,
                "launch",
                "panda_simulation.launch.py",
            )
        )
    )

    # Load the installed Panda MoveIt configuration.
    moveit_config = (
        MoveItConfigsBuilder("moveit_resources_panda")
        .robot_description_semantic(
            file_path="config/panda.srdf"
        )
        .robot_description_kinematics(
            file_path="config/kinematics.yaml"
        )
        .joint_limits(
            file_path="config/joint_limits.yaml"
        )
        .trajectory_execution(
            file_path=os.path.join(
                package_share,
                "config",
                "moveit_controllers.yaml",
            )
        )
        .planning_pipelines(
            pipelines=["ompl"]
        )
        .to_moveit_configs()
    )

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    # Connect the Panda base frame to the world frame.
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="world_to_panda",
        arguments=[
            "0", "0", "0",
            "0", "0", "0",
            "world", "panda_link0",
        ],
    )

    rviz_config = os.path.join(
        moveit_share,
        "launch",
        "moveit.rviz",
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription([
        gazebo_launch,
        static_tf,
        TimerAction(
            period=10.0,
            actions=[move_group, rviz],
        ),
    ])
