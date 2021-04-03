#!/bin/bash

# This script is created to measure the throughput and latency of Software/Virtual switches

MOONGEN_DIR=/opt/tools/MoonGen/
CURR_DIR=$(pwd)

# default values for packet rates [Mbps] and packet size [bytes]

conf="$CONFIG_DIR/dpdk_conf_dump.lua"
filter=""

while getopts ":f:" arg; do
	case "${arg}" in
                f)
                        filter=${OPTARG}
                        ;;
	esac
done

if [[ "${UID}" -ne 0 ]]
then
	echo "Need root priviledge"
	exit 1
fi

usage(){ echo "Usage: ${0}"; exit 1; }

cd $MOONGEN_DIR
sudo ./build/MoonGen libmoon/examples/dump-pkts.lua --dpdk-config="${conf}" 0 "${filter}" -f "/dev/null"
