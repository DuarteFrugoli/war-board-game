# Lógica principal do jogo War

import json
import random
from pathlib import Path
from .territory import Territory
from .continent import Continent
from .card import Card

def load_map_data():
	with open(Path(__file__).parent.parent / 'data' / 'map.json', encoding='utf-8') as f:
		return json.load(f)

def load_missions():
	with open(Path(__file__).parent.parent / 'data' / 'missions.json', encoding='utf-8') as f:
		return json.load(f)

def create_territories(map_data):
	return [Territory(t['name'], t['continent']) for t in map_data['territories']]

def create_continents(map_data):
	return [Continent(c['name'], c['territories']) for c in map_data['continents']]

def create_cards(territories):
	# Símbolos: quadrado, círculo, triângulo (distribuição igual)
	symbols = ['quadrado', 'círculo', 'triângulo']
	cards = []
	for i, territory in enumerate(territories):
		symbol = symbols[i % 3]
		cards.append(Card(territory.name, symbol))
	return cards

def distribute_missions(players, missions):
	random.shuffle(missions)
	for i, player in enumerate(players):
		player.mission = missions[i]

def distribute_cards(players, cards, dealer):
	# Começa do próximo ao dealer
	n = len(players)
	dealer_idx = players.index(dealer)
	order = [(dealer_idx + 1 + i) % n for i in range(n)]
	deck = cards[:]
	random.shuffle(deck)
	idx = 0
	while deck:
		player = players[order[idx % n]]
		player.cards.append(deck.pop(0))
		idx += 1

def assign_territories(players, territories):
	# Cada player recebe os territórios das cartas que possui
	territory_dict = {t.name: t for t in territories}
	for player in players:
		for card in player.cards:
			terr = territory_dict.get(card.territory_name)
			if terr:
				terr.owner = player
				player.territories.append(terr)

def setup_game(players, dealer):
	map_data = load_map_data()
	missions = load_missions()
	territories = create_territories(map_data)
	continents = create_continents(map_data)
	cards = create_cards(territories)
	distribute_missions(players, missions)
	distribute_cards(players, cards, dealer)
	assign_territories(players, territories)
	return territories, continents, cards

def get_first_player_after_dealer(players, dealer):
	idx = players.index(dealer)
	return players[(idx + 1) % len(players)]
