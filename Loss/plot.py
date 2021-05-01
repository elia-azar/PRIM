import matplotlib.pyplot as plt
from numpy import var, mean, sqrt
import parser as the_parser

METHOD = "tcpdump" 

# create data 
file_name = "data/%s/results_%s" % (METHOD, METHOD)
N = 50

def loss(rec, trans):
    loss = []
    for r,t in zip(rec, trans):
        loss.append(100-r*100/t)
    return loss

def parse(file_name):
    if METHOD == "tcpdump":
        return parse_tcpdump(file_name)
    elif METHOD == "moongen":
        return parse_moongen(file_name)

def parse_moongen(file_name):
    received = []
    sent = []
    for i in range(1,19):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines() 
        # Strips the newline character 
        for j in range(0, len(Lines), 4):
            line = Lines[j].strip().split()
            if len(line) < 1:
                continue
            elif line[0] == "New":
                index = Lines[j+1].strip().split().index("total") + 1
                received.append(int(Lines[j+1].strip().split()[index]))
                index = Lines[j+3].strip().split().index("total") + 1
                sent.append(int(Lines[j+3].strip().split()[index]))
    return received, sent

def parse_tcpdump(file_name):
    received = []
    sent = []
    for i in range(1,19):
        file = open(file_name + str(i) + ".txt", 'r')
        Lines = file.readlines() 
        # Strips the newline character 
        for j in range(0, len(Lines), 5):
            line = Lines[j].strip().split()
            if len(line) < 1:
                continue
            elif line[0] == "New":
                received.append(int(Lines[j+1].split()[0].strip()))
    sent = the_parser.sent_list("data/%s/%s_results_generator" % (METHOD, METHOD))
    #print("THIS IS THE RX LIST: ")
    #print_list(received)
    #print("-------------------------------------------")
    #print("THIS IS THE SENT LIST: ")
    #print_list(sent)
    return received, sent

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
    for xx in x:
        print("{:.2f}".format(xx), end=', ')
    print()


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
#plot_loss(x,y,z)