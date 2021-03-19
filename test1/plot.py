import matplotlib.pyplot as plt
from numpy import var, mean, sqrt

# create data 
file_name = "results_dump"
received = []
mean_received = []
upper_received = []
lower_received = []
sent = []
mean_sent = []
upper_sent = []
lower_sent = []
pkt_loss = []
upper_loss = []
lower_loss = []

N = 50
# value returned by parser.py
x = [0.9980000000000001, 2.0036, 3.0095999999999994, 4.0186, 5.0254, 6.0295999999999985, 7.035200000000001, 8.0556, 9.055399999999999, 10.0658, 11.057999999999998, 11.917, 12.3904, 12.9014, 13.401800000000003, 13.8924, 14.389199999999999, 14.852200000000003]

def loss(rec, trans):
    loss = []
    for r,t in zip(rec, trans):
        loss.append(100-r*100/t)
    return loss

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

def print_list(x):
    for xx in x:
        print("{:.2f}".format(xx), end=', ')
    print()

print_list(lower_loss)
print_list(pkt_loss)
print_list(upper_loss)

plt.plot(x, lower_loss, color='blue', alpha=0.1)
plt.plot(x, upper_loss, color='blue', alpha=0.1)
plt.fill_between(x, lower_loss, upper_loss, where=upper_loss >= lower_loss, alpha=0.3, facecolor='blue', interpolate=True)

# plot lines 
plt.plot(x, pkt_loss, color="blue") 
plt.title('Packet Loss vs. sending rate')
plt.ylabel('Pkt loss (%)')
plt.xlabel('Pkt rate in Mpps')
plt.legend() 

plt.savefig("loss.png")