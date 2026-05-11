import rclpy
from rclpy.node import Node
from nmea_msgs.msg import Sentence
from rtcm_msgs.msg import Message
import serial


class GpsBridge(Node):

    def __init__(self):
        super().__init__('gps_bridge')

        # Serial connection
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

        # NMEA publisher
        self.nmea_pub = self.create_publisher(
            Sentence,
            '/nmea',
            10
        )

        # RTCM subscriber
        self.rtcm_sub = self.create_subscription(
            Message,
            '/rtcm',
            self.rtcm_callback,
            10
        )

        # Timer
        self.timer = self.create_timer(
            0.01,
            self.read_serial
        )

        self.get_logger().info("GPS Bridge Started")

    def rtcm_callback(self, msg):
        try:
            # Send RTCM corrections to GPS
            self.ser.write(bytearray(msg.message))
        except Exception as e:
            self.get_logger().warn(f"RTCM write error: {e}")

    def read_serial(self):

        while self.ser.in_waiting > 0:

            try:
                raw = self.ser.readline()

                # Skip binary / invalid
                if b'$' not in raw:
                    continue

                line = raw.decode('ascii', errors='ignore').strip()

                # Only valid NMEA sentences
                if not line.startswith('$'):
                    continue

                # Ignore broken lines
                if '*' not in line:
                    continue

                msg = Sentence()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "gps"
                msg.sentence = line

                self.nmea_pub.publish(msg)

            except Exception as e:
                self.get_logger().warn(f"Serial read error: {e}")


def main():
    rclpy.init()
    node = GpsBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()