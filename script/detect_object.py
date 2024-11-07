import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class ObjectDetection(Node):

    def __init__(self):
        super().__init__('laser_obstacle')
        self.laser_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10)  # QoS profile can be adjusted
        self.scan_msg = None

    def laser_callback(self, msg):
        self.scan_msg = msg
        self.process_msg(self.scan_msg)

    def process_msg(self, msg):
            range_msg = min(msg.ranges) # Adjust for indexing from -30 to 30 degrees

            # If the distance to the obstacle is less than 1.0 meters, it’s detected.
            if range_msg < 2.0:
                self.get_logger().info("Obstacle detected")



def main(args=None):
    rclpy.init(args=args)
    object_detection = ObjectDetection()
    rclpy.spin(object_detection)
    object_detection.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
