# MakeWayBot ROS2

## Overview

MakeWayBot ROS2 is a project designed for robotic applications using ROS2 Humble. It includes both simulation capabilities in Gazebo and real-world deployment instructions. This guide covers installation, usage, directory structure, predefined movements, known issues, troubleshooting, contributing, and future plans.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Files and Directories](#files-and-directories)
- [Predefined Movements](#predefined-movements)
- [Known Issues](#known-issues)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Future](#future)

## Installation

### Install ROS 2 Humble

1. Clone the repository:
    ```bash
    git clone https://github.com/linorobot/ros2me.git
    ```

2. Open a terminal and run the installation script:
    ```bash
    ./install
    ```

### Development Machine Setup

1. Create and set up the workspace:
    ```bash
    mkdir -p ~/dev_ws/src
    cd ~/dev_ws/src
    ```

2. Clone the `make_way_bot_ros2` repository:
    ```bash
    git clone --depth 1 --branch DEV-Machine https://github.com/reaper1947/make_way_bot_ros2.git .
    ```

3. Build the workspace:
    ```bash
    cd ~/dev_ws
    colcon build
    ```

### Robot Machine Setup

1. Create and set up the workspace:
    ```bash
    mkdir -p ~/robot_ws/src
    cd ~/robot_ws/src
    ```

2. Clone the required repositories:
    ```bash
    git clone --depth 1 --branch ROBOT-Machine https://github.com/reaper1947/make_way_bot_ros2.git .
    git clone https://github.com/reaper1947/ros_arduino_bridge.git
    git clone https://github.com/Slamtec/sllidar_ros2.git
    ```

3. Build the workspace:
    ```bash
    cd ~/robot_ws
    colcon build
    ```

## Usage

### Using the Robot in Simulation (Gazebo)

#### On Development Machine

1. Launch the simulation:
    ```bash
    ros2 launch nbt_bot launch_sim.launch.py world:=./src/nbt_bot/worlds/test1.world
    ```

2. Launch RViz2 for visualization:
    ```bash
    rviz2 -d src/nbt_bot/config/map.rviz
    ```

### Using the Robot in Real

#### Network Configuration

Ensure that ROS2 is properly connected on the network. Test the sub-pub on topics.

#### On Robot Machine

1. SSH into the robot machine from the development machine:
    ```bash
    ssh robot@192.168.1.xx
    ```

2. Run the following commands on the robot machine in separate terminals:

    - **Terminal 1: Start the robot:**
        ```bash
        ros2 launch nbt_bot launch_robot.launch.py
        ```

    - **Terminal 2: Start the LIDAR:**
        ```bash
        ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/ttyUSB0 -p serial_baudrate:=460800 -p frame_id:=laser_frame -p angle_compensate:=true -p scan_mode:=Standard
        ```

    - **Terminal 3: Start the camera:**
        ```bash
        ros2 launch nbt_bot camera.launch.py
        ```

#### On Development Machine

1. Start SLAM mapping:
    ```bash
    ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/nbt_bot/config/mapper_params_online_async.yaml use_sim_time:=false
    ```

2. Launch RViz2 to monitor and command:
    ```bash
    rviz2 -d src/nbt_bot/config/all.rviz
    ```

3. Control the robot with a joystick:
    ```bash
    ros2 launch nbt_bot joystick.launch.py
    ```

4. Control the robot with a keyboard:
    ```bash
    ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
    ```

## Navigation (Nav2)

To start navigation, open multiple terminals on the development machine and run the following commands:

- **Terminal 1: Start Map Server**
    ```bash
    ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=test.yaml -p use_sim_time:=false
    ```

- **Terminal 2: Start Lifecycle Manager**
    ```bash
    ros2 run nav2_util lifecycle_bringup map_server
    ```

- **Terminal 3: Start Localization**
    ```bash
    ros2 launch nav2_bringup localization_launch.py map:=./test.yaml use_sim_time:=false
    ```

- **Terminal 4: Start Navigation**
    ```bash
    ros2 launch nav2_bringup navigation_launch.py use_sim_time:=false
    ```

## Files and Directories

- **`~/dev_ws`**: Development workspace.
- **`~/robot_ws`**: Robot workspace.
- **`src/nbt_bot/`**: Contains launch files, configurations, and mappings.
- **`src/ros_arduino_bridge/`**: ROS-Arduino bridge integration.
- **`src/sllidar_ros2/`**: LIDAR integration.

## Predefined Movements

Details on predefined movements will be added here. 

## Known Issues

- (List any known issues or limitations here.)

## Troubleshooting

- **Problem**: (Describe common problems and their solutions.)

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## Future

(coming....)

## License

This project is licensed under the [MIT License](LICENSE).
