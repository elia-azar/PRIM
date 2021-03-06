MAX = (256 << 24) + (256 << 16) + (256 << 8) + 256

def hex2num(hex):
    value = int(hex[3].strip(), 16)
    value *= 256
    value += int(hex[2].strip(), 16)
    value *= 256
    value += int(hex[1].strip(), 16)
    value *= 256
    value += int(hex[0].strip(), 16)
    return value

def parse_generator(i, method):
    x = []
    file = open("data/%s/results_generator%i.txt" % (method, i), 'r')
    Lines = file.readlines()
    # Strips the newline character 
    for j in range(0, len(Lines), 4):
        res = 0
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            index = Lines[j+1].strip().split().index("total") + 1
            res += float(Lines[j+1].strip().split()[index])
            index = Lines[j+2].strip().split().index("total") + 1
            res += float(Lines[j+2].strip().split()[index])
            index = Lines[j+3].strip().split().index("total") + 1
            res += float(Lines[j+3].strip().split()[index])
            x.append(res)
    return x

def u32_sub(n1, n2):
    if n1 >= n2:
        return n1 - n2
    else:
        return n1 + MAX - n2

def print_list(x):
    print("-------------------------------------------")
    print("this is the length of the list: %i" % len(x))
    for xx in x:
        print("{:.2f}".format(xx), end=', ')
    print()
    print("-------------------------------------------")