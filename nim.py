'''
Created by Manuel Herrera Ojea
https://github.com/Herrjea/
'''

from random import randint
from functools import reduce
import time 						# time.sleep(s)

def show( board ):
	"""
	Show the game board
	"""
	print()
	for i in range( len(board) ):
		print( str(i+1) + "  ", end = "" )
		for j in range( board[i] ):
			# This mess just to ease the reading
			# to count faster how many stones are left.
			# All items were initially '|' and it was
			# a pain in the eye just counting them.
			# And printing the actual number
			# was just not pretty enough =D
			n = j % 4
			if n == 0:
				char = "|"
			elif n == 2:
				char = "‡"
			else:
				char = "†"
			print( char, end = "" )
		print()
	print()


def count_remaining( board ):
	"""
	Count stones still on the board
	"""
	return sum( board )


def intro():
	"""
	Main menu of the game
	"""
	print( "\n\nWellcome to my Nim game!" )
	print( "\n\nChoose one of the following to begin with, or anything else to begin playing:" )
	print( "   Rules - What this game is about and how to play it" )
	print( "   Info - What this program is about and how to use it" )
	option = input().lower()

	while "rules" in option or "info" in option:

		# Rules of the game
		if "rules" in option:
			print( "\nA set of heaps of stones is presented as a board." )
			print( "Two players take turns to remove an arbitrary, positive number of stones from one of the heaps." )
			print( "The goal of the game is not being the one to take the last stone on the board." )
			print( "This is the misère version of the game. An alternative exists where the winner is the player who takes the last stone on the board, but it wasn't one of the goals of this implementation." )

		# General information about the implementation
		else:
			print( "\nYou are set to play agaist the machine in this program." )
			print( "In every turn the machine will try to leave the board in a state that will make it impossible for you to win." )
			print( "But you move always first, which could make you win if you make exactly zero mistakes =D" )
			print( "" )
			print( "As there is no GUI, you will be prompted to keyboardly choose a heap # and an amount of stones to remove." )
			print( "Just don't tell the game something unnice =D" )
			print( "The items in a heap are painted following the pattern |†‡† so that they're relatively similar to each other and relatively easy to count." )

		print( "\n\nNow! Choose again as before:" )
		print( "   Rules - What this game is about" )
		print( "   Info - What this program is about" )
		option = input().lower()

	print( "\nLet's play then!\n" )


intro()


heaps = 5
board = [ randint(1,9) for i in range(heaps) ]
remaining = count_remaining( board )
human_turn = True
heap = 0
amount = 0
error = False



# Main game loop
while remaining > 0:

	show( board )

	#
	# Player turn
	#
	if human_turn:

		heap = input( "Choose a heap: " )
		# Input error checking and informing
		try:
			heap = int( heap )
		except:
			error = True
		while error or heap < 1 or heap > heaps or board[heap-1] < 1:
			if error:
				print( heap + " is not a valid number" )
				error = False
			elif board[heap] == 0:
				print( "There are no items left in heap #" + str(heap) )
			else:
				print( "There's no heap #" + str(heap) )
			heap = input( "Choose a valid heap: " )
			try:
				heap = int( heap )
			except:
				error = True

		amount = input( "Choose an amount of items: " )
		# Input error checking and informing
		try:
			amount = int( amount )
		except:
			error = True
		while error or amount < 1 or amount > board[heap-1]:
			if error:
				print( heap + " is not a valid number" )
				error = False
			elif amount < 1:
				print( "You have to take one item at least" )
			else:
				print( "Heap #" + str(heap) + " only has " + str(board[heap-1]) + " items" )
			amount = input( "Choose a valid amount of items: " )
			try:
				amount = int( amount )
			except:
				error = True
		print()


	#
	# Machine turn
	#
	else:

		# Wikipedia and Mathologer really helped out here =D

		# Every time the machine has to make a move it checks if the board is balanced.
		# A board in considered balanced if one of the following happens after the move is executed:
		# 	All heaps have at most 1 stone and there is an odd number of non empty heaps.
		# or:
		#	For every amount of stones remaining in each heap, there is an even number overall of every specific power of 2 in the binary representation of those amounts. This is:
		#	Having heaps with 1, 2, 4 and 6 stones:
		#	In binary it would be
		#		001
		#		010
		#		100
		#		110
		#	which gives 1 2^0, 2 2^1's and 2 2^2's.
		#	There is an odd number of 2^0's, so the machine will make sure it's gone after its move, and will take 1 stone (1 because it's in the 2^0's position) in its turn.


		# Sum in Z2 of the powers of 2
		# of the amount of stones left in each heap
		X = reduce( lambda a,b: a ^ b, board )

		# If the board is balanced, we'll lose
		# if the human plays perfect.
		# We just remove the first non-empty heap
		if X == 0:

			for i, current_heap in enumerate( board ):
				if current_heap > 0:
					heap, amount = i, current_heap
					break

		# If the board is not balanced,
		# we make sure that it is back so
		# after we have moved
		else:

			# Taking the amount of stones in each heap,
			# calculate the powers of 2 present in it
			# and not in X or vice versa, to see where
			# a power of 2 should be removed
			sums = [ h^X < h for h in board ]
			# Only the first heap where it occurs will matter
			heap = sums.index( True )
			# From that heap, take the amount of stones
			# corresponding to that missing power of 2
			amount = board[heap] - ( board[heap]^X )

			# Calculate the amount of heaps that'll be left
			# with two or more stones in it ather the move
			heaps_twomore = 0
			for i, current_heap in enumerate( board ):
				if i == heap:
					n = current_heap - amount
				else:
					n = heap
				if n > 1:
					heaps_twomore += 1

			# If the move is going to leave no heap of size 2 or larger, leave an odd number of heaps of size 1 instead
			if heaps_twomore == 0:
				# Count the amount of heaps of size 1
				heap = board.index( max( board ) )
				heaps_one = sum( h == 1 for h in board )
				# If it is even make it odd
				if heaps_one % 2 == 0:
					amount = board[heap] - 1
				# If it was already odd, remain with the previously selected move

		# Adjust to first = 1 instead of first = 0
		heap += 1


	# Making the movement
	board[heap-1] -= amount
	if human_turn:
		player = "You"
	else:
		player = "The machine"
		time.sleep(2)
	print( player + " removed " + str( amount ) + " items from heap #" + str( heap ) )
			

	# Change turn
	human_turn = not human_turn

	# Check for end of game
	remaining = count_remaining( board )


# Game ended
print( "\n" )
if human_turn:
	print( "The AI defeated you as foreseen =D" )
else:
	print( "You just beat the machine! Well that was unexpected =D" )
print()


