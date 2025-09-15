import random

class Deck:
	def __init__(self, cards=None):
		self.cards = cards if cards is not None else []

	def shuffle(self):
		random.shuffle(self.cards)

	def draw(self):
		return self.cards.pop() if self.cards else None

	def peek(self):
		return self.cards[-1] if self.cards else None

	def is_empty(self):
		return len(self.cards) == 0

	def add_card(self, card):
		self.cards.append(card)

	def add_cards(self, cards):
		self.cards.extend(cards)
		