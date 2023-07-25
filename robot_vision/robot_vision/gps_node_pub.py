import rclpy
from rclpy.node import Node
import serial
import pynmea2
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from std_msgs.msg import Header


class GpsNode(Node):

    def __init__(self):
        super().__init__('gps_node')
        self.publisher_ = self.create_publisher(NavSatFix, 'gps/fix', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.gps = serial.Serial('/dev/ttyACM0', timeout=9600)

    def timer_callback(self):
            data = pynmea2.NMEAStreamReader()
            newdata = str(self.gps.readline())
        #print(newdata)
        #print("############################################################################################")
            if str(newdata[2:8]) == '$GNGGA':
                msg = NavSatFix()
                msg.header = Header()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "gps"

                msg.status.status = NavSatStatus.STATUS_FIX
                msg.status.service = NavSatStatus.SERVICE_GPS
                newmessage = pynmea2.parse(str(newdata[2:-5]))
                try:
                    
                    lat = newmessage.lat
                    lon = newmessage.lon
                    alti = newmessage.altitude
                    

                        # Position in degrees.
                    msg.latitude = float(lat)
                    msg.longitude = float(lon)
                    msg.altitude = float(alti)
                    # Altitude in metres.
            

                    msg.position_covariance[0] = 0
                    msg.position_covariance[4] = 0
                    msg.position_covariance[8] = 0
                    msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

                    self.publisher_.publish(msg)
                    print(msg)
                    self.best_pos_a = None
                    print("############################################################################################")
                except:
                    lat = 0.0
                    lon = 0.0
                    alti = 0.0
                    

                        # Position in degrees.
                    msg.latitude = float(lat)
                    msg.longitude = float(lon)

                    # Altitude in metres.
            

                    msg.position_covariance[0] = 0
                    msg.position_covariance[4] = 0
                    msg.position_covariance[8] = 0
                    msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

                    self.publisher_.publish(msg)
                    print(msg)
                    self.best_pos_a = None

def main(args=None):
    try:
        rclpy.init(args=args)

        gps_node = GpsNode()

        rclpy.spin(gps_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
        gps_node.destroy_node()
        rclpy.shutdown()
    except:
        print("NO DATA! PLEASE TURN ON GPS TRACKER! ")


if __name__ == '__main__':
    main()