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

    launch_sick_laserscanner = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('sick_scan2'),
                'launch/sick_lms_5xx.launch.py'
                )
            )
        )

    launch_intel_stereocamera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch/rs_launch.py')),
            launch_arguments={'enable_pointcloud': 'true'}.items()
        )
    

    rosbag_master_node = Node(
            package='rosbag_master',
            executable='input_to_csv',
        )
    
    laserscan_fake_node =  Node(
            package='laserscan_fakedata',
            executable='fakelaserpub',
        )

    ultrasonic_fake_node =  Node(
            package='ultrasonic',
            executable='ultrasonic_fake_data'
        )

    rviz2_intel_stereocamera = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2_stereocam',
        arguments=['-d', os.path.join(
            get_package_share_directory('realsense2_camera'),
            'rviz/d415_picture_pointcloud.rviz'
            )]
        )


    rviz2_sick_laserscan = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_laserscan',
            arguments=['-d', os.path.join(
                get_package_share_directory('sick_scan2'),
                'share/sick_scan2/launch/rviz/testbench.rviz'
                )]
        )

    rviz2_fake_ultrasonic = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_2',
            arguments=['-d',"config/rviz/ultrasonic_frame_fake.rviz"]
        )

    return LaunchDescription([
        #Nodes
        rosbag_master_node,
        laserscan_fake_node,
        ultrasonic_fake_node,
        #rviz2
        rviz2_sick_laserscan,
        rviz2_fake_ultrasonic,
        rviz2_intel_stereocamera,
        #launch-files
        launch_sick_laserscanner,
        launch_intel_stereocamera,
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
    

