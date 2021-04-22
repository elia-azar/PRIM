/* Automatically generated by p4c-ebpf from pkt-filter.p4 on Thu Apr 22 00:02:39 2021
 */
#include "pkt-filter.h"
#include "ebpf_kernel.h"

enum ebpf_errorCodes {
    NoError,
    PacketTooShort,
    NoMatch,
    StackOutOfBounds,
    HeaderTooShort,
    ParserTimeout,
    ParserInvalidArgument,
};

#define EBPF_MASK(t, w) ((((t)(1)) << (w)) - (t)1)
#define BYTES(w) ((w) / 8)
#define write_partial(a, s, v) do { u8 mask = EBPF_MASK(u8, s); *((u8*)a) = ((*((u8*)a)) & ~mask) | (((v) >> (8 - (s))) & mask); } while (0)
#define write_byte(base, offset, v) do { *(u8*)((base) + (offset)) = (v); } while (0)

void* memcpy(void* dest, const void* src, size_t num);

//struct MyFilter_udp_exact_key key_save = {.field0 = 320};
//struct MyFilter_udp_exact_value value_save = {.action = 1};

REGISTER_START()
REGISTER_TABLE(MyFilter_udp_exact, BPF_MAP_TYPE_HASH, sizeof(struct MyFilter_udp_exact_key), sizeof(struct MyFilter_udp_exact_value), 8)
REGISTER_TABLE(MyFilter_udp_exact_defaultAction, BPF_MAP_TYPE_ARRAY, sizeof(u32), sizeof(struct MyFilter_udp_exact_value), 1)
REGISTER_TABLE(MyFilter_drop_save_counter, BPF_MAP_TYPE_HASH, sizeof(MyFilter_drop_save_counter_key), sizeof(MyFilter_drop_save_counter_value), 2)
REGISTER_END()

//BPF_MAP_UPDATE_ELEM(MyFilter_udp_exact, &key_save, &value, BPF_ANY);

SEC("prog")

