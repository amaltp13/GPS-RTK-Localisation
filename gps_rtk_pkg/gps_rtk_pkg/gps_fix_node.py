#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from nmea_msgs.msg import Sentence

class GpsFixNode(Node):

    def __init__(self):
        super().__init__('gps_fix_node')

        self.sub = self.create_subscription(
            Sentence,
            '/nmea',
            self.nmea_callback,
            10)

        self.pub = self.create_publisher(
            NavSatFix,
            '/fix',
            10)

    def convert(self, raw, direction):
        deg = int(float(raw) / 100)
        minutes = float(raw) - deg * 100
        value = deg + minutes / 60
        if direction in ['S','W']:
            value = -value
        return value

    def nmea_callback(self, msg):

        line = msg.sentence

        if not line.startswith('$GNGGA'):
            return

        data = line.split(',')

        if data[2] == '' or data[4] == '':
            return

        lat = self.convert(data[2], data[3])
        lon = self.convert(data[4], data[5])
        alt = float(data[9])

        fix = NavSatFix()
        fix.header.stamp = self.get_clock().now().to_msg()
        fix.header.frame_id = "gps"

        fix.latitude = lat
        fix.longitude = lon
        fix.altitude = alt

        self.pub.publish(fix)


def main():
    rclpy.init()
    node = GpsFixNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
