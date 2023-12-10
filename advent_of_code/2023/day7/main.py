
import numpy as np

with open('input.txt') as file:
    lines = [line.rstrip() for line in file]

cards = '23456789TJQKA'
card_map = {
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    'T': 8,
    'J': 9,
    'Q': 10,
    'K': 11,
    'A': 12
}


hand = []
cards = []
total_strength = []
card_strength = []
hand_strength = []
bid = []
count = 0
for line in lines :
    game = line.split(' ')
    hand.append(game[0])
    bid.append(int(game[1]))

    cards.append(np.zeros(13, dtype='int64'))

    my_strength = 0
    for i in range (0, 5) :
        cards[count][card_map[hand[count][i]]] += 1
        my_strength += pow(13, 4-i) * card_map[hand[count][i]]

    card_strength.append(my_strength)

    if 5 in cards[count] :
        hand_strength.append(6)

    elif 4 in cards[count] :
        hand_strength.append(5)

    elif 2 in cards[count] and 3 in cards[count]:
        hand_strength.append(4)

    elif 3 in cards[count]:
        hand_strength.append(3)

    elif 2 in cards[count] and list(cards[count]).count(2) == 2:
        hand_strength.append(2)

    elif 2 in cards[count]:
        hand_strength.append(1)

    else :
        hand_strength.append(0)

    total_strength.append(pow(13, 5) * hand_strength[count] + card_strength[count])

    count += 1

# rank the hands
total_strength, bid = zip(*sorted(zip(total_strength, bid)))

total = 0
for i in range (0, len(total_strength)):
    total += (i+1) * bid[i]
print(total)

# part 2
card_map = {
    'J': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'Q': 10,
    'K': 11,
    'A': 12
}

hand = []
cards = []
total_strength = []
card_strength = []
hand_strength = []
bid = []
count = 0
for line in lines :
    game = line.split(' ')
    hand.append(game[0])
    bid.append(int(game[1]))

    cards.append(np.zeros(13, dtype='int64'))

    my_strength = 0
    for i in range (0, 5) :
        cards[count][card_map[hand[count][i]]] += 1
        my_strength += pow(13, 4-i) * card_map[hand[count][i]]

    card_strength.append(my_strength)

    # true five of a kind with no jokers
    if 5 in cards[count] and cards[count][0] == 0 :
        hand_strength.append(6)

    # five of a kind with a joker
    elif 4 in cards[count] and cards[count][0] == 1 :
        hand_strength.append(6)

    # five of a kind with two jokers
    elif 3 in cards[count] and cards[count][0] == 2 :
        hand_strength.append(6)

    # five of a kind with three jokers
    elif 2 in cards[count] and cards[count][0] == 3 :
        hand_strength.append(6)

    # five of a kind with four jokers
    elif 1 in cards[count] and cards[count][0] == 4 :
        hand_strength.append(6)

    # five of a kind with only jokers
    elif cards[count][0] == 5 :
        hand_strength.append(6)

    # true four of a kind with no jokers
    elif 4 in cards[count] and cards[count][0] == 0 :
        hand_strength.append(5)

    # four of a kind with a joker
    elif 3 in cards[count] and cards[count][0] == 1:
        hand_strength.append(5)

    # four of a kind with two jokers
    elif 2 in cards[count] and list(cards[count]).count(2) == 2 and cards[count][0] == 2:
        hand_strength.append(5)

    # four of a kind with three jokers
    elif cards[count][0] == 3:
        hand_strength.append(5)

    # four of a kind with only jokers (this is actually five of a kind)
    #elif cards[count][0] == 4 and cards[count][0] == 0:
    #    hand_strength.append(10)

    # full house with no jokers 
    elif 2 in cards[count] and 3 in cards[count] and cards[count][0] == 0 :
        hand_strength.append(4)

    # full house from two pair plus one joker
    elif 2 in cards[count] and list(cards[count]).count(2) == 2 and cards[count][0] == 1 :
        hand_strength.append(4)

    # true three of a kind with no jokers
    elif 3 in cards[count] and cards[count][0] == 0:
        hand_strength.append(3)

    # three of a kind with one joker
    elif 2 in cards[count] and cards[count][0] == 1:
        hand_strength.append(3)

    # three of a kind with two jokers
    elif 1 in cards[count] and cards[count][0] == 2:
        hand_strength.append(3)

    # three of a kind with three jokers
    elif cards[count][0] == 3:
        hand_strength.append(3)

    # true two pair with no jokers
    elif 2 in cards[count] and list(cards[count]).count(2) == 2 and cards[count][0] == 0:
        hand_strength.append(2)

    # true pair with no jokers
    elif 2 in cards[count] and cards[count][0] == 0 :
        hand_strength.append(1)

    # pair with one joker
    elif 1 in cards[count] and cards[count][0] == 1 :
        hand_strength.append(1)

    else :
        hand_strength.append(0)

    total_strength.append(pow(13, 5) * hand_strength[count] + card_strength[count])

    count += 1

# rank the hands
total_strength, bid, hand = zip(*sorted(zip(total_strength, bid, hand)))

total = 0
for i in range (0, len(total_strength)):
    #print(hand[i], bid[i])
    total += (i+1) * bid[i]
print(total)

