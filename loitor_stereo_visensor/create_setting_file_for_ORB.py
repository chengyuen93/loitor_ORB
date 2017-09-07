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

Left = {"Name": "LEFT", "D": [], "K": [], "R": [], "P": [], "width": 0, "height": 0}
Right = {"Name": "RIGHT", "D": [], "K": [], "R": [], "P": [], "width": 0, "height": 0}

calib_file = open(input_file, 'r')
lines = calib_file.readlines()
for i in range(len(lines)):
	if "Left" in lines[i]:
		for val in Left:
			for j in range(5):
				if val in lines[i+j]:
					line = lines[i+j]
					line = line.strip().split("', ")
					line = line[-1].split(")")[0]
					Left[val] = line
	elif "Right" in lines[i]:
		for val in Right:
			for j in range(5):
				if val in lines[i+j]:
					line = lines[i+j]
					line = line.strip().split("', ")
					line = line[-1].split(")")[0]
					Right[val] = line

width = 0
height = 0

for k in range(len(lines)): 
	if "width" in lines[k]:
		width = lines[k+1].strip()
	if "height" in lines[k]:
		height = lines[k+1].strip()
	if "left" in lines[k]:
		Left["width"] = width
		Left["height"] = height
	elif "right" in lines[k]:
		Right["width"] = width
		Right["height"] = height 

cm0 = Left["P"].split(", ")
fx = float(cm0[0][1:])
cx = float(cm0[2])
fy = float(cm0[5])
cy = float(cm0[6])

distn = Left["D"].split(", ")
k1 = float(distn[0][1:])
k2 = float(distn[1])
p1 = float(distn[2])
if "]" in distn[3]:
	p2 = float(distn[3][:-1])
else:
	p2 = float(distn[3])
if len(distn) == 5:
	k3 = float(distn[4][:-1])
else:
	k3 = float(0)

Tf = float(Right["P"].split(', ')[3])
bf = -1*Tf

calib_file.close()

set_file = open(output_file, 'w')
set_file.write("%YAML:1.0\n\n")
set_file.write("#"+100*"-"+"\n")
set_file.write("# Camera Parameters. Adjust them!\n")
set_file.write("#"+100*"-"+"\n\n")
set_file.write("# Camera calibration and distortion parameters (OpenCV)\n")
set_file.write("Camera.fx: %.15f\nCamera.fy: %.15f\nCamera.cx: %.15f\nCamera.cy: %.15f\n\n"%(fx,fy,cx,cy))
set_file.write("Camera.k1: %.15f\nCamera.k2: %.15f\nCamera.p1: %.15f\nCamera.p2: %.15f\nCamera.k3: %.15f\n\n"%(k1,k2,p1,p2,k3))
set_file.write("Camera.width: %s\nCamera.height: %s\n\n"%(Left["width"], Left["height"]))
set_file.write("# Camera frames per second\n")
set_file.write("Camera.fps: 20.0\n\n")
set_file.write("# stereo baseline times fx\n")
set_file.write("Camera.bf: %.15f\n\n"%bf)
set_file.write("# Color order of the images (0: BGR, 1: RGB. It is ignored if images are grayscale)\n")
set_file.write("Camera.RGB: 1\n\n")
set_file.write("# Close/Far threshold. Baseline times.\n")
set_file.write("ThDepth: 35\n\n")
set_file.write("#"+100*"-"+"\n")
set_file.write("# Stereo Rectification. Only if you need to pre-rectify the images\n")
set_file.write("# Camera.fx, .fy, etc must be the same as in LEFT.P\n")
set_file.write("#"+100*"-"+"\n")

cam = [Left, Right]
for ii in cam:
	set_file.write("%s.height: %s\n"%(ii["Name"], ii["height"]))
	set_file.write("%s.width: %s\n"%(ii["Name"], ii["width"]))
	set_file.write("%s.D: !!opencv-matrix\n    rows: 1\n    cols: 5\n    dt: d\n    data: %s\n"%(ii["Name"], ii["D"]))
	set_file.write("%s.K: !!opencv-matrix\n    rows: 3\n    cols: 3\n    dt: d\n    data: %s\n"%(ii["Name"], ii["K"]))
	set_file.write("%s.R: !!opencv-matrix\n    rows: 3\n    cols: 3\n    dt: d\n    data: %s\n"%(ii["Name"], ii["R"]))
	set_file.write("%s.P: !!opencv-matrix\n    rows: 3\n    cols: 4\n    dt: d\n    data: %s\n\n"%(ii["Name"], ii["P"]))

set_file.write("#"+100*"-"+"\n")
set_file.write("# ORB Parameters\n")
set_file.write("#"+100*"-"+"\n\n")
set_file.write("# ORB Extractor: Number of features per image\n")
set_file.write("ORBextractor.nFeatures: 1200\n\n")
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
set_file.write("Viewer.PointSize: 2\nViewer.CameraSize: 0.08\nViewer.CameraLineWidth: 3\n")
set_file.write("Viewer.ViewpointX: 0\nViewer.ViewpointY: -0.7\nViewer.ViewpointZ: -1.8\nViewer.ViewpointF: 500")
set_file.close()
