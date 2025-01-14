import random as r
import time as t
import os as os
from termcolor import colored
from pyfiglet import Figlet
f = Figlet(font='standard')

print(colored(f.renderText("Game configuration!")))
# Falta opcion de SEPARAR (MAX 3 veces)

def Deck(AmountOfDecks) :

	def Shuffle(deck) :
		return r.sample(deck, 52)
	
	def GenDeck() :
		numbers = "A,2,3,4,5,6,7,8,9,10,J,Q,K".split(",")
		deck = []

		# Generating Permutations

		for i in numbers :
			colours = ["c", "d", "h", "s"] 
			for x in colours :
				deck.append(i+x)

		return deck

	d = []
	
	# Mix a bigger than one amount of decks, to randomize cards in the game and as a result -
	# change probabilities, or expectations

	for i in range(AmountOfDecks) : 
		d += Shuffle(GenDeck())

	return d

def SumOfCards(cards) :

	def count(card) :

		if card[0] in "23456789" : return int(card[0])
		if card[0] in "1JQK" : return 10

		else : return "A"

	res = 0
	ases = 0

	for i in cards :
		c = count(i)
		if c != "A" : res += c
		else :
			res += 11
			ases += 1

		# To maximize efficiency for the value of the Ase, a 11 or 1, depending on -
		# the situation

		if res > 21 :
			if ases >= 1 : 
				res -= 10
				ases -= 1
			else : return "Off"

	if len(cards) == 2 and res == 21 : return "BlackJack"
	return res

def SumOfCardsForBankAverage(cards) :

	def count(card) :

		if card[0] in "23456789" : return int(card[0])
		if card[0] in "1JQK" : return 10

		else : return "A"

	res = 0
	ases = 0

	for i in cards :
		c = count(i)
		if c != "A" : res += c
		else :
			res += 11
			ases += 1

		# To maximize efficiency for the value of the Ase, a 11 or 1, depending on -
		# the situation

		if res > 21 :
			if ases >= 1 : 
				res -= 10
				ases -= 1
			else : return res

	if len(cards) == 2 and res == 21 : return res
	return res



def PrintCard(card) :

	# Print the card in the terminal for a better " UI "

	num = card[:len(card)-1]
	colour = card[-1]

	symbol = ""
	if colour == "d" : symbol = "|  ♢  |"
	if colour == "h" : symbol = "|  ♡  |"
	if colour == "c" : symbol = "|  ♣  |"
	if colour == "s" : symbol = "|  ♤  |"


	print( "-------")
	if num == "10" : print(f"|  {num} |")
	else : print(f"|  {num}  |")
	print(symbol)
	print( "-------")

	return ""

