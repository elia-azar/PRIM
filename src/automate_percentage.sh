#!/bin/bash


for p in {0..10}
do
	echo "Starting with percentage $p"
	for j in {1..20}
	do
		echo "Starting with test $j"
		./dump_automate.sh -n $p &
		sleep 4
		timeout 60s ./moongen.sh -p $p > test_generator.txt
		sleep 2
		echo "New results $j" >> results_generator${p}.txt
		cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> results_generator${p}.txt
		sleep 7
		rm /dev/hugepages/*
	done
done
echo "Finished"
