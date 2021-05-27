#!/bin/bash

filter=""
filt_num=0

while getopts ":f:n:" arg; do
	case "${arg}" in
		f)
			filter=${OPTARG}
			;;
		n)
			filt_num=${OPTARG}
			;;
	esac
done

echo $filter

timeout 70s tcpdump -i enp4s0f0 -w /dev/null ${filter} 2>test.txt

sleep 2
echo "New results" >> results_tcpdump_${filt_num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_tcpdump_${filt_num}.txt
