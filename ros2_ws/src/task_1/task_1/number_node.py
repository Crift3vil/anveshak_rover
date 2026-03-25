#!usr/bin/env python3
import rclpy
from rclpy.node import Node

from std_msgs.msg import Int8


class MaximalPublisher(Node):

    def __init__(self):
        super().__init__('number_node')
        self.n = 0
        self.publisher_ = self.create_publisher(Int8, '/number', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.pub_callback)



        self.subscription = self.create_subscription(
            Int8,
            '/count',
            self.sub_callback,
            10)
        self.subscription  # prevent unused variable warning

    def pub_callback(self):
        msg = Int8()
        msg.data = self.n
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
    
    def sub_callback(self,msg):
        self.get_logger().info("Recieving '%s'" % msg.data)
        if msg.data >= self.n:
            self.n+=1



def main(args=None):
    rclpy.init(args=args)

    number_node = MaximalPublisher()

    rclpy.spin(number_node)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    number_node.destroy_node()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()