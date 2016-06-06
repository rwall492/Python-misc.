'''Problem 2: Set Solver
 
The problem at hand is to write a solver for the game of Set. In case you're not familiar with the game, you can find a tutorial here:
http://www.setgame.com/sites/default/files/tutorials/tutorial/SetTutorial.swf
 
Task 1: Each card has symbols on it that vary across four dimensions: color, number, shape, and shading. There are three possible values per dimension (e.g. there are three possible colors: red, green, and purple). Start by writing a solver that takes in a collection of these cards (e.g. 9 cards, 12 cards, 15 cards, etc.), and  returns all possible sets that can be made from the inputs.
 
Task 2: Then, once you've solved the basic game, extend your solution to handle an arbitrary number of dimensions per card (e.g. each card now has a background color, with three possible values).
 
Task 3: Then, once you've got arbitrary dimensions, extend your solution to handle an arbitrary size for the dimensions (e.g. there are now four possible shapes, four colors, four of every dimension).  You may assume the number of cards remains three, or solve for an arbitrary number greater than three for extra credit.
'''

from tests import *
from classes import *
import numpy as np
import itertools as iter
import sys

def run(my_deck, n_cards):
    #get details of the deck
    n_total = len(my_deck.cards)
    n_features = len(my_deck.cards[0].feats)
    n_values = 0
    for x in my_deck.cards:
        for y in x.feats:
            if y > n_values:
                n_values = y

    #use python magic to get sets of n_cards with unique index combinations
    list = []
    for x in range(0,n_total):
        list.append(x)

    hands = iter.combinations(list, n_cards)

    #check how many correct combinations we can make, and print out information about them
    num_winners = 0
    for x in hands:
        this_hand = Hand()
        for y in range(0,n_cards):
            this_hand.add_card(my_deck.cards[x[y]])
        if this_hand.is_winner():
            print 'index of cards from original deck for a set', x
            num_winners += 1

    print 'number of sets: ', num_winners

def main():
#I wanted a script that could take command line inputs. main() does that, and throws some warnings if you make bad choices
    n_cards = 3
    input = ''
    
    if len(sys.argv) == 1:
        print ' '
        print 'Running with default values'
        print 'More general usage: python run.py n_cards input'
        print ' ' 
    elif len(sys.argv) == 2:
        n_cards = int(sys.argv[1])
    elif len(sys.argv) == 3:
        n_cards = int(sys.argv[1])
        input = sys.argv[2]
    else:
        print ' ' 
        print 'You have too many arguments! Please try again!'
        print ' ' 
        return

    if (n_cards <= 2):
        print ' ' 
        print 'Poor parameter choices!  Too few total cards!'
        print ' ' 
        return
    
    my_deck = Hand()
    if len(input) < 1:
        random_deck(my_deck)#can modify features, values & size in classes.py
    else:
        read_in_deck(my_deck,input)

    run(my_deck,n_cards)

main()
