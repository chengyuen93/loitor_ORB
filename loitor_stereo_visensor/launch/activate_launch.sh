imu_port="None"

for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev)
do
	syspath="${sysdevpath%/dev}"
	devname="$(udevadm info -q name -p $syspath)"
	[[ "$devname" == "bus/"* ]] && continue
	eval "$(udevadm info -q property --export -p $syspath)"
	[[ -z "$ID_SERIAL" ]] && continue

	#id_serial below has to change accordingly
	if [[ $ID_SERIAL == *"FTDI_FT232R_USB_UART_A98BF1DD"* ]]
	then
		export imu_port="/dev/$devname"
		continue
	fi
done

roslaunch loitor_stereo_visensor loitor_ORBSLAM2.launch imu_dev:=$imu_port
