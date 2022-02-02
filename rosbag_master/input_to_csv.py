import transforms3d
import rclpy

from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range
from geometry_msgs.msg import Quaternion
from rosidl_runtime_py import *
from transforms3d import *

import sys
import numpy
import tf2_py
import pandas as pd  
import csv
import math
import io

laser = 0
ultrasonic = 1

location_laser = [0.0,1.0,2.0,0.0,0.0,0.0] #location of the laserscanner in x-/y-/z- coordinate and rotations from the Base
location_ultrasonic = [0.0,1.0,2.0,0.0,0.0,0.0] #location of the ultrasonic-sensor in x-/y-/z- coordinate and rotations from the Base
current_data = 0

class RosbagMaster(Node):

    def __init__(self): #define the topics to subscribe to 
        super().__init__('rosbag_master')
        ##########################################################
        #init the used cache variables                           #
        ##########################################################
        self.statelaser = 0
        self.stateultrasonic = 0


        #########################################################
        # Laserscanner, Sensor index = 0                        #
        #########################################################

        self.subscription = self.create_subscription(
            LaserScan,
            'laserscan',
            self.laserscan_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        #########################################################
        # Ultrasonic   , Sensor index = 1                       #
        #########################################################

        self.subscription2 = self.create_subscription(
            Range,
            'fake_ultrasonic_scan',
            self.ultrasonic_callback,
            10
        )
        self.subscription2 # prevent unused variable warning
        
        ##########################################################
        #init the used cache variables                           #
        ##########################################################
        self.lasersensor = LaserScan()
        self.ultrasonicsensor = Range()

        
        print('Rosbag-Master, init-state ---- waits for an input!')

    def laserscan_callback(self, msg):
        sensorindex = laser #index of the sensor
        #State-Machine
        if self.statelaser == 0: #init
            print('Laserscanner ready - Publishing Data!')
            self.statelaser += 1

        if self.statelaser == 1: #run
            self.get_logger().info('Laserscan: Data received. Timestamp: "{}"'.format(msg.header.stamp))      
            self.statelaser += 1

        if self.statelaser == 2: #write to csv
            with open('laserscan_data.csv', 'a') as a:
                writer = csv.writer(a,delimiter=',')
                writer.writerow([str(location_laser).replace('[','').replace(']','').replace(' ','') + message_to_csv(msg)])
            self.statelaser = 1

    def ultrasonic_callback(self, msg):
        sensorindex = ultrasonic #index of the sensor
        #State-Machine
        if self.stateultrasonic == 0: #init
            print('Ultrasonic Sensor ready- Publishing Data!')
            self.stateultrasonic += 1

        if self.stateultrasonic == 1: #run, get new data
            self.get_logger().info('Ultrasonic: Data recieved. Timestamp: "{}"'.format(msg.header.stamp))
            self.stateultrasonic += 1

        if self.stateultrasonic == 2: #write to csv
            with open('ultrasonic_data.csv', 'a') as b:
                writer = csv.writer(b,delimiter=',')
                writer.writerow([str(location_ultrasonic).replace('[','').replace(']','').replace(' ','') + message_to_csv(msg)]) 
            self.stateultrasonic = 1 #reset


def main(args=None):
    rclpy.init(args=args)

    rosbag_master = RosbagMaster()

    rclpy.spin(rosbag_master)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rosbag_master.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()