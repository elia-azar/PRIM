#!/bin/bash


for j in {1..20}
do
for i in {1..18}
do
	echo "Starting $i"
	./dump_automate.sh -n $i &
	sleep 4
	timeout 60s ./moongen.sh -r $(($i*515)) > test_generator.txt
	sleep 2
	echo "New results $i" >> results_generator${i}.txt
	cat test_generator.txt | awk '/StdDev/ {print $0} {}' >> results_generator${i}.txt
	sleep 7
	rm /dev/hugepages/*
done
done
echo "Finished"