def play() :

	seats = 6

	# Game Configuration
	#print("-------------")
	#print("| BlackJack |")
	#print("-------------\n")
	amountOfPlayers = int(input("How many players : "))

	while amountOfPlayers > 6 or amountOfPlayers < 1 :
		print("Max player amount : 6")
		amountOfPlayers = int(input("How many players : "))

	minBet = int(input("Minimum bet : "))
	while minBet < 1 : 
		print("Bets have to be bigger or equal to 1")
		minBet = int(input("Minimum bet : "))


	maxBet = int(input("Maximum bet : "))
	while maxBet <= minBet :
		print("Maximum bet has to be bigger than the minimum")
		maxBet = int(input("Maximum bet : "))

	bank = maxBet * 3 * amountOfPlayers
	# jugador = maxBet * 2

	print(f"\nThe bank has {bank} chips, each player has {maxBet * 2} chips\n")
 
	t.sleep(3.5)
	os.system('cls')
	print(colored(f.renderText("Black Jack"), "green"))
			

	# OPTIONAL
	AverageBankResults = []

	chips = [maxBet*2 for x in range(amountOfPlayers)]

	while bank > 0 :

		
		bets = []
		dealtCardCounter = 0
		resultNumbers = []
		
		for x in range(amountOfPlayers) :

			if chips[x] >= minBet :

				betIsNumber = True
				while betIsNumber :
					try :
						bet = int(input(f"Player {x+1} bets : "))

						while bet > chips[x] :
							print(f"Player {x+1} only has {chips[x]} chips to bet")
							bet = int(input(f"Player {x+1} bets : "))

						while bet > maxBet or bet < minBet :
							print("Incorrect value")
							bet = int(input(f"Player {x+1} bets : "))
							
						bets.append(bet)
						betIsNumber = False
					except :
						print("Incorrect value")

			else :
				print(f"Player {x+1} lost with {chips[x]} chips remaining")
				bets.append(0)

		deck = Deck(6)
		initialHand = deck[:amountOfPlayers * 2 + 1]

		pointer2 = 1
		pointer1 = 0

		for i in range(amountOfPlayers) :
			if bets[i] > 0 :

				print(f"\nPlayer {i+1} :")
				PrintCard(initialHand[pointer1])
				PrintCard(initialHand[pointer2])

				pointer1 += 2
				pointer2 += 2
				print("")

			else :
				continue

		print("\nBank :")
		PrintCard(initialHand[-1])

		safeBets = []
		AseAsFirstHouseCard = False

		if "A" in initialHand[-1] :
			AseAsFirstHouseCard = True
			for x in range(amountOfPlayers) :
				if chips[x] != 0 :
					if (chips[x] - bets[x] - (bets[x] // 2)) >= 0 :
						safe = input(f"Player {x+1}, safe bet? y (yes) / n (no) : ").lower()
						while safe not in "yn" :
							print("Incorrect value")
							safe = input(f"Player {x+1}, safe bet? y (yes) / n (no) : ").lower()
						
						if safe == "y" : safeBets.append(bets[x] // 2)
						else : safeBets.append(0)
				else : safeBets.append(0)


		pointer1 = 0
		pointer2 = 1

		for i in range(amountOfPlayers) :

			stop = False
			
			cards = initialHand[pointer1:pointer2+1]
			result = SumOfCards(cards)

			if chips[i] >= minBet :
				print(f"Player {i+1} : {cards} : {result}")

				# SPLIT (black jack = 21)
				splitResults = []
				if SumOfCards([cards[0]]) == SumOfCards([cards[1]]) :
					if chips[i] >= (bets[i] * 2) :
						split = input(f"\nPlayer{i+1}, do you want to split? y/n : ").lower()
						while split not in "yn" :
							print("Incorrect value")
							split = input(f"\nPlayer{i+1}, do you want to split? y/n : ").lower()

						if split == "y" :

							bets[i] *= 2
							chips[i] -= bets[i]

							# First 

							newCards = [cards[0]]
							newCard = deck[dealtCardCounter]
							dealtCardCounter += 1
							t.sleep(1)
							PrintCard(newCard)
							newCards.append(newCard)
							splitRes = SumOfCards(newCards)
							print(f"Player {i+1} : {newCards} : {splitRes}")

							if splitRes == "BlackJack" :
								splitResults.append(21)
							else :

								while not stop and splitRes <= 21:

									if splitRes == 21 : 
										splitResults.append(splitRes)
										break

									deal = input(f"\nPlayer{i+1}, deal (d) or stop (s)? : ").lower()
									while deal not in "sd" :
										print("Incorrect value")
										deal = input(f"Player{i+1}, deal (d) or stop (s)? : ").lower()
									if deal == "s" :
										splitResults.append(splitRes)
										break
									else :
										newCard = deck[dealtCardCounter]
										dealtCardCounter += 1
										t.sleep(1)
										PrintCard(newCard)
										newCards.append(newCard)
										splitRes = SumOfCards(newCards)
										print(f"Player {i+1} : {newCards} : {splitRes}")
										if result == "Off" :
											splitResults.append("Off")
											chips[i] -= bets[i]
											bank += bets[i]
											break

							cards = [cards[1]]
							newCard = deck[dealtCardCounter]
							dealtCardCounter += 1
							t.sleep(1)
							PrintCard(newCard)
							cards.append(newCard)
							splitRes = SumOfCards(cards)
							print(f"Player {i+1} : {cards} : {splitRes}")


				# DOUBLE

				if result == 9 or result == 10 or result == 11 :
					if chips[i] >= (bets[i] * 2) :
						double = input(f"\nPlayer{i+1}, do you want to double? y/n : ").lower()
						while double not in "yn" :
							print("Incorrect value")
							double = input(f"\nPlayer{i+1}, do you want to double? y/n : ").lower()

						if double == "y" :
							bets[i] = bets[i] * 2
							newCard = deck[dealtCardCounter]
							dealtCardCounter += 1
							t.sleep(1)
							PrintCard(newCard)
							cards.append(newCard)
							result = SumOfCards(cards)
							pointer2 += 2
							pointer1 += 2
							print(f"Player {i+1} : {cards} : {result}")
							if result == "Off" :
								resultNumbers.append("Off")
								chips[i] -= bets[i]
								bank += bets[i]
								continue
							else :
								resultNumbers.append(result)
								continue
				
				if result == "BlackJack" :
					chips[i] += int(bets[i] * 1.5)
					bank -= int(bets[i] * 1.5)
					print(f"Player {i+1} wins {int(bets[i] * 1.5)} chips!\n")
					resultNumbers.append("BlackJack")
				else :

					while not stop and result <= 21:

						if result == 21 : 
							resultNumbers.append(result)
							break

						deal = input(f"\nPlayer{i+1}, deal (d) or stop (s)? : ").lower()
						while deal not in "sd" :
							print("Incorrect value")
							deal = input(f"Player{i+1}, deal (d) or stop (s)? : ").lower()
						if deal == "s" :
							resultNumbers.append(result)
							break
						else :
							newCard = deck[dealtCardCounter]
							dealtCardCounter += 1
							t.sleep(1)
							PrintCard(newCard)
							cards.append(newCard)
							result = SumOfCards(cards)
							print(f"Player {i+1} : {cards} : {result}")
							if result == "Off" :
								resultNumbers.append("Off")
								chips[i] -= bets[i]
								bank += bets[i]
								break

				pointer2 += 2
				pointer1 += 2

				if splitResults != [] :
					resultNumbers.append(splitResults)
			else :
				resultNumbers.append("Lost")
			
		newBankCard = deck[dealtCardCounter]
		bankCards = [initialHand[-1], newBankCard]
		bankResult = SumOfCards(bankCards)


		t.sleep(1.5)
		PrintCard(newBankCard)
		print(f"Bank : {bankCards} : {bankResult}")

		dealtCardCounter += 1
		bankStillStanding = True

		while bankStillStanding :
			if bankResult == "BlackJack" : break
			if bankResult == "Off" : break
			if bankResult >= 17 : break

			newBankCard = deck[dealtCardCounter]
			PrintCard(newBankCard)
			dealtCardCounter += 1

			bankCards.append(newBankCard)
			bankResult = SumOfCards(bankCards)

			#OPTIONAL
			AverageBankResults.append(SumOfCardsForBankAverage(bankCards))

			print(f"Bank : {bankCards} : {bankResult}")
			t.sleep(1.5)

		for res in range(amountOfPlayers) :

			if type(resultNumbers[res]) == list :

				###
				
				for x in resultNumbers[res] : 

					if resultNumbers[res] == "Lost" :
						continue

					if resultNumbers[res] == "BlackJack" :
						print(f"\nPlayer {res+1} had BlackJack")
						print(f"Player {res+1} has {chips[res]} remaining chips")
						continue

					elif resultNumbers[res] == "Off" :
						print(f"\nPlayer {res+1} lost {bets[res]} chips ({resultNumbers[res]})")

					elif bankResult == "Off" :
						print(f"\nPlayer {res+1} won {bets[res]} chips ({resultNumbers[res]})")
						chips[res] += bets[res]
						bank -= bets[res]

					elif bankResult == "BlackJack" or bankResult > resultNumbers[res] :

						if bankResult == "BlackJack" and AseAsFirstHouseCard and safeBets[res] != 0 :
							chips[res] += safeBets[res]
							bank -= safeBets[res]
							print(f"\nPlayer {res+1} won {safeBets[res]} chips due to safe bet (house blackjack)")

						chips[res] -= bets[res]
						bank += bets[res]
						print(f"\nPlayer {res+1} lost {bets[res]} chips ({resultNumbers[res]})")

					elif bankResult == resultNumbers[res] :
						print(f"\nPlayer {res+1} tied with the bank ({resultNumbers[res]})")

					else :
						print(f"\nPlayer {res+1} won {bets[res]} chips ({resultNumbers[res]})")
						chips[res] += bets[res]
						bank -= bets[res]

					if AseAsFirstHouseCard and bankResult != "BlackJack" and safeBets[res] != 0 :
						chips[res] -= safeBets[res]
						bank += safeBets[res]
						print(f"\nPlayer {res+1} lost {safeBets[res]} chips due to safe bet (no house blackjack)")

			
			
				###
			
			if resultNumbers[res] == "Lost" :
				continue

			if resultNumbers[res] == "BlackJack" :
				print(f"\nPlayer {res+1} had BlackJack")
				print(f"Player {res+1} has {chips[res]} remaining chips")
				continue

			elif resultNumbers[res] == "Off" :
				print(f"\nPlayer {res+1} lost {bets[res]} chips ({resultNumbers[res]})")

			elif bankResult == "Off" :
				print(f"\nPlayer {res+1} won {bets[res]} chips ({resultNumbers[res]})")
				chips[res] += bets[res]
				bank -= bets[res]

			elif bankResult == "BlackJack" or bankResult > resultNumbers[res] :

				if bankResult == "BlackJack" and AseAsFirstHouseCard and safeBets[res] != 0 :
					chips[res] += safeBets[res]
					bank -= safeBets[res]
					print(f"\nPlayer {res+1} won {safeBets[res]} chips due to safe bet (house blackjack)")

				chips[res] -= bets[res]
				bank += bets[res]
				print(f"\nPlayer {res+1} lost {bets[res]} chips ({resultNumbers[res]})")

			elif bankResult == resultNumbers[res] :
				print(f"\nPlayer {res+1} tied with the bank ({resultNumbers[res]})")

			else :
				print(f"\nPlayer {res+1} won {bets[res]} chips ({resultNumbers[res]})")
				chips[res] += bets[res]
				bank -= bets[res]

			if AseAsFirstHouseCard and bankResult != "BlackJack" and safeBets[res] != 0 :
				chips[res] -= safeBets[res]
				bank += safeBets[res]
				print(f"\nPlayer {res+1} lost {safeBets[res]} chips due to safe bet (no house blackjack)")


			print(f"Player {res+1} has {chips[res]} remaining chips")

		print(f"\nThe bank has {bank} remaining chips")

		#OPTIONAL
		print(f"Average bank result so far : {sum(AverageBankResults) // len(AverageBankResults)}")
  
		if sum(chips) != 0 : 
		
			print("Waiting for next game ... 5")
			t.sleep(1)
			print("Waiting for next game ... 4")
			t.sleep(1)
			print("Waiting for next game ... 3")
			t.sleep(1)
			print("Waiting for next game ... 2")
			t.sleep(1)
			print("Waiting for next game ... 1")
			t.sleep(1)

			print("\nLoading next game!\n")


			t.sleep(3.5)
			os.system('cls')
			print(colored(f.renderText("Black Jack"), "green"))
		else : 
			print("\n\n")
			print(colored(f.renderText("All players lost!"), "green"))
			t.sleep(10)
			os.system('exit')
   
		if bank == 0 :
			print("\n\n")
			print(colored(f.renderText("The bank is without chips!"), "green"))
			t.sleep(10)
			os.system('exit')
			
	return None

print(play())
