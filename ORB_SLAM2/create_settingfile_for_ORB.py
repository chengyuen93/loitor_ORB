#!/usr/bin/env python

import os

input_file = raw_input("Input calibration file (.txt): ")

if not os.path.exists(os.path.abspath(input_file)):
	print "Input file does not exist!"
	quit()

output_file = raw_input("Output setting file (.yaml): ")

if os.path.exists(os.path.abspath(output_file)):
	print "Output file already existed"
	overwrite = raw_input("Overwrite? [Y/N]")
	if overwrite != "Y":
		print "Quit .."
		quit()


calib_file = open(input_file, 'r')
lines = calib_file.readlines()
for i in range(len(lines)):
	if "projection\n" in lines[i]:
		camera_matrix = [lines[i+1],lines[i+2],lines[i+3]]
	if "distortion\n" in lines[i]:
		distortion = lines[i+1]

cm0 = camera_matrix[0].strip().split(" ")
fx = float(cm0[0])
cx = float(cm0[2])

cm1 = camera_matrix[1].strip().split(" ")
fy = float(cm1[1])
cy = float(cm1[2])

distn = distortion.split(" ")
k1 = float(distn[0])
k2 = float(distn[1])
p1 = float(distn[2])
p2 = float(distn[3])
if len(distn) == 5:
	k3 = float(distn[4])
else:
	k3 = float(0)

calib_file.close()

set_file = open(output_file, 'w')
set_file.write("%YAML:1.0\n\n")
set_file.write("#"+100*"-"+"\n")
set_file.write("# Camera Parameters. Adjust them!\n")
set_file.write("#"+100*"-"+"\n\n")
set_file.write("# Camera calibration and distortion parameters (OpenCV)\n")
set_file.write("Camera.fx: %.6f\nCamera.fy: %.6f\nCamera.cx: %.6f\nCamera.cy: %.6f\n\n"%(fx,fy,cx,cy))
set_file.write("Camera.k1: %.6f\nCamera.k2: %.6f\nCamera.p1: %.6f\nCamera.p2: %.6f\nCamera.k3: %.6f\n\n"%(k1,k2,p1,p2,k3))
set_file.write("# Camera frames per second\n")
set_file.write("Camera.fps: 25.0\n\n")
set_file.write("# Color order of the images (0: BGR, 1: RGB. It is ignored if images are grayscale)\n")
set_file.write("Camera.RGB: 0\n\n")
set_file.write("#"+100*"-"+"\n")
set_file.write("# ORB Parameters\n")
set_file.write("#"+100*"-"+"\n\n")
set_file.write("# ORB Extractor: Number of features per image\n")
set_file.write("ORBextractor.nFeatures: 1000\n\n")
set_file.write("# ORB Extractor: Scale factor between levels in the scale pyramid\n\n")
set_file.write("ORBextractor.scaleFactor: 1.2\n\n")
set_file.write("# ORB Extractor: Number of levels in the scale pyramid\n")
set_file.write("ORBextractor.nLevels: 8\n\n")
set_file.write("# ORB Extractor: Fast threshold\n# Image is divided in a grid. At each cell FAST are extracted imposing a minimum response.\n# Firstly we impose iniThFAST. If no corners are detected we impose a lower value minThFAST\n# You can lower these values if your images have low contrast\n")
set_file.write("ORBextractor.iniThFAST: 20\nORBextractor.minThFAST: 7\n\n")
set_file.write("#"+100*"-"+"\n")
set_file.write("# Viewer Parameters\n")
set_file.write("#"+100*"-"+"\n")
set_file.write("Viewer.KeyFrameSize: 0.05\nViewer.KeyFrameLineWidth: 1\nViewer.GraphLineWidth: 0.9\n")
set_file.write("Viewer.PointSize:2\nViewer.CameraSize: 0.08\nViewer.CameraLineWidth: 3\n")
set_file.write("Viewer.ViewpointX: 0\nViewer.ViewpointY: -0.7\nViewer.ViewpointZ: -1.8\nViewer.ViewpointF: 500")
set_file.close()
