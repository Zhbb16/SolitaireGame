import pygame


class Foundation:

    def __init__(self, x, suit):
        self.foundation_pile = []
        self.x = x
        self.y = 10
        self.suit = suit

    def get_foundation(self):
        return self.foundation_pile

    def add_card(self, card):
        self.foundation_pile.append(card)
        card.set_coordinates(self.x, self.y)

    def remove_card(self):
        self.foundation_pile.pop()

    def get_top_card(self):
        if len(self.foundation_pile) > 0:
            return self.foundation_pile[len(self.foundation_pile) - 1]

    def get_suit(self):
        return self.suit

    def set_cards(self):
        self.foundation_pile[len(self.foundation_pile) - 1].set_coordinates(self.x, self.y)
