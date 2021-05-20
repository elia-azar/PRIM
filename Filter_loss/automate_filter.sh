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

	echo "Starting with percentage $p"
	for ((i = 0; i < ${#FilterArray[@]}; i++))
	do
		for j in {1..50}
		do
			echo "Starting with test $j"
			./dump_automate.sh -n $p -f "${FilterArray[$i]}" -m $i &
			sleep 4
			timeout 60s ./moongen.sh -p $p > test_generator.txt
			sleep 2
			echo "New results $j" >> results_generator${p}_${i}.txt
			cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> results_generator${p}_${i}.txt
			sleep 8
			rm /dev/hugepages/*
		done
	done
echo "Finished"
