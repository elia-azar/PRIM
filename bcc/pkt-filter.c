#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

#define IP_UDP   17
#define UDP_PORT 320
#define ETH_HLEN 14

BPF_HASH(pkt_count);

/*eBPF program.
  Filter UDP packets
  The program is loaded as PROG_TYPE_SOCKET_FILTER and attached to a socket
  return  0 -> DROP the packet
  return -1 -> KEEP the packet and return it to user space (userspace can read it from the socket_fd )
*/
int udp_filter(struct __sk_buff *skb) {

    u8 *cursor = 0;
    u64 key = 1;
    u64 counter = 0;
    u64 *p;
    
    struct ethernet_t *ethernet = cursor_advance(cursor, sizeof(*ethernet));
    //filter IP packets (ethernet type = 0x0800)
    if (!(ethernet->type == 0x0800)) {
        key = 0;
        goto END;
    }

    struct ip_t *ip = cursor_advance(cursor, sizeof(*ip));
    //filter UDP packets (ip next protocol = 0x11)
    if (ip->nextp != IP_UDP) {
        key = 0;
        goto END;
    }

    u32  udp_header_length = 8;
    u32  ip_header_length = 0;
    u32  payload_length = 0;

    //calculate ip header length
    ip_header_length = ip->hlen << 2;

    //check ip header length against minimum
    if (ip_header_length < sizeof(*ip)) {
        key = 0;
        goto END;
    }

    //shift cursor forward for dynamic ip header size
    void *_ = cursor_advance(cursor, (ip_header_length-sizeof(*ip)));

    struct udp_t *udp = cursor_advance(cursor, sizeof(*udp));

    u16 port = udp->dport;

    //check ip header length against minimum
    if (port != UDP_PORT){
        key = 0;
        goto END;
    }

    //key = 1 -> keep the packet and send it to userspace by returning -1
    //key = 0 -> drop the packet by returning 0
    END:
    p = pkt_count.lookup(&key);
    if (p != 0) {
        counter = *p;
    }
    counter++;
    pkt_count.update(&key, &counter);
    return -key;
}