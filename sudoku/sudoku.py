import numpy as np


def read_puzzle(f):
    """
    read puzzle 

    :param f: a file pointer to the open file containing the puzzles

    :return puzzle: a 9x9 numpy array containing the puzzle
    """

    puzzle = np.zeros((9,9),dtype=np.int8)

    # read grid number
    f.readline()

    for i in range (0,9):
        line = f.readline()
        for j in range (0,9):
            puzzle[i,j] = line[j]

    return puzzle

def check_block(puzzle, row, col, target):
    """
    check a block of the puzzle for a specific target

    :param puzzle: the sudoku puzzle
    :param row: a specific row of the puzzle
    :param column: a specific column of the puzzle
    :param target: a target value

    :return: true/false 
    """

    start_row = row - row % 3
    start_col = col - col % 3

    for i in range (start_row, start_row + 3):
        for j in range (start_col, start_col + 3):
            if ( puzzle[i,j] == target ):
                return True

    return False

def update_candidate_list(puzzle, candidate_list):
    """
    update candidate list for each element of puzzle

    :param puzzle: the sudoku puzzle
    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # clear candiate list
    for i in range (0,9):
        for j in range (0,9):
            position = i * 9 + j
            candidate_list[position].clear()

    # build candidate list
    for i in range (0,9):
        for j in range (0,9):
            position = i * 9 + j
            if ( puzzle[i,j] != 0 ):
                continue
            for target in range (1,10):
                in_row   = target in puzzle[i,:]
                in_col   = target in puzzle[:,j]
                in_block = check_block(puzzle, i, j, target)

                if in_row:
                    continue
                if in_col:
                    continue
                if in_block:
                    continue

                candidate_list[position].append(target)

    return candidate_list 

def loners(candidate_list):
    """
    if a candidate only occurs once in a row/column/box, then it can be designated
    as the sole valid candiate for that position

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    for target in range (1,10):

        # check for target in candidate lists of given row
        for row in range (0,9):
            n_instances = 0
            for col in range (0,9):
                position = row * 9 + col
                if target in candidate_list[position]:
                    n_instances += 1

            if n_instances != 1 :
                continue

            for col in range (0,9):
                position = row * 9 + col
                if target in candidate_list[position]:
                    candidate_list[position].clear()
                    candidate_list[position].append(target)

        # check for target in candidate lists of given column
        for col in range (0,9):
            n_instances = 0
            for row in range (0,9):
                position = row * 9 + col
                if target in candidate_list[position]:
                    n_instances += 1

            if n_instances != 1 :
                continue

            for row in range (0,9):
                position = row * 9 + col
                if target in candidate_list[position]:
                    candidate_list[position].clear()
                    candidate_list[position].append(target)
        
        # check for target in candidate lists of given block
        for bi in range (0,3):
            start_row = 3*bi
            for bj in range (0,3):
                start_col = 3*bj

                n_instances = 0
                for row in range (start_row,start_row + 3):
                    for col in range (start_col,start_col + 3):
                        position = row * 9 + col
                        if target in candidate_list[position]:
                            n_instances += 1

                if n_instances != 1 :
                    continue

                for row in range (start_row,start_row + 3):
                    for col in range (start_col,start_col + 3):
                        position = row * 9 + col
                        if target in candidate_list[position]:
                            candidate_list[position].clear()
                            candidate_list[position].append(target)

    return candidate_list

