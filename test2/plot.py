import matplotlib.pyplot as plt
from numpy import sum

# create data 
file_name = "results_dump"
cap = []
lower_cap = []
upper_cap = []
cap_box = []
filter = []
lower_filter = []
upper_filter = []
filter_box = []
total = []
lower_total = []
upper_total = []
total_box = []

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
    #cap.append(captured/20)
    #filter.append(filtered/20)


for i,j in zip(cap,filter):
    total.append(i+j)

for i,j in zip(cap_box,filter_box):
    total_box.append(i+j)


# basic plot

for i in range(11):
    sub_cap = cap_box[20*i:20*(i+1)]
    sub_filter = filter_box[20*i:20*(i+1)]
    sub_total = total_box[20*i:20*(i+1)]
    sub_total, sub_cap, sub_filter = (list(t) for t in zip(*sorted(zip(sub_total, sub_cap, sub_filter))))
    lower_total.append(sub_total[4])
    upper_total.append(sub_total[-5])
    total.append(sum(sub_total)/12)
    lower_cap.append(sub_cap[4])
    upper_cap.append(sub_cap[-5])
    cap.append(sum(sub_cap)/12)
    lower_filter.append(sub_filter[4])
    upper_filter.append(sub_filter[-5])
    filter.append(sum(sub_filter)/12)


plt.plot(x, lower_cap, x, upper_cap, color='blue', alpha=0.1)
plt.fill_between(x, lower_cap, upper_cap, where=upper_cap >= lower_cap, alpha=0.3, facecolor='blue', interpolate=True)
plt.plot(x, lower_filter, x, upper_filter, color='orange', alpha=0.1)
plt.fill_between(x, lower_filter, upper_filter, where=upper_filter >= lower_filter, alpha=0.3, facecolor='orange', interpolate=True)
plt.plot(x, lower_total, x, upper_total, color='green', alpha=0.1)
plt.fill_between(x, lower_total, upper_total, where=upper_total >= lower_total, alpha=0.3, facecolor='green', interpolate=True)

# plot lines 
plt.plot(x, cap, label = "Captured pkts", color="blue") 
plt.plot(x, filter, label = "Dropped pkts", color="orange")
plt.plot(x, total, label = "Treated pkts", color="green")
plt.title('Packet filtering behaviour')
plt.ylabel('RX pkts (%)')
plt.xlabel('Pkts matching the filter (%)')
plt.legend() 

plt.savefig("percentage.png")