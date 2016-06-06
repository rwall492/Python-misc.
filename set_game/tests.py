import numpy as np
from classes import *

def all_same(hand):
    hand.add_card(Card([0, 0, 0, 0]))
    hand.add_card(Card([0, 0, 0, 0]))
    hand.add_card(Card([0, 0, 0, 0]))

def one_diff(hand):
    hand.add_card(Card([0, 0, 0, 0]))
    hand.add_card(Card([1, 0, 0, 0]))
    hand.add_card(Card([2, 0, 0, 0]))

def all_diff(hand):
    hand.add_card(Card([0, 0, 0, 0]))
    hand.add_card(Card([1, 1, 1, 1]))
    hand.add_card(Card([2, 2, 2, 2]))

def no_match(hand):
    hand.add_card(Card([0, 0, 0, 0]))
    hand.add_card(Card([1, 0, 1, 0]))
    hand.add_card(Card([0, 2, 0, 2]))

def one_same(hand):
    hand.add_card(Card([0, 2, 0, 1]))
    hand.add_card(Card([1, 0, 2, 1]))
    hand.add_card(Card([2, 1, 1, 1]))

def test_all():
    hand1 = Hand()
    all_same(hand1)
    hand2 = Hand()
    one_diff(hand2)
    hand3 = Hand()
    all_diff(hand3)
    hand4 = Hand()
    no_match(hand4)
    hand5 = Hand()
    one_same(hand5)

    print hand1.is_winner()
    print hand2.is_winner()
    print hand3.is_winner()
    print hand4.is_winner()
    print hand5.is_winner()

#Used this code to check itertools for 3 card case
#    hands = []
#    for x in range(0,n_total):
#        this_hand = []
#        for y in range(x+1,n_total):
#            for z in range(y+1,n_total):
#                hands.append([x,y,z])