def naked_pairs(candidate_list):
    """
    if a pair of positions in the same row/column/block have only two candidates and these candidates
    are identical, those values can be removed from the candidate lists for the remaining positions
    in that row/column/block

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # march along pairs in this row by column
    for row in range (0,9):

        # march along pairs column
        for col1 in range (0,9):
            position1 = row * 9 + col1
            if len(candidate_list[position1]) != 2:
                continue
            for col2 in range (col1+1,9):
                position2 = row * 9 + col2
                if len(candidate_list[position2]) != 2:
                    continue

                # are candidate lists identical?
                if candidate_list[position1] != candidate_list[position2] :
                    continue

                val0 = candidate_list[position1][0]
                val1 = candidate_list[position1][1]

                # eliminate these candidates from other lists in the row
                for col3 in range (0,9):
                    if col3 == col1 :
                        continue
                    if col3 == col2 :
                        continue
                    position3 = row * 9 + col3

                    if val0 in candidate_list[position3]:
                        candidate_list[position3].remove(val0)

                    if val1 in candidate_list[position3]:
                        candidate_list[position3].remove(val1)

    # march along pairs in this column by row
    for col in range (0,9):

        # march along pairs row
        for row1 in range (0,9):
            position1 = row1 * 9 + col
            if len(candidate_list[position1]) != 2:
                continue
            for row2 in range (row1+1,9):
                position2 = row2 * 9 + col
                if len(candidate_list[position2]) != 2:
                    continue

                # are candidate lists identical?
                if candidate_list[position1] != candidate_list[position2] :
                    continue

                val0 = candidate_list[position1][0]
                val1 = candidate_list[position1][1]

                # eliminate these candidates from other lists in the row
                for row3 in range (0,9):
                    if row3 == row1 :
                        continue
                    if row3 == row2 :
                        continue
                    position3 = row3 * 9 + col

                    if val0 in candidate_list[position3]:
                        candidate_list[position3].remove(val0)

                    if val1 in candidate_list[position3]:
                        candidate_list[position3].remove(val1)

    # march along pairs in this block
    for bi in range (0,3):
        start_row = 3*bi
        for bj in range (0,3):
            start_col = 3*bj

            for row1 in range (start_row,start_row+3):
                for col1 in range (start_col,start_col+3):

                    # march along pairs row
                    position1 = row1 * 9 + col1
                    if len(candidate_list[position1]) != 2:
                        continue

                    for row2 in range (start_row,start_row+3):
                        for col2 in range (start_col,start_col+3):

                            position2 = row2 * 9 + col2
                            if position1 == position2:
                                continue

                            if len(candidate_list[position2]) != 2:
                                continue

                            # are candidate lists identical?
                            if candidate_list[position1] != candidate_list[position2] :
                                continue

                            val0 = candidate_list[position1][0]
                            val1 = candidate_list[position1][1]

                            # eliminate these candidates from other lists in the row
                            for row3 in range (start_row,start_row+3):
                                for col3 in range (start_col,start_col+3):

                                    position3 = row3 * 9 + col3
                                    if position1 == position3:
                                        continue
                                    if position2 == position3:
                                        continue

                                    if val0 in candidate_list[position3]:
                                        candidate_list[position3].remove(val0)

                                    if val1 in candidate_list[position3]:
                                        candidate_list[position3].remove(val1)

    candidate_list = loners(candidate_list)

    return candidate_list

def hidden_pairs(candidate_list):
    """
    if a pair of positions in the same row/column/block shared two common candidates that appear
    in no other position in the row/common/block, then these are the only viable candidates for these two
    positions 

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # check for hidden pairs in each row, by column
    for row in range (0,9):

        # march along pairs column
        for col1 in range (0,9):
            position1 = row * 9 + col1
            if len(candidate_list[position1]) < 2:
                continue
            for col2 in range (col1+1,9):
                position2 = row * 9 + col2
                if len(candidate_list[position2]) < 2:
                    continue

                kill_search = False
                for val1 in candidate_list[position1]:
                    for val2 in candidate_list[position1]:
                        if val1 >= val2:
                            continue

                        # ensure this pair shows up in candidate list 2
                        if val1 not in candidate_list[position2]:
                            continue
                        if val2 not in candidate_list[position2]:
                            continue

                        # do these values appear in other lists in the row
                        hidden_pair = True
                        for col3 in range (0,9):
                            position3 = row * 9 + col3
                            if position1 == position3:
                                continue
                            if position2 == position3:
                                continue
                            if val1 in candidate_list[position3]:
                                hidden_pair = False
                                break
                            if val2 in candidate_list[position3]:
                                hidden_pair = False
                                break

                        if not hidden_pair:
                            continue

                        candidate_list[position1].clear()
                        candidate_list[position2].clear()

                        candidate_list[position1].append(val1)
                        candidate_list[position2].append(val1)

                        candidate_list[position1].append(val2)
                        candidate_list[position2].append(val2)

                        kill_search = True
                        break
                    if kill_search: 
                        break

    # check for hidden pairs in each column, by column
    for col in range (0,9):

        # march along pairs row
        for row1 in range (0,9):
            position1 = row1 * 9 + col
            if len(candidate_list[position1]) < 2:
                continue
            for row2 in range (row1+1,9):
                position2 = row2 * 9 + col
                if len(candidate_list[position2]) < 2:
                    continue

                kill_search = False
                for val1 in candidate_list[position1]:
                    for val2 in candidate_list[position1]:
                        if val1 >= val2:
                            continue

                        # ensure this pair shows up in candidate list 2
                        if val1 not in candidate_list[position2]:
                            continue
                        if val2 not in candidate_list[position2]:
                            continue

                        # do these values appear in other lists in the row
                        hidden_pair = True
                        for row3 in range (0,9):
                            position3 = row3 * 9 + col
                            if position1 == position3:
                                continue
                            if position2 == position3:
                                continue
                            if val1 in candidate_list[position3]:
                                hidden_pair = False
                                break
                            if val2 in candidate_list[position3]:
                                hidden_pair = False
                                break

                        if not hidden_pair:
                            continue

                        candidate_list[position1].clear()
                        candidate_list[position2].clear()

                        candidate_list[position1].append(val1)
                        candidate_list[position2].append(val1)

                        candidate_list[position1].append(val2)
                        candidate_list[position2].append(val2)

                        kill_search = True
                        break
                    if kill_search: 
                        break

    # check for hidden pairs in each block
    for bi in range (0,3):
        start_row = 3*bi
        for bj in range (0,3):
            start_col = 3*bj

            # march along pairs in this block
            for row1 in range (start_row,start_row+3):
                for col1 in range (start_col,start_col+3):
                    position1 = row1 * 9 + col1
                    if len(candidate_list[position1]) < 2:
                        continue
                    for row2 in range (start_row,start_row+3):
                        for col2 in range (start_col,start_col+3):
                            position2 = row2 * 9 + col2
                            if position1 == position2:
                                continue
                            if len(candidate_list[position2]) < 2:
                                continue

                            kill_search = False
                            for val1 in candidate_list[position1]:
                                for val2 in candidate_list[position1]:
                                    if val1 >= val2:
                                        continue

                                    # ensure this pair shows up in candidate list 2
                                    if val1 not in candidate_list[position2]:
                                        continue
                                    if val2 not in candidate_list[position2]:
                                        continue

                                    # do these values appear in other lists in the row
                                    hidden_pair = True
                                    for row3 in range (start_row,start_row+3):
                                        for col3 in range (start_col,start_col+3):
                                            position3 = row3 * 9 + col3
                                            if position1 == position3:
                                                continue
                                            if position2 == position3:
                                                continue
                                            if val1 in candidate_list[position3]:
                                                hidden_pair = False
                                                break
                                            if val2 in candidate_list[position3]:
                                                hidden_pair = False
                                                break
                                        if not hidden_pair:
                                            break

                                    if not hidden_pair:
                                        continue

                                    candidate_list[position1].clear()
                                    candidate_list[position2].clear()

                                    candidate_list[position1].append(val1)
                                    candidate_list[position2].append(val1)

                                    candidate_list[position1].append(val2)
                                    candidate_list[position2].append(val2)

                                    kill_search = True
                                    break
                                if kill_search: 
                                    break

    candidate_list = loners(candidate_list)
    candidate_list = naked_pairs(candidate_list)

    return candidate_list

