#!/bin/bash

## INFO
## This config file should be sourced at the beginning of the experiments.
## You can also automatically source it through the .bashrc file
##
## Remember to set values according to your system:
##
## 1. Linecards PCI addresses
## 2. Router-friendly and Linux-friendly names
## 3. MAC and IP addresses of your linecards
## 4. RTE_SDK, RTE_PKTGEN etc for the traffic generator of your choice
##
## Configuration variables and aliases are provided at the end of the file

# Linecards
export LC0P0=0000:04:00.0
export LC0P1=0000:04:00.1
export LC1P0=0000:05:00.0
export LC1P1=0000:05:00.1

# Router-friendly names
export NAMELC0P0="TenGigabitEthernet4/0/0"
export NAMELC0P1="TenGigabitEthernet4/0/1"
export NAMELC1P0="TenGigabitEthernet5/0/0"
export NAMELC1P1="TenGigabitEthernet5/0/1"

# Linux-friendly names
export DEVLC0P0="enp4s0f0"
export DEVLC0P1="enp4s0f1"
export DEVLC1P0="enp5s0f0"
export DEVLC1P1="enp5s0f1"

# MAC addresses
export MACLC0P0="90:e2:ba:cb:f5:38"
export MACLC0P1="90:e2:ba:cb:f5:39"
export MACLC1P0="90:e2:ba:cb:f5:44"
export MACLC1P1="90:e2:ba:cb:f5:45"

export MACLOOP="90:e2:ba:cb:f5:46"

# Port numbers (For MoonGen)
export IDLC0P0="0"
export IDLC0P1="1"
export IDLC1P0="2"
export IDLC1P1="3"


# IP addresses
export IPLC0P0="1.1.1.11"
export IPLC0P1="1.1.1.12"
export IPLC1P0="1.1.1.21"
export IPLC1P1="1.1.1.22"

export IPLOOP="10.0.0.0"

# Default routes
DEFAULTIP="99.99.99.99"


# DPDK
export RTE_SDK=/opt/tools/dpdk-20.11
export RTE_TARGET=x86_64-native-linuxapp-gcc

# MoonGen
export MOONDIR=/opt/tools/MoonGen

# FloWatcher
export FLOWATCHER=/opt/tools/FloWatcher-DPDK/run_to_completion/build

# Software-swicthes
export SS=/opt/software-switches
export TRAFFIC_GEN=$SS/moongen

# Config
export CONFIG_DIR=/opt/scripts

# Aliases
alias show-conf="cat $CONFIG_DIR/config.sh"
alias list-scripts="ls -l $CONFIG_DIR/*.sh"
#alias dpdk-setup="$RTE_SDK/usertools/dpdk-setup.sh"
alias dpdk-devbind="python $RTE_SDK/usertools/dpdk-devbind.py"
alias show-hugepages="cat /proc/meminfo | grep Huge; python $RTE_SDK/usertools/dpdk-hugepages.py -s"
alias dpdk-hugepages="python $RTE_SDK/usertools/dpdk-hugepages.py"
alias rm-hugepages="rm /dev/hugepages/*"
