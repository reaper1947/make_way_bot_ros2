# Launch file to start the robot state publisher node

import os

from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Set the path to different files and folders
    pkg_description = FindPackageShare(package='mpu6050_demo_description').find('mpu6050_demo_description')
    urdf_model_path = os.path.join(pkg_description, 'urdf/mpu6050.urdf.xacro')
    robot_description_config = Command(['xacro ', urdf_model_path])

    # Robot state publisher node
    params = {'robot_description': robot_description_config}
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[params])

    return LaunchDescription([
        robot_state_publisher_node
    ])