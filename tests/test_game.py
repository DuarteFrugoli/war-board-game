# test_game.py
# Testes para a lógica do jogo

import unittest
from unittest.mock import patch, MagicMock
from war.Game import Game
from war.Player import Player
from war.Territory import Territory
from war.Card import Card
from war.Deck import Deck

class TestGame(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("João", "Azul")
        self.player2 = Player("Maria", "Vermelho")
        self.players = [self.player1, self.player2]
        self.dealer = self.player1

    @patch('war.Game.load_map_data')
    @patch('war.Game.load_missions')
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

    @patch('war.Game.load_map_data')
    @patch('war.Game.load_missions')
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

    @patch('war.Game.load_map_data')
    @patch('war.Game.load_missions')
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

if __name__ == '__main__':
    unittest.main()
