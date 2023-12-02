import numpy as np

def main():

    with open("input.txt") as file:
        lines = [line.rstrip() for line in file]

    value = 1
    strength_sum = 0

    cycle = 1
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        tmp = lines[i].split(' ')

        if tmp[0] == 'noop':
            cycle += 1
            if cycle == 20 :
                strength_sum += value * cycle
            elif (cycle - 20) % 40 == 0 :
                strength_sum += value * cycle
                
            
        else :
            cycle += 1
            if cycle == 20 :
                strength_sum += value * cycle
            elif (cycle - 20) % 40 == 0 :
                strength_sum += value * cycle
            cycle += 1
            value += int(tmp[1])
            if cycle == 20 :
                strength_sum += value * cycle
            elif (cycle - 20) % 40 == 0 :
                strength_sum += value * cycle

    print(strength_sum)

    # part 2

    image = np.zeros( [6, 40], dtype = 'bool')

    def render(image):
        print('')
        for i in range (0, 6):
            
            string = ''
            for j in range (0, 40):
                if not image[i, j]:
                    string += '.'
                else:
                    string += '#'
            print(string)
        print('')

    render(image)
    
    cycle = 0 # start with zero this time for simpler mods
    sprite = 1
    pixel = 0
    for i in range (0, len(lines)):

        tmp = lines[i].split(' ')
        tmp = lines[i].split(' ')

        #row = int((cycle - cycle % 40)  / 40)
        #print(pixel, cycle, row)

        if tmp[0] == 'noop':

            if np.abs(pixel - sprite) < 2:
                row = int((cycle - cycle % 40)  / 40)
                #print(pixel, cycle, row)
                image[row][pixel] = '#'

            # update pixel position
            cycle += 1
            pixel += 1
            if pixel == 40: 
                pixel = 0

        else :

            if np.abs(pixel - sprite) < 2:
                row = int((cycle - cycle % 40)  / 40)
                #print(pixel, cycle, row)
                image[row][pixel] = '#'

            # update pixel position
            cycle += 1
            pixel += 1
            if pixel == 40: 
                pixel = 0

            if np.abs(pixel - sprite) < 2:
                row = int((cycle - cycle % 40)  / 40)
                #print(pixel, cycle, row)
                image[row][pixel] = '#'

            # update pixel position
            cycle += 1
            pixel += 1
            if pixel == 40: 
                pixel = 0


            sprite += int(tmp[1])

    render(image)

if __name__ == "__main__":
    main()
