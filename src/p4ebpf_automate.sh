#!/bin/bash

num=0
id=0

echo 'STARTING P4-eBPF'

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

echo "New results" >> results_p4ebpf${num}.txt
bpftool map dump id $id > results_p4ebpf${num}.txt
