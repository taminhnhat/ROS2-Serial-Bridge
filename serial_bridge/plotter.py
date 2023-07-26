# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist

import json

import serial
serialPort = serial.Serial('/dev/ttyUSB1',115200,timeout=1)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'diff_cont/cmd_vel_unstamped',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        cmd_msg = "{x:.1f} {y:.1f} {z:.1f} {roll:.1f} {pitch:.1f} {yaw:.1f}".format(
            x = msg.linear.x,
            y = msg.linear.y,
            z = msg.linear.z,
            roll = msg.angular.x,
            pitch = msg.angular.y,
            yaw = msg.angular.z
            )+"\r\n"
        print(cmd_msg)
        serialPort.write(bytes(cmd_msg,'utf-8'))

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)
    while True:
        serialString = serialPort.readLine()
        print(serialString)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
