import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np
import math

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        # กรองค่าระยะทางที่เป็น inf ออก


    def scan_callback(self, msg):
        
        print("NUMBER ", len(msg.ranges))
        print("Min ", min(msg.ranges))
        filtered_ranges = [distance for distance in msg.ranges if distance < float('inf')]
        print("Max ", max(filtered_ranges) if filtered_ranges else "No valid ranges")       
        print("min_angle", msg.angle_min)
        print("max_angle", msg.angle_max)
        print("angle_increment", msg.angle_increment)
        print("time_increment", msg.time_increment)
        self.calculate_sq(msg)
        print(" ")


    def calculate_sq(self, msg):
        filtered_ranges = [distance for distance in msg.ranges if distance < float('inf')]
    
        if len(filtered_ranges) < 4:
            self.last_object_time = None
            return

        sorted_filtered_ranges = sorted(filtered_ranges)[:4]  # Get the closest 4 points
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment

        # Find the index for each distance in the original ranges to get angles
        min_indices = [msg.ranges.index(dist) for dist in sorted_filtered_ranges]
        # first_two = sorted_filtered_ranges[:4]  # define index

        num_elements = len(filtered_ranges)  # number of index
        self.get_logger().info(f"The number of elements in Index: {num_elements}")
        # self.get_logger().info(f"First two ranges detected: {first_two}")
        # Calculate x, y coordinates for each of the closest points
        points = []
        for i, dist in zip(min_indices, sorted_filtered_ranges):
            angle = angle_min + i * angle_increment
            x = dist * math.cos(angle)
            y = dist * math.sin(angle)
            points.append((x, y))

        # Calculate width and length using the closest two distances
        w = sorted_filtered_ranges[0]
        l = sorted_filtered_ranges[1]

        self.get_logger().info(f"x1, y1: {points[0]}")
        self.get_logger().info(f"x2, y2: {points[1]}")
        self.get_logger().info(f"x3, y3: {points[2]}")
        self.get_logger().info(f"x4, y4: {points[3]}")
        # print(print("intensity", (msg.intensities)))
        # self.get_logger().info(f'number of rays ', len(msg.ranges)) 
        # self.get_logger().info(f'Minimum distance to a value ', min(msg.ranges)) 
        # self.get_logger().info(f'Maximum distance to a value ', max(msg.ranges)) 

        # distance_threshold = 1.0  
        # objects = []

        # for distance in msg.ranges:
        #     if distance < distance_threshold and distance > 0:
        #         objects.append(distance)

        # # แสดงผล
        # self.get_logger().info(f'Detected objects: {len(objects)}')
        # for idx, obj_distance in enumerate(objects):
        #     self.get_logger().info(f'Object {idx + 1}: {obj_distance:.2f} m')

def main(args=None):
    rclpy.init(args=args)
    object_detector = ObjectDetector()
    rclpy.spin(object_detector)
    object_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
