# Assignment: Create a ROS 2 Service That Generates a Random Number
# In this exercise, you will build a client node that requests a random integer
# from a service server. The client sends a minimum and maximum value, and the
# service responds with a generated number within that range.
#
# The exercise introduces the basic ROS 2 service client pattern:
# - create a custom node class that inherits from rclpy.node.Node
# - initialize the node with a unique name
# - create a client with self.create_client(...)
# - define a request object with the required fields
# - call the service and wait for a response
# - log or print the returned result
#
# This file is the client half of the exercise. It sends a request to the server
# and prints the generated random value. Together, these two nodes demonstrate
# how ROS 2 services provide synchronous request/response communication.

import sys
import rclpy
from rclpy.node import Node

# Service design:
#   Request: min_value, max_value
#   Response: random_number
# 
# Here, import RandomNumber from the interfaces.srv module
# RandomNumber is the custom Service type.
from interfaces.srv import RandomNumber

# ROS 2 boilerplate pattern:
# 1. Import rclpy and the base Node class.
# 2. Create a custom node class that inherits from Node.
# 3. In __init__, call super().__init__("node_name") to register the node.
# 4. Add services, publishers, subscribers, timers, and other ROS interfaces in __init__.
# 5. In main(), initialize rclpy, create the node, then make request to server and wait for result.
#    Finally destroy the node and shutdown ROS.
# This pattern is the standard starting point for most ROS 2 Python nodes.


class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')

        # TODO: Create a client for the random-number service
        self.client = self.create_client(RandomNumber, 'generate_random_number')

        # TODO: Wait for the service to be available
        # TODO: Create a request containing min and max values

        # self.create_client:
        #   Creates a service client used to call a ROS service.
        #   Usage: self.create_client(ServiceType, 'service_name')
        #   - ServiceType: the ROS service class you defined in an .srv file
        #   - 'service_name': name of the service to call
        #   Typical use: request a computation, configuration, or value from a server.
        #
        # client.wait_for_service:
        #   Waits until the service server is available before sending a request.
        #   Usage: self.client.wait_for_service(timeout_sec=1.0)
        #   - timeout_sec: maximum number of seconds to wait for this check
        #   The method returns True when the service is available and False on timeout.
        #
        # self.get_logger():
        #   Returns the node's ROS logger, used to print request/response details.
        #   Usage: self.get_logger().info('message')

    # Create a method that sends the service request.
    def send_request(self, min_value, max_value):
        # TODO: Build a request object with a min and max range
        self.request.min_value = min_value
        self.request.max_value = max_value
        # TODO: Call the service and wait for a response
        future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        
        # TODO: Log the returned random number
        self.get_logger().info(f"Generated Random Number: {response.random_number}")
        

def main():
    rclpy.init()
    node = ServiceClient()
    # Get handle on request which will resolve in the future
    future = node.send_request()
    # Continue running node until response recieved
    rclpy.spin_until_future_complete(node, future)
    try:
        # Get response from handle
        response = future.result()
        node.get_logger().info(f'Generated number: {response.random_number}')
    except Exception as error:
        # Log the error if the service call fails
        node.get_logger().error(f'Service call failed: {error}')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()