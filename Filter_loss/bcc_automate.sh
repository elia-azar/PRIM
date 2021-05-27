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

cd ~
timeout 70s ./pkt-filter.py -i enp4s0f0 -m 5 -f 1
cd $CONFIG_DIR

sleep 2
echo "New results" >> results_bcc_${filt_num}.txt
cat test.txt | awk '/ID/ {print $0} {}' >> results_bcc_${filt_num}.txt
