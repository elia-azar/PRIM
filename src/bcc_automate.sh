#!/bin/bash

num=0

echo 'STARTING BCC'

while getopts ":n:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
	esac
done


timeout 70s ~/pkt-filter.py -i enp4s0f0 -m 5 -f 0

sleep 2
echo "New results" >> results_bcc${num}.txt
cat test.txt | awk '/ID/ {print $0} {}' >> results_bcc${num}.txt
