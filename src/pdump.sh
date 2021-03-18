#!/bin/bash

: ${DPDK_CONF:=/opt/scripts/dpdk.conf}

##########################
declare -A param
param["main-dump"]="14"
param["workers-dump"]="15-17"
param["dump-dev"]=""
#########################

#ARHG[$A]=$B

cd $RTE_SDK/build/app/

echo "***************************"
echo "Config-script: $DPDK_CONF"
echo "***************************"

for i in "${!param[@]}"; do param["$i"]=$(echo -e `grep $i $DPDK_CONF | cut -d '=' -f 2-`); done

echo 'STARTING dpdk-pdump'
echo "./dpdk-pdump -l ${param['main-dump']},${param['workers-dump']} -n 1 ${param['dump-dev']} -m 1024 -- --pdump 'port=0,queue=*,rx-dev=/opt/pcap/rx.pcap'"

./dpdk-pdump -l ${param['main-dump']},${param['workers-dump']} -n 1 -m 1024 ${param['dump-dev']} --file-prefix pdump -- --pdump 'port=0,queue=*,rx-dev=/opt/pcap/rx.pcap'
