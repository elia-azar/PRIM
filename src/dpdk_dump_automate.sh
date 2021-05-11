#!/bin/bash

num=0

echo 'STARTING DPDK-DUMP'

while getopts ":n:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
	esac
done

cd /opt/tools/dpdk-20.11/examples/flow_filtering

timeout 70s ./build/flow --lcores='(0,1)@(0-5)' -n 4 -m 1024 -w 0000:04:00.0 --file-prefix flow_dpdk -- -m 0

cd $CONFIG_DIR

echo "New results" >> results_dpdkdump${num}.txt
cat test.txt | tail -1 - >> results_dpdkdump${num}.txt
