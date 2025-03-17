#!/usr/bin/env python3

import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle import TransitionCallbackReturn
from ros_tcp_endpoint import TcpServer

class LifecycleTcpServer(LifecycleNode):
    def __init__(self):
        super().__init__('unity_endpoint_lifecycle')
        self.server = None

    def on_configure(self, state):
        self.get_logger().info("Configuring TCP Server...")
        self.server = TcpServer("UnityEndpoint")
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state):
        self.get_logger().info("Activating TCP Server...")
        if self.server:
            self.server.start()
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state):
        self.get_logger().info("Deactivating TCP Server...")
        if self.server:
            self.server.stop()
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state):
        self.get_logger().info("Cleaning up TCP Server...")
        if self.server:
            self.server.stop()
            self.server = None
        return TransitionCallbackReturn.SUCCESS

def main(args=None):
    rclpy.init(args=args)
    node = LifecycleTcpServer()
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == '__main__':
    main()