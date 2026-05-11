import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PointStamped
import math


class GPSXYNode(Node):
    def __init__(self):
        super().__init__('gps_xy_node')

        # 🔥 Declare parameters (so you can change without editing code)
        self.declare_parameter('origin_lat', 28.50755530)
        self.declare_parameter('origin_lon', 77.07306242)#it is 1m around from wheel edge to to wall, tag corner , security area,as world zero

        self.origin_lat = self.get_parameter('origin_lat').value
        self.origin_lon = self.get_parameter('origin_lon').value

        self.get_logger().info(
            f"Using FIXED origin: lat={self.origin_lat}, lon={self.origin_lon}"
        )

        # Subscriber
        self.sub = self.create_subscription(
            NavSatFix,
            '/fix',
            self.callback,
            10
        )

        # Publisher
        self.pub = self.create_publisher(
            PointStamped,
            '/gps/xy',
            10
        )

    def callback(self, msg):
        lat = msg.latitude
        lon = msg.longitude

        # 🔥 More accurate conversion (use origin latitude)
        lat_rad = math.radians(self.origin_lat)

        meters_per_deg_lat = 110540
        meters_per_deg_lon = 111320 * math.cos(lat_rad)

        dx = (lon - self.origin_lon) * meters_per_deg_lon
        dy = (lat - self.origin_lat) * meters_per_deg_lat

        pt = PointStamped()
        pt.header.stamp = self.get_clock().now().to_msg()
        pt.header.frame_id = "map"

        pt.point.x = dx
        pt.point.y = dy
        pt.point.z = 0.0

        self.pub.publish(pt)


def main():
    rclpy.init()
    node = GPSXYNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
