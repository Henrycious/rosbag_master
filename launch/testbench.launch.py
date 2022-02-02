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
import subprocess

def generate_launch_description():
    ############
    ## config ##
    ############
    sick_s3000_ethercat_adress = "131.173.120.103:2112"
    intel_d415_serial_no = '_748512060060'
    intel_d435_serial_no = '_819312070187'

    ############
    ## Launch ##
    ############  
    launch_intel_d415 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch/rs_launch.py')), 
        launch_arguments={
            #'hostname':intel_d415_serial_no,
            'device_type':'d415',
            'camera_name':'my_d415',
            'inital_reset':'false',
            'filters':'pointcloud'
        }.items()
    )

    launch_intel_d435 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch/rs_launch.py')), 
        launch_arguments={
            #'hostname':intel_d435_serial_no,
            'device_type':'d435',
            'camera_name':'my_d435',
            'inital_reset':'false',
            'filters':'pointcloud'
        }.items()
    )

    ###########
    ## Nodes ##
    ###########
    node_sick_lms511 = Node(
            package='sick_scan',
            executable='sick_generic_caller',
            name='sick_scan_lms',
    )
    #ros2 run sick_scan sick_generic_caller ./src/sick_scan_xd/launch/sick_lms_5xx.launch
    

    rviz2_sick_laserscan = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_sick_laserscan',
            arguments=['-d',os.path.join( os.path.dirname( __file__ ), '..','config/rviz/sick_lms511.rviz' )]
    )

    rviz2_intel_d415 = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_intel_d415',
            arguments=['-d',os.path.join( os.path.dirname( __file__ ), '..','config/rviz/intel_d415.rviz' )]       
    )


    rviz2_intel_d435 = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_intel_d435',
            arguments=['-d',os.path.join( os.path.dirname( __file__ ), '..','config/rviz/intel_d435.rviz' )]
    )

    rosbag_master_node = Node(
            package='rosbag_master',
            executable='input_to_rosbag',
    )
	
    
    


    return LaunchDescription([
         #launch-files
        launch_intel_d415,
        launch_intel_d435,
        #Nodes
        node_sick_lms511,
        #rosbag_master_node,
        rviz2_sick_laserscan,
        rviz2_intel_d415,
        rviz2_intel_d435,
        #laserscan_lms511,

    ])
