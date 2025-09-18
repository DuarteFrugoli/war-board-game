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

	# Sistema de Turnos
	def calculate_armies_to_receive(self, player):
		"""Calcula quantos exércitos o jogador deve receber no início do turno."""
		territory_count = len(player.territories)
		armies = territory_count // 2  # Divisão inteira (arredondamento para baixo)
		return max(armies, 1)  # Mínimo de 1 exército por turno

	def phase_1_distribute_armies(self, player):
		"""Etapa 1: O jogador recebe e distribui exércitos."""
		armies = self.calculate_armies_to_receive(player)
		return armies  # Retorna quantos exércitos o jogador pode distribuir

	def place_armies(self, player, territory_name, army_count):
		"""
		Coloca exércitos em um território do jogador.
		"""
		for territory in player.territories:
			if territory.name == territory_name:
				territory.troops += army_count
				return
		raise ValueError(f"Territory {territory_name} not owned by player {player.name}")

	def phase_2_attack(self, player):
		"""Etapa 2: Fase de ataque (opcional)."""
		territories_conquered = 0  # Contador de territórios conquistados neste turno
		# Esta será uma implementação básica - pode ser expandida para interface
		return territories_conquered

	def attack_territory(self, attacker_territory, defender_territory, attacking_armies):
		"""
		Executa um ataque entre territórios.
		Retorna True se o território foi conquistado, False caso contrário.
		"""
		if attacker_territory.owner == defender_territory.owner:
			raise ValueError("Não é possível atacar território próprio")
		
		if attacker_territory.troops <= attacking_armies:
			raise ValueError("Tropas insuficientes para ataque")
		
		if defender_territory.name not in attacker_territory.borders:
			raise ValueError("Territórios não são adjacentes")
		
		# Simulação simples de combate (pode ser expandida com dados)
		# Por enquanto, vamos usar probabilidade baseada nas tropas
		attacker_strength = min(attacking_armies, 3)  # Máximo 3 dados para atacante
		defender_strength = min(defender_territory.troops, 2)  # Máximo 2 dados para defensor
		
		# Simulação básica: atacante precisa superar defensor
		if attacker_strength > defender_strength:
			# Território conquistado
			old_owner = defender_territory.owner
			new_owner = attacker_territory.owner
			
			# Remove território do jogador anterior
			if old_owner:
				old_owner.territories.remove(defender_territory)
			
			# Adiciona território ao novo jogador
			defender_territory.owner = new_owner
			new_owner.territories.append(defender_territory)
			
			# Move tropas do atacante para o território conquistado
			attacker_territory.troops -= attacking_armies
			defender_territory.troops = attacking_armies
			
			return True
		else:
			# Ataque falhou, atacante perde tropas
			attacker_territory.troops -= 1
			return False

	def phase_3_troop_movement(self, player):
		"""Etapa 3: Deslocamento de tropas entre territórios próprios."""
		# Implementação básica - pode ser expandida
		pass

	def move_troops(self, from_territory, to_territory, troop_count):
		"""
		Move tropas entre territórios do mesmo jogador.
		Os territórios devem ser adjacentes e pertencer ao mesmo jogador.
		"""
		if from_territory.owner != to_territory.owner:
			raise ValueError("Territórios devem pertencer ao mesmo jogador")
		
		if to_territory.name not in from_territory.borders:
			raise ValueError("Territórios devem ser adjacentes")
		
		if from_territory.troops <= troop_count:
			raise ValueError("Deve manter pelo menos 1 tropa no território de origem")
		
		from_territory.troops -= troop_count
		to_territory.troops += troop_count

	def phase_4_draw_card(self, player, territories_conquered):
		"""Etapa 4: Recebe carta se conquistou pelo menos 1 território."""
		if territories_conquered > 0:
			if not self.deck.is_empty():
				card = self.deck.draw()
				player.receive_card(card)
				return card
		return None

	def play_turn(self, player):
		"""Executa um turno completo de um jogador."""
		print(f"\n=== Turno de {player.name} ===")
		
		# Etapa 1: Distribuir exércitos
		armies_to_place = self.phase_1_distribute_armies(player)
		print(f"Etapa 1: {player.name} recebe {armies_to_place} exércitos para distribuir")
		
		# Etapa 2: Atacar (retorna quantos territórios foram conquistados)
		print("Etapa 2: Fase de ataque")
		territories_conquered = self.phase_2_attack(player)
		
		# Etapa 3: Mover tropas
		print("Etapa 3: Deslocamento de tropas")
		self.phase_3_troop_movement(player)
		
		# Etapa 4: Receber carta (se conquistou território)
		print("Etapa 4: Recebimento de carta")
		card_received = self.phase_4_draw_card(player, territories_conquered)
		if card_received:
			print(f"{player.name} recebeu uma carta: {card_received.territory_name or 'Coringa'}")
		else:
			print(f"{player.name} não recebeu carta (não conquistou territórios)")
		
		return {
			'armies_placed': armies_to_place,
			'territories_conquered': territories_conquered,
			'card_received': card_received
		}

	def start_game(self):
		"""Inicia o jogo após o setup, começando com o primeiro jogador após o dealer."""
		current_player_index = (self.players.index(self.dealer) + 1) % len(self.players)
		return current_player_index

	def get_next_player(self, current_player_index):
		"""Retorna o índice do próximo jogador."""
		return (current_player_index + 1) % len(self.players)

	def is_game_over(self):
		"""Verifica se o jogo terminou (algum jogador cumpriu a missão ou eliminou todos)."""
		# Verifica se algum jogador foi eliminado (sem territórios)
		active_players = [p for p in self.players if len(p.territories) > 0]
		if len(active_players) == 1:
			return True, active_players[0]  # Último jogador sobrevivente
		
		# Aqui poderia verificar missões, mas isso dependeria da implementação das missões
		return False, None

	def get_game_state(self):
		"""Retorna informações sobre o estado atual do jogo."""
		state = {
			'players': [],
			'total_territories': len(self.territories),
			'cards_in_deck': len(self.deck.cards) if hasattr(self.deck, 'cards') else 0
		}
		
		for player in self.players:
			player_info = {
				'name': player.name,
				'color': player.color,
				'territories_count': len(player.territories),
				'total_troops': sum(t.troops for t in player.territories),
				'cards_count': len(player.cards)
			}
			state['players'].append(player_info)
		
		return state
