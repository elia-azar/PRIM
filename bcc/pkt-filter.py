#!/usr/bin/python3
#
#eBPF application that parses UDP packets
#and extracts destination port number
#
#eBPF program udp_filter is used as SOCKET_FILTER attached to specified interface.
#only packet of type ip and udp with dst_port=320 are returned to userspace, others dropped


#from __future__ import print_function
from bcc import BPF
from sys import argv
from time import sleep

import socket
import os

#args
def usage():
    print("USAGE: %s [-i <if_name>]" % argv[0])
    print("")
    print("Try '%s -h' for more options." % argv[0])
    exit()

#help
def help():
    print("USAGE: %s [-i <if_name>]" % argv[0])
    print("")
    print("optional arguments:")
    print("   -h                       print this help")
    print("   -i if_name               select interface if_name. Default is enp4s0f0")
    print("")
    print("examples:")
    print("   pkt-filter -i enp4s0f0     # bind socket to enp4s0f0")
    exit()

#arguments
interface="enp4s0f0"

if len(argv) == 2:
    if str(argv[1]) == '-h':
        help()
    else:
        usage()

if len(argv) == 3:
    if str(argv[1]) == '-i':
        interface = argv[2]
    else:
        usage()

if len(argv) > 3:
    usage()

print ("binding socket to '%s'" % interface)

# initialize BPF - load source code from pkt-filter.c
bpf = BPF(src_file = "pkt-filter.c",debug = 0)

#load eBPF program udp_filter of type SOCKET_FILTER into the kernel eBPF vm
function_udp_filter = bpf.load_func("udp_filter", BPF.SOCKET_FILTER)

#create raw socket, bind it to interface
#attach bpf program to socket created
BPF.attach_raw_socket(function_udp_filter, interface)

#get file descriptor of the socket previously created inside BPF.attach_raw_socket
socket_fd = function_udp_filter.sock

#create python socket object, from the file descriptor
sock = socket.fromfd(socket_fd,socket.AF_NETLINK,socket.SOCK_DGRAM)
#set it as blocking socket
#sock.setblocking(True)

while 1:
    
    #retrieve raw packet from socket
    packet_str = os.read(socket_fd,256)

    #DEBUG - print raw packet in hex format
    #packet_hex = toHex(packet_str)
    #print ("%s" % packet_hex)

    #convert packet into bytearray
    packet_bytearray = bytearray(packet_str)

    #ethernet header length
    ETH_HLEN = 14

    #calculate ip header length
    ip_header_length = packet_bytearray[ETH_HLEN]               #load Byte
    ip_header_length = ip_header_length & 0x0F                  #mask bits 0..3
    ip_header_length = ip_header_length << 2                    #shift to obtain length

    #retrieve udp destination port
    dst_port = packet_bytearray[ETH_HLEN + ip_header_length + 2]
    dst_port = dst_port << 8
    dst_port = dst_port + packet_bytearray[ETH_HLEN+ ip_header_length +3]
    
    #sleep(2)
    #print stats
    s = ""
    if len(bpf["pkt_count"].items()):
        for k,v in bpf["pkt_count"].items():
            s += "ID {}: {}\t".format(k.value, v.value)
        print(s)
    else:
        print("No entries yet")