echo "Building ROS nodes"

cd orb_slam2
mkdir build
cd build
cmake .. -DROS_BUILD_TYPE=Release
make -j
