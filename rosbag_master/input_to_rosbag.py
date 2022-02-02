import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from std_msgs.msg import String
from std_msgs.msg import ByteMultiArray
from sensor_msgs.msg import Image
from datetime import datetime

import rosbag2_py

class SimpleBagRecorder(Node):
    def __init__(self):
        super().__init__('simple_bag_recorder')

        self.subscription_web = self.create_subscription(
            ByteMultiArray,
            'web_commands',
            self.topic_callback_web,
            10
        )
        self.subscription_web

    def topic_callback(self, msg):
        self.writer.write(
            'thermal_stream',
            serialize_message(msg),
            self.get_clock().now().nanoseconds)

    def topic_callback_web(self, data):
        self.get_logger().info('Receiving Command')
        #start, when the first bit of the command is true
        if data.data[0]: #start
            self.get_logger().info('Starting the Rosbag')
            self.writer2 = rosbag2_py.SequentialWriter()
            now = datetime.now()

            current_time = now.strftime("%H_%M_%S")

            storage_options = rosbag2_py._storage.StorageOptions(
                uri='my_bag_' + current_time,
                storage_id='sqlite3')
            converter_options = rosbag2_py._storage.ConverterOptions('', '')
            self.writer2.open(storage_options, converter_options)

            topic_info = rosbag2_py._storage.TopicMetadata(
                name='thermal_stream',
                type='sensor_msgs/msg/Image',
                serialization_format='cdr')
            self.writer2.create_topic(topic_info)

            self.subscription = self.create_subscription(
                Image,
                'thermal_stream',
                self.topic_callback,
                10)
            self.subscription

        #stop when the first bit of the command is false
        if not data.data[0]: #stop
            self.get_logger().info('Stopping the Rosbag')
            self.destroy_subscription
            self.writer2.close()

def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()


if __name__ == '__main__':
    main()