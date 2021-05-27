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

timeout 70s ./moongen_dump_pcap.sh -f "${filter}" > test.txt

sleep 2
echo "New results" >> results_moongen${filt_num}_.txt
cat test.txt | awk '/StdDev/ {print $0} {}' >> results_moongen${filt_num}_.txt
