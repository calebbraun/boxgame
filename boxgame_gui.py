#!/usr/bin/python
#
# Also known as the dot game or pig pen.  Connect lines and try to be the player
# that completes a box.  If you complete a box, you get another turn! Made
# for fun, to learn Tkinter, bitwise operations, and hopefully to make a good AI.
#
# Caleb Braun
# 12/27/15
#

from Tkinter import *
import Tkinter as tk
import tkFont
import sys
import string
import random
from boxgame_player import Player


# The graphical interface
class Application(tk.Frame):
    WIDTH = 500
    HEIGHT = 500
    LINE_WIDTH = 5

    def __init__(self, grid_size, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        # Initialize board data structures
        self.lines = dict()
        self.boxes = [[] for i in range(grid_size)]

        # Display variables
        self.bgColor1 = "#AEE1FC"
        self.bgColor2 = "#BAFCAE"
        self.titlefont = tkFont.Font(family='BlairMdITC TT', size=64, weight='bold')
        self.buttonfont = tkFont.Font(family='Avalon', size=30)

        # Initialize game variables
        self.grid_size = grid_size + 1
        self.boxes_left = (grid_size)**2

        # Start the game
        self.show_title_screen()

    def show_title_screen(self):
        # Title and background
        self.title_screen = tk.Canvas(self, width = self.WIDTH,
                                            height = self.HEIGHT,
                                            background = self.bgColor1)
        self.title = tk.Label(self, text = "PIG PEN",
                                    font = self.titlefont,
                                    pady = 10,
                                    bg = self.bgColor1)

        img = tk.PhotoImage(file = 'pig.gif')
        self.pig = tk.Label(self, image = img, borderwidth = 0)
        self.pig.img = img

        # Custom buttons
        self.modeButton1 = tk.Label(self,   text = "vs. player",
                                            font = self.buttonfont,
                                            bg = self.bgColor2,
                                            padx = 10,
                                            pady = 10,
                                            relief = GROOVE)
        self.modeButton2 = tk.Label(self,   text = "vs. computer",
                                            font = self.buttonfont,
                                            bg = self.bgColor2,
                                            padx = 10,
                                            pady = 10,
                                            relief = RIDGE)
        self.modeButton1.bind('<Button-1>', self.set_up_player_mode)
        self.modeButton2.bind('<Button-1>', self.set_up_player_mode)

        self.quitButton = tk.Button(self, text = 'Quit', bg = self.bgColor1, command = self.quit)

        # Draw the screen
        self.title_screen.grid(rowspan=5)
        self.title.grid(column=0, row=0)
        self.pig.grid(row=1)
        self.modeButton1.grid(row=2)
        self.modeButton2.grid(row=3)
        self.quitButton.grid(row = 4)

    def set_up_player_mode(self, event):
        self.modeButton1.destroy()
        self.modeButton2.destroy()
        self.title.destroy()
        self.pig.destroy()
        self.get_player_name()

    def get_player_name(self):
        # Entry boxes for users to enter names
        l = tk.Label(self, text = "Player 1 Name: ")
        l2 = tk.Label(self, text = "Player 2 Name: ")
        entry_box = tk.Entry(self)
        entry_box2 = tk.Entry(self)

        # Display entry boxes
        l.grid(row = 0)
        l2.grid(row = 2)
        entry_box.grid(row = 1)
        entry_box2.grid(row = 3)

        # Needs to be defined after variable declaration.
        def entry_handler(event = 0):
            self.set_up_game(entry_box.get(), entry_box2.get())
            l.destroy()
            l2.destroy()
            entry_box.destroy()
            entry_box2.destroy()

        # New screen - Update how the display looks
        self.quitButton.configure(text = 'Done', command = entry_handler)
        self.quitButton.bind('<Return>', entry_handler)
        self.title_screen.configure(bg = self.bgColor2)


    def set_up_game(self, player1name, player2name):
        self.player1 = Player(player1name, "HUMAN")
        self.player2 = Player(player2name, "HUMAN")
        self.player1.color = "red"
        self.player2.color = "blue"
        self.current_turn = self.player1
        self.quitButton.configure(text = 'Quit', command = self.quit)
        self.title_screen.destroy()
        self.init_display()
        self.fill_board()


    def init_display(self):
        font = tkFont.Font(family='Helvetica', size=16, weight='bold')
        # Set up the canvas
        self.board = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT)
        self.board.grid()
        self.display_message = self.board.create_text(  self.WIDTH / 2,
                                                        self.HEIGHT - 25,
                                                        text = "It is " + self.player1.name + "'s turn!",
                                                        font = font)
        self.player1.score_display = self.board.create_text(100, 25, text = "%s: 0" %(self.player1.name), font = font)
        self.player2.score_display = self.board.create_text(self.WIDTH - 100, 25, text = "%s: 0" %(self.player2.name), font = font)
        self.quitButton.grid()


    # Popluates the board with dots and lines
    def fill_board(self):
        # Constant dot variables
        dot_spacing = self.WIDTH / self.grid_size
        margin = dot_spacing / 2
        if self.grid_size < 10:
            dot_size = 10 - self.grid_size
        else:
            dot_size = 2

        for i in range(0, self.grid_size):
            for j in range(0, self.grid_size):
                # Dot variables
                dot_left = (dot_spacing*i) - dot_size + margin
                dot_top = (dot_spacing*j) - dot_size + margin
                dot_right = (dot_spacing*i) + dot_size + margin
                dot_bottom = (dot_spacing*j) + dot_size + margin

                # Create horizontal lines
                if (i != self.grid_size-1):
                    hline = self.board.create_line(dot_left, (dot_size + dot_top), (dot_left + dot_spacing), (dot_top + dot_size), fill = '#E4E4E4', width = self.LINE_WIDTH)
                    def handler(event, self = self, id = hline):
                        return self.lineClick(event, "HORIZONTAL", id)
                    self.board.tag_bind(hline, '<ButtonPress-1>', handler)

                    # Add the boxes that are adjacent to the line to our 'lines' dictionary.
                    if j == 0:
                        self.lines[hline] = [i,j]
                    elif j == self.grid_size-1:
                        self.lines[hline] = [i,j-1]
                    else:
                        self.lines[hline] = [i,j-1], [i,j]

                # Create vertical lines
                if (j != self.grid_size-1):
                    line = self.board.create_line((dot_left + dot_size), dot_top, (dot_left + dot_size), (dot_top + dot_spacing), fill = '#E4E4E4', width = self.LINE_WIDTH)
                    def handler(event, self = self, id = line):
                        return self.lineClick(event, "VERTICAL", id)
                    self.board.tag_bind(line, '<ButtonPress-1>', handler)

                    if i == 0:
                        self.lines[line] = [i,j]
                    elif i == self.grid_size-1:
                        self.lines[line] = [i-1, j]
                    else:
                        self.lines[line] = [i-1,j], [i,j]

                # Fill up the box 2d array and the display boxes
                if (i != self.grid_size-1 and j != self.grid_size-1):
                    self.boxes[i].append(0)
                    # Make the squares for when they are surrounded
                    square_id = self.board.create_rectangle((dot_left+dot_size+self.LINE_WIDTH), (dot_top+dot_size+self.LINE_WIDTH), (dot_left+dot_spacing), (dot_bottom+dot_spacing-dot_size-self.LINE_WIDTH), fill='white', outline='white')

                # Dots, position goes: left, top, right, bottom
                dot = self.board.create_oval(dot_left, dot_top, dot_right, dot_bottom, fill = 'black')


    def lineClick(self, event, line_type, lineID=0):
        selected_line = self.board.itemconfigure(lineID, fill = '#696969', state = tk.DISABLED)

        if line_type == "HORIZONTAL":
            l_weight = 2
        else:
            l_weight = 1

        # Add the boxes that are adjacent to the line to our 'lines' dictionary.
        # The boxes are represented by a triple: the first two are the coords,
        # and the third is the state of the box.
        # The state integer is 4 bits: 1=right, 2=bottom, 4=left, 8=top.
        adjacent_boxes = self.lines[lineID]

        # If the line clicked only has one adjacent box...
        if not isinstance(adjacent_boxes, tuple):
            if adjacent_boxes[l_weight - 1] == 0:
                self.boxes[adjacent_boxes[0]][adjacent_boxes[1]] += 4 * l_weight
            else:
                self.boxes[adjacent_boxes[0]][adjacent_boxes[1]] += l_weight
        # If it has two adjacent boxes...
        else:
            self.boxes[adjacent_boxes[0][0]][adjacent_boxes[0][1]] += l_weight
            self.boxes[adjacent_boxes[1][0]][adjacent_boxes[1][1]] += 4 * l_weight

        self.refresh_display("It is %s's turn!" %(self.current_turn.name))


    def refresh_display(self, error):
        self.board.itemconfig(self.display_message, text=error)
        claimed_box = False

        # Test for completed boxes
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes)):
                #print self.boxes[i][j]
                if self.boxes[i][j] == 15:
                    # We've completed a box! Find which one and fill it in.
                    rect_id = self.board.find_closest(((i+1)*(self.WIDTH / self.grid_size)), ((j+1)*(self.HEIGHT / self.grid_size)))
                    plyr = self.current_turn
                    plyr.score += 1
                    self.board.itemconfig(self.display_message, text = plyr.name + " got a box! Take another turn.")
                    self.board.itemconfig(plyr.score_display, text="%s:  %d" %(plyr.name, plyr.score))
                    self.board.itemconfig(rect_id, fill = plyr.color)
                    # Change the box's value so that it doesn't come up again, and subtract a box from the total.
                    self.boxes[i][j] = 0
                    self.boxes_left -= 1
                    # The player gets another turn.
                    claimed_box = True

        # Switch turns
        if claimed_box == False:
            if self.player1.turn:
                self.current_turn = self.player2
            else:
                self.current_turn = self.player1
            self.player1.turn = not self.player1.turn

        if self.boxes_left == 0:
            self.game_over()


    def game_over(self):
        if self.player1.score < self.player2.score:
            winning_message = self.player2.name + " Wins!"
        elif self.player1.score > self.player2.score:
            winning_message = self.player1.name + " Wins!"
        else:
            winning_message = "It's a tie!"
        font = tkFont.Font(family='Helvetica', size=48, weight='bold')
        #self.board.create_rectangle(0,0,self.WIDTH, self.HEIGHT, fill='black')
        self.board.create_text(self.WIDTH / 2, self.HEIGHT / 2, text=winning_message, font = font, fill='white', activefill='magenta')


def main():
    # Argument for board size
    if sys.argv[1:]:
        n = string.atoi(sys.argv[1])
        if 2 > n or n > 20:
            print "Value must be between 2 and 20. Playing with default 5x5 grid."
            n = 5
    else:
        n = 5

    app = Application(n)
    app.master.title("Dot Game")
    app.mainloop()

# Call main when run as script
if __name__ == '__main__':
        main()
