
os: UBUNTU 22.04 jammy
ROS2: HUMBLE
install ROS2 by clone this git on your ubuntu >>> https://github.com/linorobot/ros2me.git <<<  
 open terminal type >>> ./install <<< then wait ROS2 auto install by your ubuntu Version (if you use Ubuntu 22.4 this will give you install HUMBLE)

Dev Machine/dev_ws
	created dev_ws and src 
	>>> mkdir -p ~/dev_ws/src <<<
        >>> cd ~/dev_ws/src <<<
	Then clone this git >>> git clone --depth 1 --branch DEV-Machine https://github.com/reaper1947/make_way_bot_ros2.git . <<< 
	go back to build this work_space 
	>>> cd ~/dev_ws/ <<<
	>>> colcon build <<<
	
Robot Machine/robot_ws
	created robot_ws and src 
	>>> mkdir -p ~/robot_ws/src <<<
        >>> cd ~/robot_ws/src <<<
	Then clone this git >>> git clone --depth 1 --branch ROBOT-Machine https://github.com/reaper1947/make_way_bot_ros2.git . <<< 
	Then clone this git >>> git clone https://github.com/reaper1947/ros_arduino_bridge.git <<<
	Then clone this git >>> git clone https://github.com/Slamtec/sllidar_ros2.git <<<
	go back to build this work_space 
	>>> cd ~/robot_ws/ <<<
	>>> colcon build <<<	 

HOW TO USE THIS ROBOT ON GAZEBO (simulation)
 Only ON DEV MACHINE 
	>>> ros2 launch nbt_bot launch_sim.launch.py world:=./src/nbt_bot/worlds/test1.world <<< or you created a new world and modify your world 
	>>> rviz2 -d src/nbt_bot/config/map.rviz <<<  
	
HOW TO USE THIS ROBOT ON REAL
 firstly you need to sure about connecting ROS2 on network  just test about sub-pub on topic
 now ssh robot machine from dev machine Ex. >>> ssh robot@192.168.1.xx <<< 
 
 ON ROBOT MACHINE
 	run this command on 3 terminal ssh
 	>>> ros2 launch nbt_bot launch_robot.launch.py <<<  Start ROBOT
>>> ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/ttyUSB0 -p serial_baudrate:=460800 -p frame_id:=laser_frame -p angle_compensate:=true -p scan_mode:=Standard <<< Start LIDAR
 	>>> ros2 launch nbt_bot camera.launch.py  <<<
 	
 ON DEV MACHINE
        >>> ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/nbt_bot/config/mapper_params_online_async.yaml use_sim_time:=false <<< mapping
        >>> rviz2 -d src/nbt_bot/config/all.rviz <<<                                                                                              Monitor and command on RVIZ2
        >>> ros2 launch nbt_bot joystick.launch.py <<<  control by Joystick 
	>>> ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped <<<                                        control by Keyboard
	Next is start nav2
	>>> ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=test.yaml -p use_sim_time:=false <<<   change NBT_BIG.yaml to your .yaml      RUN map_server
	>>> ros2 run nav2_util lifecycle_bringup map_server <<<                                                                                                  RUN UTILL server
	>>> ros2 launch nav2_bringup localization_launch.py map:=./test.yaml use_sim_time:=false <<<                   change ./test.yaml to your .yaml
	>>> ros2 launch nav2_bringup navigation_launch.py use_sim_time:=false <<<                                                                                RUN nav2


Robot WEB SERVER FOXGLOVE
robot ws
ros2 run web_video_server web_video_server
 ros2 launch nbt_bot camera.launch.py 
 ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /home/nbt/robot_ws/src/usb_cam/config/params_1.yaml
 ros2 launch nbt_bot launch_robot.launch.py

dev ws
ros2 launch nbt_bot joystick.launch.py
ros2 run rosbridge_server  rosbridge_websocket
ros2 run rosapi rosapi_node
https://app.foxglove.dev/taweeporn-maneesin/view?ds=rosbridge-websocket&ds.url=ws%3A%2F%2Flocalhost%3A9090&layoutId=ce4e0a06-a750-41a9-8e0b-db52fffeaf78
























































