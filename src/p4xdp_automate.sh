#!/bin/bash

num=0
id=0
echo 'STARTING P4-XDP'

while getopts ":n:i:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
		i)
			id=${OPTARG}
			;;
	esac
done


sleep 70

echo "New results" >> results_p4xdp${num}.txt
# retrieve value from the map
bpftool map dump id $id >> results_p4xdp${num}.txt

# delete entries from the map
bpftool map delete id $id key 1 0 0 0