def naked_triples(candidate_list):
    """
    if three positions in the same row/column/block share the same three candidates,
    those values can be removed from the candidate lists for the remaining positions
    in that row/column/block

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # rows
    for row in range (0,9):

        # march along triples in this row by column
        for col1 in range (0,9):
            position1 = row * 9 + col1
            if ( len(candidate_list[position1]) > 3 ):
                continue
            if ( len(candidate_list[position1]) == 0 ):
                continue
            list1 = candidate_list[position1].copy()
            for col2 in range (col1+1,9):
                position2 = row * 9 + col2
                if ( len(candidate_list[position2]) > 3 ):
                    continue
                if ( len(candidate_list[position2]) == 0 ):
                    continue
                list2 = list1.copy()
                for i in range (0,len(candidate_list[position2])):

                    if ( candidate_list[position2][i] not in list2 ):
                        list2.append(candidate_list[position2][i])
                    if ( len(list2) > 3 ) :
                        continue

                for col3 in range (col2+1,9):
                    position3 = row * 9 + col3
                    if ( len(candidate_list[position3]) > 3 ):
                        continue
                    if ( len(candidate_list[position3]) == 0 ):
                        continue
                    list3 = list2.copy()
                    for i in range (0,len(candidate_list[position3])):
                        if ( candidate_list[position3][i] not in list3 ):
                            list3.append(candidate_list[position3][i])
                    if ( len(list3) != 3 ) :
                        continue

                    # remove the naked triple from other lists in this row
                    for col4 in range (col3+1,9):
                        position4 = row * 9 + col4
                        if ( position4 == position1 ) :
                            continue
                        if ( position4 == position2 ) :
                            continue
                        if ( position4 == position3 ) :
                            continue
                        val0 = list3[0]
                        val1 = list3[1]
                        val2 = list3[2]
                        if ( val0 in candidate_list[position4] ):
                            candidate_list[position4].remove(val0)
                        if ( val1 in candidate_list[position4] ):
                            candidate_list[position4].remove(val1)
                        if ( val2 in candidate_list[position4] ):
                            candidate_list[position4].remove(val2)

    # columns
    for col in range (0,9):

        # march along triples in this row by row
        for row1 in range (0,9):
            position1 = row1 * 9 + col
            if ( len(candidate_list[position1]) > 3 ):
                continue
            if ( len(candidate_list[position1]) == 0 ):
                continue
            list1 = candidate_list[position1].copy()
            for row2 in range (row1+1,9):
                position2 = row2 * 9 + col
                if ( len(candidate_list[position2]) > 3 ):
                    continue
                if ( len(candidate_list[position2]) == 0 ):
                    continue
                list2 = list1.copy()
                for i in range (0,len(candidate_list[position2])):

                    if ( candidate_list[position2][i] not in list2 ):
                        list2.append(candidate_list[position2][i])
                    if ( len(list2) > 3 ) :
                        continue

                for row3 in range (row2+1,9):
                    position3 = row3 * 9 + col
                    if ( len(candidate_list[position3]) > 3 ):
                        continue
                    if ( len(candidate_list[position3]) == 0 ):
                        continue
                    list3 = list2.copy()
                    for i in range (0,len(candidate_list[position3])):
                        if ( candidate_list[position3][i] not in list3 ):
                            list3.append(candidate_list[position3][i])
                    if ( len(list3) != 3 ) :
                        continue

                    # remove the naked triple from other lists in this row
                    for row4 in range (row3+1,9):
                        position4 = row4 * 9 + col
                        if ( position4 == position1 ) :
                            continue
                        if ( position4 == position2 ) :
                            continue
                        if ( position4 == position3 ) :
                            continue
                        val0 = list3[0]
                        val1 = list3[1]
                        val2 = list3[2]
                        if ( val0 in candidate_list[position4] ):
                            candidate_list[position4].remove(val0)
                        if ( val1 in candidate_list[position4] ):
                            candidate_list[position4].remove(val1)
                        if ( val2 in candidate_list[position4] ):
                            candidate_list[position4].remove(val2)

    # blocks
    for row_block in range (0,3):
        for col_block in range (0,3):
            for row1 in range (3*row_block, 3*row_block+3):
                for col1 in range (3*col_block, 3*col_block+3):
                    position1 = row1*9 + col1
                    if ( len(candidate_list[position1]) > 3 ):
                        continue
                    if ( len(candidate_list[position1]) == 0 ):
                        continue
                    list1 = candidate_list[position1].copy()
                    for row2 in range (3*row_block, 3*row_block+3):
                        for col2 in range (3*col_block, 3*col_block+3):
                            position2 = row2*9 + col2
                            if ( position1 == position2 ):
                                continue
                            if ( len(candidate_list[position2]) > 3 ):
                                continue
                            if ( len(candidate_list[position2]) == 0 ):
                                continue
                            list2 = list1.copy()
                            for i in range (0,len(candidate_list[position2])):

                                if ( candidate_list[position2][i] not in list2 ):
                                    list2.append(candidate_list[position2][i])
                                if ( len(list2) > 3 ) :
                                    continue
                            for row3 in range (3*row_block, 3*row_block+3):
                                for col3 in range (3*col_block, 3*col_block+3):
                                    position3 = row3*9 + col3
                                    if ( position1 == position3 ):
                                        continue
                                    if ( position2 == position3 ):
                                        continue
                                    if ( len(candidate_list[position3]) > 3 ):
                                        continue
                                    if ( len(candidate_list[position3]) == 0 ):
                                        continue

                                    list3 = list2.copy()
                                    for i in range (0,len(candidate_list[position3])):
                                        if ( candidate_list[position3][i] not in list3 ):
                                            list3.append(candidate_list[position3][i])
                                    if ( len(list3) != 3 ) :
                                        continue

                                    # remove the naked triple from other lists in this row
                                    for row4 in range (3*row_block, 3*row_block+3):
                                        for col4 in range (3*col_block, 3*col_block+3):
                                            position4 = row4*9 + col4
                                            if ( position4 == position1 ) :
                                                continue
                                            if ( position4 == position2 ) :
                                                continue
                                            if ( position4 == position3 ) :
                                                continue
                                            val0 = list3[0]
                                            val1 = list3[1]
                                            val2 = list3[2]
                                            if ( val0 in candidate_list[position4] ):
                                                candidate_list[position4].remove(val0)
                                            if ( val1 in candidate_list[position4] ):
                                                candidate_list[position4].remove(val1)
                                            if ( val2 in candidate_list[position4] ):
                                                candidate_list[position4].remove(val2)

    candidate_list = loners(candidate_list)
    candidate_list = naked_pairs(candidate_list)
    candidate_list = hidden_pairs(candidate_list)

    return candidate_list

def hidden_triples(candidate_list):
    """
    if three positions in the same row/column/block shared three common candidates that appear
    in no other position in the row/common/block, then these are the only viable candidates for these 
    three positions 

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # rows
    for row in range (0,9):

        # march along triples in this row by column
        for col1 in range (0,9):
            position1 = row * 9 + col1
            # need at least two candidates
            if ( len(candidate_list[position1]) < 2 ):
                continue
            for col2 in range (col1+1,9):
                position2 = row * 9 + col2
                # need at least two candidates
                if ( len(candidate_list[position2]) < 2 ):
                    continue
                for col3 in range (col2+1,9):
                    position3 = row * 9 + col3
                    # need at least two candidates
                    if ( len(candidate_list[position3]) < 2 ):
                        continue

                    # triplets of candidates from position1:
                    kill_search = False
                    for val1 in candidate_list[position1]:
                        for val2 in candidate_list[position1]:
                            if val2 <= val1 :
                                continue
                            for val3 in candidate_list[position1]:
                                if val3 <= val2 :
                                    continue

                                # ensure these candidates are candidates for position2:
                                if ( val1 not in candidate_list[position2] or val2 not in candidate_list[position2] or val3 not in candidate_list[position2]):
                                    continue
                                # ensure these candidates are candidates for position3:
                                if ( val1 not in candidate_list[position3] or val2 not in candidate_list[position3] or val3 not in candidate_list[position3]):
                                    continue

                                # do these candidates appear elsewhere in this row?
                                hidden_triple = True
                                for col4 in range (0,9):
                                    position4 = row * 9 + col4
                                    if ( position4 == position1 or position4 == position2 or position4 == position3 ):
                                        continue
                                    if ( val1 in candidate_list[position4] ):
                                        hidden_triple = False
                                        break
                                    if ( val2 in candidate_list[position4] ):
                                        hidden_triple = False
                                        break
                                    if ( val3 in candidate_list[position4] ):
                                        hidden_triple = False
                                        break

                                # so is this a hidden triple?
                                if ( not hidden_triple ):
                                    continue

                                # remove all candidates except val1, val2, and val3 from position1, position2, and position3
                                #print('wow, found a hidden triple (row)')
                                #print(candidate_list[position1],candidate_list[position2],candidate_list[position3])
                                candidate_list[position1].clear()
                                candidate_list[position2].clear()
                                candidate_list[position3].clear()
                                candidate_list[position1].append(val1)
                                candidate_list[position2].append(val1)
                                candidate_list[position3].append(val1)
                                candidate_list[position1].append(val2)
                                candidate_list[position2].append(val2)
                                candidate_list[position3].append(val2)
                                candidate_list[position1].append(val3)
                                candidate_list[position2].append(val3)
                                candidate_list[position3].append(val3)
                                kill_search = True
                                break
                            if ( kill_search ):
                                break
                        if ( kill_search ):
                            break

    # columns
    for col in range (0,9):

        # march along triples in this column by row
        for row1 in range (0,9):
            position1 = row1 * 9 + col
            # need at least two candidates
            if ( len(candidate_list[position1]) < 2 ):
                continue
            for row2 in range (row1+1,9):
                position2 = row2 * 9 + col
                # need at least two candidates
                if ( len(candidate_list[position2]) < 2 ):
                    continue
                for row3 in range (row2+1,9):
                    position3 = row3 * 9 + col
                    # need at least two candidates
                    if ( len(candidate_list[position3]) < 2 ):
                        continue

                    # triplets of candidates from position1:
                    kill_search = False
                    for val1 in candidate_list[position1]:
                        for val2 in candidate_list[position1]:
                            if val2 <= val1 :
                                continue
                            for val3 in candidate_list[position1]:
                                if val3 <= val2 :
                                    continue

                                # ensure these candidates are candidates for position2:
                                if ( val1 not in candidate_list[position2] or val2 not in candidate_list[position2] or val3 not in candidate_list[position2]):
                                    continue
                                # ensure these candidates are candidates for position3:
                                if ( val1 not in candidate_list[position3] or val2 not in candidate_list[position3] or val3 not in candidate_list[position3]):
                                    continue

                                # do these candidates appear elsewhere in this row?
                                hidden_triple = True
                                for row4 in range (0,9):
                                    position4 = row4 * 9 + col
                                    if ( position4 == position1 or position4 == position2 or position4 == position3 ):
                                        continue
                                    if ( val1 in candidate_list[position4] ):
                                        hidden_triple = False
                                        break
                                    if ( val2 in candidate_list[position4] ):
                                        hidden_triple = False
                                        break
                                    if ( val3 in candidate_list[position4] ):
                                        hidden_triple = False
                                        break

                                # so is this a hidden triple?
                                if ( not hidden_triple ):
                                    continue

                                # remove all candidates except val1, val2, and val3 from position1, position2, and position3
                                #print('wow, found a hidden triple (column)')
                                #print(candidate_list[position1],candidate_list[position2],candidate_list[position3])
                                candidate_list[position1].clear()
                                candidate_list[position2].clear()
                                candidate_list[position3].clear()
                                candidate_list[position1].append(val1)
                                candidate_list[position2].append(val1)
                                candidate_list[position3].append(val1)
                                candidate_list[position1].append(val2)
                                candidate_list[position2].append(val2)
                                candidate_list[position3].append(val2)
                                candidate_list[position1].append(val3)
                                candidate_list[position2].append(val3)
                                candidate_list[position3].append(val3)
                                kill_search = True
                                break
                            if ( kill_search ):
                                break
                        if ( kill_search ):
                            break
    # blocks
    for row_block in range (0,3):
        for col_block in range (0,3):

            for row1 in range (3*row_block, 3*row_block+3):
                for col1 in range (3*col_block, 3*col_block+3):
                    position1 = row1 * 9 + col1

                    # need at least two candidates
                    if ( len(candidate_list[position1]) < 2 ):
                        continue
                    for row2 in range (3*row_block, 3*row_block+3):
                        for col2 in range (3*col_block, 3*col_block+3):
                            position2 = row2 * 9 + col2
                            if ( position1 == position2 ) :
                                continue

                            # need at least two candidates
                            if ( len(candidate_list[position2]) < 2 ):
                                continue
                            for row3 in range (3*row_block, 3*row_block+3):
                                for col3 in range (3*col_block, 3*col_block+3):
                                    position3 = row3 * 9 + col3
                                    if ( position1 == position3 ) :
                                        continue
                                    if ( position2 == position3 ) :
                                        continue

                                    # need at least two candidates
                                    if ( len(candidate_list[position3]) < 2 ):
                                        continue

                                    # triplets of candidates from position1:
                                    kill_search = False
                                    for val1 in candidate_list[position1]:
                                        for val2 in candidate_list[position1]:
                                            if val2 <= val1 :
                                                continue
                                            for val3 in candidate_list[position1]:
                                                if val3 <= val2 :
                                                    continue

                                                # ensure these candidates are candidates for position2:
                                                if ( val1 not in candidate_list[position2] or val2 not in candidate_list[position2] or val3 not in candidate_list[position2]):
                                                    continue
                                                # ensure these candidates are candidates for position3:
                                                if ( val1 not in candidate_list[position3] or val2 not in candidate_list[position3] or val3 not in candidate_list[position3]):
                                                    continue

                                                # do these candidates appear elsewhere in this row?
                                                hidden_triple = True
                                                for row4 in range (3*row_block, 3*row_block+3):
                                                    for col4 in range (3*col_block, 3*col_block+3):
                                                        position4 = row4 * 9 + col4
                                                        if ( position4 == position1 or position4 == position2 or position4 == position3 ):
                                                            continue
                                                        if ( val1 in candidate_list[position4] ):
                                                            hidden_triple = False
                                                            break
                                                        if ( val2 in candidate_list[position4] ):
                                                            hidden_triple = False
                                                            break
                                                        if ( val3 in candidate_list[position4] ):
                                                            hidden_triple = False
                                                            break
                                                    if ( not hidden_triple ):
                                                        break

                                                # so is this a hidden triple?
                                                if ( not hidden_triple ):
                                                    continue

                                                # remove all candidates except val1, val2, and val3 from position1, position2, and position3
                                                #print('wow, found a hidden triple (block)')
                                                #print(candidate_list[position1],candidate_list[position2],candidate_list[position3])
                                                candidate_list[position1].clear()
                                                candidate_list[position2].clear()
                                                candidate_list[position3].clear()
                                                candidate_list[position1].append(val1)
                                                candidate_list[position2].append(val1)
                                                candidate_list[position3].append(val1)
                                                candidate_list[position1].append(val2)
                                                candidate_list[position2].append(val2)
                                                candidate_list[position3].append(val2)
                                                candidate_list[position1].append(val3)
                                                candidate_list[position2].append(val3)
                                                candidate_list[position3].append(val3)
                                                kill_search = True
                                                break
                                            if ( kill_search ):
                                                break
                                        if ( kill_search ):
                                            break

    candidate_list = loners(candidate_list)
    candidate_list = naked_pairs(candidate_list)
    candidate_list = hidden_pairs(candidate_list)
    candidate_list = naked_triples(candidate_list)

    return candidate_list

