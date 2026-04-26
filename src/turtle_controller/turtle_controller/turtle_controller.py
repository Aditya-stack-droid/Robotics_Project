#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.callback, 10)

        self.pose = Pose()

    def callback(self, msg):
        self.pose = msg
        self.control()

    def control(self):
        cmd = Twist()

        dist = min(
            self.pose.x,
            11 - self.pose.x,
            self.pose.y,
            11 - self.pose.y
        )

        if dist < 1.5:
            
            cmd.linear.x = 0.5
            cmd.angular.z = 1.8
        else:
            Kp = 1.0
            cmd.linear.x = Kp * dist
            cmd.linear.x = min(cmd.linear.x, 2.5)
            cmd.angular.z = 0.0

        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleController()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()