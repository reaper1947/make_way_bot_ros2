import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg):
        angle_increment = msg.angle_increment
        threshold_distance = 5.0  # Threshold for obstacle detection
        found_objects = []

        # Find indices of valid (non-infinite) distances that are below the threshold
        for i, distance in enumerate(msg.ranges):
            if distance < threshold_distance and not math.isinf(distance):
                found_objects.append(i)


        if len(found_objects) >= 2:
            # Sort found objects by distance
            closest_objects = sorted(found_objects, key=lambda idx: msg.ranges[idx])[:2]
            angle_a = closest_objects[0] 
            angle_b = closest_objects[1] 
            print("found_object", angle_a)
            print("found_object2", angle_b)
            # Calculate the number of angle increments between the two angles
            angle_difference = abs(angle_b - angle_a)
            num_angle_increments = angle_difference / angle_increment

            self.get_logger().info(f"Closest objects detected at angles: {angle_a:.3f} rad and {angle_b:.3f} rad")
            self.get_logger().info(f"Number of angle increments between them: {num_angle_increments:.3f}")

def main(args=None):
    rclpy.init(args=args)
    object_detector = ObjectDetector()
    rclpy.spin(object_detector)
    object_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
