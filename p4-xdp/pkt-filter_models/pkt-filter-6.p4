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
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            0x11: parse_udp;
	        default: accept;
	    }
    }

    state parse_udp {
	    packet.extract(hdr.udp);
	    transition accept;
    }
}

control MyIngress(inout headers hdr, in xdp_input xin, out xdp_output xout) {
    bool xoutdrop = false;
    CounterArray(32w10, true) counters;

    action save() {
    }

    action drop() {
        xoutdrop = true;
    }

    table src_ether_exact {
        key = {
            hdr.ethernet.srcAddr: exact;
        }
        actions = {
            drop;
            save;
        }
        default_action = drop();

        implementation = hash_table(8);
    }

    table dst_ether_exact {
        key = {
            hdr.ethernet.srcAddr: exact;
        }
        actions = {
            drop;
            save;
        }
        default_action = drop();

        implementation = hash_table(8);
    }

    table src_ip_exact {
        key = {
            hdr.ipv4.srcAddr: exact;
        }
        actions = {
            drop;
            save;
        }
        default_action = drop();

        implementation = hash_table(8);
    }

    table dst_ip_exact {
        key = {
            hdr.ipv4.srcAddr: exact;
        }
        actions = {
            drop;
            save;
        }
        default_action = drop();

        implementation = hash_table(8);
    }

    table src_udp_exact {
        key = {
            hdr.udp.sport: exact;
        }
        actions = {
            drop;
            save;
        }
        default_action = drop();

        implementation = hash_table(8);
    }

    apply {
        if(hdr.ethernet.isValid() && hdr.ipv4.isValid() && hdr.udp.isValid()){
            src_ether_exact.apply();
            dst_ether_exact.apply();
            src_ip_exact.apply();
            dst_ip_exact.apply();
            src_udp_exact.apply();
            if (xoutdrop) {
                counters.increment(0);
                xout.output_action = xdp_action.XDP_DROP;
            }else {
                counters.increment(1);
                xout.output_action = xdp_action.XDP_PASS;
            }
        }
        else{
            xout.output_action = xdp_action.XDP_DROP;
        }
        xout.output_port = 0;
    }
}

control MyDeparser(in headers hdr, packet_out packet) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.udp);
    }
}

xdp(MyParser(), MyIngress(), MyDeparser()) main;