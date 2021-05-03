import matplotlib.pyplot as plt
from numpy import var, mean, sqrt
import parser as the_parser

METHOD = "p4xdp" 

# create data 
file_name = "data/%s/results_%s" % (METHOD, METHOD)
N = 50

def loss(rec, trans):
    loss = []
    for r,t in zip(rec, trans):
        loss.append(100-r*100/t)
    return loss

def parse(file_name):
    received = []
    for i in range(1,19):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines() 
        if METHOD == "tcpdump":
            parse_tcpdump(Lines, received)
        elif METHOD == "moongen":
            parse_moongen(Lines, received)
        elif METHOD == "p4ebpf" or METHOD == "p4xdp":
            parse_p4ebpf_p4xdp(Lines, received)
    
    sent = the_parser.sent_list("data/%s/%s_results_generator" % (METHOD, METHOD))

    return received, sent

def parse_moongen(Lines, received):
    for j in range(0, len(Lines), 4):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            index = Lines[j+1].strip().split().index("total") + 1
            received.append(int(Lines[j+1].strip().split()[index]))

def parse_tcpdump(Lines, received):
    for j in range(0, len(Lines), 5):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            received.append(int(Lines[j+1].split()[0].strip()))

def parse_p4ebpf_p4xdp(Lines, received):
    for j in range(0, len(Lines), 3):
        line = Lines[j].strip().split()
        value = 0
        if len(line) < 1:
            continue
        elif line[0] == "New":
            splitted_line = Lines[j+1].split()
            value += int(splitted_line[9].strip(), 16)
            value *= 256
            value += int(splitted_line[8].strip(), 16)
            value *= 256
            value += int(splitted_line[7].strip(), 16)
            value *= 256
            value += int(splitted_line[6].strip(), 16)
            received.append(value)

def compute_min_mean_max(file_name):
    pkt_loss = []
    upper_loss = []
    lower_loss = []
    received, sent = parse(file_name)
    for i in range(18):
        rx = []
        tx = []
        for j in range(N):
            rx.append(received[i*N+j])
            tx.append(sent[i*N+j])
        loss_val = loss(rx,tx)
        mean_val = mean(loss_val)
        pkt_loss.append(mean_val)
        std = sqrt(var(loss_val))
        lower_loss.append(max(0,mean_val - 1.96 * std / sqrt(len(loss_val))))
        upper_loss.append(mean_val + 1.96 * std / sqrt(len(loss_val)))
    return lower_loss, pkt_loss, upper_loss

def print_list(x):
    print("this is the length of the list: %i" % len(x))
    for xx in x:
        print("{:.2f}".format(xx), end=', ')
    print()
    print("-------------------------------------------")


def plot_loss(lower_loss, pkt_loss, upper_loss):
    # value returned by parser.py
    x = the_parser.mean_list("data/%s/%s_results_generator" % (METHOD, METHOD))
    # plot lower and upper bounds
    plt.plot(x, lower_loss, color='blue', alpha=0.1)
    plt.plot(x, upper_loss, color='blue', alpha=0.1)
    plt.fill_between(x, lower_loss, upper_loss, where=upper_loss >= lower_loss, alpha=0.3, facecolor='blue', interpolate=True)
    # plot mean pkt loss
    plt.plot(x, pkt_loss, color="blue") 
    plt.title('Packet Loss as a function input rate -- %s' % METHOD)
    plt.ylabel('Pkt loss (%)')
    plt.xlabel('Pkt rate (Mpps)')
    plt.legend() 
    plt.savefig("images/loss_%s.png" % METHOD)

x,y,z = compute_min_mean_max(file_name)
print_list(x)
print_list(y)
print_list(z)
plot_loss(x,y,z)