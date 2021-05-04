#!/bin/bash

method=""

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
	export P4EBPF=$P4C/backends/ebpf
	tc qdisc add dev enp4s0f0 clsact
	tc filter add dev enp4s0f0 ingress bpf da obj $P4EBPF/pkt-filter.o section prog verbose
	# retrieve prog id with the following command
	read prog_id <<< $( tc filter show dev enp4s0f0 ingress | awk '{for (I=1;I<NF;I++) if ($I == "id") print $(I+1)}' )
	# retrieve map id with the following command
	read id <<< $( bpftool prog show id $prog_id | awk '{for (I=1;I<NF;I++) if ($I == "map_ids") print $(I+1)}' | sed 's/,.*$//' )

elif [ $method == "p4xdp" ]
then
	export P4XDP=$P4C/extensions/p4c-xdp/tests;
	ip link set dev enp4s0f0 xdp obj $P4XDP/pkt-filter.o
	# retrieve prog id with the following command
	read prog_id <<< $( ip -d link show enp4s0f0 | awk '{for (I=1;I<NF;I++) if ($I == "id") print $(I+1)}' )
	# retrieve map id with the following id
	read id <<< $( bpftool prog show id $prog_id | awk '{for (I=1;I<NF;I++) if ($I == "map_ids") print $(I+1)}' | sed 's/,.*$//' )
fi

for p in {0..10}
do
	echo "Starting with percentage $p"
	for j in {1..50}
	do
		echo "Starting with test $p:$j"
		if [ $method == "p4ebpf" ] || [ $method == "p4xdp" ]
		then
			echo "Map id: $id"
			./${method}_automate.sh -n $p -i $id &
		else
			./${method}_automate.sh -n $p -f 1 &
		fi
		sleep 6
		timeout 60s ./moongen.sh -p $p > test_generator.txt
		sleep 1
		echo "New results $j" >> results_generator${p}.txt
		cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> results_generator${p}.txt
		sleep 7
		rm /dev/hugepages/*
	done
done

if [ $method == "p4ebpf" ]
then
	tc qdisc del dev enp4s0f0 clsact

elif [ $method == "p4xdp" ]
then
	ip link set dev enp4s0f0 xdp off
fi

echo "DONE"