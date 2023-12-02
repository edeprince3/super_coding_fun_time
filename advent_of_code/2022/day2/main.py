
def main():

    with open('input.txt') as file:
        lines = [line.rstrip() for line in file]


    score = 0
    for i in range (0, len(lines)):
        moves = lines[i].split(" ")
        print(moves)

        if ( moves[1] == 'X' ):
            score += 1
            if ( moves[0] == 'A' ):
                score += 3
            elif ( moves[0] == 'C' ):
                score += 6

        elif ( moves[1] == 'Y' ):
            score += 2
            if ( moves[0] == 'B' ):
                score += 3
            elif ( moves[0] == 'A' ):
                score += 6

        elif ( moves[1] == 'Z' ):
            score += 3
            if ( moves[0] == 'C' ):
                score += 3
            elif ( moves[0] == 'B' ):
                score += 6
   
    print(score) 

    score = 0
    for i in range (0, len(lines)):
        moves = lines[i].split(" ")
        print(moves)

        # lose
        if ( moves[1] == 'X' ):
            if ( moves[0] == 'A' ):
                score += 3
            elif ( moves[0] == 'B' ):
                score += 1
            elif ( moves[0] == 'C' ):
                score += 2

        # tie
        elif ( moves[1] == 'Y' ):
            score += 3
            if ( moves[0] == 'A' ):
                score += 1
            elif ( moves[0] == 'B' ):
                score += 2
            elif ( moves[0] == 'C' ):
                score += 3
        # win
        elif ( moves[1] == 'Z' ):
            score += 6
            if ( moves[0] == 'A' ):
                score += 2
            elif ( moves[0] == 'B' ):
                score += 3
            elif ( moves[0] == 'C' ):
                score += 1

    print(score) 

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
