#!/bin/bash

num=0

echo 'STARTING xdp-dump'

while getopts ":n:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
	esac
done

timeout 70s xdpdump -P -i enp4s0f0 -w /dev/null &> test.txt


sleep 2
echo "New results" >> results_xdpdump${num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_xdpdump${num}.txt
