import numpy as np

def main():

    with open("boxes.txt") as file:
        lines = [line.rstrip() for line in file]

    boxes = []
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        boxes.append(tmp)

    boxes = np.asarray(boxes).transpose()
    boxes = np.flip(boxes, axis=1)
    boxes = boxes.tolist()
    for i in range (0, len(boxes)):
        n = boxes[i].count('x')
        for j in range (0, n):
            boxes[i].remove('x')
        print(boxes[i])

    with open("instructions.txt") as file:
        lines = [line.rstrip() for line in file]

    moves = []
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        moves.append(tmp)

    for i in range (0, len(moves)):
        # move moves[i][0] from moves[i][1] to moves[i][2]
        n = int(moves[i][0])
        start = int(moves[i][1]) - 1
        end = int(moves[i][2]) - 1

        for j in range (0, n):
            boxes[end].append(boxes[start][len(boxes[start])-1])
            boxes[start].pop()

    print('')
    for i in range (0, len(boxes)):
        print(boxes[i])

    for i in range (0, len(boxes)):
        print(boxes[i][len(boxes[i])-1])

    # ok start over
    with open("boxes.txt") as file:
        lines = [line.rstrip() for line in file]

    boxes = []
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        boxes.append(tmp)

    boxes = np.asarray(boxes).transpose()
    boxes = np.flip(boxes, axis=1)
    boxes = boxes.tolist()
    for i in range (0, len(boxes)):
        n = boxes[i].count('x')
        for j in range (0, n):
            boxes[i].remove('x')
        print(boxes[i])

    with open("instructions.txt") as file:
        lines = [line.rstrip() for line in file]

    moves = []
    for i in range (0, len(lines)):
        tmp = lines[i].split(' ')
        moves.append(tmp)

    for i in range (0, len(moves)):
        # move moves[i][0] from moves[i][1] to moves[i][2]
        n = int(moves[i][0])
        start = int(moves[i][1]) - 1
        end = int(moves[i][2]) - 1

        for j in range (0, n):
            boxes[end].append(boxes[start][len(boxes[start]) - n + j])
        for j in range (0, n):
            boxes[start].pop()

    print('')
    for i in range (0, len(boxes)):
        print(boxes[i])

    for i in range (0, len(boxes)):
        print(boxes[i][len(boxes[i])-1])

if __name__ == "__main__":
    main()
