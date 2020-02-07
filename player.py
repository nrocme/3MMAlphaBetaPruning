#!usr/bin/en python3

from random import choice,shuffle
    # set of edges
    # each edge is the pos on the board that your coming from and the position that you could go to
    # i.e edge [0,1] shows that the position on the graphical board is connected to position 1 on the graphical board
edges = [{0, 1}, {1, 2}, {3, 4}, {4, 5}, {6, 7}, {7, 8}, {0, 3}, {3, 6},
         {1, 4}, {4, 7}, {2, 5}, {5, 8}, {0, 4}, {2, 4}, {6, 4}, {8, 4}]
    # list of winning positions
winners = ((0, 1, 2), (3, 4, 5), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6), (6, 7, 8))
def boardvalue(board, who):
    # board value for alpha player
    if who == -1:
        for pat in winners[:-1]:
            tmp = {board[x] for x in pat}
            if len(tmp) == 1 and who in tmp: # if the new move caused a victory position return the value as who
                return who
    # board value if beta board
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
    # shuffle the movelist so that it is randomized before considering the moves
    shuffle(movelist)

    # for each move in the movelist make a move that is randomized by the shuffle above.
    # make that move on the copy board and check the value of the board
    # use this return value choose what to do with the move
    for move in movelist:
        bcopy[move[0]] = 0  # make a move onto the copy board that can be evaluated
        bcopy[move[1]] = -1
        val = boardvalue(bcopy, -1) # check the value of this move
        if val == 0 and depth < 4: # value returns 0 and the depth allows us to continue call alpha
            _, val = alpha(bcopy,depth+1)
        if val < bestval:
            bestmove, bestval = move, val
        bcopy[move[0]] = -1 # undo the move from the board copy
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

# this function generates a list of possible moves that can be made for a board and the player
def posmovgenerator(bcopy, who):
    posMov = []
    x = 0
    while x < 9:
        i = 0
        while i < 9:
            if bcopy[x] == who and {x, i} in edges: # if the position is controlled by who and the newpos is empty append
                if bcopy[i] == 0:
                    posMov.append([x, i])
            i += 1
        x += 1
    return posMov
