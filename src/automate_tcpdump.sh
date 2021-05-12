#!/bin/bash

for f in {0..1}
do
	for i in {1..5}
	do
		echo "Starting $f:$i"
		
		./tcpdump_automate.sh -n $i -f $f &

		sleep 6
		timeout 60s ./moongen.sh > test_generator.txt
		sleep 1
		echo "New results $i" >> tcpdump_results_generator_${f}_${i}.txt
		cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> tcpdump_results_generator_${f}_${i}.txt
		sleep 7
		rm /dev/hugepages/*
	done
done

echo "DONE"
