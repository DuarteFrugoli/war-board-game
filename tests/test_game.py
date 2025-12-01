# test_game.py
# Testes para a lógica do jogo

import unittest
from unittest.mock import patch, MagicMock
from war.game import Game
from war.player import Player
from war.territory import Territory
from war.card import Card
from war.deck import Deck

class TestGame(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("João", "Azul")
        self.player2 = Player("Maria", "Vermelho")
        self.players = [self.player1, self.player2]
        self.dealer = self.player1

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_game_initialization(self, mock_missions, mock_map):
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': ['Brasil'], 'symbol': 'círculo'}
            ],
            'continents': [
                {'name': 'América do Sul', 'territories': ['Brasil', 'Argentina']}
            ]
        }
        mock_missions.return_value = [
            {'id': 1, 'description': 'Conquistar América do Sul'},
            {'id': 2, 'description': 'Conquistar Europa'}
        ]

        game = Game(self.players, self.dealer)
        
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.dealer, self.dealer)
        self.assertIsNotNone(game.territories)
        self.assertIsNotNone(game.cards)
        self.assertIsInstance(game.deck, Deck)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_create_territories(self, mock_missions, mock_map):
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': ['Brasil'], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [
            "Conquistar 18 territórios",
            "Conquistar América do Norte"
        ]

        game = Game(self.players, self.dealer)
        territories = game.territories
        
        self.assertEqual(len(territories), 2)
        self.assertEqual(territories[0].name, 'Brasil')
        self.assertEqual(territories[0].borders, ['Argentina'])
        self.assertEqual(territories[1].name, 'Argentina')

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_create_cards(self, mock_missions, mock_map):
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'symbol': 'círculo'},
                {'name': 'França', 'continent': 'Europa', 'symbol': 'triângulo'}
            ]
        }
        mock_missions.return_value = [
            "Conquistar 18 territórios",
            "Conquistar América do Norte"
        ]

        game = Game(self.players, self.dealer)
        cards, jokers = game.cards, game.jokers
        
        self.assertEqual(len(cards), 3)  # Uma carta por território
        self.assertEqual(len(jokers), 2)  # Dois curingas
        
        # Verifica símbolos das cartas
        symbols = [card.symbol for card in cards]
        expected_symbols = ['quadrado', 'círculo', 'triângulo']
        self.assertEqual(symbols, expected_symbols)

    def test_get_first_player_after_dealer(self):
        game = Game.__new__(Game)  # Cria instância sem chamar __init__
        game.players = self.players
        game.dealer = self.player1
        
        first_player = game.get_first_player_after_dealer()
        self.assertEqual(first_player, self.player2)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_distribute_missions(self, mock_missions, mock_map):
        """Testa se missões são distribuídas corretamente."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': [], 'symbol': 'quadrado'}
            ]
        }
        mock_missions.return_value = [
            {'id': 1, 'description': 'Missão 1'},
            {'id': 2, 'description': 'Missão 2'},
            {'id': 3, 'description': 'Missão 3'}
        ]
        
        game = Game(self.players, self.dealer)
        
        # Cada jogador deve ter recebido uma missão
        for player in self.players:
            self.assertIsNotNone(player.mission)
            self.assertIn('id', player.mission)
            self.assertIn('description', player.mission)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_calculate_armies_to_receive(self, mock_missions, mock_map):
        """Testa o cálculo de exércitos a receber."""
        mock_map.return_value = {
            'territories': [
                {'name': f'T{i}', 'continent': 'C', 'borders': [], 'symbol': 'quadrado'}
                for i in range(10)
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        # Testa com diferentes quantidades de territórios
        # 10 territórios = 10 // 2 = 5 exércitos
        self.player1.territories = [MagicMock() for _ in range(10)]
        armies = game.calculate_armies_to_receive(self.player1)
        self.assertEqual(armies, 5)
        
        # 1 território = 1 // 2 = 0, mas mínimo é 1
        self.player1.territories = [MagicMock()]
        armies = game.calculate_armies_to_receive(self.player1)
        self.assertEqual(armies, 1)
        
        # 7 territórios = 7 // 2 = 3 exércitos
        self.player1.territories = [MagicMock() for _ in range(7)]
        armies = game.calculate_armies_to_receive(self.player1)
        self.assertEqual(armies, 3)

    def test_place_armies(self):
        """Testa a colocação de exércitos em territórios."""
        # Cria game sem setup completo para testar função isolada
        game = Game.__new__(Game)
        game.players = self.players
        
        # Cria território e adiciona ao jogador
        territory = Territory('Brasil', 'América do Sul', [])
        territory.troops = 1
        self.player1.territories = [territory]
        
        # Coloca 5 exércitos no Brasil
        game.place_armies(self.player1, 'Brasil', 5)
        self.assertEqual(territory.troops, 6)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_place_armies_invalid_territory(self, mock_missions, mock_map):
        """Testa erro ao tentar colocar exércitos em território que não possui."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': [], 'symbol': 'quadrado'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        # Tenta colocar exércitos em território que não possui
        with self.assertRaises(ValueError):
            game.place_armies(self.player1, 'Argentina', 5)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_attack_territory_success(self, mock_missions, mock_map):
        """Testa ataque bem-sucedido entre territórios."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': ['Brasil'], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        # Configura territórios
        brasil = Territory('Brasil', 'América do Sul', ['Argentina'])
        brasil.owner = self.player1
        brasil.troops = 10
        self.player1.territories.append(brasil)
        
        argentina = Territory('Argentina', 'América do Sul', ['Brasil'])
        argentina.owner = self.player2
        argentina.troops = 1
        self.player2.territories.append(argentina)
        
        # Realiza ataque (com tropas suficientes, deve conquistar)
        result = game.attack_territory(brasil, argentina, 5)
        
        # Verifica se foi bem-sucedido
        self.assertTrue(result)
        self.assertEqual(argentina.owner, self.player1)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_attack_own_territory(self, mock_missions, mock_map):
        """Testa que não é possível atacar território próprio."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': ['Brasil'], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        brasil = Territory('Brasil', 'América do Sul', ['Argentina'])
        brasil.owner = self.player1
        brasil.troops = 10
        
        argentina = Territory('Argentina', 'América do Sul', ['Brasil'])
        argentina.owner = self.player1  # Mesmo dono
        argentina.troops = 5
        
        with self.assertRaises(ValueError) as context:
            game.attack_territory(brasil, argentina, 5)
        
        self.assertIn("próprio", str(context.exception).lower())

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_attack_non_adjacent(self, mock_missions, mock_map):
        """Testa que não é possível atacar território não adjacente."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Japão', 'continent': 'Ásia', 'borders': [], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        brasil = Territory('Brasil', 'América do Sul', ['Argentina'])
        brasil.owner = self.player1
        brasil.troops = 10
        
        japao = Territory('Japão', 'Ásia', [])
        japao.owner = self.player2
        japao.troops = 5
        
        with self.assertRaises(ValueError) as context:
            game.attack_territory(brasil, japao, 5)
        
        self.assertIn("adjacentes", str(context.exception).lower())

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_move_troops_between_own_territories(self, mock_missions, mock_map):
        """Testa movimento de tropas entre territórios próprios."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': ['Brasil'], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        brasil = Territory('Brasil', 'América do Sul', ['Argentina'])
        brasil.owner = self.player1
        brasil.troops = 10
        
        argentina = Territory('Argentina', 'América do Sul', ['Brasil'])
        argentina.owner = self.player1
        argentina.troops = 5
        
        # Move 3 tropas do Brasil para Argentina
        game.move_troops(brasil, argentina, 3)
        
        self.assertEqual(brasil.troops, 7)
        self.assertEqual(argentina.troops, 8)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_move_troops_different_owners(self, mock_missions, mock_map):
        """Testa que não é possível mover tropas entre territórios de jogadores diferentes."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': ['Argentina'], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': ['Brasil'], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        brasil = Territory('Brasil', 'América do Sul', ['Argentina'])
        brasil.owner = self.player1
        brasil.troops = 10
        
        argentina = Territory('Argentina', 'América do Sul', ['Brasil'])
        argentina.owner = self.player2  # Dono diferente
        argentina.troops = 5
        
        with self.assertRaises(ValueError) as context:
            game.move_troops(brasil, argentina, 3)
        
        self.assertIn("mesmo jogador", str(context.exception).lower())

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_is_game_over_single_player(self, mock_missions, mock_map):
        """Testa detecção de fim de jogo quando resta apenas um jogador."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': [], 'symbol': 'quadrado'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        # Player1 tem territórios, Player2 não tem
        self.player1.territories = [MagicMock()]
        self.player2.territories = []
        
        is_over, winner = game.is_game_over()
        
        self.assertTrue(is_over)
        self.assertEqual(winner, self.player1)

    @patch('war.game.load_map_data')
    @patch('war.game.load_missions')
    def test_get_game_state(self, mock_missions, mock_map):
        """Testa obtenção do estado do jogo."""
        mock_map.return_value = {
            'territories': [
                {'name': 'Brasil', 'continent': 'América do Sul', 'borders': [], 'symbol': 'quadrado'},
                {'name': 'Argentina', 'continent': 'América do Sul', 'borders': [], 'symbol': 'círculo'}
            ]
        }
        mock_missions.return_value = [{'id': 1, 'description': 'M1'}, {'id': 2, 'description': 'M2'}]
        
        game = Game(self.players, self.dealer)
        
        # Adiciona territórios aos jogadores
        t1 = Territory('Brasil', 'América do Sul', [])
        t1.troops = 5
        self.player1.territories.append(t1)
        
        state = game.get_game_state()
        
        self.assertIn('players', state)
        self.assertIn('total_territories', state)
        self.assertEqual(len(state['players']), 2)
        self.assertEqual(state['total_territories'], 2)

if __name__ == '__main__':
    unittest.main()
