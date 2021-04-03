#!/bin/bash

num=0
filter=""
echo 'STARTING Moongen traffic generator'

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


timeout 70s ./moongen_dump_pcap.sh -f $filter > test.txt

sleep 2
echo "New results" >> results_dump${num}_${filter}.txt
cat test.txt | awk '/StdDev/ {print $0} {}' >> results_dump${num}_${filter}.txt
