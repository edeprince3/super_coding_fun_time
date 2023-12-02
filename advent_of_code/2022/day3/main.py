
def main():

    with open("input.txt") as file:
        lines = [line.rstrip() for line in file]

    total = 0
    for i in range (len(lines)):
        n = len(lines[i]) // 2
        list1 = []
        list2 = []
        for j in range (0,n):

            # value in first list: a = 1 ... A = 27 ...
            val = ord(lines[i][j])
            if val - 97 < 0:
                val = val - 65 + 27
            else : val = val - 97 + 1

            list1.append(val)

            # value in second list: a = 1 ... A = 27 ...
            val = ord(lines[i][j + n])
            if val - 97 < 0:
                val = val - 65 + 27
            else :
                val = val - 97 + 1

            list2.append(val)

        # in both compartments?
        for j in range (0,n):

            # item 2 in list 1?
            if list1.count(list2[j]) > 0:
                total += list2[j]
                break

            # item 1 in list 2?
            if list2.count(list1[j]) > 0:
                total += list1[j]
                break


    print(total)

    total = 0

    ngroups = len(lines) // 3

    for i in range (0, ngroups):

        n1 = len(lines[3*i])
        list1 = []
        for j in range (0,n1):

            # value in first list: a = 1 ... A = 27 ...
            val = ord(lines[3*i][j])
            if val - 97 < 0:
                val = val - 65 + 27
            else :
                val = val - 97 + 1

            list1.append(val)

        n2 = len(lines[3*i+1])
        list2 = []
        for j in range (0,n2):

            # value in first list: a = 1 ... A = 27 ...
            val = ord(lines[3*i+1][j])
            if val - 97 < 0:
                val = val - 65 + 27
            else :
                val = val - 97 + 1

            list2.append(val)


        n3 = len(lines[3*i+2])
        list3 = []
        for j in range (0,n3):

            # value in first list: a = 1 ... A = 27 ...
            val = ord(lines[3*i+2][j])
            if val - 97 < 0:
                val = val - 65 + 27
            else :
                val = val - 97 + 1

            list3.append(val)

        # now, which item is in all three lists?
        for j in range (0,n1):

            # item 1 in list 2?
            if list2.count(list1[j]) > 0 and list3.count(list1[j]) > 0 :
                total += list1[j]
                break

    print(total)

if __name__ == "__main__":
    main()
