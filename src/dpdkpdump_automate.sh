#!/bin/bash

num=0

# make sure that the following is up and running in a separate shell
# dpdk-devbind -b 04:00.0 uio_pci_generic
# ./dpdk-testpmd -l 0,1-5 -n 4 -a 0000:04:00.0 -- -i --port-topology=chained
# testpmd >set fwd io
# testpmd > start

echo 'STARTING DPDK-PDUMP'

while getopts ":n:" arg; do
	case "${arg}" in
		n)
			num=${OPTARG}
			;;
	esac
done


timeout 70s ./dpdk-pdump -l 6,7-10 -n 4 -- --pdump 'port=0,queue=*,rx-dev=/dev/null' &> test.txt

sleep 2
echo "New results" >> results_dpdkpdump${num}.txt
cat test.txt | awk '/packets/ {print $0} {}' >> results_dpdkpdump${num}.txt
