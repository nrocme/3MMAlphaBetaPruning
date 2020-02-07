#!/usr/bin/env python3

from tkinter import *
import player as pl


class TMM(Tk):
    # set of edges
    # each edge is the pos on the board that your coming from and the position that you could go to
    # i.e edge [0,1] shows that the position on the graphical board is connected to position 1 on the graphical board
    edges = [{0, 1}, {1, 2}, {3, 4}, {4, 5}, {6, 7}, {7, 8}, {0, 3}, {3, 6},
             {1, 4}, {4, 7}, {2, 5}, {5, 8}, {0, 4}, {2, 4}, {6, 4}, {8, 4}]
    # list of winning positions
    winners = ((0, 1, 2), (3, 4, 5), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6), (6, 7, 8))

    def __init__(self):
        self.parent = Tk.__init__(self)

        # make lists of all 27 images: 9 for empty square, 9 for blue, 9 for red
        self.emptypix = []
        self.redpix = []
        self.bluepix = []
        for i in range(9):
            self.emptypix.append(PhotoImage(file=f"Images/x{i}.gif"))
            self.redpix.append(PhotoImage(file=f"Images/r{i}.gif"))
            self.bluepix.append(PhotoImage(file=f"Images/b{i}.gif"))

        # starting board configuration
        self.board = [1, 1, 1, 0, 0, 0, 2, 2, 2]
        # list of buttons
        self.blist = []

        # fill the graphical board with images from the directory 3MMAlphaBetaPruning/Images
        for i in range(9):
            if self.board[i] == 1:  # 1 is blue
                bu = Button(self, image=self.bluepix[i])
            elif self.board[i] == 2:  # 2 is red
                bu = Button(self, image=self.redpix[i])
            else:  # 0 is empty
                bu = Button(self, image=self.emptypix[i])
            # the lambda trick: used to identify the button since this is not able to be down with tkinter alone
            bu.configure(command=lambda b=bu: self.click(b))
            # store button number in the object itself
            bu.position = i
            # grid coordinates
            bu.grid(row=(i // 3), column=(i % 3))
            # append to button list
            self.blist.append(bu)

        self.moving = False  # start the game, moving is True after we pick the piece to move
        self.ai_player = 2   # 2 if you want ai to be red 1 if blue
        self.turn = 1        # red moves first if 2 blue if 1
    # function checkgame checks if the game is over after a move returns who won or if the game is not over returns 0
    def checkgame(self):
        who = self.turn # assigns current player to who
        # if no possible moves exist then the other player wins
        if(len(pl.posmovgenerator(self.board,who)) == 0):
            return 3 - who

        #checks if blue won
        if who == 1:
            for pat in TMM.winners[1:]:
                if all([self.board[x] == who for x in pat]):
                    return who
        # Checks if red won
        else:
            for pat in TMM.winners[:-1]:
                if all([self.board[x] == who for x in pat]):
                    return who
        return 0


    # do move executes a givene move using the new position(newpos) and the old position(oldpos) and the current player(who)
    def do_move(self, newpos, oldpos, who):
        self.blist[oldpos].configure(image=self.emptypix[oldpos])  # put empty image at old location
        self.board[oldpos] = 0                                     # update the board
        self.board[newpos] = who

        # if the player is blue replace square with blue dot
        # else the player is red so replace the square on the grpahical board with a red dot
        if who == 1:
            self.blist[newpos].configure(image=self.bluepix[newpos])
        else:
            self.blist[newpos].configure(image=self.redpix[newpos])

        # Checks if game is over 2 = red win 1 = blue win 0 = gamenotover
        retval = self.checkgame()
        if retval != 0:
            self.gameover = True
            # resets the board
            self.reset()
            # calls the popupmsg depending on who won
            if retval == 1:
                self.popupmsg("BLUE WINS")
            if retval == 2:
                self.popupmsg("RED WINS")
        self.moving = False
        self.turn = 3 - who
        if self.turn == 2:
            # calls beta from player.py that starts the alpha beta pruning for the ai player
            move, _ = pl.beta(self.board, 0)
            self.do_move(move[1], move[0], self.turn)


    # creates a popup msg to shgow who has won the match
    def popupmsg(self, msg):
        popup = Tk()
        popup.wm_title("VICTORY MESSAGE")
        label = Label(popup, text=msg, font="helvetica")
        label.pack(side="top", fill="x", pady=10)
        okayButton = Button(popup, text="Okay", command=popup.destroy)
        okayButton.pack()
        popup.mainloop()

    # Resets the board to its default settings so a new game can start
    def reset(self):
        self.board = [1, 1, 1, 0, 0, 0, 2, 2, 2]
        i = 0

        while i < 3:
            self.blist[i].configure(image=self.bluepix[i])
            i += 1
        while i < 6:
            self.blist[i].configure(image=self.emptypix[i])
            i += 1
        while i < 9:
            self.blist[i].configure(image=self.redpix[i])
            i += 1

        self.moving = False
        self.turn = 1

    def click(self, button):
        x = button.position  # number of the button that was clicked
        if self.moving:
            if self.board[x] == 0 and {x, self.savepos} in TMM.edges:
                self.do_move(x, self.savepos, self.turn)
        else:
            if self.board[x] == self.turn:  # need a reminder of old position
                self.savepos = x
                self.moving = True

if __name__ == "__main__":
    game = TMM()
    game.mainloop()