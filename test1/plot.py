import matplotlib.pyplot as plt
from numpy import sum

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

# value returned by parser.py
x = [0.9964999999999998, 2.0029999999999997, 3.0089999999999995, 4.017999999999999, 5.024499999999999, 6.0295000000000005, 7.036, 8.056000000000001, 9.054000000000002, 10.068499999999998, 11.059000000000001, 11.941500000000001, 12.424499999999998, 12.91, 13.376, 13.854500000000002, 14.4055, 14.8375]

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
    for j in range(20):
        rx.append(received[i*18+j])
        tx.append(sent[i*18+j])
    loss_val = loss(rx,tx)
    loss_val.sort()
    pkt_loss.append(sum(loss_val)/12)
    lower_loss.append(loss_val[4])
    upper_loss.append(loss_val[-5])

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