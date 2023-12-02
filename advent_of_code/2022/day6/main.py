import numpy as np

def main():

    with open("input.txt") as file:
        lines = [line.rstrip() for line in file]

    # find four unique characters
    mylist = []
    for i in range (0, len(lines[0])):

        mylist.append(lines[0][i])
        if len(mylist) == 4 :

            # how many times does each index appear?
            unique = True
            for j in range (0, 4):
                if mylist.count(mylist[j]) > 1 :
                    unique = False
                    break

            if unique :
                print(mylist, i+1)
                break
            tmp = []
            tmp.append(mylist[1])
            tmp.append(mylist[2])
            tmp.append(mylist[3])
            mylist = tmp
                

    # find 14 unique characters
    mylist = []
    for i in range (0, len(lines[0])):

        mylist.append(lines[0][i])
        if len(mylist) == 14 :

            # how many times does each index appear?
            unique = True
            for j in range (0, 14):
                if mylist.count(mylist[j]) > 1 :
                    unique = False
                    break

            if unique :
                print(mylist, i+1)
                break
            tmp = []
            for j in range (0, 13):
                tmp.append(mylist[j+1])
            mylist = tmp
                

if __name__ == "__main__":
    main()
