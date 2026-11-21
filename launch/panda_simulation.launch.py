
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_name = "gazebo_panda"
    package_share = get_package_share_directory(package_name)

    xacro_file = os.path.join(
        package_share, "urdf", "panda.urdf.xacro"
    )

    controller_config = os.path.join(
        package_share, "config", "panda_controllers.yaml"
    )

    robot_description = ParameterValue(
        Command([
            "xacro ",
            xacro_file,
            " controllers_file:=",
            controller_config,
        ]),
        value_type=str,
    )

    gazebo = ExecuteProcess(
        cmd=[
            "gazebo",
            "--verbose",
            "-s", "libgazebo_ros_init.so",
            "-s", "libgazebo_ros_factory.so",
        ],
        output="screen",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": robot_description,
            "publish_robot_description": True,
        }],
    )

    spawn_panda = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="panda_spawner",
        output="screen",
        arguments=[
            "-topic", "/robot_description",
            "-entity", "panda",
            "-timeout", "120",
        ],
    )

    start_controllers = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_panda,
            on_exit=[
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["joint_state_broadcaster"],
                    output="screen",
                ),
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["joint_trajectory_controller"],
                    output="screen",
                ),
            ],
        )
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_panda,
        start_controllers,
    ])
