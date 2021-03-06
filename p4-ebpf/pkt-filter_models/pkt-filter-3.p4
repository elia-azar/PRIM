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
        transition accept;
    }

}


/*************************************************************************
****************  F I L T E R   P R O C E S S I N G   ********************
*************************************************************************/

control MyFilter(inout headers hdr, out bool accept) {
    
    CounterArray(32w2, true) drop_save_counter;

    action drop() {
        accept = false;
    }

    action save(){
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
            hdr.ethernet.dstAddr: exact;
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
    
    apply {
        accept = true;
        if (hdr.ethernet.isValid() && hdr.ipv4.isValid()) {
            src_ether_exact.apply();
            dst_ether_exact.apply();
            src_ip_exact.apply();
            if (accept) {
                drop_save_counter.increment(1);
            }else{
                drop_save_counter.increment(0);
            }
        }
        else{
            accept = false;
        }
    }
}

ebpfFilter(
MyParser(),
MyFilter()) main;
