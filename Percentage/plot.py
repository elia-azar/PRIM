import matplotlib.pyplot as plt
from numpy import mean, sqrt, var
import common as common

METHOD = "p4xdp"
file_name = "data/%s/results_%s" % (METHOD, METHOD)
N = 50

x = [0,10,20,30,40,50,60,70,80,90,100]

def parse(file_name):
    xdp_last = 0
    cap_box = []
    filtered_box = []
    total_box = []
    for i in range(11):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines()
        if METHOD == "moongen":
            parse_moongen(Lines, cap_box, filtered_box, total_box)
        elif METHOD == "tcpdump":
            parse_tcpdump(Lines, cap_box, filtered_box, total_box)
        elif METHOD == "xdpdump":
            parse_xdpdump(Lines, cap_box, filtered_box, total_box)
        elif METHOD == "bcc":
            parse_bcc(i, Lines, cap_box, filtered_box, total_box)
        elif METHOD == "p4ebpf":
            parse_p4_ebpf(i, Lines, cap_box, filtered_box, total_box)
        elif METHOD == "p4xdp":
            xdp_last = parse_p4_xdp(i, Lines, cap_box, filtered_box, total_box, xdp_last)

    return cap_box, filtered_box, total_box

def parse_moongen(Lines, cap_box, filtered_box, total_box):
    captured = 0
    filtered = 0
    for j in range(len(Lines)):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        if line[0] == "Capture":
            captured = int(line[-1])
        elif line[0] == "Filter":
            filtered = int(line[-1])
        elif line[0] == "Device:":
            dev = int(line[-1])
            cap_box.append(captured * 100 / dev)
            filtered_box.append(filtered * 100 / dev)
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(i+j)

def parse_tcpdump(Lines, cap_box, filtered_box, total_box):
    captured = 0
    for j in range(0, len(Lines), 5):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            captured = int(Lines[j+1].split()[0].strip())
            dev = int(Lines[j+4].split()[0].strip()) + captured
            cap_box.append(captured * 100 / dev)
            filtered_box.append(0)
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(i+j)

def parse_xdpdump(Lines, cap_box, filtered_box, total_box):
    captured = 0
    for j in range(0, len(Lines), 4):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            captured = int(Lines[j+1].split()[0].strip())
            dev = int(Lines[j+3].split()[0].strip()) + captured
            cap_box.append(captured * 100 / dev)
            filtered_box.append(0)
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(i+j)

def parse_bcc(i, Lines, cap_box, filtered_box, total_box):
    captured = []
    filtered = []
    for j in range(0, len(Lines), 2):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        line = Lines[j+1].split()
        if len(line) == 3:
            if line[1].strip() == "0:":
                captured.append(0)
                filtered.append(int(line[2].strip()))
            elif line[1].strip() == "1:":
                captured.append(int(line[2].strip()))
                filtered.append(0)
        elif len(line) == 6:
                filtered.append(int(line[2].strip()))
                captured.append(int(line[5].strip()))
    dev = common.parse_generator(i, METHOD)
    cap_box.extend([100 * a / b for a, b in zip(captured, dev)])
    filtered_box.extend([100 * a / b for a, b in zip(filtered, dev)])
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(i+j)

def parse_p4_ebpf(i, Lines, cap_box, filtered_box, total_box):
    captured = []
    filtered = []
    step = 4
    if i in [0, 10]:
        step = 3
    for j in range(0, len(Lines), step):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        if step == 3:
            line = Lines[j+1].split()
            key = line[1]
            if key == "01":
                captured.append(common.hex2num(line[-4:]))
                filtered.append(0)
            elif key == "00":
                filtered.append(common.hex2num(line[-4:]))
                captured.append(0)
        elif step == 4:
            filtered.append(common.hex2num(Lines[j+1].split()[-4:]))
            captured.append(common.hex2num(Lines[j+2].split()[-4:]))

    dev = common.parse_generator(i, METHOD)
    cap_box.extend([100 * a / b for a, b in zip(captured, dev)])
    filtered_box.extend([100 * a / b for a, b in zip(filtered, dev)])
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(i+j)

