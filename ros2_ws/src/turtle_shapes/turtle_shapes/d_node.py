#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('d_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.sub_callback,
            10)
        self.subscription

        self.t = 0
        self.r = 1
        self.phase = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.initial = [0,0,0]
        self.pi = 3.1415

    def sub_callback(self,msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta
        if self.phase == 0:
            self.initial = [self.x,self.y,self.theta]
            self.phase+=1

        self.pub()
        


    def pub(self):
        
        msg = Twist()
        if self.phase == 1:
            msg.angular.z = 0.2

        if self.theta >= 0.98*self.pi/2 and self.theta <= 1.02*self.pi/2 and self.phase == 1:
            self.phase = 2
            self.get_logger().info(f'ph{self.phase}')
        
        if self.phase == 2: 
            msg.angular.z = 0.0
            msg.linear.x = 1.0
            
        if self.y >= (self.initial[1] + 2*self.r) and self.phase == 2:
            self.phase = 3
            self.get_logger().info(f'ph{self.phase}')
            self.get_logger().info(f'{(self.initial[1] + 2*self.r)}')
            self.get_logger().info(f'{self.y}')
        
        if self.phase == 3:
            msg.angular.z = -1.0
            msg.linear.x = 0.0

        if self.theta >= -0.01 and self.theta <= 0.01 and self.phase == 3:
            self.phase = 4
            self.get_logger().info(f'ph{self.phase}')
        
        if self.phase == 4:
            msg.linear.x = 1.0
            msg.angular.z = -1/self.r
        
        if self.y >= 0.97*self.initial[1] and self.y <= 1.03*self.initial[1] and self.phase == 4:
            self.phase = 5
            self.get_logger().info(f'ph{self.phase}')
        
        if self.phase == 5:
            msg.linear.x = 0.0
            msg.angular.z = 1.0

        if self.theta >= -0.01 and self.theta <= 0.01 and self.phase == 5:
            self.phase = 6
            self.get_logger().info(f'ph{self.phase}')

        if self.phase == 6:
            msg.angular.z = 0.0
            msg.angular.x = 0.0

        self.publisher_.publish(msg)
        





def main(args=None):
    rclpy.init(args=args)

    d_node = MinimalPublisher()

    rclpy.spin(d_node)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    d_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()