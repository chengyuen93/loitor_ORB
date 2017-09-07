#!/usr/bin/env python

import rospy
import sys
import os
import math
from time import sleep
import cv2
import shutil

rospy.init_node('capture_sequence', anonymous=True)


if __name__ == '__main__':

	output_location = raw_input("Output sequence folder location: ")
	if not os.path.exists(os.path.dirname(os.path.abspath(output_location))):
		print "Location does not exist"
		quit()
	if not os.path.exists(os.path.abspath(output_location)):
		os.mkdir(os.path.abspath(output_location))
	sequence_folder_tum = os.path.abspath(output_location) + '/rgb'
	sequence_folder_kitti = os.path.abspath(output_location) + '/image_0'
	if os.path.exists(sequence_folder_tum):
		overwrite = raw_input("rgb folder exists. Overwrite? [Y/N] ")
		if overwrite == 'Y':
			shutil.rmtree(sequence_folder_tum)
		else:
			print "Quit .."
			quit()
	if os.path.exists(sequence_folder_kitti):
		overwrite = raw_input("image_0 folder exists. Overwrite? [Y/N] ")
		if overwrite == 'Y':
			shutil.rmtree(sequence_folder_kitti)
		else:
			print "Quit .."
			quit()
	os.mkdir(sequence_folder_tum)
	os.mkdir(sequence_folder_kitti)
	rgb_file = open(os.path.abspath(output_location) + "/rgb.txt", 'w')
	times_file = open(os.path.abspath(output_location) + "/times.txt", 'w')
	rgb_file.write("# color images\n# file: 'nova_office'\n# timestamp filename\n")
	webcam = cv2.VideoCapture(1)

	count = 0

	try:
		
		while not rospy.is_shutdown() and webcam.isOpened():
			_, frame = webcam.read()

			cv2.imshow("Webcam", frame)
			now = rospy.get_rostime()
			rospy.loginfo("Current time %i %i", now.secs, now.nsecs)
			nsecs = '%d'%now.nsecs
			if len(nsecs) >6:
				nsecs = nsecs[:6]
			else:
				nsecs = nsecs + (6-len(nsecs)) * '0'
			time_now = "%10d.%6s"%(now.secs, nsecs)

			count_str = '%d'%count
			if len(count_str) <= 6:
				count_str = (6 - len(count_str)) * '0' + count_str

			cv2.imwrite(sequence_folder_kitti + '/' + count_str + '.png', frame)
			cv2.imwrite(sequence_folder_tum + '/' + time_now + '.png', frame)
			rgb_file.write("%s %s"%(time_now, os.path.split(sequence_folder_tum)[-1] + '/' + time_now + '.png\n'))
			times_file.write("%s\n"%time_now)

			count = count + 1

			if cv2.waitKey(40) & 0xFF == 27:
				cv2.destroyAllWindows()
				rgb_file.close()
				times_file.close()
				break
	except rospy.ROSInterruptException or KeyboardInterrupt:
		cv2.destroyAllWindows()
		rgb_file.close()
		times_file.close()
		webcam.release()