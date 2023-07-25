#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage, NavSatFix
import cv2

class CompressedImageAndGPSSubscriber(Node):
    def __init__(self):
        super().__init__('image_and_gps_subscriber')
        self.image_subscription = self.create_subscription(
            CompressedImage,
            'image_raw',  # Замените 'compressed_image_topic' на тему с компрессированными изображениями
            self.image_callback,
            10
        )
        self.gps_subscription = self.create_subscription(
            NavSatFix,
            'gps/fix',  # Замените 'gps_topic' на тему с данными GPS
            self.gps_callback,
            10
        )
        self.image_subscription
        self.gps_subscription
        self.gps_data = None

    def image_callback(self, compressed_image_msg):
            #this is the unprocessed image decoded from Unity 
        subscribed_image = CvBridge().compressed_imgmsg_to_cv2(compressed_image_msg, desired_encoding="bgr8")
        
        if self.gps_data is not None:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            text = f"Latitude: {self.gps_data['latitude']}, Longitude: {self.gps_data['longitude']}, Altitude: {self.gps_data['altitude']}"
            text_org = (10, 20)
            text_color = (0, 0, 255)
            cv2.putText(subscribed_image, text, text_org, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        cv2.imshow("CompressedImage", subscribed_image)
        #pass the unprocessed image into the gesture recognition app
        cv2.waitKey(1)
    
    def gps_callback(self, gps_msg):
        # Получение данных GPS из сообщения
        latitude = gps_msg.latitude
        longitude = gps_msg.longitude
        altitude = gps_msg.altitude

        # Сохраняем данные GPS в переменной класса
        self.gps_data = {'latitude': latitude, 'longitude': longitude, 'altitude': altitude}


def main(args=None):
    rclpy.init(args=args)
    node = CompressedImageAndGPSSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
   main()