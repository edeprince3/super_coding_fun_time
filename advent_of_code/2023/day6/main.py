
with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

time = lines[0].split(' ')
while '' in time :
    time.remove('')

dist = lines[1].split(' ')
while '' in dist :
    dist.remove('')

total = 1
for race in range (1, len(time)):

    count = 0
    for speed in range (0, int(time[race])) :

        my_distance = speed * (int(time[race]) - speed)

        if my_distance  > int(dist[race]) :
            count += 1
        
    total *= count

print(total)

# part 2

real_time = ''
real_dist = ''
for race in range (1, len(time)):
    real_time += time[race]
    real_dist += dist[race]

count = 0
for speed in range (0, int(real_time)):

    my_distance = speed * (int(real_time) - speed)

    if my_distance  > int(real_dist) :
        count += 1
        
print(count)