def parse_p4_xdp(i, Lines, cap_box, filtered_box, total_box, xdp_last):
    captured = []
    filtered = []
    step = 4
    if i == 0:
        step = 3
    for j in range(0, len(Lines), step):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        if i == 0:
            line = Lines[j+1].split()
            current_value = common.u32_sub(common.hex2num(line[-4:]), xdp_last)
            filtered.append(current_value)
            captured.append(0)
            xdp_last = common.hex2num(line[-4:])
        elif i == 10:
            line = Lines[j+2].split()
            captured.append(common.hex2num(line[-4:]))
            filtered.append(0)
        else:
            current_value = common.u32_sub(common.hex2num(Lines[j+1].split()[-4:]), xdp_last)
            filtered.append(current_value)
            captured.append(common.hex2num(Lines[j+2].split()[-4:]))
            xdp_last = common.hex2num(Lines[j+1].split()[-4:])

    dev = common.parse_generator(i, METHOD)
    cap_box.extend([100 * a / b for a, b in zip(captured, dev)])
    filtered_box.extend([100 * a / b for a, b in zip(filtered, dev)])
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(i+j)
    return xdp_last


def compute_min_mean_max(file_name):
    lower_cap = []
    cap = []
    upper_cap = []
    lower_filtered = []
    filtered = []
    upper_filtered = []
    lower_total = []
    total = []
    upper_total = []
    cap_box, filtered_box, total_box = parse(file_name)
    for i in range(11):
        # divinding the list per file
        sub_cap = cap_box[N*i:N*(i+1)]
        sub_filtered = filtered_box[N*i:N*(i+1)]
        sub_total = total_box[N*i:N*(i+1)]
        
        mean_cap = mean(sub_cap)
        cap.append(mean_cap)
        std = sqrt(var(sub_cap))
        lower_cap.append(max(0,mean_cap - 1.96 * std / sqrt(len(sub_cap))))
        upper_cap.append(mean_cap + 1.96 * std / sqrt(len(sub_cap)))

        mean_filtered = mean(sub_filtered)
        filtered.append(mean_filtered)
        std = sqrt(var(sub_filtered))
        lower_filtered.append(max(0,mean_filtered - 1.96 * std / sqrt(len(sub_filtered))))
        upper_filtered.append(mean_filtered + 1.96 * std / sqrt(len(sub_filtered)))

        mean_total = mean(sub_total)
        total.append(mean_total)
        std = sqrt(var(sub_total))
        lower_total.append(max(0,mean_total - 1.96 * std / sqrt(len(sub_total))))
        upper_total.append(mean_total + 1.96 * std / sqrt(len(sub_total)))
    
    return lower_cap, cap, upper_cap, lower_filtered, filtered, upper_filtered, lower_total, total, upper_total


def plot_percentage(lower_cap, cap, upper_cap, lower_filtered, filtered, upper_filtered, lower_total, total, upper_total):
    plt.plot(x, lower_cap, x, upper_cap, color='blue', alpha=0.1)
    plt.fill_between(x, lower_cap, upper_cap, where=upper_cap >= lower_cap, alpha=0.3, facecolor='blue', interpolate=True)
    if METHOD not in ["tcpdump", "xdpdump"]:
        plt.plot(x, lower_filtered, x, upper_filtered, color='orange', alpha=0.1)
        plt.fill_between(x, lower_filtered, upper_filtered, where=upper_filtered >= lower_filtered, alpha=0.3, facecolor='orange', interpolate=True)
        plt.plot(x, lower_total, x, upper_total, color='green', alpha=0.1)
        plt.fill_between(x, lower_total, upper_total, where=upper_total >= lower_total, alpha=0.3, facecolor='green', interpolate=True)

    # plot lines 
    plt.plot(x, cap, label = "Captured pkts", color="blue")
    if METHOD not in ["tcpdump", "xdpdump"]:
        plt.plot(x, filtered, label = "Dropped pkts", color="orange")
        plt.plot(x, total, label = "Treated pkts", color="green")
    plt.title('Packet filtering behaviour -- %s' % METHOD)
    plt.ylabel('RX pkts (%)')
    plt.xlabel('Pkts matching the filter (%)')
    plt.legend() 

    # save fig
    plt.savefig("images/%s_percentage.png" % METHOD)

a,b,c,d,e,f,g,h,i = compute_min_mean_max(file_name)
plot_percentage(a,b,c,d,e,f,g,h,i)