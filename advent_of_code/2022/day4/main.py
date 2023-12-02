
def main():

    with open("input.txt") as file:
        lines = [line.rstrip() for line in file]

    
    range1 = []
    range2 = []
    for i in range (0, len(lines)):
        list1 = []
        list2 = []
        tmp = lines[i].split(',')
        tmp1 = tmp[0].split('-')
        tmp2 = tmp[1].split('-')

        range1.append([int(tmp1[0]), int(tmp1[1])])
        range2.append([int(tmp2[0]), int(tmp2[1])])

    total = 0
    for i in range (0, len(lines)):

        if range1[i][0] >= range2[i][0] and range1[i][1] <= range2[i][1]:
           total += 1

        elif range2[i][0] >= range1[i][0] and range2[i][1] <= range1[i][1]:
           total += 1

    print(total)

    total = 0
    for i in range (0, len(lines)):

        if range1[i][0] >= range2[i][0] and range1[i][0] <= range2[i][1]:
           total += 1
        elif range1[i][1] >= range2[i][0] and range1[i][1] <= range2[i][1]:
           total += 1
        elif range2[i][0] >= range1[i][0] and range2[i][0] <= range1[i][1]:
           total += 1
        elif range2[i][1] >= range1[i][0] and range2[i][1] <= range1[i][1]:
           total += 1

    print(total)
if __name__ == "__main__":
    main()
