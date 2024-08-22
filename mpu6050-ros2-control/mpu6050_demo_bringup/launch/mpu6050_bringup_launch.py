import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Set the path to different files and folders
    pkg_path= FindPackageShare(package='mpu6050_demo_bringup').find('mpu6050_demo_bringup')
    controller_params_file= os.path.join(pkg_path, 'config/controllers.yaml')

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_path, 'launch', 'robot_state_publisher_launch.py')]))

    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])
    
    # Launch controller manager
    controller_manager_node= Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[{'robot_description': robot_description},
                        controller_params_file])
    
    # Delayed controller manager action   
    start_delayed_controller_manager = TimerAction(period=1.0, actions=[controller_manager_node])

    # Spawn joint_state_broadcaser
    joint_state_broadcaster_spawner= Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_broadcaster'])

    # Spawn imu_sensor_broadcaser
    imu_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['imu_broadcaster'])

    return LaunchDescription([
        robot_state_publisher_cmd,
        start_delayed_controller_manager,
        joint_state_broadcaster_spawner,
        imu_broadcaster_spawner
    ])
