import matplotlib.pyplot as plt
from numpy import mean, sqrt, var

METHOD = "tcpdump"

file_name = "data/%s/results_%s" % (METHOD, METHOD)
N = 50

x = [0,10,20,30,40,50,60,70,80,90,100]

def parse(file_name):
    total_box = []
    for i in range(11):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines()
        if METHOD == "moongen":
            parse_moongen(Lines, total_box)

    return total_box

def parse_moongen(Lines, total_box):
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


def compute_min_mean_max(file_name):
    total_box = parse(file_name)
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

a,b,c = compute_min_mean_max(file_name)
plot_percentage_loss(a,b,c)