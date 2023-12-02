import numpy as np

def main():

    with open("input.txt") as file:
        lines = [line.rstrip() for line in file]

    # remove spaces
    for i in range (0, len(lines)):
        lines[i] = lines[i].split(' ')


    size_list = []
    dir_list = []
    i = 0
    mydir = []
    mysize = []
    while(i < len(lines) - 1):  
        #print(i, lines[i])

        # command
        if lines[i][0] == '$':
            # cd
            if lines[i][1] == 'cd':

                if lines[i][2] == '/':
                    mydir.clear()
                    mydir.append('/')
                    mysize.clear()
                    mysize.append(0)

                elif lines[i][2] == '..':

                    # done with this directory ... add name to final list
                    dir_list.append(mydir[len(mydir)-1])

                    # done with this directory ... add size to final list
                    size_list.append(mysize[len(mysize)-1])

                    # done with this directory ... add size to the directory above it
                    if len(mysize) > 1:
                        mysize[len(mysize)-2] += mysize[len(mysize)-1]
                    
                    # remove this directory and its size from temporary lists
                    mydir.pop()
                    mysize.pop()

                else:
                    # add directory to the temorary list
                    mydir.append(lines[i][2])

                    # initialize size of the directory
                    mysize.append(0)


                #increment i
                i = i + 1

            # ls
            elif lines[i][1] == 'ls':
                
                for j in range (i + 1, len(lines)):

                    if lines[j][0] == '$':

                        # increment i, but not so much to skip the next $
                        i = j # - 1

                        # break
                        break
                        
                    else:
                        if lines[j][0] != 'dir':
                            mysize[len(mysize)-1] += int(lines[j][0])

                        # increment i
                        i = i + 1


    # add dangling directories to final lists
    while len(mysize) > 1:
        mysize[len(mysize)-2] += mysize[len(mysize)-1]
        size_list.append(mysize[len(mysize)-1])
        dir_list.append(mydir[len(mysize)-1])
        mysize.pop()
        mydir.pop()

    # and lastly the top directory
    size_list.append(mysize[0])
    dir_list.append(mydir[0])

    print(size_list)
    total_size = 0
    for i in range (0, len(size_list)):
        if size_list[i] < 100000:
            total_size += size_list[i]
    print(total_size)
    print('')

    total_memory = 70000000
    required_memory = 30000000
    used_memory = size_list[len(size_list)-1]
    free_memory = total_memory - used_memory
    need_to_free = required_memory - free_memory

    print('required memory:',required_memory)
    print('used memory:',used_memory)
    print('need to free:',need_to_free)
    print('')

    candidate_list = []
    for i in range (0, len(size_list)):
        if size_list[i] >= need_to_free:
            candidate_list.append(size_list[i])
            
    print(candidate_list)
    print(np.min(candidate_list))

if __name__ == "__main__":
    main()
