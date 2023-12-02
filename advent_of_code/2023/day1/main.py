"""
part 1
 
You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""


"""
part 2 

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

import numpy as np

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

# part 1

total = 0
for line in lines:
    numbers = []
    for chars in line:
        val = ord(chars) - ord('0')
        if val < 10 :
            numbers.append(val)
    if len(numbers) > 1 :
        total += 10 * numbers[0] + numbers[-1]
    else :
        total += 10 * numbers[0] + numbers[0]
            
print(total)

# part 2

total = 0
for line in lines:
    numbers = []
    for i in range (0, len(line)):
        chars = line[i]
        val = ord(chars) - ord('0')
        if val < 10 :
            numbers.append(val)
        else :
            if len(line[i:]) >= 3 and line[i:i+3] == 'one' :
                numbers.append(1)
            elif len(line[i:]) >= 3 and line[i:i+3] == 'two' :
                numbers.append(2)
            elif len(line[i:]) >= 5 and line[i:i+5] == 'three' :
                numbers.append(3)
            elif len(line[i:]) >= 4 and line[i:i+4] == 'four' :
                numbers.append(4)
            elif len(line[i:]) >= 4 and line[i:i+4] == 'five' :
                numbers.append(5)
            elif len(line[i:]) >= 3 and line[i:i+3] == 'six' :
                numbers.append(6)
            elif len(line[i:]) >= 5 and line[i:i+5] == 'seven' :
                numbers.append(7)
            elif len(line[i:]) >= 5 and line[i:i+5] == 'eight' :
                numbers.append(8)
            elif len(line[i:]) >= 4 and line[i:i+4] == 'nine' :
                numbers.append(9)
            elif len(line[i:]) >= 4 and line[i:i+4] == 'zero' :
                numbers.append(0)

    if len(numbers) > 1 :
        total += 10 * numbers[0] + numbers[-1]
    else :
        total += 10 * numbers[0] + numbers[0]
            
print(total)
