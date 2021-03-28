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
            IPV4_ETHTYPE: parse_ipv4;
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

    Register<bit<32>, bit<32>>(1) packet_counter_reg;

    apply {
        bit<32> last_count;
        bit<32> index = 0;
        last_count = packet_counter_reg.read(index);
        packet_counter_reg.write(index, last_count + 1);
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