def box_claiming(candidate_list):
    """
    if a candidate appears in only one row/column of a block, then the number is claimed for that block 
    and removed from the candidate lists for the same row/column in other blocks. 

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # rows in block
    for bi in range (0,3):
        start_row = 3*bi
        for bj in range (0,3):
            start_col = 3*bj

            for target in range (1,10):

                # in how many rows does this target appear?
                n_rows = 0
                my_row = -1
                for row in range (start_row,start_row+3):
                    in_row = False
                    for col in range (start_col,start_col+3):
                        position = row * 9 + col
                        in_row = target in candidate_list[position]
                        if in_row:
                            my_row = row
                            break

                    n_rows += int(in_row)

                # can we claim this target for this block
                if n_rows != 1:
                    continue

                for col in range (0,9):
                    if col >= start_col and col < start_col + 3:
                        continue
                    position = my_row * 9 + col
                    if target in candidate_list[position]:
                        candidate_list[position].remove(target)
    # columns in block
    for bi in range (0,3):
        start_row = 3*bi
        for bj in range (0,3):
            start_col = 3*bj

            for target in range (1,10):

                # in how many colums does this target appear?
                n_cols = 0
                my_col = -1
                for col in range (start_col,start_col+3):
                    in_col = False
                    for row in range (start_row,start_row+3):
                        position = row * 9 + col
                        in_col = target in candidate_list[position]
                        if in_col:
                            my_col = col
                            break

                    n_cols += int(in_col)

                # can we claim this target for this block
                if n_cols != 1:
                    continue

                for row in range (0,9):
                    if row >= start_row and row < start_row + 3:
                        continue
                    position = row * 9 + my_col
                    if target in candidate_list[position]:
                        candidate_list[position].remove(target)
                        

    candidate_list = loners(candidate_list)
    candidate_list = naked_pairs(candidate_list)
    candidate_list = hidden_pairs(candidate_list)
    candidate_list = naked_triples(candidate_list)

    return candidate_list

def row_claiming(candidate_list):
    """
    if the only instances of a candidate in a row occur within the same block, then that number 
    can be removed from the candidate lists of all other positions within that block

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # loop over targets
    for target in range (1,10):

        # rows
        for row in range (0,9):

            # starting row for the given block
            start_row = row - row % 3

            # if target in this row, which block
            in_block = [False, False, False]

            # loop over blocks
            for block in range (0,3):
                # each column in the block
                for off in range (0,3):
                    col = 3 * block + off
                    position = row * 9 + col
                    in_block[block] = target in candidate_list[position]
                    if ( in_block[block] ):
                        break

            # 3 cases that matter ... eliminate target from lists elsehwere in block

            if in_block[0] and not in_block[1] and not in_block[2]:
                for elim_row in range (start_row, start_row+3):
                    if elim_row == row:
                        continue
                    for elim_col in range (0,3):
                        position = elim_row * 9 + elim_col
                        if target in candidate_list[position]:
                            candidate_list[position].remove(target)
            elif not in_block[0] and in_block[1] and not in_block[2]:
                for elim_row in range (start_row, start_row+3):
                    if elim_row == row:
                        continue
                    for elim_col in range (3,6):
                        position = elim_row * 9 + elim_col
                        if target in candidate_list[position]:
                            candidate_list[position].remove(target)
            elif not in_block[0] and not in_block[1] and in_block[2]:
                for elim_row in range (start_row, start_row+3):
                    if elim_row == row:
                        continue
                    for elim_col in range (6,9):
                        position = elim_row * 9 + elim_col
                        if target in candidate_list[position]:
                            candidate_list[position].remove(target)

    candidate_list = loners(candidate_list)
    candidate_list = naked_pairs(candidate_list)
    candidate_list = hidden_pairs(candidate_list)
    candidate_list = naked_triples(candidate_list)
    candidate_list = box_claiming(candidate_list)

    return candidate_list

