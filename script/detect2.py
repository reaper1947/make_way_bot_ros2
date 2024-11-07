import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import tf2_ros
import geometry_msgs.msg
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
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

    def scan_callback(self, msg):
        regions = [min(msg.ranges[i:i + 10]) for i in range(0, len(msg.ranges), 10)]
        
        detected_objects = []
        table_threshold = 5.0
        for idx, distance in enumerate(regions):
            if distance < table_threshold:
                angle = idx * (msg.angle_increment)
                detected_objects.append((distance, angle))

        if len(detected_objects) >= 2:
            x_total, y_total = 0.0, 0.0
            for dist, ang in detected_objects:
                x_total += dist * math.cos(ang)
                y_total += dist * math.sin(ang)
            
            center_x = x_total / len(detected_objects)
            center_y = y_total / len(detected_objects)
            
            self.publish_table_tf(center_x, center_y)

    def publish_table_tf(self, x, y):
        transform = geometry_msgs.msg.TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "scan"
        transform.child_frame_id = "table_center"
        transform.transform.translation.x = x
        transform.transform.translation.y = y
        transform.transform.translation.z = 0.0
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(transform)

def main(args=None):
    rclpy.init(args=args)
    object_detector = ObjectDetector()
    rclpy.spin(object_detector)
    object_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
