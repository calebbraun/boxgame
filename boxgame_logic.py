#!/usr/bin/python
#
# Caleb Braun
# 12/22/15
#
# The typical box game

import os
import random

def refresh_display(board_array, initial, error):
	os.system("clear")
	size = len(board_array)
	for i in range(0,size):
		for j in range(0,size):
			x = board_array[i][j]
			box = ": :"
			if x==0: print ": :",
			if x==1: print ": |",
			if x==2: print ":_:",
			if x==3: print ":_|",
			if x==4: print "| :",
			if x==5: print "| |",
			if x==6: print "|_:",
			if x==7: print "|_|",
			if x==8: print ":-:",
			if x==9: print ":-|",
			if x==10: print "===",
			if x==11: print "==]",
			if x==12: print "|-:",
			if x==13: print "|-|",
			if x==14: print "[==",
			if x==15: print "[%s]" %(initial),
		print
	print error

def line_choice_to_int(choice):
	if choice == 'r':
		return 1
	elif choice == 'd':
		return 2
	elif choice == 'l':
		return 4
	elif choice == 'u':
		return 8
	else:
		return 0

def AI_choice(board_array):
	choice = "111"
	size = len(board_array)
	for row in range(0,size):
		for col in range(0,size):
			for x in (1,2,4,8):
				if board_array[row][col]|x == 15 and board_array[row][col] < 15:
					choice = "%d%d%d" %(row+1, col+1, x)
					print choice
	return choice

def main():
	# Initialize variables
	player_initial = raw_input("Enter your box initial: ")[0].upper()
	computer_initial = "$"
	quit = 0
	size = 5
	error = ""
	is_player_turn = False

	# Initialize board
	board_array = []
	for i in range(0,size):
		board_array.append([])
		for j in range(0,size):
			board_array[i].append(0)
	refresh_display(board_array, player_initial, error)

	#Main game loop
	while quit == 0:
		#Updates for new turn
		error = ""
		is_player_turn = not is_player_turn
		initial = player_initial

		#Take the turn
		if is_player_turn:
			selection = raw_input("Type line you select (e.g. 15r): ")
			line_choice = line_choice_to_int(selection[2])
		else:
			initial = computer_initial
			selection = AI_choice(board_array)
			line_choice = int(selection[2])
			raw_input("computer turn")

		#Analyze selection and update game board
		if selection == 'q':
			quit=1
		else:
			x_choice = int(selection[0])-1
			y_choice = int(selection[1])-1

			if (board_array[x_choice][y_choice] & line_choice) == line_choice:
				error = 'That line has already been filled.'
			elif line_choice != 0:
				board_array[x_choice][y_choice] += line_choice
				#Update ajacent box
				if line_choice == 1 and y_choice < size-1:
					board_array[x_choice][y_choice+1] += 4
				if line_choice == 2 and x_choice < size-1:
					board_array[x_choice+1][y_choice] += 8
				if line_choice == 4 and y_choice > 0:
					board_array[x_choice][y_choice-1] += 1
				if line_choice == 8 and x_choice > 0:
					board_array[x_choice-1][y_choice] += 2

				error = 'Last turn: %d,%d,%d' %(x_choice, y_choice, line_choice)
			else:
				error = 'Incorrect line choice'

		refresh_display(board_array, initial, error)

main()
