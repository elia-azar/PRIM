#!/bin/bash

: ${DPDK_CONF:=/opt/scripts/dpdk.conf}

##########################
declare -A param
param["coremask"]="1"
param["flow-dev"]=""
param["flow-socket-mem"]=""
#########################

#ARHG[$A]=$B

cd $FLOWATCHER

echo "***************************"
echo "Config-script: $DPDK_CONF"
echo "***************************"

for i in "${!param[@]}"; do param["$i"]=$(echo -e `grep $i $DPDK_CONF | cut -d '=' -f 2-`); done

echo 'STARTING  FLOWATCHER'
echo "./FloWatcher-DPDK -c ${param['coremask']} -m ${param['flow-socket-mem']} ${param['flow-dev']} --file-prefix flowatcher"

sudo -E ./FloWatcher-DPDK -c ${param['coremask']} -m ${param['flow-socket-mem']} ${param['flow-dev']} --file-prefix flowatcher
