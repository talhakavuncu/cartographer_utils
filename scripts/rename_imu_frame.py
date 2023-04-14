#!/usr/bin/env python3
import rospy
import tf
import math
from sensor_msgs.msg import Imu

pub=rospy.Publisher('cartographer_imu',Imu,queue_size=10)

def imu_callback(imu_data):
    global pub
    imu_data.header.frame_id = 'imu_link_cartographer'
    pub.publish(imu_data)

rospy.init_node("cartographer_imu_node")

sub=rospy.Subscriber('/xsens_gnss/imu/data',Imu,imu_callback,queue_size=10)
rospy.spin()