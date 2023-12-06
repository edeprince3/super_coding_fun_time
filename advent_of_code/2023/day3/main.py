""" 

--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""

def number_either_way(row, col, adjacent_numbers, numbers, lines) :

    # if we find a number
    if lines[row][col] in numbers :

        # where does this number start?
        start = 0
        for i in range (col-1, -1, -1):
            if lines[row][i] not in numbers :
                start = i + 1
                break

        # where does this number end?
        end = 0
        for i in range (col+1, len(lines[row])):
            if lines[row][i] not in numbers :
                end = i - 1
                break

        digits = []
        for i in range (start, end+1):
            digits.append(lines[row][i])

        my_number = 0
        for digit in range (0, len(digits)) :
            my_number += int(digits[digit]) * pow(10, len(digits) - digit - 1)

        adjacent_numbers.append(my_number)

    return adjacent_numbers

def number_to_left(row, col, adjacent_numbers, numbers, lines) :

    # to left? 
    if col > 0 :
        if lines[row][col-1] in numbers :

            # where does this number start?
            digits = []
            for i in range (col-1, -1, -1):
                if lines[row][i] not in numbers :
                    break
                else :
                    digits.append(lines[row][i])
            digits.reverse()

            my_number = 0
            for digit in range (0, len(digits)) :
                my_number += int(digits[digit]) * pow(10, len(digits) - digit - 1)

            adjacent_numbers.append(my_number)

    return adjacent_numbers

def number_to_right(row, col, adjacent_numbers, numbers, lines) :

    # to right? 
    if col + 1 < len(lines[row]) :
        if lines[row][col+1] in numbers :

            # where does this number end?
            digits = []
            for i in range (col+1, len(lines[row])):
                if lines[row][i] not in numbers :
                    break
                else :
                    digits.append(lines[row][i])

            my_number = 0
            for digit in range (0, len(digits)) :
                my_number += int(digits[digit]) * pow(10, len(digits) - digit - 1)

            adjacent_numbers.append(my_number)

    return adjacent_numbers

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

# part 1
numbers = '1234567890'

total = 0
for row in range (0, len(lines)) : 

    line = lines[row]

    for col in range(0, len(lines[row])) :

        number = []
        if lines[row][col] in numbers :
            number.append(lines[row][col])
            for idx in range (col + 1, len(lines[row])):
                if lines[row][idx] not in numbers :
                    break
                number.append(lines[row][idx])

        if len(number) > 0 :
            value = 0
            for digit in range (0, len(number)) :
                value += int(number[digit]) * pow(10, len(number) - digit - 1)
        
        if len(number) == 0 : 
            continue

        # am i in the middle of a number?
        if col > 0 :
            if lines[row][col-1] in numbers :
                continue
        if col + len(number) < len(lines[row]) :
            if lines[row][col + len(number)] in numbers :
                continue

        # is a symbol adjacent to me?
        found_symbol = False

        # to left? 
        if col > 0 :
            if lines[row][col-1] != '.' :
                found_symbol = True
        
        # to right? 
        if col + len(number) < len(lines[row]) :
            if lines[row][col + len(number)] != '.' :
                found_symbol = True

        # above
        if row > 0 :
            for i in range (max(0, col - 1), min(len(lines[row])-1, col + len(number) + 1)) :
                if lines[row-1][i] != '.' :
                    found_symbol = True

        # below
        if row < len(lines) - 1 :
            for i in range (max(0, col - 1), min(len(lines[row])-1, col + len(number) + 1)) :
                if lines[row+1][i] != '.' :
                    found_symbol = True

        if found_symbol :
            total += value

print(total)

# part 2

total = 0
for row in range (0, len(lines)) : 

    line = lines[row]

    for col in range(0, len(lines[row])) :

        if lines[row][col] != '*' :
            continue

        adjacent_numbers = []

        # to left? 
        adjacent_numbers = number_to_left(row, col, adjacent_numbers, numbers, lines)
        
        # to right? 
        adjacent_numbers = number_to_right(row, col, adjacent_numbers, numbers, lines)

        # above 
        if row > 0 :

            # is no number directly above? then we could find two
            if lines[row-1][col] == '.' :
                # to left? 
                adjacent_numbers = number_to_left(row-1, col, adjacent_numbers, numbers, lines)
                
                # to right? 
                adjacent_numbers = number_to_right(row-1, col, adjacent_numbers, numbers, lines)

            elif lines[row-1][col] in numbers :
                adjacent_numbers = number_either_way(row-1, col, adjacent_numbers, numbers, lines)

        # below
        if row < len(lines) - 1 :

            # is no number directly below? then we could find two
            if lines[row+1][col] == '.' :
                # to left? 
                adjacent_numbers = number_to_left(row+1, col, adjacent_numbers, numbers, lines)
                
                # to right? 
                adjacent_numbers = number_to_right(row+1, col, adjacent_numbers, numbers, lines)

            elif lines[row+1][col] in numbers :
                adjacent_numbers = number_either_way(row+1, col, adjacent_numbers, numbers, lines)

        if len(adjacent_numbers) == 2 :
            #print(adjacent_numbers)
            total += adjacent_numbers[0] * adjacent_numbers[1]

print(total)
