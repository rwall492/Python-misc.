import numpy as np
import csv

class Card:
    def __init__(self,feats):
        self.feats = feats

    def debug(self):
        for x in self.feats:
            print 'value of feature: ', x

class Hand:
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        self.cards.append(card)

    def debug(self):
        for x in self.cards:
            print 'card details'
            x.debug()

    def is_winner(self):
        result = True
        n_cards = len(self.cards)
        n_feat = len(self.cards[0].feats)

        for x in range(0,n_feat):
            same = True
            diff = True
            for y in range(0,n_cards):
                same = same and (self.cards[y].feats[x] == self.cards[0].feats[x])
                for z in range(y+1,n_cards):
                    diff = diff and (self.cards[y].feats[x] != self.cards[z].feats[x])

            test = same or diff
            result = result and test 

        return result
            
def random_card(values,features):
    #make a card with N features, each of which can take M values
    vals = np.random.randint(0,values,features)
    card = Card(vals)
    return card

def random_deck(hand):
    np.random.seed(0)

    n_total = 36
    n_features = 4
    n_values = 3

    #draw n_total cards
    for x in range(0,n_total):
        hand.add_card(random_card(n_values,n_features))

    return hand

def read_in_deck(hand,input):
    with open(input,'rb') as csvfile:    
        file = csv.reader(csvfile,delimiter=',')
        for x in file:
            vals = []
            for y in x:
                vals.append(int(y))
            hand.add_card(Card(vals))
