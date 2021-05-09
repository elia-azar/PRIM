import matplotlib.pyplot as plt
from numpy import mean, sqrt, var

METHOD = "bcc"

file_name = "data/%s/results_%s" % (METHOD, METHOD)
N = 50

x = [0,10,20,30,40,50,60,70,80,90,100]

def parse_loss(file_name):
    total_box = []
    for i in range(11):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines()
        if METHOD == "moongen":
            parse_loss_moongen(Lines, total_box)
        elif METHOD == "bcc":
            parse_loss_bcc(i, Lines, total_box)

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
    dev = parse_generator(i)
    cap_box = [100 * a / b for a, b in zip(captured, dev)]
    filtered_box = [100 * a / b for a, b in zip(filtered, dev)]
    for i,j in zip(cap_box,filtered_box):
        total_box.append(100 - i - j)


def parse_generator(i):
    x = []
    file = open("data/bcc/results_generator" + str(i) + ".txt", 'r')
    Lines = file.readlines()
    # Strips the newline character 
    for j in range(0, len(Lines), 4):
        res = 0
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            index = Lines[j+1].strip().split().index("total") + 1
            res += float(Lines[j+1].strip().split()[index])
            index = Lines[j+2].strip().split().index("total") + 1
            res += float(Lines[j+2].strip().split()[index])
            index = Lines[j+3].strip().split().index("total") + 1
            res += float(Lines[j+3].strip().split()[index])
            x.append(res)
    return x

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
    plt.plot(x, lower_total, x, upper_total, color='red', alpha=0.1)
    plt.fill_between(x, lower_total, upper_total, where=upper_total >= lower_total, alpha=0.3, facecolor='red', interpolate=True)

    # plot lines 
    plt.plot(x, total, label = "Lost pkts", color="red")
    plt.title('Packet loss vs matching filter -- %s' % METHOD)
    plt.ylabel('Lost pkts (%)')
    plt.xlabel('Pkts matching the filter (%)')
    plt.legend() 

    # save fig
    plt.savefig("images/%s_percentage_loss.png" % METHOD)

a,b,c = compute_min_mean_max_loss(file_name)
plot_percentage_loss(a,b,c)