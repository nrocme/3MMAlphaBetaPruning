#!usr/bin/en python3

from random import choice,shuffle
edges = [{0, 1}, {1, 2}, {3, 4}, {4, 5}, {6, 7}, {7, 8}, {0, 3}, {3, 6},
         {1, 4}, {4, 7}, {2, 5}, {5, 8}, {0, 4}, {2, 4}, {6, 4}, {8, 4}]

winners = ((0, 1, 2), (3, 4, 5), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6), (6, 7, 8))
def boardvalue(board, who):
    #board value for red player
    if who == -1:
        for pat in winners[:-1]:
            tmp = {board[x] for x in pat}
            if len(tmp) == 1 and who in tmp:
                return who
    #board value if beta board
    if who == 1:
        for pat in winners[1:]:
            tmp = {board[x] for x in pat}
            if len(tmp) == 1 and who in tmp:
                return who
    return 0

def beta(bcopy, depth):     # considering red's moves
    # copy board
    bcopy = [-1 if x == 2 else x for x in bcopy]
    # generate list of possible moves
    movelist = posmovgenerator(bcopy,-1)
    # best value may need increased to allow more parameters for tghe value of moves?
    bestval = 2

    shuffle(movelist)

    # for each move in the movelist make a move that is randomized by the shuffle above.
    # make that move on the copy board and check the value of the board
    # use this return value choose what to do with the move
    for move in movelist:
        bcopy[move[0]] = 0
        bcopy[move[1]] = -1
        val = boardvalue(bcopy, -1)
        if val == 0 and depth < 4:
            _, val = alpha(bcopy,depth+1)
        if val < bestval:
            bestmove, bestval = move, val
        bcopy[move[0]] = -1
        bcopy[move[1]] = 0
    return bestmove, bestval

def alpha(bcopy, depth):     # considering red's moves
    bcopy = [-1 if x == 2 else x for x in bcopy]
    movelist = posmovgenerator(bcopy,1)
    bestval = -3
    shuffle(movelist)
    for move in movelist:
        bcopy[move[0]] = 0
        bcopy[move[1]] = 1
        val = boardvalue(bcopy, 1)
        if val == 0 and depth < 4:
            _, val = beta(bcopy,depth+1)
        if val > bestval:
            bestmove, bestval = move, val
        bcopy[move[0]] = 1
        bcopy[move[1]] = 0
    return bestmove, bestval

def posmovgenerator(bcopy, who):
    posMov = []
    x = 0
    while x < 9:
        i = 0
        while i < 9:
            if bcopy[x] == who and {x, i} in edges:
                if bcopy[i] == 0:
                    posMov.append([x, i])
            i += 1
        x += 1
    return posMov