int ebpf_filter(SK_BUFF *skb){
    struct headers hdr = {
        .ethernet = {
            .ebpf_valid = 0
        },
        .ipv4 = {
            .ebpf_valid = 0
        },
        .udp = {
            .ebpf_valid = 0
        },
    };
    unsigned ebpf_packetOffsetInBits = 0;unsigned ebpf_packetOffsetInBits_save = 0;
    enum ebpf_errorCodes ebpf_errorCode = NoError;
    void* ebpf_packetStart = ((void*)(long)skb->data);
    void* ebpf_packetEnd = ((void*)(long)skb->data_end);
    u8 accept = 0;
    u32 ebpf_zero = 0;
    unsigned char ebpf_byte;

    goto start;
    start: {
/* extract(hdr.ethernet)*/
        if (ebpf_packetEnd < ebpf_packetStart + BYTES(ebpf_packetOffsetInBits + 112)) {
            ebpf_errorCode = PacketTooShort;
            goto reject;
        }
        hdr.ethernet.dstAddr = (u64)((load_dword(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits)) >> 16) & EBPF_MASK(u64, 48));
        ebpf_packetOffsetInBits += 48;

        hdr.ethernet.srcAddr = (u64)((load_dword(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits)) >> 16) & EBPF_MASK(u64, 48));
        ebpf_packetOffsetInBits += 48;

        hdr.ethernet.etherType = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.ethernet.ebpf_valid = 1;
        switch (hdr.ethernet.etherType) {
            case 0x800: goto parse_ipv4;
            default: goto accept;
        }
    }
    parse_ipv4: {
/* extract(hdr.ipv4)*/
        if (ebpf_packetEnd < ebpf_packetStart + BYTES(ebpf_packetOffsetInBits + 160)) {
            ebpf_errorCode = PacketTooShort;
            goto reject;
        }
        hdr.ipv4.version = (u8)((load_byte(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits)) >> 4) & EBPF_MASK(u8, 4));
        ebpf_packetOffsetInBits += 4;

        hdr.ipv4.ihl = (u8)((load_byte(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))) & EBPF_MASK(u8, 4));
        ebpf_packetOffsetInBits += 4;

        hdr.ipv4.diffserv = (u8)((load_byte(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 8;

        hdr.ipv4.totalLen = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.ipv4.id = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.ipv4.flags = (u8)((load_byte(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits)) >> 5) & EBPF_MASK(u8, 3));
        ebpf_packetOffsetInBits += 3;

        hdr.ipv4.fragOffset = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))) & EBPF_MASK(u16, 13));
        ebpf_packetOffsetInBits += 13;

        hdr.ipv4.ttl = (u8)((load_byte(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 8;

        hdr.ipv4.protocol = (u8)((load_byte(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 8;

        hdr.ipv4.hdrChecksum = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.ipv4.srcAddr = (u32)((load_word(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 32;

        hdr.ipv4.dstAddr = (u32)((load_word(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 32;

        hdr.ipv4.ebpf_valid = 1;
        switch (hdr.ipv4.protocol) {
            case 0x11: goto parse_udp;
            default: goto accept;
        }
    }
    parse_udp: {
/* extract(hdr.udp)*/
        if (ebpf_packetEnd < ebpf_packetStart + BYTES(ebpf_packetOffsetInBits + 64)) {
            ebpf_errorCode = PacketTooShort;
            goto reject;
        }
        hdr.udp.sport = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.udp.dport = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.udp.len = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.udp.checksum = (u16)((load_half(ebpf_packetStart, BYTES(ebpf_packetOffsetInBits))));
        ebpf_packetOffsetInBits += 16;

        hdr.udp.ebpf_valid = 1;
        goto accept;
    }

    reject: { return TC_ACT_SHOT; }

    accept:
    {
        u8 hit;
        {
accept = false;
            if (/* hdr.udp.isValid()*/
            hdr.udp.ebpf_valid) {
/* udp_exact_0.apply()*/
                {
                    /* construct key */
                    struct MyFilter_udp_exact_key key = {};
                    key.field0 = hdr.udp.dport;
                    /* value */
                    struct MyFilter_udp_exact_value *value = NULL;
                    /* perform lookup */
                    value = BPF_MAP_LOOKUP_ELEM(MyFilter_udp_exact, &key);
                    if (value == NULL) {
                        /* miss; find default action */
                        hit = 0;
                        value = BPF_MAP_LOOKUP_ELEM(MyFilter_udp_exact_defaultAction, &ebpf_zero);
                    } else {
                        hit = 1;
                    }
                    if (value != NULL) {
                        /* run action */
                        switch (value->action) {
                            case MyFilter_drop: 
                            {
accept = false;
                            }
                            break;
                            case MyFilter_save: 
                            {
accept = true;
                            }
                            break;
                            default: return TC_ACT_SHOT;
                        }
                    }
                    else return TC_ACT_SHOT;
                }
;
                if (accept) {
/* drop_save_counter_0.increment(1)*/
{
                        MyFilter_drop_save_counter_value *value_0;
                        MyFilter_drop_save_counter_value init_val = 1;
                        MyFilter_drop_save_counter_key key_0 = 1;
                        value_0 = BPF_MAP_LOOKUP_ELEM(MyFilter_drop_save_counter, &key_0);
                        if (value_0 != NULL)
                            __sync_fetch_and_add(value_0, 1);
                        else
                            BPF_MAP_UPDATE_ELEM(MyFilter_drop_save_counter, &key_0, &init_val, BPF_ANY);
                    }
;                }

                else {
/* drop_save_counter_0.increment(0)*/
{
                        MyFilter_drop_save_counter_value *value_1;
                        MyFilter_drop_save_counter_value init_val = 1;
                        MyFilter_drop_save_counter_key key_1 = 0;
                        value_1 = BPF_MAP_LOOKUP_ELEM(MyFilter_drop_save_counter, &key_1);
                        if (value_1 != NULL)
                            __sync_fetch_and_add(value_1, 1);
                        else
                            BPF_MAP_UPDATE_ELEM(MyFilter_drop_save_counter, &key_1, &init_val, BPF_ANY);
                    }
;                }

            }
        }
    }
    ebpf_end:
    if (accept)
        return TC_ACT_OK;
    else
        return TC_ACT_SHOT;
}
char _license[] SEC("license") = "GPL";
