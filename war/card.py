# card.py
class Card:
	def __init__(self, territory_name, symbol):
		self.territory_name = territory_name
		self.symbol = symbol  # 'quadrado', 'círculo' ou 'triângulo'

	def __repr__(self):
		return f"<Card {self.territory_name} [{self.symbol}]>"
