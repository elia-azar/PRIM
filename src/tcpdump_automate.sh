#!/bin/bash

num=0
filter=0
echo 'STARTING Tcpdump'

while getopts ":n:f:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
		f)
			filter=${OPTARG}
			;;
	esac
done


if [[ $filter == 0 ]]
then
	timeout 70s tcpdump -i enp4s0f0 -w /dev/null 2>test.txt
else
	timeout 70s tcpdump -i enp4s0f0 -w /dev/null udp dst port 320 2>test.txt
fi
sleep 2
echo "New results" >> results_tcpdump${num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_tcpdump${num}.txt
