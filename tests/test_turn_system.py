import unittest
from unittest.mock import MagicMock
from war.Game import Game
from war.Player import Player
from war.Territory import Territory


class TestTurnSystem(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.player1 = Player("Alice", "vermelho")
        self.player2 = Player("Bob", "azul")
        self.players = [self.player1, self.player2]
        self.game = Game(self.players, self.player1)

    def test_calculate_armies_to_receive(self):
        """Testa o cálculo de exércitos recebidos baseado nos territórios."""
        # Player com 21 territórios deve receber 10 exércitos (21 // 2 = 10)
        armies = self.game.calculate_armies_to_receive(self.player1)
        expected = len(self.player1.territories) // 2
        self.assertEqual(armies, max(expected, 1))
        
        # Teste com jogador com poucos territórios
        test_player = Player("Test", "verde")
        # Player sem territórios deve receber pelo menos 1
        armies_empty = self.game.calculate_armies_to_receive(test_player)
        self.assertEqual(armies_empty, 1)

    def test_phase_1_distribute_armies(self):
        """Testa a fase 1 de distribuição de exércitos."""
        armies = self.game.phase_1_distribute_armies(self.player1)
        expected = len(self.player1.territories) // 2
        self.assertEqual(armies, max(expected, 1))

    def test_place_armies(self):
        """Testa a colocação de exércitos em territórios."""
        if self.player1.territories:
            territory = self.player1.territories[0]
            initial_troops = territory.troops
            
            self.game.place_armies(self.player1, territory.name, 5)
            self.assertEqual(territory.troops, initial_troops + 5)

    def test_place_armies_invalid_territory(self):
        """Testa erro ao tentar colocar exércitos em território não próprio."""
        with self.assertRaises(ValueError):
            self.game.place_armies(self.player1, "território_inexistente", 5)

    def test_move_troops(self):
        """Testa movimento de tropas entre territórios."""
        # Encontrar dois territórios adjacentes do mesmo jogador
        player_territories = self.player1.territories
        if len(player_territories) >= 2:
            from_territory = None
            to_territory = None
            
            for territory in player_territories:
                for border_name in territory.borders:
                    # Encontrar território adjacente que também pertença ao jogador
                    for other_territory in player_territories:
                        if other_territory.name == border_name:
                            from_territory = territory
                            to_territory = other_territory
                            break
                    if from_territory and to_territory:
                        break
                if from_territory and to_territory:
                    break
            
            if from_territory and to_territory:
                # Adicionar tropas suficientes para o teste
                from_territory.troops = 5
                to_territory.troops = 2
                
                initial_from = from_territory.troops
                initial_to = to_territory.troops
                
                self.game.move_troops(from_territory, to_territory, 2)
                
                self.assertEqual(from_territory.troops, initial_from - 2)
                self.assertEqual(to_territory.troops, initial_to + 2)

    def test_move_troops_invalid_owner(self):
        """Testa erro ao mover tropas entre territórios de jogadores diferentes."""
        territory1 = self.player1.territories[0] if self.player1.territories else None
        territory2 = self.player2.territories[0] if self.player2.territories else None
        
        if territory1 and territory2:
            with self.assertRaises(ValueError):
                self.game.move_troops(territory1, territory2, 1)

    def test_phase_4_draw_card_success(self):
        """Testa recebimento de carta quando conquistou territórios."""
        initial_cards = len(self.player1.cards)
        card = self.game.phase_4_draw_card(self.player1, 1)  # Conquistou 1 território
        
        if card:  # Se havia carta no deck
            self.assertEqual(len(self.player1.cards), initial_cards + 1)
            self.assertIn(card, self.player1.cards)

    def test_phase_4_draw_card_no_conquest(self):
        """Testa que não recebe carta quando não conquistou territórios."""
        initial_cards = len(self.player1.cards)
        card = self.game.phase_4_draw_card(self.player1, 0)  # Não conquistou territórios
        
        self.assertIsNone(card)
        self.assertEqual(len(self.player1.cards), initial_cards)

    def test_play_turn_structure(self):
        """Testa a estrutura básica do turno."""
        result = self.game.play_turn(self.player1)
        
        # Verifica se o resultado tem todas as chaves esperadas
        self.assertIn('armies_placed', result)
        self.assertIn('territories_conquered', result)
        self.assertIn('card_received', result)
        
        # Verifica tipos dos valores
        self.assertIsInstance(result['armies_placed'], int)
        self.assertIsInstance(result['territories_conquered'], int)
        # card_received pode ser None ou Card

    def test_start_game(self):
        """Testa o início do jogo."""
        current_player_index = self.game.start_game()
        expected_index = (self.players.index(self.game.dealer) + 1) % len(self.players)
        self.assertEqual(current_player_index, expected_index)

    def test_get_next_player(self):
        """Testa a rotação de jogadores."""
        current_index = 0
        next_index = self.game.get_next_player(current_index)
        expected_index = (current_index + 1) % len(self.players)
        self.assertEqual(next_index, expected_index)

    def test_is_game_over(self):
        """Testa detecção do fim do jogo."""
        # Jogo normal não deve ter terminado
        game_over, winner = self.game.is_game_over()
        self.assertFalse(game_over)
        self.assertIsNone(winner)

    def test_get_game_state(self):
        """Testa a obtenção do estado do jogo."""
        state = self.game.get_game_state()
        
        # Verifica estrutura do estado
        self.assertIn('players', state)
        self.assertIn('total_territories', state)
        self.assertIn('cards_in_deck', state)
        
        # Verifica informações dos jogadores
        self.assertEqual(len(state['players']), len(self.players))
        
        for player_info in state['players']:
            self.assertIn('name', player_info)
            self.assertIn('color', player_info)
            self.assertIn('territories_count', player_info)
            self.assertIn('total_troops', player_info)
            self.assertIn('cards_count', player_info)


if __name__ == '__main__':
    unittest.main()