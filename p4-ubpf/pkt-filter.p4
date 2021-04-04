#define UBPF_MODEL_VERSION 20200304
#include <ubpf_model.p4>
#include <core.p4>

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

parser MyParser(packet_in packet, out headers hdr, inout metadata meta) {
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
        transition select(hdr.ipv4.diffserv) {
            0x11: parse_udp;
	        default: accept;
	    }
    }

    state parse_udp {
	    packet.extract(hdr.udp);
	    transition accept;
    }
}

control MyPipe(inout headers hdr, inout metadata meta) {
    bool to_drop = false;
    CounterArray(32w10, true) counters;

    action save() {
        to_drop = false;
    }

    action drop() {
        to_drop = true;
    }

    table udp_exact {
        key = {
            hdr.udp.dport: exact;
        }
        actions = {
            drop;
            save;
        }
        default_action = drop();

        // match port 320
        const entries = {
            (0x0140) : save();
        }
        implementation = hash_table(8);
    }

    apply {
		if (hdr.ipv4.isValid()) {
            udp_exact.apply();
		}
        if (to_drop) {
            counters.increment(0);
            meta.output_action = ubpf_action.DROP;
        }else {
            counters.increment(1);
            meta.output_action = ubpf_action.PASS;
        }
        meta.output_port = 0;
    }
}

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.udp);
    }
}

ubpf(MyParser(), MyPipe(), MyDeparser()) main;
