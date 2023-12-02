
import numpy as np

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

calories = []

total = 0
for line in range(0,len(lines)):
    if lines[line] == '' :
        calories.append(total)
        total = 0
    else :
        total += int(lines[line])

print(np.max(calories))

total = 0
for i in range (0, 3): 

    val = np.max(calories)
    calories[ calories.index(val) ] = 0
    total += val

print(total)
