import matplotlib.pyplot as plt
import numpy as np

labels = ['print', 'pcap', '/dev/null', '/dev/null w. filter']
tcpdump = [3854197, 62527430, 62907788, 61602103]
moongen = [279853, 212805119, 518657863, 448772404]
pdump = [0, 102185086, 158297349, 0]
xdp = [892457, 97197078, 103568567, 66722471]
bcc = [1412441, 4190632, 61040784, 59974560]
p4_ebpf = [0, 0, 75746418 ,74753022]
p4_xdp = [0, 0, 56924483, 56543853]
dpdkdump = [7379281, 176716151, 399777254, 0]

tcpdump_loss = [99.56, 92.64, 92.60, 92.75]
moongen_loss = [99.97, 75.33, 40.01, 48.13]
pdump_loss = [0, 88.20,  81.75, 0]
xdp_loss = [99.9, 88.67, 88, 92.24]
bcc_loss = [99.84, 99.52, 92.69, 93.12]
p4_ebpf_loss = [0, 0, 91.27 ,91.39]
p4_xdp_loss = [0, 0, 93.44, 93.50]
dpdkdump_loss = [99.13, 79.32, 53.22, 0]

x = np.arange(len(labels))  # the label locations
width = 0.30  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - 3*width/8 + width/16, dpdkdump_loss, width/8, label='dpdk-dump')
rects2 = ax.bar(x - 4*width/8 + width/16, p4_xdp_loss, width/8, label='p4-xdp')
rects3 = ax.bar(x - 2*width/8 + width/16, xdp_loss, width/8, label='xdp-dump')
rects4 = ax.bar(x - width/8 + width/16, bcc_loss, width/8, label='bcc')
rects5 = ax.bar(x + width/8 - width/16, tcpdump_loss, width/8, label='tcpdump')
rects6 = ax.bar(x + 2*width/8 - width/16, moongen_loss, width/8, label='moongen')
rects7 = ax.bar(x + 3*width/8 - width/16, p4_ebpf_loss, width/8, label='p4-ebpf')
rects8 = ax.bar(x + 4*width/8 - width/16, pdump_loss, width/8, label='pdump')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Packet Loss')
ax.set_title('Packet Loss vs. method')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc="upper center",prop={'size': 7})

fig.tight_layout()

plt.savefig("pkt_loss.png")

fig, ax = plt.subplots()
rects1 = ax.bar(x - 3*width/8 + width/16, dpdkdump, width/8, label='dpdk-dump')
rects2 = ax.bar(x - 4*width/8 + width/16, p4_xdp, width/8, label='p4-xdp')
rects3 = ax.bar(x - 2*width/8 + width/16, xdp, width/8, label='xdp-dump')
rects4 = ax.bar(x - 1*width/8 + width/16, bcc, width/8, label='bcc')
rects5 = ax.bar(x + width/8 - width/16, tcpdump, width/8, label='tcpdump')
rects6 = ax.bar(x + 2*width/8 - width/16, moongen, width/8, label='moongen')
rects7 = ax.bar(x + 3*width/8 - width/16, p4_ebpf, width/8, label='p4-ebpf')
rects8 = ax.bar(x + 4*width/8 - width/16, pdump, width/8, label='pdump')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('RX packets')
ax.set_title('RX packets vs. method')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend( prop={'size': 7})

fig.tight_layout()

plt.savefig("rx_methods.png")

#plt.show()