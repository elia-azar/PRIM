import matplotlib.pyplot as plt
from numpy import mean, sqrt, var
import common as common

METHOD = "p4xdp"
Methods = ["bcc", "moongen", "p4ebpf", "p4xdp"]

N = 50

x = [0,10,20,30,40,50,60,70,80,90,100]

def parse_loss(file_name):
    total_box = []
    xdp_last = 0
    for i in range(11):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines()
        if METHOD == "moongen":
            parse_loss_moongen(Lines, total_box)
        elif METHOD == "bcc":
            parse_loss_bcc(i, Lines, total_box)
        elif METHOD == "p4ebpf":
            parse_loss_p4_ebpf(i, Lines, total_box)
        elif METHOD == "p4xdp":
            xdp_last = parse_loss_p4_xdp(i, Lines, total_box, xdp_last)

    return total_box

def parse_loss_moongen(Lines, total_box):
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
            total_box.append(100 - (captured + filtered) * 100 / dev )

def parse_loss_bcc(i, Lines, total_box):
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
    cap_box = [100 * a / b for a, b in zip(captured, dev)]
    filtered_box = [100 * a / b for a, b in zip(filtered, dev)]
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(100 - i - j)

def parse_loss_p4_ebpf(i, Lines, total_box):
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
    cap_box = [100 * a / b for a, b in zip(captured, dev)]
    filtered_box = [100 * a / b for a, b in zip(filtered, dev)]
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(100 - i - j)

def parse_loss_p4_xdp(i, Lines, total_box, xdp_last):
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
    cap_box = [100 * a / b for a, b in zip(captured, dev)]
    filtered_box = [100 * a / b for a, b in zip(filtered, dev)]
    for i,j in zip(cap_box[-50:],filtered_box[-50:]):
        total_box.append(100 - i - j)
    return xdp_last

def compute_min_mean_max_loss(file_name):
    total_box = parse_loss(file_name)
    lower_total = []
    total = []
    upper_total = []
    for i in range(11):
        sub_total = total_box[N*i:N*(i+1)]
        mean_total = mean(sub_total)
        total.append(mean_total)
        std = sqrt(var(sub_total))
        lower_total.append(max(0,mean_total - 1.96 * std / sqrt(len(sub_total))))
        upper_total.append(mean_total + 1.96 * std / sqrt(len(sub_total)))
    return lower_total, total, upper_total

def plot_percentage_loss(lower_total, total, upper_total):
    fig, ax = plt.subplots()
    ax.plot(x, lower_total, x, upper_total, color='red', alpha=0.1)
    ax.fill_between(x, lower_total, upper_total, where=upper_total >= lower_total, alpha=0.3, facecolor='red', interpolate=True)

    # plot lines 
    ax.plot(x, total, label = "Lost pkts", color="red")
    ax.set_title('Packet loss vs matching filter -- %s' % METHOD)
    ax.set_ylabel('Lost pkts (%)')
    ax.set_xlabel('Pkts matching the filter (%)')
    ax.grid(linestyle="--")
    ax.legend() 

    # save fig
    plt.savefig("images/%s_percentage_loss.png" % METHOD)

for METHOD in Methods:
    file_name = "data/%s/results_%s" % (METHOD, METHOD)
    a,b,c = compute_min_mean_max_loss(file_name)
    plot_percentage_loss(a,b,c)