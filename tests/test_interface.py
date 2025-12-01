# test_interface.py
# Testes para funções de interface de usuário

import unittest
from unittest.mock import patch, MagicMock
from war.interface import get_number_of_players, create_players, determine_card_dealer
from war.player import Player


class TestInterface(unittest.TestCase):
    """Testes para funções de interface com usuário."""

    @patch('builtins.input', side_effect=['3'])
    def test_get_number_of_players_valid(self, mock_input):
        """Testa entrada válida de número de jogadores."""
        num_players = get_number_of_players()
        self.assertEqual(num_players, 3)

    @patch('builtins.input', side_effect=['6'])
    def test_get_number_of_players_max(self, mock_input):
        """Testa entrada com número máximo de jogadores."""
        num_players = get_number_of_players()
        self.assertEqual(num_players, 6)

    @patch('builtins.input', side_effect=['2', '7', 'abc', '4'])
    @patch('builtins.print')
    def test_get_number_of_players_invalid_retry(self, mock_print, mock_input):
        """Testa que repete quando entrada é inválida."""
        num_players = get_number_of_players()
        self.assertEqual(num_players, 4)
        # Verifica que mostrou mensagens de erro
        self.assertTrue(mock_print.called)

    @patch('builtins.input', side_effect=[
        'Alice', '1',  # Jogador 1: nome Alice, cor 1 (Vermelho)
        'Bob', '1'      # Jogador 2: nome Bob, cor 1 (primeira disponível após remover Vermelho = Azul)
    ])
    @patch('builtins.print')
    def test_create_players_two_players(self, mock_print, mock_input):
        """Testa criação de 2 jogadores."""
        from war.enums import COLORS
        players = create_players(2, COLORS, Player)
        
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, 'Alice')
        self.assertEqual(players[0].color, 'Vermelho')
        self.assertEqual(players[1].name, 'Bob')
        self.assertEqual(players[1].color, 'Azul')  # Azul é a primeira cor restante após Vermelho

    @patch('builtins.input', side_effect=[
        'Player1', '1',
        'Player2', '2',
        'Player3', '3'
    ])
    @patch('builtins.print')
    def test_create_players_colors_unique(self, mock_print, mock_input):
        """Testa que cada jogador recebe uma cor única."""
        from war.enums import COLORS
        players = create_players(3, COLORS, Player)
        
        colors = [p.color for p in players]
        # Verifica que não há cores duplicadas
        self.assertEqual(len(colors), len(set(colors)))

    @patch('builtins.input', side_effect=['7', 'invalid', '2'])
    @patch('builtins.print')
    def test_create_players_invalid_color_retry(self, mock_print, mock_input):
        """Testa retry quando cor inválida é escolhida."""
        from war.enums import COLORS
        players = create_players(1, COLORS, Player)
        
        self.assertEqual(len(players), 1)
        # Verifica que mensagem de erro foi exibida
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_determine_card_dealer_clear_winner(self, mock_print):
        """Testa seleção de dealer quando há vencedor claro."""
        player1 = Player("Alice", "Vermelho")
        player2 = Player("Bob", "Azul")
        players = [player1, player2]
        
        # Mock de roll_die que retorna valores específicos
        rolls = iter([6, 3])
        mock_roll_die = lambda: next(rolls)
        
        dealer = determine_card_dealer(players, roll_die=mock_roll_die)
        
        self.assertEqual(dealer, player1)  # Alice rolou 6, Bob rolou 3

    @patch('builtins.print')
    def test_determine_card_dealer_tie_then_win(self, mock_print):
        """Testa seleção de dealer com empate e depois vitória."""
        player1 = Player("Alice", "Vermelho")
        player2 = Player("Bob", "Azul")
        players = [player1, player2]
        
        rolls = iter([4, 4, 6, 2])  # Empate, depois Alice vence
        mock_roll_die = lambda: next(rolls)
        
        dealer = determine_card_dealer(players, roll_die=mock_roll_die)
        
        self.assertEqual(dealer, player1)

    @patch('builtins.print')
    def test_determine_card_dealer_three_players(self, mock_print):
        """Testa seleção de dealer com 3 jogadores."""
        player1 = Player("Alice", "Vermelho")
        player2 = Player("Bob", "Azul")
        player3 = Player("Charlie", "Verde")
        players = [player1, player2, player3]
        
        rolls = iter([3, 5, 3])  # Bob tem maior (5)
        mock_roll_die = lambda: next(rolls)
        
        dealer = determine_card_dealer(players, roll_die=mock_roll_die)
        
        self.assertEqual(dealer, player2)  # Bob rolou 5

    @patch('builtins.print')
    def test_determine_card_dealer_multiple_tie(self, mock_print):
        """Testa seleção de dealer com empate múltiplo."""
        player1 = Player("Alice", "Vermelho")
        player2 = Player("Bob", "Azul")
        player3 = Player("Charlie", "Verde")
        players = [player1, player2, player3]
        
        rolls = iter([6, 6, 6, 4, 2, 5])  # Empate triplo, Charlie vence
        mock_roll_die = lambda: next(rolls)
        
        dealer = determine_card_dealer(players, roll_die=mock_roll_die)
        
        self.assertEqual(dealer, player3)  # Charlie venceu no desempate


if __name__ == '__main__':
    unittest.main()
