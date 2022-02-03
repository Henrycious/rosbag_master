import rclpy
import subprocess
from rclpy.node import Node
from rclpy.serialization import serialize_message
from std_msgs.msg import String
from std_msgs.msg import ByteMultiArray
from sensor_msgs.msg import Image
from datetime import datetime
from termcolor import colored


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
            print(colored('Already Recording, Please Stop the Recording and Try again!\n', 'red'))

        #start, when the first bit of the command is true
        elif cmd_sub[0] =='1' and not self.recording: #start
            print(colored('Starting the Rosbag!\n', 'green'))

            #check if there is a sensor that needs to be recorded
            for x in cmd_sub[1:]:
                if x == '1':
                    self.recording = True
                    break
                if x == '0':
                    continue

            #command-string for the subprocess
            cmd_str = 'ros2 bag record '
            if cmd_sub[1] == '1':
                cmd_str += '/cloud'
            if cmd_sub[2] == '1':
                cmd_str += ''
            if cmd_sub[3] == '1':
                cmd_str += ''
            if cmd_sub[4] == '1':
                cmd_str += ''
            if cmd_sub[5] == '1':
                cmd_str += ''
            
        elif cmd_sub[0] == '0': #stop
            print(colored('Stopping the Rosbag!\n', 'yellow'))
            self.recording = False
        
        else:
            print(colored('Web command is not valid!\n', 'red'))

def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()


if __name__ == '__main__':
    main()