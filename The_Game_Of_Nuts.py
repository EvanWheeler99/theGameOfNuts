'''
Evan Wheeler's Assignment 3
Boyde lecture 03
The commented print statement for the trained AI table after playing against a human is in line 95.
(note, it will only print on the first time the player plays against the AI.
It will not print after a player tries to play again.)
'''


#Import statements
import random
import copy


def main():
	'''
	The main function that is called when the program is run as '__main__'.
	It executes the function that asks for the number of nuts on the table and then executes the function that will go to the options menu.
	'''
	print('Welcome to the game of nuts!')
	nuts = nuts_on_the_table()
	options(nuts)


def options(nuts):
	'''
	This is the options menu. It takes input from the player and then directs the program to the appropriate choice of gamemode (PvP, PvAI, or AIvAI).
	'''
	print('''Options:\n\tPlay against a friend (1)\n\tPlay against the computer (2)\n\tPlay against the trained computer (3)''')
	choice = input('Which option do you take (1-3)?')
	if choice == '1':
		pvp(nuts)
	elif choice == '2':
		pvai(nuts)
	elif choice == '3':
		aivai(nuts)
	else:
		#Executes if the player does not put in a valid input
		print('Sorry, please choose a valid gamemode (1, 2, or 3)')
		return options(nuts)


def pvp(nuts):
	'''
	The player vs. player function of The Game of Nuts.
	It will play the game and then ask if the player wants to play again.
	'''
	game_loop(nuts, 1, 1)
	again = play_again()
	if (again == True):
		pvp(nuts)


def pvai(nuts):
	'''
	The player vs. AI function.
	It will create an IA with default values that will randomly make choices of how many nuts to take and then make the play play against it.
	'''

	hats = []
	for i in range(nuts + 1):
		hats += [[None, 1, 1, 1]]

	game_loop(nuts, 1, 2, hats)#Calls the function that starts a game with a player against the AI.

	again = play_again()#Asks if the player wants to play against another untrained AI.
	if (again == True):
		return pvai(nuts)


def aivai(nuts):
	'''
	This function will be called if the player wants to play against a trained Ai.
	It will create two AI's and will call a game to make them play each other for a number of times based on the number of nuts on the table.
	After the training is complete the program will call another game between one of the trained AI and a player.
	After the game the player will be asked if they want to play another against the trained AI.
	'''
	ai1 = []
	for i in range(nuts + 1):#There will be an extra hat with index 0 just to make it easier to index into the hats.
		ai1 += [[None, 1, 1, 1]]

	ai2 = copy.deepcopy(ai1)#ai2 will start as a copy of ai1 with all of it's sublists.

	print('Training AI, please wait...')
	goFirst = random.randint(1,2)#choses randomly which Ai will go first

	trainingPerNut = 1000 #The number of times the AI will play against it's self for each nut on the table.

	for i in range (nuts * trainingPerNut):
		(ai1, ai2) = game_loop(nuts, goFirst, 3, ai2, ai1)
		goFirst = random.randint(1,2)#Randomly chooses which AI goes first after each round so that the AI that goes second does not get to continue going second.

	game_loop(nuts, 1, 2, ai1)#Uses ai1 to play against the player using gamemode 2. Given the number of tests and the fact that the AI that gets to go first is chosen randomly after each game both of the lists should be similar enough that chosing ai1 or ai2 should not affect the outcome.

	# print(ai1) #The print statement that shows the ai's list of probabilities

	again = play_again()#Asks if the player wants to play against the ai again.
	if (again == True):
		return ai_again(nuts, ai1)


def ai_again(nuts, ai1):
	'''
	This function is called if the player plays against a trained AI and wants to play another game against it.
	It is simmilar to the aivai function however it does not waste time training the AI again.
	'''
	game_loop(nuts, 1, 2, ai1)
	again = play_again()
	if (again == True):
		return ai_again(nuts, ai1)


def select(hat):
	'''
	Selects an integer between 1 and 3 based on the weight of the values in the list
	This code was based on the code shown in the assignment description.
	'''
	total = hat[1] + hat[2] + hat[3]
	weightedRandom = random.randint(1, total)
	if (weightedRandom <= hat[1]):
		move = 1
	elif (weightedRandom <= hat[1] + hat[2]):
		move = 2
	else:
		move = 3
	return move


