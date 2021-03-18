import matplotlib.pyplot as plt
from numpy import mean, sqrt, var

# create data 
file_name = "results_dump"
cap_box = []
filter_box = []
lower_total = []
upper_total = []
total_box = []
total = []

N = 20

x = [0,10,20,30,40,50,60,70,80,90,100] 

for i in range(11):
    file = open(file_name + str(i) + ".txt", 'r')
    Lines = file.readlines() 
    captured = 0
    filtered = 0
    captured_ = 0
    filtered_ = 0
    dev_ = 0
    # Strips the newline character 
    for j in range(len(Lines)):
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        if line[0] == "Capture":
            captured_ = int(line[-1])
        elif line[0] == "Filter":
            filtered_ = int(line[-1])
        elif line[0] == "Device:":
            dev_ = int(line[-1])
            captured += captured_ * 100 / dev_
            cap_box.append(captured_ * 100 / dev_)
            filtered += filtered_ * 100 / dev_
            filter_box.append(filtered_ * 100 / dev_)


for i,j in zip(cap_box,filter_box):
    total_box.append(100 - (i+j))


# basic plot

for i in range(11):
    sub_total = total_box[N*i:N*(i+1)]
    mean_total = mean(sub_total)
    total.append(mean_total)
    std = sqrt(var(sub_total))
    lower_total.append(max(0,mean_total - 1.96 * std / sqrt(len(sub_total))))
    upper_total.append(mean_total + 1.96 * std / sqrt(len(sub_total)))


plt.plot(x, lower_total, x, upper_total, color='blue', alpha=0.1)
plt.fill_between(x, lower_total, upper_total, where=upper_total >= lower_total, alpha=0.3, facecolor='blue', interpolate=True)

# plot lines 
plt.plot(x, total, label = "Lost pkts", color="blue")
plt.title('Packet loss vs matching filter')
plt.ylabel('Lost pkts (%)')
plt.xlabel('Pkts matching the filter (%)')
plt.legend() 

plt.savefig("percentage_loss.png")