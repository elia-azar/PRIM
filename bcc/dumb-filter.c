#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>


BPF_HASH(pkt_count);

/*eBPF program.
  Accepts all the incoming packets and increments the counter for every packet
*/
int dumb_filter(struct __sk_buff *skb) {

    u64 key = 1;
    u64 counter = 0;
    u64 *p;

    p = pkt_count.lookup(&key);
    if (p != 0) {
        counter = *p;
    }
    counter++;
    pkt_count.update(&key, &counter);
    return -key;
}