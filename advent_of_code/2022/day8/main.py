import numpy as np

def main():

    with open("input.txt") as file:
        inlines = [line.rstrip() for line in file]

    nrow = len(inlines)
    ncol = len(inlines[0])

    lines = np.zeros( [nrow, ncol], dtype = 'int')
    for i in range (0, nrow):
        for j in range (0, ncol):
            lines[i, j]  = int(inlines[i][j])
        #print(lines[i])
       
    is_visible = np.zeros( [nrow, ncol], dtype = 'int')
    for i in range (0, nrow):
        is_visible[i, 0] = 1
        is_visible[i, ncol-1] = 1

    for i in range (0, ncol):
        is_visible[0, i] = 1
        is_visible[nrow-1, i] = 1

    for i in range (1, nrow-1):
        for j in range (1, ncol-1):

            am_i_visible = False

            my_height = lines[i][j]

            # row, left
            am_i_visible_left = True
            for k in range (0, i):
                if lines[k][j] >= my_height :
                    am_i_visible_left = False
                    #break

            # row, right
            am_i_visible_right = True
            for k in range (i+1, nrow):
                if lines[k][j] >= my_height :
                    am_i_visible_right = False
                    #break

            if am_i_visible_left or am_i_visible_right:
                am_i_visible = True

            # col, above
            am_i_visible_above = True
            for k in range (0, j):
                if lines[i][k] >= my_height :
                    am_i_visible_above = False
                    #break

            # col, below
            am_i_visible_below = True
            for k in range (j+1, ncol):
                if lines[i][k] >= my_height :
                    am_i_visible_below = False
                    #break

            if am_i_visible_above or am_i_visible_below:
                am_i_visible = True

            if am_i_visible :
                is_visible[i, j] = 1
                
    print(is_visible)
    print(np.sum(is_visible))
    
    # scenic score!
    scenic_score = np.zeros( [nrow, ncol], dtype = 'int')

    for i in range (0, nrow):
        for j in range (0, ncol):
            
            my_height = lines[i][j]

            # looking left
            n_left = 0
            for k in range (j-1, -1, -1):
                n_left += 1
                if lines[i][k] >= my_height :
                    break

            # looking right
            n_right = 0
            for k in range (j+1, ncol):
                n_right += 1
                if lines[i][k] >= my_height :
                    break

            # looking up
            n_up = 0
            for k in range (i-1, -1, -1):
                n_up += 1
                if lines[k][j] >= my_height :
                    break

            # looking down
            n_down = 0
            for k in range (i+1, nrow):
                n_down += 1
                if lines[k][j] >= my_height :
                    break

            scenic_score[i, j] = n_left * n_right * n_up * n_down

    print(scenic_score)
    print(np.max(scenic_score))



if __name__ == "__main__":
    main()
