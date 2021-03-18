#!/bin/bash

: ${DPDK_CONF:=/opt/scripts/dpdk.conf}

##########################
declare -A param
param["main-core"]="1"
param["workers"]="3-4"
param["l2fwd-dev"]=""
#########################

#ARHG[$A]=$B

cd $RTE_SDK/build/examples/

echo "***************************"
echo "Config-script: $DPDK_CONF"
echo "***************************"

for i in "${!param[@]}"; do param["$i"]=$(echo -e `grep $i $DPDK_CONF | cut -d '=' -f 2-`); done

echo 'STARTING l2fwd'
echo "./dpdk-l2fwd -l ${param['main-core']},${param['workers']} -n 1 ${param['l2fwd-dev']} -m 1024 -- -p 0x3"

./dpdk-l2fwd -l ${param['main-core']},${param['workers']} -n 1 -m 1024 ${param['l2fwd-dev']} --file-prefix l2fwd -- -p 0x3
