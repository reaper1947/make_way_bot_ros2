from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import time
import RPLFunctions as rpl
import rclpy
from rclpy.node import Node

class LidarNode(Node):
    def __init__(self, segthreshold):
        super().__init__('lidar_node')
        self.segthreshold = segthreshold
        self.create_timer(0.1, self.timer_callback)
        self.rplidar = RPLidar('/dev/ttyUSB0')  

    def timer_callback(self):
        start_time = time.time()
        plt.clf()


        scanvals = rpl.getScan()
        x = (scanvals[:, 2]) * (np.cos(np.deg2rad(scanvals[:, 1])))
        y = (scanvals[:, 2]) * (np.sin(np.deg2rad(scanvals[:, 1])))
        
    
        scanvals = rpl.segment(scanvals, self.segthreshold)

    
        colors = ['b', 'g', 'c', 'm', 'y', 'k', 'w']
        j = 0
        for i in range(int(scanvals[-1][3])):
            plt.scatter((x[(scanvals[:, 3] == i)]), (y[(scanvals[:, 3] == i)]), marker='*', c=colors[j])
            j += 1
            j %= len(colors)

        plt.axis('equal')
        plt.draw()
        plt.pause(0.001)
        print("Time: ", time.time() - start_time, "seconds")

def main(args=None):
    rclpy.init(args=args)
    segthreshold = 150  # ปรับตามที่ต้องการ
    lidar_node = LidarNode(segthreshold)
    rclpy.spin(lidar_node)
    lidar_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
