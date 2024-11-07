import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import tf2_ros
import geometry_msgs.msg
from rclpy.timer import Timer

class DistanceCalculator(Node):
    def __init__(self):
        super().__init__('distance_calculator')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)
        self.subscription
        
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.last_object_time = None
        self.timer = self.create_timer(0.1, self.remove_transform)  # Check every 0.1 seconds

    # Continue with the rest of your code logic for processing

    def lidar_callback(self, msg):
        filtered_ranges = [distance for distance in msg.ranges if distance < 2.0 and distance < float('inf')]
        
        if len(filtered_ranges) < 2:
            self.last_object_time = None
            return
        sorted_filtered_ranges = sorted(filtered_ranges) # sort index
        first_two = sorted_filtered_ranges[:2] #define index
        num_elements = len(filtered_ranges)  #number of index
        # print(f"The number of elements in filtered_ranges: {num_elements}") #show number index
        # print("len ", first_two) #show define index



        a = 1
        b = min(filtered_ranges)
        c = max(filtered_ranges)

        # Calculate angles A, B, C in radians with domain check
        cos_value_A = (b**2 + c**2 - a**2) / (2 * b * c)
        cos_value_B = (a**2 + c**2 - b**2) / (2 * a * c)
        cos_value_C = (a**2 + b**2 - c**2) / (2 * a * b)
    

        # Ensure the values are within the domain of acos [-1, 1]
        cos_value_A = max(-1, min(1, cos_value_A))
        cos_value_B = max(-1, min(1, cos_value_B))
        cos_value_C = max(-1, min(1, cos_value_C))

        angle_A_rad = math.acos(cos_value_A)
        angle_B_rad = math.acos(cos_value_B)
        angle_C_rad = math.acos(cos_value_C)
    
        # Convert radians to degrees
        angle_A_deg = angle_A_rad * (180 / math.pi)
        angle_B_deg = angle_B_rad * (180 / math.pi)
        angle_C_deg = angle_C_rad * (180 / math.pi)


        a2 = None  

        if math.sin(angle_B_rad) != 0:
            a2 = (b * math.sin(angle_A_rad)) / math.sin(angle_B_rad)
        else:
            self.get_logger().warn("angle_B_rad is too small, skipping calculation.")

        if a2 is not None:
            self.get_logger().info(f"Calculated a: {a2:.7f}")
            # self.index_detect(a,b,c, msg)

        if angle_A_deg + angle_B_deg + angle_C_deg == 180:  # Object detected
            self.last_object_time = self.get_clock().now()
            self.send_transform(a, b, c, angle_B_rad, msg) 
            self.calculate_sq(msg)
        self.get_logger().info(f"Angle A: {angle_A_deg:.3f}° , Angle B: {angle_B_deg:.3f}° , Angle C: {angle_C_deg:.3f}°")

    # def index_detect(self, a, b, c, msg):
    #     filtered_ranges = [distance for distance in msg.ranges if distance < float('inf')]
    
    #     if len(filtered_ranges) < 2:
    #         self.last_object_time = None
    #         return

    #     sorted_filtered_ranges = sorted(filtered_ranges)  # sort index
    #     first_two = sorted_filtered_ranges[:4]  # define index

    #     num_elements = len(filtered_ranges)  # number of index
    #     self.get_logger().info(f"The number of elements in Index: {num_elements}")
    #     self.get_logger().info(f"First two ranges detected: {first_two}")

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

        # self.get_logger().info(f"x1, y1: {points[0]}")
        # self.get_logger().info(f"x2, y2: {points[1]}")
        # self.get_logger().info(f"x3, y3: {points[2]}")
        # self.get_logger().info(f"x4, y4: {points[3]}")



    def send_transform(self, a, b, c, angle_B_rad, msg):

        transform = geometry_msgs.msg.TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'laser_frame'
        transform.child_frame_id = 'object'


        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        min_index = msg.ranges.index(b)
        angle_min_point = min_index * angle_increment
        x_min = b * math.cos(angle_min_point)
        y_min = b * math.sin(angle_min_point)

        max_index = msg.ranges.index(c)
        angle_max_point = max_index * angle_increment
        x_max = c * math.cos(angle_max_point)
        y_max = c * math.sin(angle_max_point)

        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2

        
        transform.transform.translation.x = x_mid
        transform.transform.translation.y = y_mid
        transform.transform.translation.z = 0.0
        
        # No rotation for this example
        transform.transform.rotation.w = 1.0
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        
        self.tf_broadcaster.sendTransform(transform)

    def remove_transform(self):
        if self.last_object_time and (self.get_clock().now() - self.last_object_time).nanoseconds > 0.5 * 1e9:  # 0.5 seconds
            self.get_logger().warn("Removing transform for object.")
            self.last_object_time = None

def main(args=None):
    rclpy.init(args=args)
    distance_calculator = DistanceCalculator()
    rclpy.spin(distance_calculator)
    distance_calculator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
