import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage, Image
import cv2
import numpy as np


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('vision')
        self.publisher_ = self.create_publisher(
            CompressedImage, "image_raw", 10)
        self.bridge = CvBridge()
        timer_period = 1.0 / 30  # seconds
        self.timer = self.create_timer(timer_period, self.callback)
        self.cap = cv2.VideoCapture(0)

    def callback(self):
      # compress image into buffer
        ret, frame = self.cap.read()
        if ret:
            msg = CompressedImage()
            msg = self.bridge.cv2_to_compressed_imgmsg(np.array(frame), dst_format='jpeg')
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing an CompressedImage')


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
