import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace

def generate_launch_description():
    rviz_path = "/home/henry/teststand_ws/config/rviz/laser_frame_fake.rviz"
    sick_s3000_ethercat_adress = "131.173.120.103:2112"



    launch_sick_laserscanner = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('sick_scan'),
                'launch/sick_lms_5xx.launch.py')), 
        launch_arguments={'hostname':sick_s3000_ethercat_adress}.items()
        )

    rosbag_master_node = Node(
            package='rosbag_master',
            executable='input_to_rosbag',
        )

    rviz2_sick_laserscan = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_1',
            arguments=['-d',"/home/henry/sick_scan_ws/install/sick_scan2/share/sick_scan2/launch/rviz/testbench.rviz"]
        )


    return LaunchDescription([
        #Nodes
        rosbag_master_node,
        rviz2_sick_laserscan,
        
        #launch-files
        
        launch_sick_laserscanner
    ])



    #Old Fake-Laser-Publisher
    #
    #
    #    Node(
    #        package='rviz2',
    #        executable='rviz2',
    #        name='rviz2_1',
    #        arguments=['-d',"/home/henry/teststand_ws/config/rviz/laser_frame_fake.rviz"]
    #    ),
    

