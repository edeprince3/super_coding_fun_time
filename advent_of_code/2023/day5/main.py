with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

# part 1

seeds = lines[0].split(' ')[1:]

maps = [ [] for _ in range(7) ]

map_count = 0
for i in range(2, len(lines)) :
    tmp = lines[i].split(' ')
    if len(tmp) > 1 and tmp[1] == 'map:' :
        keys = tmp[0].split('-')
        inkey = keys[0]
        outkey = keys[2]
        for j in range(i+1, len(lines)) :
            tmp = lines[j].split(' ')
            if len(tmp) == 1 :
                continue
            elif len(tmp) > 1 and tmp[1] == 'map:' :
                map_count += 1
                break
            vals = [int(tmp[0]), int(tmp[1]), int(tmp[2])]
            maps[map_count].append(vals)

seeds = [eval(i) for i in seeds]

inputs = seeds.copy()

for i in range (0, 7):
    # loop over inputs
    outputs = []
    for j in range (0, len(inputs)): 
        # loop over possible maps
        found_value = False
        for k in range (0, len(maps[i])): 
            if inputs[j] in range (maps[i][k][1], maps[i][k][1] + maps[i][k][2]) :
                diff = inputs[j] - maps[i][k][1]
                outputs.append(maps[i][k][0] + diff)
                found_value = True
                break
        if not found_value :
            outputs.append(inputs[j])
    inputs = outputs.copy()

print(min(inputs))

# part 2

seeds_start = []
seeds_end = []
for i in range (0, len(seeds)//2):
    seeds_start.append(int(seeds[2*i]))
    seeds_end.append(int(seeds[2*i+1])+int(seeds[2*i]))

# loop over seeds
min_location = 9e9
for j in range (0, len(seeds_start)): 

    start = seeds_start[j]
    end = seeds_end[j]

    for my_seed in range (start, end + 1) :

        input_value = my_seed

        for i in range (0, 7):

            # loop over possible maps
            found_value = False
            for k in range (0, len(maps[i])): 
                if input_value in range(maps[i][k][1], maps[i][k][1] + maps[i][k][2]):
                    diff = input_value - maps[i][k][1]
                    output_value = maps[i][k][0] + diff
                    found_value = True
                    break
            if not found_value :
                output_value = input_value
            input_value = output_value

        if input_value < min_location :
            #print(j, 'of', len(seeds_start), 'seed', my_seed - start, 'of' , end + 1 - start, min_location, input_value, input_value < min_location)
            min_location = input_value

print(min_location)
