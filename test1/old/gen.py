file_name = "results_generator"

x = []

for i in range(5):
    file = open(file_name + str(i) + ".txt", 'r')
    Lines = file.readlines() 
    # Strips the newline character 
    for j in range(0, len(Lines), 4):
        res = 0
        line = Lines[j].strip().split()
        if len(line) < 1:
            continue
        elif line[0] == "New":
            res += float(Lines[j+1].strip().split()[0])
            res += float(Lines[j+2].strip().split()[0])
            res += float(Lines[j+3].strip().split()[0])
            x.append(res)

print(x)