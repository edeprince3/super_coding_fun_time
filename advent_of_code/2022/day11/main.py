import numpy as np
import sys

class monkey():

    def __init__(self, items_list, fxn_type, fxn_val, test_list):

        self.items_list = items_list
        self.test_list = test_list
        self.n_inspections = 0
        self.fxn_type = fxn_type
        self.fxn_val = fxn_val

    def add_item(self, item):
        self.insert(0, item)
        #tmp = [item]
        #for i in range (0, len(self.items_list)):
        #    tmp.append(self.items_list[i])
        #return tmp

    def remove_item(self, item):
        tmp = []
        for i in range (0, len(self.items_list)):
            if i == item:
                continue
            tmp.append(self.items_list[i])
        return tmp
 
    # old * old
    def fxn0(self, old):
        return old * old

    # old + val
    def fxn1(self, old):
        return old + self.fxn_val

    # old * val
    def fxn2(self, old):
        return old * self.fxn_val

    def operation(self, old):

        if self.fxn_type == 0: 
            return self.fxn0(old)
        if self.fxn_type == 1: 
            return self.fxn1(old)
        if self.fxn_type == 2: 
            return self.fxn2(old)

    def test(self, value):

        ret = value % self.test_list[0]
        if ret == 0 :
            return self.test_list[1]
        ret = value / self.test_list[0] - np.round(value / self.test_list[0])
        if np.abs(ret) <= 1e-6 :
            return self.test_list[1]
        return self.test_list[2]


def main():

    with open("test") as file:
        lines = [line.rstrip() for line in file]

    monkeys = []
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        #print(lines[i])
        if tmp[0] == 'Monkey' :
            i += 1
            items_list = []
            
            # items: (reversed from input)
            tmp = lines[i].split(' ')
            for j in range (len(tmp)-1, 3, -1):
                items_list.append(float(tmp[j]))
                
            # operations: 
            i += 1
            tmp = lines[i].split(' ')

            fxn_type = 0
            fxn_val = 0
            if tmp[7] == 'old':
                fxn_type = 0
            elif tmp[6] == '+':
                fxn_type = 1
                fxn_val = int(tmp[7])
            else:
                fxn_type = 2
                fxn_val = int(tmp[7])

            # tests: 
            i += 1
            tmp = lines[i].split(' ')
            test_list = [ int(tmp[5]) ]

            i += 1
            tmp = lines[i].split(' ')
            test_list.append(int(tmp[9]))

            i += 1
            tmp = lines[i].split(' ')
            test_list.append(int(tmp[9]))
            
            monkeys.append(monkey(items_list, fxn_type, fxn_val, test_list))

    # find a common factor for reducing worry
    #maxval = 100000
    #factors = []
    #for i in range (0, len(monkeys)):
    #    my_factors = np.zeros( [maxval], dtype='int')
    #    for j in range (0, maxval):
    #        val = j * monkeys[i].test_list[0]
    #        if val < maxval :
    #            my_factors[val] = 1
    #        else:
    #            break
    #    print( monkeys[i].test_list[0])
    #    print(my_factors)
    #    factors.append(my_factors)

    #common_factor = 1
    #for j in range (1, maxval):
    #    is_common = True
    #    for i in range (0, len(monkeys)):
    #        if factors[i][j] == 0:
    #            is_common = False
    #    if is_common :
    #        common_factor = j
    #        break
    #    
    #print('common factor', common_factor)
    #exit()

    sys.set_int_max_str_digits(10000000)
 
    # play n rounds
    n = 20
    for i in range (0, n):
        print(i)
        
        for j in range (0, len(monkeys)):

            for k in range (len(monkeys[j].items_list)-1, -1, -1):

                # update worry level
                tmp = monkeys[j].operation(monkeys[j].items_list[k])

                # reduce worry level 
                #tmp = float(int(np.floor(tmp / 3.0)))

                print(tmp)

                # toss item
                who = monkeys[j].test(tmp)
                monkeys[who].items_list.insert(0, tmp)

                # udpate number of inspections
                monkeys[j].n_inspections += 1

            # clear current list
            monkeys[j].items_list.clear()


    print('number of monkeys:',len(monkeys))
    for i in range (0, len(monkeys)):                
        print(monkeys[i].n_inspections)

if __name__ == "__main__":
    main()
