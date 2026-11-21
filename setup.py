
import os
from glob import glob

from setuptools import setup

package_name = "gazebo_panda"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],

    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (
            os.path.join("share", package_name, "config", "robot_description"),
            glob("config/robot_description/*.yaml"),
        ),
        (
            os.path.join("share", package_name, "urdf"),
            glob("urdf/*"),
        ),
    ],

    install_requires=["setuptools", "PyYAML"],
    zip_safe=True,
    maintainer="Mahrukh",
    description="Gazebo Classic simulation of a Franka Panda arm with ROS 2 waypoint control.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "waypoint_executor = gazebo_panda.waypoint_executor:main",
        ],
    },
)
