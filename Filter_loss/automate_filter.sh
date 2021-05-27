#!/bin/bash

declare -a FilterArray=("" \
"ether src host 01:02:03:04:05:06" \
"ether src host 01:02:03:04:05:06 ether dst host aa:cc:dd:cc:00:01" \
"ether src host 01:02:03:04:05:06 ether dst host aa:cc:dd:cc:00:01 src host 179.14.12.10" \
"ether src host 01:02:03:04:05:06 ether dst host aa:cc:dd:cc:00:01 src host 179.14.12.10 dst host 10.0.0.10 " \
"ether src host 01:02:03:04:05:06 ether dst host aa:cc:dd:cc:00:01 src host 179.14.12.10 dst host 10.0.0.10 src port 1234" \
"ether src host 01:02:03:04:05:06 ether dst host aa:cc:dd:cc:00:01 src host 179.14.12.10 dst host 10.0.0.10 src port 1234 dst port 320" \
"ether src host 01:02:03:04:05:06 ether dst host aa:cc:dd:cc:00:01 src host 179.14.12.10 dst host 10.0.0.10 udp src port 1234 dst port 320")

declare -i p=10

method=""

while getopts ":m:" arg; do
	case "${arg}" in
		m)
			method=${OPTARG}
			;;
	esac
done

echo "Starting with percentage $p"
for ((i = 0; i < ${#FilterArray[@]}; i++))
do
	if [ $method == "xdpdump" ]
	then
		cd $XDP_TOOLS/xdp-dump
		case $i in
			1)
				xdp-filter load enp4s0f0 -f ethernet,ipv4 -p deny
				xdp-filter ethernet 01:02:03:04:05:06 -m src
				;;
			2)
				xdp-filter ethernet aa:cc:dd:cc:00:01 -m dst
				;;
			3)
				xdp-filter ip 179.14.12.10 -m src
				;;
			4)
				xdp-filter ip 10.0.0.10 -m dst
				;;
			5)
				xdp-filter port 1234 -m src
				;;
			6)
				xdp-filter port 320 -m dst
				;;
			7)
				ip link set dev enp4s0f0 xdp off
				xdp-filter load enp4s0f0 -f ethernet,ipv4,udp -p deny
				xdp-filter ethernet 01:02:03:04:05:06 -m src
				xdp-filter ethernet aa:cc:dd:cc:00:01 -m dst
				xdp-filter ip 179.14.12.10 -m src
				xdp-filter ip 10.0.0.10 -m dst
				xdp-filter port 1234 -m src
				xdp-filter port 320 -m dst
				;;
		esac
		cd $CONFIG_DIR
	fi
	for j in {1..50}
	do
		echo "Starting with test $j"
		./${method}_automate.sh -f "${FilterArray[$i]}" -n $i &
		sleep 4
		timeout 60s ./moongen.sh -p $p > test_generator.txt
		sleep 2
		echo "New results $j" >> results_generator_${method}_${i}.txt
		cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> results_generator_${method}_${i}.txt
		sleep 8
		rm /dev/hugepages/*
	done
done

if [ $method == "xdpdump" ]
then
	ip link set dev enp4s0f0 xdp off
fi

echo "Finished"
