#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

import math
#import tf



def Quaternion_toEulerianAngle(x, y, z, w):
	ysqr = y*y
	
	t0 = +2.0 * (w * x + y*z)
	t1 = +1.0 - 2.0 * (x*x + ysqr)
	X = math.atan2(t0, t1)
	
	t2 = +2.0 * (w*y - z*x)
	t2 =  1 if t2 > 1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = math.asin(t2)
	
	t3 = +2.0 * (w * z + x*y)
	t4 = +1.0 - 2.0 * (ysqr + z*z)
	Z = math.atan2(t3, t4)
	
	
	return X, Y, Z 

#def global_rotate_about_y(x, y, z):
#	rot_deg = math.pi/2.0
#	R1 = [math.cos(rot_deg), 0, -math.sin(rot_deg)]
#	R2 = [0, 1, 0]
#	R3 = [math.sin(rot_deg), 0, math.cos(rot_deg)]
#	R = [R1, R2, R3]
#	new_angles = []
#	for i in R:
#		angle = i[0]*x + i[1]*y + i[2]*z
#		new_angles.append(angle)
#	roll = new_angles[0]
#	pitch = new_angles[1]
#	yaw = new_angles[2]
#	print "roll: %.10f pitch: %.10f yaw: %.10f\n\n"%(math.degrees(roll), math.degrees(pitch), math.degrees(yaw))


def imu_callback(data):
	x = data.orientation.x
	y = data.orientation.y
	z = data.orientation.z
	w = data.orientation.w
	#q = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
	#euler = tf.transformations.euler_from_quaternion(q)
	#roll = euler[0]	#roll
	#pitch = euler[1]	#pitch
	#yaw = euler[2]	#yaw
	ex,ey,ez = Quaternion_toEulerianAngle(x,y,z,w)
	print data.header.seq
	print "function x: %.10f y: %.10f z: %.10f\n"%(math.degrees(ex), math.degrees(ey), math.degrees(ez))
	#print "tf roll: %.10f pitch: %.10f yaw: %.10f\n\n"%(roll, pitch, yaw)
	#global_rotate_about_y(ex, ey, ez)
	


if __name__ == "__main__":
	rospy.init_node("quaternion2euler")
	rospy.Subscriber("imu0", Imu, imu_callback)
	try:
		while not rospy.is_shutdown():
			pass
	except rospy.ROSInterruptException:
		pass
	