def column_claiming(candidate_list):
    """
    if the only instances of a candidate in a column occur within the same block, then that number 
    can be removed from the candidate lists of all other positions within that block

    :param candidate_list: list of possible values for each element of puzzle

    :return candidate_list: list of possible values for each element of puzzle
    """

    # loop over targets
    for target in range (1,10):

        # columns
        for col in range (0,9):

            # starting row for the given block
            start_col = col - col % 3

            # if target in this column, which block
            in_block = [False, False, False]

            # loop over blocks
            for block in range (0,3):
                # each column in the block
                for off in range (0,3):
                    row = 3 * block + off
                    position = row * 9 + col
                    in_block[block] = target in candidate_list[position]
                    if ( in_block[block] ):
                        break

            # 3 cases that matter ... eliminate target from lists elsehwere in block

            if in_block[0] and not in_block[1] and not in_block[2]:
                for elim_col in range (start_col, start_col+3):
                    if elim_col == col:
                        continue
                    for elim_row in range (0,3):
                        position = elim_row * 9 + elim_col
                        if target in candidate_list[position]:
                            candidate_list[position].remove(target)
            elif not in_block[0] and in_block[1] and not in_block[2]:
                for elim_col in range (start_col, start_col+3):
                    if elim_col == col:
                        continue
                    for elim_row in range (3,6):
                        position = elim_row * 9 + elim_col
                        if target in candidate_list[position]:
                            candidate_list[position].remove(target)
            elif not in_block[0] and not in_block[1] and in_block[2]:
                for elim_col in range (start_col, start_col+3):
                    if elim_col == col:
                        continue
                    for elim_row in range (6,9):
                        position = elim_row * 9 + elim_col
                        if target in candidate_list[position]:
                            candidate_list[position].remove(target)

    candidate_list = loners(candidate_list)
    candidate_list = naked_pairs(candidate_list)
    candidate_list = hidden_pairs(candidate_list)
    candidate_list = naked_triples(candidate_list)
    candidate_list = box_claiming(candidate_list)
    candidate_list = row_claiming(candidate_list)

    return candidate_list

