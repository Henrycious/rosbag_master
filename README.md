################################################
## README - Testbench				##
##						##
## Author: Henry Gennet			##
## E-mail: henry.gennet@hs-osnabrueck.de 	##
##						##	
## License: Apache License 2.0		##	
##						##
################################################

#Check for the right settings (e.g. Ethernet-Adress of Laserscanner)
ID Sick S3000: 131.173.120.103:2111 / 2112 (can be found in the programm: SOPAS)
Sopas Login: authorised customer /pw: client
CHANGE IP in PROGRAM: ../sick_scan_xd/src/driver/sick_generic_laser => search for Hostname 

#Commands to start the testbench:
cd ~/teststand_ws/launch
source ./install/setup.bash
ros2 launch testbench.launch.py

#start the SLR Canon Eos 2000d and publish video to /dev/video0
sudo modprobe v4l2loopback

gphoto2 --stdout --capture-movie --set-config --capture-preview --set-config autofocusdrive=1 | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video0
#show slr preview-stream
vlc v4l2:///dev/video0

#webserver
cd ~/webserver_ws/src/rosboard
./run

ros2 launch rosbridge_server rosbridge_websocket_launch.xml



#Data-Usage
CSV:
    Laserscanner        : 25MB / min. 
    Ultrasonic(fake)    : 39kB / min. 

Rosbag:
    Laserscanner    : 12MB / min. 
    Stereokamera    : ~1GB / min.


#install packages
sudo apt-get install libjsoncpp-dev
sudo apt-get install ros-foxy-rclcpp
sudo apt-get install libusb-1.0-0-dev
sudo apt-get install libboost-all-dev
sudo apt-get install build-essential g++ python-dev autotools-dev libicu-dev libbz2-dev libboost-all-dev
sudo apt-get install ros-foxy-xacro
sudo apt-get install ros-foxy-v4l2-camera
sudo apt-get install apt-utils
sudo apt-get install python3-bson
sudo apt-get install python3-tornado
sudo apt-get install ros-foxy-ros2bag
https://github.com/ros2/rosbag2 (foxy-future)
#optional
sudo apt-get install vlc
sudo apt-get install ros-foxy-angles

#not sure so far
sudo apt-get install docker-compose
sudo apt-get install ros-foxy-tf-transformations
pip install transforms3d
pip install pandas
pip3 install simplejpeg
sudo apt get install ros-foxy-usb-cam

#install librealsense sdk2.0
https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md

#fix errors in packages
sick-scan-xd: In find_package() add nav_msgs and visualization_msgs





#darknet not working atm!!
darknet-ros: add to beginning of /src/image_opencv.cpp

	#include "opencv2/core/core_c.h"
	#include "opencv2/videoio/legacy/constants_c.h"
	#include "opencv2/highgui/highgui_c.h"

	Additionally change the line 
		IplImage ipl = m to 
		IplImage ipl = cvIplImage(m)
	 
	any other problems with darknet-ros: https://github.com/leggedrobotics/darknet_ros/issues/223
 


#Additional Lines (include into rviz):
ros2 launch view_model.launch.py model:=test_d435_multiple_cameras.urdf.xacro

ros2 run sick_scan sick_generic_caller ./src/sick_scan_xd/launch/sick_lms_5xx.launch hostname:=131.173.120.103:2112 sw_pll_only_publish:=False

##NOTES!
duplicate launch-files if you just them more than one time to minimize the risk of errors


#start the Stereocamera Intel Realsense D415
ros2 launch realsense2_camera rs_launch.py config_file:="'$COLCON_PREFIX_PATH/realsense2_camera/share/realsense2_camera/config/d435i.yaml'" initial_reset:=true filters:=pointcloud
#start multiple Stereocams (1st cam: d415, 2nd cam: d435)
ros2 launch realsense2_camera rs_launch.py camera_name:=my_d415 serial_no:=_748512060060 inital_reset:=true filters:=pointcloud
ros2 launch realsense2_camera rs_launch.py camera_name:=my_d435 serial_no:=_819312070187 inital_reset:=true filters:=pointcloud







Old Version:
Commands to start the testbench:
#Terminal 1: Start the sick-scanner (LMS551)
ros2 launch sick_scan2 sick_lms_5xx.launch.py
#Terminal 2: Start a world to cloud transformer
cd ~/sick_scan_ws
source ./install/setup.bash
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 world cloud
#Terminal 3: Start rviz2 with a config file
cd ~/sick_scan_ws
source ./install/setup.bash
rviz2 ./install/sick_scan2/share/sick_scan2/launch/rviz/testbench.rviz
#Terminal 4: Start the Rosbag Master to record the data
cd ~/teststand_ws/launch
source ./install/setup.bash
ros2 launch testbench_launch.py