def game_loop(nuts, player, gamemode, ai2 = [], ai1 = []):
	'''
	This is the function that is used to play the actual games.
	It is mainly composed of a while loop that runs as long as there are nuts on the table.
	It the series of nested if statements are to allow the same function to be called for all three gamemodes.
	The bulk of the code is in this function and to helpmake it more clear it is commented between major sections.
	'''
	while (nuts > 0):#Runs until there are no more nuts on the table.
	#Must be strictly larger than 0.
		#Empty line to space out responses if the game is not being played between two IA's.
		if gamemode != 3:
			print('') #Print an empty line

		'''
		This section is where either a player or an AI chooses how many nuts to take.
		After the choice, the number of nuts chosen is subtracted from the total nuts on the table.
		'''
		if gamemode == 1:
			#For player vs. player
			if nuts != 1:
				print('There are ' +  str(nuts) + ' nuts on the board.')
				nuts -= player_input(player)
			else:
				print('There is 1 nut left (and you must take it).')
				nuts -= player_input(player)

		elif (gamemode == 2) and (player == 1):
			#Person playing against an AI
			if nuts != 1:
				print('There are ' +  str(nuts) + ' nuts on the board.')
				nuts -= player_input(player)
			else:
				print('There is 1 nut left (and you must take it).')
				nuts -= player_input(player)

		elif (gamemode == 2) and (player == 2):
			#The AI while playing against a player
			choice = select(ai2[nuts])
			if nuts != 1:
				print('There are ' +  str(nuts) + ' nuts on the board.')
				print('AI selects ' + str(choice))
			else:
				print('There is 1 on the board.')
				print('The AI is forced to take the last nut.')
			nuts -= choice

		else:
			'''
			The ai will move the value of how many nuts it chose into index[0] of the given 'hat'.
			It will then reduce the value of the choice by one (as long as there is at least one)
			This will automatically adjust the list values if the AI loses
			If the AI wins the values stored in index[1] of each hat will later be used to augment the values in the list and make the AI better at making decisions.
			'''

			if player == 1:
				choice = select(ai1[nuts])
				ai1[nuts][0] = choice #moves the choice to index 0
				if ai1[nuts][choice] < 1: #reduces the entry by 1 (but not to 0)
					ai1[nuts][choice] -= 1
				nuts -= choice

			if player == 2:
				choice = select(ai2[nuts])
				ai2[nuts][0] = choice #moves the choice to index 0
				if ai2[nuts][choice] < 1: #reduces the entry by 1 (but not to 0)
					ai2[nuts][choice] -= 1
				nuts -= choice

		#Changes who's turn it is so that in the next itteration the other player gets to choose how many nuts to take.
		player = swapPlayer(player)

	player = swapPlayer(player) #Swaps to the loser
	#If it is in a verbose gamemode, the loser wil be informed that they lost
	#(or if playing against the AI the player will be informed that they won.)
	if gamemode == 1:
		print('Player ' + str(player) + ', you lose.')
	elif (gamemode == 2) and (player == 1):
		print('Player 1, you lose.')
	elif (gamemode == 2) and (player == 2):
		print('Player 1, you beat the AI!')

	'''
	Resets the index [0] of the losing ai's list.
	(The number was already decreased after the ai made it's  choice.)
	'''
	if (gamemode == 3) and (player == 1):
		for i in (ai1):
			i[0] = None

	if (gamemode == 3) and (player == 2):
		for i in (ai2):
			i[0] = None


	player = swapPlayer(player)#Swaps to the winner

	'''
	If the made a choice from the 'hat' it will augment the value in the hat and then sets index[0] to None for the next round.
	'''
	if (gamemode == 3) and (player == 1):
		for i in (ai1):
			if i[0] != None:
				indexToAugment = i[0]
				if i[indexToAugment] == 1:
					i[indexToAugment] += 1
				else:
					i[indexToAugment] += 2
				i[0] = None

	if (gamemode == 3) and (player == 2):
		for i in (ai2):
			if i[0] != None:
				indexToAugment = i[0]
				if i[indexToAugment] == 1:
					i[indexToAugment] += 1
				else:
					i[indexToAugment] += 2
				i[0] = None

	return (ai1,ai2) #Returns both of the lists so that they can play against each other again.


def player_input(player):
	'''
	This is the functin that takes player input on how many nuts to take and then returns the choice as an integer.
	'''
	taken = input('Player ' + str(player) + ': How many nuts do you take (1-3)?')
	if (taken == '1') or (taken == '2') or (taken == '3'):
		taken = int(taken)
		return taken
	print('Sorry, (' + str(taken) + ') is not a valid input. Please try again.')
	return player_input(player)


def swapPlayer(player):
	'''
	This is a simple function that will swap who the player is and return the new player.
	'''
	if player == 1:
		player = 2
	else:
		player = 1
	return player


def nuts_on_the_table():
	'''
	This functions asks for input on how many nuts should start on the table.
	It must be an integer between 10 and 100.
	The try/except is for if the input can not be interpreted as an integer.
	'''
	while True:
		try:
			number = int(input('How many nuts are there on the table initially (10-100)?'))
		except ValueError:#For if the player inputs something that can not be interpreted as an integer.
			print('Sorry, please choose a number between 10 and 100')
			return nuts_on_the_table()

		if (10 <= number <= 100):
			return number
		print('Sorry, please choose a number between 10 and 100')
		return nuts_on_the_table()


def play_again():
	'''
	This is the function that will ask if the player wants to play again when called and then return a true or false value based on the choice.
	'''
	choice = input('Play again (1 = yes, 0 = no)?')
	if choice == '0':
		return False
	elif choice == '1':
		return True
	else:
		print('Sorry, that is not a valid input.')
		return play_again()


if __name__ == '__main__':
	'''
	The code that will run if the program is run as main.
	'''
	main()
