#!/bin/bash

# This script is created to measure the throughput and latency of Software/Virtual switches

MOONGEN_DIR=/opt/tools/MoonGen/
CURR_DIR=$(pwd)

# default values for packet rates [Mbps] and packet size [bytes]
rate=10000
size=60
percentage=10
conf="$CONFIG_DIR/dpdk_conf.lua"
if [[ "${UID}" -ne 0 ]]
then
	echo "Need root priviledge"
	exit 1
fi

usage(){ echo "Usage: ${0} [-s packet size][-r packet rate][-c dpdk config file]"; exit 1; }

while getopts ":s:r:c:p:" arg; do
	case "${arg}" in
		s)
			size=${OPTARG}
			;;
		r)
			rate=${OPTARG}
			;;
		c)
			conf=${OPTARG}
			;;
                p)
                        percentage=${OPTARG}
                        ;;
		h | *)
			usage
			;;
	esac
done

echo "Packet rate: ${rate}, Packet size: ${size}, Percentage: ${percentage}"

cd $MOONGEN_DIR

echo "sudo ./build/MoonGen ${CURR_DIR}/throughput_one_port.lua --dpdk-config='${conf}' 0 -r '${rate}' -s '${size}' -p '${percentage}'"

sudo ./build/MoonGen ${CURR_DIR}/throughput_one_port.lua --dpdk-config="${conf}" 0 -r "${rate}" -s "${size}" -p "${percentage}"
