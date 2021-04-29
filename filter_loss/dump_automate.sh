#!/bin/bash

num=0
filter=""
filt_num=0

while getopts ":n:f:m:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
		f)
			filter=${OPTARG}
			;;
		m)
			filt_num=${OPTARG}
			;;
	esac
done

echo $filter

timeout 70s ./moongen_dump_pcap.sh -f "${filter}" > test.txt

sleep 2
echo "New results" >> results_dump${num}_.txt
cat test.txt | awk '/StdDev/ {print $0} {}' >> results_dump${num}_.txt
