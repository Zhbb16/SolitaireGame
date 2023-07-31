import pygame


class Waste:

    def __init__(self):
        self.waste_pile = []
        self.show_pile = []
        self.cords = [10, 10, 10]
        self.x = 270        #135

    def get_waste_pile(self):
        return self.waste_pile

    def add_card(self, card):
        card.set_coordinates(-150, 0)
        self.waste_pile.append(card)
        self.set_cards()

    def remove_card(self):
        return self.waste_pile.pop()

    def empty(self):
        self.waste_pile.clear()
        self.set_cards()

    def get_top_card(self):
        if len(self.waste_pile) > 0:
            return self.waste_pile[len(self.waste_pile) - 1]

    def set_cards(self):
        if len(self.waste_pile) > 3:
            self.show_pile = self.waste_pile[len(self.waste_pile) - 3:len(self.waste_pile)]
        else:
            self.show_pile = self.waste_pile
        for card in range(len(self.show_pile)):
            self.show_pile[card].set_coordinates(self.x, self.cords[card])

    def get_show_waste_pile(self):
        return self.show_pile
