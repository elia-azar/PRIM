import matplotlib.pyplot as plt
from numpy import var, mean, sqrt
import parser as the_parser

method_list = ["bcc", "tcpdump", "xdpdump"]

METHOD = "bcc"

SCATTER = True
N = 50
# value returned by parser.py
x = [0, 1, 2, 3, 4, 5, 6, 7]


def parse(file_name):
    received = []
    for val in x:
        file = open(file_name + str(val) + ".txt", 'r')
        Lines = file.readlines()
        if METHOD == "moongen":
            parse_moongen(Lines, received)
        elif METHOD == "tcpdump":
            parse_tcpdump(Lines, received)
        elif METHOD == "xdpdump":
            parse_xdpdump(Lines, received)
        elif METHOD == "bcc":
            parse_bcc(Lines, received)
        
    sent = the_parser.sent_list("data/%s/results_generator_%s_" % (METHOD, METHOD))

    return received, sent

def parse_moongen(Lines, received):
    for j in range(0, len(Lines), 4):
        index = Lines[j+1].strip().split().index("total") + 1
        received.append(int(Lines[j+1].strip().split()[index]))

def parse_xdpdump(Lines, received):
    for j in range(0, len(Lines), 4):
        received.append(int(Lines[j+1].split()[0].strip()))

def parse_tcpdump(Lines, received):
    for j in range(0, len(Lines), 5):
        received.append(int(Lines[j+1].split()[0].strip()))

def parse_bcc(Lines, received):
    for j in range(0, len(Lines), 2):
        received.append(int(Lines[j+1].split()[-1].strip()))


def compute(file_name):
    scatter_cap = []
    cap = []
    lower_cap = []
    upper_cap = []
    received, sent = parse(file_name)
    for i in range(7):
        sub_cap = [100*r/s for r,s in zip(received[N*i:N*(i+1)], sent[N*i:N*(i+1)])]
        scatter_cap.append(tuple(sub_cap))
        
        mean_cap = mean(sub_cap)
        cap.append(mean_cap)
        std = sqrt(var(sub_cap))
        lower_cap.append(max(0,mean_cap - 1.96 * std / sqrt(len(sub_cap))))
        upper_cap.append(mean_cap + 1.96 * std / sqrt(len(sub_cap)))
    
    return scatter_cap, lower_cap, cap, upper_cap

def plot(file_name):
    scatter_cap, lower_cap, cap, upper_cap = compute(file_name)
    if SCATTER:
        for xe, ye in zip(x, scatter_cap):
            plt.scatter([xe] * len(ye), ye, color = 'b')

        plt.xticks(x)
        plt.axes().set_xticklabels(['0','1','2','3','4','5','6','7'])
    else:
        plt.plot(x, lower_cap, x, upper_cap, color='blue', alpha=0.1)
        plt.fill_between(x, lower_cap, upper_cap, where=upper_cap >= lower_cap, alpha=0.3, facecolor='blue', interpolate=True)

        # plot lines 
        plt.plot(x, cap, label = "Captured pkts", color="blue") 


    plt.title("RX packets vs filter size with 100% packets matching the filter -- {0}".format(METHOD))
    plt.ylabel('RX pkts (%)')
    plt.xlabel('Filter size')
    plt.grid(linestyle="--")
    #plt.legend() 

    plt.savefig("images/%s_percentage_vs_filter_match_%s.png" % (("scatter", METHOD) if SCATTER else ("plot", METHOD)))


for METHOD in method_list:
    file_name = "data/%s/results_%s_" % (METHOD, METHOD)
    plot(file_name)