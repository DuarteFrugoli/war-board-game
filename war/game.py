import random
from .Territory import Territory
from .Card import Card
from .Deck import Deck
from .utils_data import load_map_data, load_missions

class Game:
	def __init__(self, players, dealer):
		self.players = players
		self.dealer = dealer
		self.map_data = load_map_data()
		self.missions = load_missions()
		self.territories = self.create_territories()
		self.cards, self.jokers = self.create_cards()
		self.deck = Deck()  # Baralho final para o jogo
		self.setup()

	def create_territories(self):
		territories = []
		for t in self.map_data['territories']:
			borders = t.get('borders', [])
			territory = Territory(t['name'], t['continent'], borders)
			territories.append(territory)
		return territories

	def create_cards(self):
		# Cartas de território vêm do map.json com símbolos definidos
		cards = []
		for territory_data in self.map_data['territories']:
			cards.append(Card(territory_data['name'], territory_data['symbol']))
		# Dois curingas clássicos
		jokers = [Card(None, 'coringa'), Card(None, 'coringa')]
		return cards, jokers

	def setup(self):
		self.distribute_missions()
		self.distribute_territory_cards()
		self.assign_territories_and_place_troops()
		self.collect_cards_and_prepare_deck()

	def distribute_missions(self):
		random.shuffle(self.missions)
		for i, player in enumerate(self.players):
			player.receive_mission(self.missions[i])

	def distribute_territory_cards(self):
		# Remove curingas, distribui só cartas de território
		n = len(self.players)
		dealer_idx = self.players.index(self.dealer)
		order = [(dealer_idx + 1 + i) % n for i in range(n)]
		deck = self.cards[:]
		random.shuffle(deck)
		idx = 0
		while deck:
			player = self.players[order[idx % n]]
			player.receive_card(deck.pop(0))
			idx += 1

	def assign_territories_and_place_troops(self):
		# Cada player recebe os territórios das cartas e coloca 1 tropa
		territory_dict = {t.name: t for t in self.territories}
		for player in self.players:
			for card in player.cards:
				terr = territory_dict.get(card.territory_name)
				if terr:
					terr.owner = player
					player.receive_territory(terr)
					terr.troops = 1  # 1 tropa inicial
			# Limpa as cartas do player após distribuição
			player.cards.clear()

	def collect_cards_and_prepare_deck(self):
		# Junta todas as cartas de território e curingas, embaralha e deixa pronto para o jogo
		all_cards = self.cards + self.jokers
		self.deck = Deck(all_cards)
		self.deck.shuffle()

	def get_first_player_after_dealer(self):
		idx = self.players.index(self.dealer)
		return self.players[(idx + 1) % len(self.players)]
