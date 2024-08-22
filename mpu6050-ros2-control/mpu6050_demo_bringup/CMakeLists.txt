cmake_minimum_required(VERSION 3.8)
project(mpu6050_demo_bringup)

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)

install(
  DIRECTORY config launch 
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
