#!/usr/bin/env python

# import geonav_transform.geonav_conversions as gc
import geonav_conversions.geonav_conversions as gc
import rospy
import tf
import math
from sensor_msgs.msg import NavSatFix

rospy.init_node('fake_navsat_node')
listener = tf.TransformListener()
pub = rospy.Publisher('NavsatFake', NavSatFix, queue_size=10)
rate = rospy.Rate(100.0)
utmzone = '35T'

while not rospy.is_shutdown():
    try:
        (trans,rot) = listener.lookupTransform('/utm', '/imu_link', rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("CANNOT OBTAIN TRANSFORM")
        continue
    
    x_coord = trans[0]
    y_coord = trans[1]
    northing = y_coord
    easting = x_coord
    lat, lon = gc.UTMtoLL(northing,easting,utmzone)
    print("lat: ",lat)
    print("lon: ",lon)
    print("-----------")
    latlong = NavSatFix()
    latlong.latitude = lat
    latlong.longitude = lon
    latlong.position_covariance = [0.5, 0, 0, 0, 0.5, 0, 0, 0, 0.5]
    latlong.position_covariance_type = 2
    pub.publish(latlong)
    rate.sleep()



# Define a local orgin, latitude and longitude in decimal degrees
# This is the standard geonav origin for working at El Estero Lake

# 41.104359, 29.022986
# # This is somewhat confusing, but Gazebo also has a local coordinate system.
# # In the elestero.launch file we define the gazebo origin relative to the 
# # heightmap used to represent the lake.
# gaz_lat = 36.596524
# gaz_lon = -121.888169

# # So in geonav coordinates, the Gazebo origin is...
# xg, yg = gc.ll2xy(gaz_lat,gaz_lon,olat,olon)
# print('Geonav ll2xy, Lat: %.4f, Lon:%.4f >> X: %.1f, Y: %.1f'
#       %(gaz_lat,gaz_lon,xg,yg))


# lat = 41.104359
# lon = 29.022986
# print(gc.LLtoUTM(lat,lon))
