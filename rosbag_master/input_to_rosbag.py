import rclpy
import subprocess
from rclpy.node import Node
from rclpy.serialization import serialize_message
from std_msgs.msg import String
from std_msgs.msg import ByteMultiArray
from sensor_msgs.msg import Image
from datetime import datetime
from termcolor import colored
import os
import signal

class SimpleBagRecorder(Node):
    def __init__(self):
        super().__init__('simple_bag_recorder')
        self.recording = False
        self.subscription_web = self.create_subscription(
            String,
            '/webcommand',
            self.topic_callback_web,
            10
        )
        self.subscription_web

    def topic_callback_web(self, data):
        now = datetime.now()
        time_now = str(now).replace(' ','_').replace(':','-').replace('.','-')

        print(colored('Receiving Cmd. Time: ' + time_now, 'white'))
        cmd_sub = data.data.replace("true","1").replace("false","0")

        if cmd_sub[0] =='1' and self.recording:
            self.get_logger().info('Already Recording')
            print(colored('Already Recording, Please Stop the Recording and Try again!\n', 'red'))

        #start, when the first bit of the command is true
        elif cmd_sub[0] =='1' and not self.recording: #start
            print(colored('Starting the Rosbag!\n', 'green'))

            #check if there is a sensor that needs to be recorded
            for x in cmd_sub[1:]:
                if x:
                    self.recording = True
                    break
                if not x:
                    continue
            
            if self.recording: 
                cmd_str = 'ros2 bag record -o rosbag2_' + time_now       
                
                if cmd_sub[1] == '1': #SICK LMS 511
                    cmd_str += ' /cloud'
                if cmd_sub[2] == '1': #Intel Realsense D415
                    cmd_str += ' /my_d415/color/image_raw'
                    cmd_str += ' /my_d415/depth/color/points'
                if cmd_sub[3] == '1': #Intel Realsense D435
                    cmd_str +=  ' /my_d435/color/image_raw'
                    cmd_str +=  ' /my_d435/depth/color/points'
                # if cmd_sub[4] == '1': #Infisense P2
                #     cmd_str +=  ''
                # if cmd_sub[5] == '1': #Microsoft Webcam
                #     cmd_str +=  ''        

                #command-string for the subprocess
                self.proc = subprocess.Popen([cmd_str], cwd='/home/henry/master_ws/testbench_ws/rosbag', shell=True, preexec_fn=os.setpgrp) 
                       
        elif cmd_sub[0] == '0' and self.recording: #stop
            print(colored('Stopping the Rosbag!\n', 'yellow'))
            self.get_logger().info(cmd_sub + ' Stopping the Rosbag!')
            self.recording = False
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        elif cmd_sub[0] == '0' and not self.recording:
            self.get_logger().info('Rosbag already stopped!')
        else:
            print(colored('Web command is not valid!\n', 'red'))

def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    os.killpg(os.getpgid(sbr.proc.pid), signal.SIGTERM)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
