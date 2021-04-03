import matplotlib.pyplot as plt
from numpy import var, mean, sqrt

# create data 
file_name = "data/results_dump5_.txt"

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

N = 50
# value returned by parser.py
x = [1, 2, 3, 4, 5, 6, 7]

file = open(file_name, 'r')
Lines = file.readlines()

for i in range(7):
    # Strips the newline character
    captured = 0
    filtered = 0
    for j in range(i*50*4, (i+1)*50*4, 4):
        line = Lines[j].strip().split()

        index = Lines[j+1].strip().split().index("total") + 1
        captured_ = int(Lines[j+1].strip().split()[index])
        index = Lines[j+2].strip().split().index("total") + 1
        filtered_ = int(Lines[j+2].strip().split()[index])
        index = Lines[j+3].strip().split().index("total") + 1
        dev_ = int(Lines[j+3].strip().split()[index])
        
        cap_box.append(captured_ * 100 / dev_)
        filter_box.append(filtered_ * 100 / dev_)


for i,j in zip(cap_box,filter_box):
    total_box.append(i+j)


# basic plot

for i in range(7):
    sub_cap = cap_box[N*i:N*(i+1)]
    sub_filter = filter_box[N*i:N*(i+1)]
    sub_total = total_box[N*i:N*(i+1)]
    #sub_total, sub_cap, sub_filter = (list(t) for t in zip(*sorted(zip(sub_total, sub_cap, sub_filter))))
    mean_cap = mean(sub_cap)
    cap.append(mean_cap)
    std = sqrt(var(sub_cap))
    lower_cap.append(max(0,mean_cap - 1.96 * std / sqrt(len(sub_cap))))
    upper_cap.append(mean_cap + 1.96 * std / sqrt(len(sub_cap)))

    mean_filter = mean(sub_filter)
    filter.append(mean_filter)
    std = sqrt(var(sub_filter))
    lower_filter.append(max(0,mean_filter - 1.96 * std / sqrt(len(sub_filter))))
    upper_filter.append(mean_filter + 1.96 * std / sqrt(len(sub_filter)))

    mean_total = mean(sub_total)
    total.append(mean_total)
    std = sqrt(var(sub_total))
    lower_total.append(max(0,mean_total - 1.96 * std / sqrt(len(sub_total))))
    upper_total.append(mean_total + 1.96 * std / sqrt(len(sub_total)))


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
plt.title('RX packets vs filter size with 50% packets matching the filter')
plt.ylabel('RX pkts (%)')
plt.xlabel('Filter size')
plt.legend() 

plt.savefig("percentage_vs_filter_50_match.png")