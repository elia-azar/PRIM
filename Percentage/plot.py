import matplotlib.pyplot as plt
from numpy import mean, sqrt, var

METHOD = "moongen"

file_name = "data/%s/results_%s" % (METHOD, METHOD)
N = 50

x = [0,10,20,30,40,50,60,70,80,90,100]

def parse(file_name):
    cap_box = []
    filtered_box = []
    total_box = []
    for i in range(11):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines()
        if METHOD == "moongen":
            parse_moongen(Lines, cap_box, filtered_box, total_box)

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
    for i,j in zip(cap_box,filtered_box):
        total_box.append(i+j)



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
    plt.plot(x, lower_filtered, x, upper_filtered, color='orange', alpha=0.1)
    plt.fill_between(x, lower_filtered, upper_filtered, where=upper_filtered >= lower_filtered, alpha=0.3, facecolor='orange', interpolate=True)
    plt.plot(x, lower_total, x, upper_total, color='green', alpha=0.1)
    plt.fill_between(x, lower_total, upper_total, where=upper_total >= lower_total, alpha=0.3, facecolor='green', interpolate=True)

    # plot lines 
    plt.plot(x, cap, label = "Captured pkts", color="blue") 
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