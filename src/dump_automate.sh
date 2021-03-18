#!/bin/bash

num=0

echo 'STARTING Moongen traffic generator'

while getopts ":n:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
	esac
done


timeout 70s ./moongen_dump_pcap.sh > test.txt

sleep 2
echo "New results" >> results_dump${num}.txt
cat test.txt | awk '/StdDev/ {print $0} {}' >> results_dump${num}.txt
