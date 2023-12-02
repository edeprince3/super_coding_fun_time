import numpy as np

def update_knot(knot_x, knot_y, k):
    
    # in row
    if knot_y[k-1] == knot_y[k]:
        if knot_x[k-1] - knot_x[k] > 1 :
            knot_x[k] += 1
        elif knot_x[k-1] - knot_x[k] < -1 :
            knot_x[k] -= 1
    # in column
    elif knot_x[k-1] == knot_x[k]:
        if knot_y[k-1] - knot_y[k] > 1 :
            knot_y[k] += 1
        elif knot_y[k-1] - knot_y[k] < -1 :
            knot_y[k] -= 1
    # diagonal
    else :
        if knot_x[k-1] - knot_x[k] > 1 :
            if knot_y[k-1] > knot_y[k] :
                knot_x[k] += 1
                knot_y[k] += 1
            else :
                knot_x[k] += 1
                knot_y[k] -= 1
        elif knot_x[k-1] - knot_x[k] < -1 :
            if knot_y[k-1] > knot_y[k] :
                knot_x[k] -= 1
                knot_y[k] += 1
            else :
                knot_x[k] -= 1
                knot_y[k] -= 1
        elif knot_y[k-1] - knot_y[k] > 1 :
            if knot_x[k-1] > knot_x[k] :
                knot_x[k] += 1
                knot_y[k] += 1
            else :
                knot_x[k] -= 1
                knot_y[k] += 1
        elif knot_y[k-1] - knot_y[k] < -1 :
            if knot_x[k-1] > knot_x[k] :
                knot_x[k] += 1
                knot_y[k] -= 1
            else :
                knot_x[k] -= 1
                knot_y[k] -= 1

    return knot_x[k], knot_y[k]

def main():

    with open("input.txt") as file:
        lines = [line.rstrip() for line in file]

    direction = []
    n = []
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        direction.append(tmp[0])
        n.append(int(tmp[1]))

    # grid
    visited = []

    # number of knots
    n_knots = 10

    # starting position
    knot_x = []
    knot_y = []

    for i in range (0, n_knots):
        knot_x.append(0)
        knot_y.append(0)

    startx = 0
    starty = 0

    #print(direction)
    #print(n)

    for i in range (len(direction)):
        if direction[i] == 'R':

            for j in range (0, n[i]):

                knot_x[0] += 1

                for k in range (1, n_knots):

                    knot_x[k], knot_y[k] = update_knot(knot_x, knot_y, k)

                visited.append([knot_x[n_knots-1], knot_y[n_knots-1]])
                    
        elif direction[i] == 'L':

            for j in range (0, n[i]):

                knot_x[0] -= 1

                for k in range (1, n_knots):

                    knot_x[k], knot_y[k] = update_knot(knot_x, knot_y, k)

                visited.append([knot_x[n_knots-1], knot_y[n_knots-1]])

        elif direction[i] == 'U':

            for j in range (0, n[i]):

                knot_y[0] -= 1

                for k in range (1, n_knots):

                    knot_x[k], knot_y[k] = update_knot(knot_x, knot_y, k)

                visited.append([knot_x[n_knots-1], knot_y[n_knots-1]])

        elif direction[i] == 'D':

            for j in range (0, n[i]):

                knot_y[0] += 1

                for k in range (1, n_knots):

                    knot_x[k], knot_y[k] = update_knot(knot_x, knot_y, k)
    
                visited.append([knot_x[n_knots-1], knot_y[n_knots-1]])

        #visual = np.zeros( [25, 25], dtype='int')
        #minx = np.min(knot_x)
        #miny = np.min(knot_y)
        #tmpx = knot_x
        #tmpy = knot_y
        #if minx < 0 :
        #    tmpx -= minx
        #if miny < 0 :
        #    tmpy -= miny
        #for k in range (0, len(knot_x)):
        #    visual[tmpy[k], tmpx[k]] = k

        #print('')
        #print(visual)
        #print('')
                

    minval = np.min(visited)
    if minval < 0 :
        visited -= minval
    maxval = np.max(visited)

    newthing = []

    for i in range (len(visited)):
        newthing.append( visited[i][0] * maxval + visited[i][1])

    maxdim = np.max(newthing)

    nvisited = 0
    skip = np.zeros( maxdim + 1, dtype='bool')

    for i in range (len(visited)):
        if not skip[newthing[i]] :
            nvisited += 1
            skip[newthing[i]] = True

    print(nvisited)

if __name__ == "__main__":
    main()
