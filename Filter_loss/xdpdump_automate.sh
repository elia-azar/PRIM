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

timeout 70s xdpdump -P -i enp4s0f0 -w /dev/null &> test.txt

sleep 2
echo "New results" >> results_xdpdump_${filt_num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_xdpdump_${filt_num}.txt