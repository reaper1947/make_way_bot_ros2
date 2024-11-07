import numpy as np
import random
from sensor_msgs.msg import LaserScan
import rclpy
from rclpy.node import Node
import subprocess

class RPLListener(Node):

    def __init__(self):
        super().__init__('RPL_Listen')
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)  # QoS profile
        self.scan_data = None

    def scan_callback(self, scan):
        self.scan_data = self.get_scan(scan)

    def get_scan(self, scan):
        ranges = np.array(scan.ranges) * 1000
        ranges = np.array(ranges[:], copy=False, subok=True, ndmin=2).T

        intensities = np.array(scan.intensities)
        intensities = np.array(intensities[:], copy=False, subok=True, ndmin=2).T

        angle_min = np.rad2deg(scan.angle_min)
        angle_max = np.rad2deg(scan.angle_max)
        angle_increment = np.rad2deg(scan.angle_increment)
        angles = [angle_min + angle_increment * i for i in range(len(scan.ranges))]
        angles = np.array(angles[:], copy=False, subok=True, ndmin=2).T

        scanvals = np.concatenate((intensities, angles, ranges), axis=1)
        scanvals = np.delete(scanvals, np.where(scanvals[:, 0] == 0), axis=0)
        scanvals = np.insert(scanvals, 3, 0, axis=1)
        return scanvals

    def start_rplidar(self):
        roslaunch_command = 'roslaunch rplidar_ros rplidar.launch'.split()
        return subprocess.Popen(roslaunch_command)

    def kill_process(self, process):
        process.kill()

    def scan_to_coord(self):
        if self.scan_data is None:
            return None
        scanvals = self.scan_data
        x = (scanvals[:, 2]) * (np.sin(np.deg2rad(scanvals[:, 1])))
        y = (scanvals[:, 2]) * (np.cos(np.deg2rad(scanvals[:, 1])))
        return np.c_[x, y]

    def segment(self, scanvals, segthreshold):
        iterseg = 0
        for i in range(1, len(scanvals)):
            if abs(scanvals[i][2] - scanvals[i - 1][2]) > segthreshold:
                iterseg += 1
            scanvals[i][3] = iterseg
        return scanvals

    def split_seg(self, scanvals, x, y):
        iterseg = 0
        coords = np.column_stack((x, y))
        dcoords = np.zeros((len(coords), 2))
        for i in range(1, len(scanvals)):
            dcoords[i] = abs(abs(coords[i]) - abs(coords[i - 1]))
        for i in range(len(dcoords)):
            if (((dcoords[i - 1][0] > dcoords[i - 1][1]) and (dcoords[i][1] > dcoords[i][0])) or
                    ((dcoords[i - 1][1] > dcoords[i - 1][0]) and (dcoords[i][0] > dcoords[i][1]))):
                iterseg += 1
            scanvals[i][3] = iterseg
        return scanvals

    # ... (ฟังก์ชันอื่น ๆ จะต้องทำการปรับเปลี่ยนด้วยในลักษณะเดียวกัน)

def main(args=None):
    rclpy.init(args=args)
    listener = RPLListener()

    try:
        listener.start_rplidar()
        rclpy.spin(listener)
    except KeyboardInterrupt:
        pass
    finally:
        listener.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
