import matplotlib.pyplot as plt
import numpy as np

labels = ['print', 'pcap', '/dev/null', '/dev/null w. filter']
tcpdump = [3854197, 97485587, 98667143, 12322299]
moongen = [279853, 212805119, 518657863, 448772404]
pdump = [0, 102185086, 158297349, 0]
xdp = [892457, 97197078, 103568567, 0]

tcpdump_loss = [99.56, 88.71, 88.53, 98.57]
moongen_loss = [99.97, 75.33, 40.01, 48.13]
pdump_loss = [0, 88.20,  81.75, 0]
xdp_loss = [99.9, 88.67, 88, 0]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2 + width/8, tcpdump_loss, width/4, label='tcpdump')
rects2 = ax.bar(x - width/8, moongen_loss, width/4, label='moongen')
rects3 = ax.bar(x + width/8, xdp_loss, width/4, label='xdp-dump')
rects4 = ax.bar(x + width/2 - width/8, pdump_loss, width/4, label='pdump')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Packet Loss')
ax.set_title('Packet Loss vs. method')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.savefig("pkt_loss.png")

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2 + width/8, tcpdump, width/4, label='tcpdump')
rects2 = ax.bar(x - width/8, moongen, width/4, label='moongen')
rects3 = ax.bar(x + width/8, xdp, width/4, label='xdp-dump')
rects4 = ax.bar(x + width/2 - width/8, pdump, width/4, label='pdump')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('RX packets')
ax.set_title('RX packets vs. method')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.savefig("rx_methods.png")

#plt.show()