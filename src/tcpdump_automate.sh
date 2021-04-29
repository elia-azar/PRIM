#!/bin/bash

num=0

echo 'STARTING Tcpdump'

while getopts ":n:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
	esac
done


timeout 70s tcpdump -i enp4s0f0 > /dev/null 2>test.txt

sleep 2
echo "New results" >> results_tcpdump${num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_tcpdump${num}.txt
