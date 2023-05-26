#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
import cv2

class CompressedImageSubscriber(Node):
    def __init__(self):
        super().__init__("image_view_sub_node")
        qos_policy = rclpy.qos.QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
                                          history=rclpy.qos.HistoryPolicy.KEEP_LAST,
                                          depth=1)
        self.sub = self.create_subscription(CompressedImage, "image_raw",
                                            self.subscriber_callback, qos_profile=qos_policy)
        self.received_msg = False

    def subscriber_callback(self, compressed_image_msg):
        if self.received_msg == False:
            print("Image Data Received... Displaying Image in CV2 window")
            self.received_msg = True
            #this is the unprocessed image decoded from Unity 
        subscribed_image = CvBridge().compressed_imgmsg_to_cv2(compressed_image_msg, desired_encoding="bgr8")
        cv2.imshow("CompressedImage", subscribed_image)
        #pass the unprocessed image into the gesture recognition app
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = CompressedImageSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
   main()