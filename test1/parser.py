from numpy import mean
file_name = "data/results_generator"

x = []

for i in range(1,19):
    file = open(file_name + str(i) + ".txt", 'r')
    Lines = file.readlines()
    xx = []
    # Strips the newline character 
    for j in range(0, len(Lines), 4):
        res = 0
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            index = Lines[j+1].strip().split().index("TX[0m:") + 1
            res += float(Lines[j+1].strip().split()[index])
            index = Lines[j+2].strip().split().index("TX[0m:") + 1
            res += float(Lines[j+2].strip().split()[index])
            index = Lines[j+3].strip().split().index("TX[0m:") + 1
            res += float(Lines[j+3].strip().split()[index])
            xx.append(res)
    x.append(xx)

def print_list(x):
    for xx in x:
        for xxx in xx:
            print("{:.2f}".format(xxx), end=', ')
        print()

def mean_list(x):
    l = []
    for xx in x:
        l.append(mean(xx))
    return l

#print_list(x)

print(mean_list(x))