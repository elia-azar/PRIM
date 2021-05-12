#!/bin/bash

for m in {0..2}
do
	for i in {1..5}
	do
		echo "Starting $m:$i"
		
		./dpdk_dump_automate.sh -n $i -m $m &

		sleep 6
		timeout 60s ./moongen.sh > test_generator.txt
		sleep 1
		echo "New results $i" >> dpdk_dump_results_generator_${m}_${i}.txt
		cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> dpdk_dump_results_generator_${m}_${i}.txt
		sleep 7
		rm /dev/hugepages/*
	done
done

echo "DONE"
