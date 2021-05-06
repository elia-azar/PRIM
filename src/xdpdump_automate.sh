#!/bin/bash

num=0
filter=0

echo 'STARTING xdp-dump'

while getopts ":n:" arg; do
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
	timeout 70s xdpdump -P -i enp4s0f0 -w /dev/null &> test.txt
else
	xdp-filter load enp4s0f0 -f udp -p deny
	xdp-filter port 320
	timeout 70s xdpdump -P -i enp4s0f0 -w /dev/null &> test.txt
fi

sleep 2
echo "New results" >> results_xdpdump${num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_xdpdump${num}.txt