def main():
    """
    Sudoku solver.
    """


    # file pointer to puzzle file
    f = open("puzzles.txt","r")

    n_puzzles = 75
    n_solved = 0
  
    for n in range (0,n_puzzles):

        # read current puzzle
        puzzle = read_puzzle(f)

        candidate_list = [ [] for _ in range(81) ]

        for it in range (0,1000):

            candidate_list = update_candidate_list(puzzle, candidate_list)

            # check for loners
            candidate_list = loners(candidate_list)

            # check for naked pairs
            candidate_list = naked_pairs(candidate_list)

            # check for hidden pairs
            candidate_list = hidden_pairs(candidate_list)

            # check for naked triples
            candidate_list = naked_triples(candidate_list)

            # check for box claims
            candidate_list = box_claiming(candidate_list)

            # check for row claims
            candidate_list = row_claiming(candidate_list)

            # check for column claims
            candidate_list = column_claiming(candidate_list)

            # update puzzle if any positions only have one candidate
            n_moves = 0
            for i in range (0,9):
                for j in range (0,9):
                    position = i * 9 + j
                    if len(candidate_list[position]) == 1 :
                        puzzle[i,j] = candidate_list[position][0]
                        n_moves += 1
            if n_moves == 0:
                break
        
        if 0 in puzzle[:,:] :
            print('failed to solve puzzle number %i' % (n+1))
        else:
            n_solved += 1
            #print(puzzle)


    print('')
    print('solved %i/%i puzzles' % (n_solved,n_puzzles))
    print('')

if __name__ == "__main__":
    main()
