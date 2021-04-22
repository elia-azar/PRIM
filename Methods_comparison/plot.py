import matplotlib.pyplot as plt
import numpy as np

labels = ['print', 'pcap', '/dev/null', '/dev/null w. filter']
tcpdump = [3854197, 97485587, 98667143, 12322299]
moongen = [279853, 212805119, 518657863, 448772404]
pdump = [0, 102185086, 158297349, 0]
xdp = [892457, 97197078, 103568567, 66722471]
bcc = [1412441, 4190632, 61040784, 59974560]
p4_ebpf = [0, 0, 75746418 ,74753022]
p4_xdp = [0, 0, 56924483, 56543853]

tcpdump_loss = [99.56, 88.71, 88.53, 98.57]
moongen_loss = [99.97, 75.33, 40.01, 48.13]
pdump_loss = [0, 88.20,  81.75, 0]
xdp_loss = [99.9, 88.67, 88, 92.24]
bcc_loss = [99.84, 99.52, 92.69, 93.12]
p4_ebpf_loss = [0, 0, 91.27 ,91.39]
p4_xdp_loss = [0, 0, 93.44, 93.50]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - 3*width/7, tcpdump_loss, width/7, label='tcpdump')
rects2 = ax.bar(x - 2*width/7, moongen_loss, width/7, label='moongen')
rects3 = ax.bar(x - width/7, xdp_loss, width/7, label='xdp-dump')
rects4 = ax.bar(x, bcc_loss, width/7, label='bcc')
rects5 = ax.bar(x + width/7, pdump_loss, width/7, label='pdump')
rects6 = ax.bar(x + 2*width/7, p4_xdp_loss, width/7, label='p4-xdp')
rects7 = ax.bar(x + 3*width/7, p4_ebpf_loss, width/7, label='p4-ebpf')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Packet Loss')
ax.set_title('Packet Loss vs. method')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.savefig("pkt_loss.png")

fig, ax = plt.subplots()
rects1 = ax.bar(x - 3*width/7, tcpdump, width/7, label='tcpdump')
rects2 = ax.bar(x - 2*width/7, moongen, width/7, label='moongen')
rects3 = ax.bar(x - width/7, xdp, width/7, label='xdp-dump')
rects4 = ax.bar(x, bcc, width/7, label='bcc')
rects5 = ax.bar(x + width/7, pdump, width/7, label='pdump')
rects6 = ax.bar(x + 2*width/7, p4_xdp, width/7, label='p4-xdp')
rects7 = ax.bar(x + 3*width/7, p4_ebpf, width/7, label='p4-ebpf')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('RX packets')
ax.set_title('RX packets vs. method')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.savefig("rx_methods.png")

#plt.show()