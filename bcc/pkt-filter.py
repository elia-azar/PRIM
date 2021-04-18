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
import ctypes
import sys

class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                ("ifr_flags", ctypes.c_short)]

class FLAGS(object):
    # linux/if_ether.h
    ETH_P_ALL     = 0x0003 # all protocols
    ETH_P_IP      = 0x0800 # IP only
    # linux/if.h
    IFF_PROMISC   = 0x100
    # linux/sockios.h
    SIOCGIFFLAGS  = 0x8913 # get the active flags
    SIOCSIFFLAGS  = 0x8914 # set the active flags

bpf = 0

#args
def usage():
    print("USAGE: %s [-i <if_name>] [-d <debug_mode>]" % argv[0])
    print("")
    print("Try '%s -h' for more options." % argv[0])
    exit()

#help
def help():
    print("USAGE: %s [-i <if_name>] [-d <debug_mode>]" % argv[0])
    print("")
    print("optional arguments:")
    print("   -h                       print this help")
    print("   -i if_name               select interface if_name. Default is enp4s0f0")
    print("   -d debug_mode            select debugging mode. Default is 1")
    print("")
    print("examples:")
    print("   pkt-filter -i enp4s0f0  -d 1   # bind socket to enp4s0f0")
    exit()

def parse_ipv4(pkt):
    return_val = ""

    src_addr = ""
    dst_addr = ""
    for i in range(4):
        src_addr += str(pkt[12 + i]) + "."
        dst_addr += str(pkt[16 + i]) + "."
    
    src_addr = src_addr[:-1]
    dst_addr = src_addr[:-1]

    #calculate ip header length
    ip_header_length = pkt[0]                   #load Byte
    ip_header_length = ip_header_length & 0x0F  #mask bits 0..3
    ip_header_length = ip_header_length << 2    #shift to obtain length

    #retrieve transport protocol
    proto = pkt[9]
    return_val += "proto:" + str(proto) + ", "

    #retrieve source port
    src_port = pkt[ip_header_length]                 #load Byte
    src_port = src_port << 8                                      #shift MSB
    src_port = src_port + pkt[ip_header_length + 1]  #add LSB
    return_val += src_addr + ":" + str(src_port) + " -> "
    
    #retrieve destination port
    dst_port = pkt[ip_header_length + 2]            #load Byte
    dst_port = dst_port << 8                                     #shift MSB
    dst_port = dst_port + pkt[ip_header_length +3]  #add LSB
    return_val += dst_addr + ":" + str(dst_port)

    return return_val

def parse_ipv6(pkt):
    return_val = ""

    #retrieve next header type
    proto = pkt[6]
    return_val += "Next Header:" + str(proto) + ", "

    src_addr = ""
    dst_addr = ""
    for i in range(16):
        src_addr += str(hex(pkt[8 + i]))[2:] + ":"
        dst_addr += str(hex(pkt[24 + i]))[2:] + ":"
    
    src_addr = src_addr[:-1]
    dst_addr = src_addr[:-1]

    return_val += src_addr + " -> " + dst_addr

    return return_val

def print_hex(pkt):
    print("-------------------------------------")
    i = 0
    for val in pkt:
        str_val = str(hex(val))[2:]
        str_val = str_val if len(str_val) != 1 else "0" + str_val
        print(str_val + " ", end = "")
        i += 1
        if i % 8 == 0:
            print("  ", end = "")
        if i % 16 == 0:
            print()
    print()
    return

def main():
    global bpf
    DEBUG = 1
    #arguments
    interface="enp4s0f0"

    if len(argv) == 1:
        print()

    elif len(argv) == 2:
        if str(argv[1]) == '-h':
            help()
        else:
            usage()

    elif len(argv) == 3:
        if str(argv[1]) == '-i':
            interface = argv[2]
        elif str(argv[1]) == '-d':
            DEBUG = int(argv[2])
        else:
            usage()

    elif len(argv) == 5:
        if str(argv[1]) != '-i' or str(argv[3]) != '-d':
            usage()
        else:
            interface = argv[2]
            DEBUG = int(argv[4])

    else:
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
    sock = socket.fromfd(socket_fd,socket.PF_PACKET, socket.SOCK_RAW, socket.htons(FLAGS.ETH_P_ALL))
    #set it as blocking socket

    import fcntl
    ifr = ifreq()
    ifr.ifr_ifrn = b'enp4s0f0'
    fcntl.ioctl(sock, FLAGS.SIOCGIFFLAGS, ifr) # get the flags
    ifr.ifr_flags |= FLAGS.IFF_PROMISC # add the promiscuous flag
    fcntl.ioctl(sock, FLAGS.SIOCSIFFLAGS, ifr) # update

    sock.setblocking(True)

    while 1:
        #retrieve raw packet from socket
        packet_str = os.read(socket_fd,256)

        #convert packet into bytearray
        packet_bytearray = bytearray(packet_str)

        if DEBUG == 1:
            print_hex(packet_bytearray)

        elif DEBUG == 2:
            #ethernet header length
            ETH_HLEN = 14

            src_mac = ""
            dst_mac = ""
            for i in range(6): 
                src_mac += str(hex(packet_bytearray[i]))[2:] + ":"
                dst_mac += str(hex(packet_bytearray[6+i]))[2:] + ":"
            
            src_mac = src_mac[:-1]
            dst_mac = src_mac[:-1]

            ether_type = str((packet_bytearray[ETH_HLEN - 2] << 8) + packet_bytearray[ETH_HLEN - 1])

            result = src_mac + " " + dst_mac + " ether_type: " + ether_type 
            if ether_type == "2048":
                result += ", " + parse_ipv4(packet_bytearray[ETH_HLEN:])
            elif ether_type == "34525":
                result += ", " + parse_ipv6(packet_bytearray[ETH_HLEN:])
            
            print("-------------------------------------")
            print(result)
            print()

        else:
            sleep(2)
            #print stats
            s = ""
            if len(bpf["pkt_count"].items()):
                for k,v in bpf["pkt_count"].items():
                    s += "ID {}: {}\t".format(k.value, v.value)
                print(s)
            else:
                print("No entries yet")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            s = ""
            if len(bpf["pkt_count"].items()):
                for k,v in bpf["pkt_count"].items():
                    s += "ID {}: {}\t".format(k.value, v.value)
                print(s)
            else:
                print("No entries yet")
            sys.exit(0)
        except SystemExit:
            os._exit(0)