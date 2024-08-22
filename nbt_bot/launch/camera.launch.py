import os

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():



    return LaunchDescription([

        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            output='screen',
            namespace='camera',
            parameters=[{
                'image_size': [640,480],
                'time_per_frame': [1, 6],
                'camera_frame_id': 'camera_link_optical'
                }]
    )
    ])
