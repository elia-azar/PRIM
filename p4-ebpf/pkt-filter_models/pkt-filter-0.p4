/* -*- P4_16 -*- */
#include <core.p4>
#include <ebpf_model.p4>

const bit<16> TYPE_IPV4 = 0x800;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   id;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header udp_t {
    bit<16>  sport;
    bit<16>  dport;
    bit<16>  len;
    bit<16>  checksum;
}

struct metadata {
    bit<32>  counter;
}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    udp_t        udp;
}

//extern void save_packet(in headers hdr);

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet, out headers hdr) {

    state start {
        transition accept;
    }

}


/*************************************************************************
****************  F I L T E R   P R O C E S S I N G   ********************
*************************************************************************/

control MyFilter(inout headers hdr, out bool accept) {
    
    CounterArray(32w2, true) drop_save_counter;
    
    apply {
        accept = true;
        drop_save_counter.increment(1);
    }
}

ebpfFilter(
MyParser(),
MyFilter()) main;
