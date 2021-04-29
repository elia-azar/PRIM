#!/bin/bash

method=""

methods_with_id="p4ebpf p4xdp"

id=0

while getopts ":m:" arg; do
	case "${arg}" in
		m)
			method=${OPTARG}
			;;
	esac
done

if [ $method == "p4ebpf" ]
then
	export P4EBPF=$P4C/backends/ebpf;
	tc qdisc add dev enp4s0f0 clsact;
	tc filter add dev enp4s0f0 ingress bpf da obj $P4EBPF/pkt-no-filter.o section prog verbose;
	# retrieve prog id with the following command
	tc filter show dev enp4s0f0 ingress;
	# retrieve map id with the following id
	bpftool prog id 64;

elif [ $method == "p4xdp" ]
then
	export P4XDP=$P4C/extensions/p4c-xdp/tests;
	ip link set dev enp4s0f0 xdp obj $P4XDP/pkt-no-filter.o;
	# retrieve prog id with the following command
	ip -d link show enp4s0f0;
	# retrieve map id with the following id
	bpftool prog id 64;
fi

for j in {1..50}
do
	for i in {1..18}
	do
		echo "Starting $i"
		if [[ $methods_with_list =~ (^|[[:space:]])$method($|[[:space:]]) ]]
		then
			./${method}_automate.sh -n $i -i $id &
		else
			./${method}_automate.sh -n $i &
		fi
		sleep 4
		timeout 60s ./moongen.sh -r $(($i*515)) > test_generator.txt
		sleep 2
		echo "New results $i" >> ${method}_results_generator${i}.txt
		cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> ${method}_results_generator${i}.txt
		sleep 7
		rm /dev/hugepages/*
	done
done

if [ $nom == "p4ebpf" ]
then
	tc qdisc del dev enp4s0f0 clsact

elif [ $method == "p4xdp" ]
then
	ip link set dev enp4s0f0 xdp off
fi

echo "DONE"
