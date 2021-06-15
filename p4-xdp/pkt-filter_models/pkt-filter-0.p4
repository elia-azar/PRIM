#include <core.p4>
#include "xdp_model.p4"

const bit<16> TYPE_IPV4 = 0x800;

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

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    udp_t        udp;
}

parser MyParser(packet_in packet, out headers hdr) {
    state start {
        transition accept;
    }
}

control MyIngress(inout headers hdr, in xdp_input xin, out xdp_output xout) {
    bool xoutdrop = false;
    CounterArray(32w10, true) counters;


    apply {
        counters.increment(1);
        xout.output_action = xdp_action.XDP_PASS;
        xout.output_port = 0;
    }
}

control MyDeparser(in headers hdr, packet_out packet) {
    apply {
    }
}

xdp(MyParser(), MyIngress(), MyDeparser()) main;