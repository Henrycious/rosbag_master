import setuptools
import os 
from glob import glob


package_name = 'rosbag_master'

setuptools.setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),glob('launch/*.launch.py')),],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='henry',
    maintainer_email='henry.gennet@hs-osnabrueck.de',
    description='Rosbag Master to collect all the published data',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'input_to_csv = rosbag_master.input_to_csv:main',
            'input_to_rosbag = rosbag_master.input_to_rosbag:main'
        ],
    },
)
