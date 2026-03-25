#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import Int8


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('count_node')
        self.publisher_ = self.create_publisher(Int8, '/count', 10)
        
        self.count = 0

        self.subscription = self.create_subscription(
            Int8,
            '/number',
            self.sub_callback,
            10)
        self.subscription  # prevent unused variable warning

    def pub(self):
        msg = Int8()
        msg.data = self.count
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing count: "%s"' % msg.data)
    
    def sub_callback(self,msg):
        self.pub()
        if self.count == msg.data:
            self.count = 0
        self.count+=1
        self.get_logger().info("Recieving '%s'" % msg.data)
        


def main(args=None):
    rclpy.init(args=args)

    count_node = MinimalPublisher()

    rclpy.spin(count_node)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    count_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()