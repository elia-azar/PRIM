from numpy import mean


def data_parser(file_name, keyword):
    x = []
    for i in range(8):
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
                index = Lines[j+1].strip().split().index(keyword) + 1
                res += float(Lines[j+1].strip().split()[index])
                index = Lines[j+2].strip().split().index(keyword) + 1
                res += float(Lines[j+2].strip().split()[index])
                index = Lines[j+3].strip().split().index(keyword) + 1
                res += float(Lines[j+3].strip().split()[index])
                xx.append(res)
        x.append(xx)
    return x

def print_list(x):
    for xx in x:
        for xxx in xx:
            print("{:.2f}".format(xxx), end=', ')
        print()

def mean_list(file_name):
    x = data_parser(file_name, "TX[0m:")
    l = []
    for xx in x:
        l.append(mean(xx))
    return l

def sent_list(file_name):
    x = data_parser(file_name, "total")
    sent = []
    for xx in x:
        sent += xx
    return sent