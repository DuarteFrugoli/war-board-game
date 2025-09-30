import unittest
from unittest.mock import patch
from war.utils import roll_die, roll_multiple_dice, get_continent_bonus, player_owns_continent, get_continent_controller
from war.player import Player
from war.territory import Territory

class TestUtilsRolling(unittest.TestCase):

    def test_roll_die_fora_do_intervalo(self):
        resultado = roll_die()
        self.assertLessEqual(resultado, 6)
        self.assertGreaterEqual(resultado, 1)

    def test_roll_multiple_dice_quantidade_negativa(self):
        resultados = roll_multiple_dice(-3)  
        self.assertEqual(len(resultados), 0)

    def test_roll_multiple_dice_quantidade_zero(self):
        resultados = roll_multiple_dice(0)  
        self.assertEqual(len(resultados), 0)

    def test_roll_multiple_dice_valores_validos(self):
        resultados = roll_multiple_dice(3)
        self.assertEqual(len(resultados), 3)
        for valor in resultados:
            self.assertBetween(valor, 1, 6)

    def assertBetween(self, value, min_val, max_val):
        self.assertGreaterEqual(value, min_val)
        self.assertLessEqual(value, max_val)

class TestUtilsContinent(unittest.TestCase):

    def setUp(self):
        self.player = Player("João", "Azul")
        self.map_data = {
            'continents': [
                {'name': 'América do Sul', 'territories': ['Brasil', 'Argentina', 'Peru']},
                {'name': 'Europa', 'territories': ['França', 'Alemanha']}
            ]
        }
        
    def test_get_continent_bonus(self):
        self.assertEqual(get_continent_bonus('América do Sul'), 2)
        self.assertEqual(get_continent_bonus('Europa'), 5)
        self.assertEqual(get_continent_bonus('Continente Inexistente'), 1)

    def test_player_owns_continent_false(self):
        # Player não possui todos os territórios
        self.player.receive_territory(Territory("Brasil", "América do Sul"))
        self.assertFalse(player_owns_continent(self.player, 'América do Sul', self.map_data))

    def test_player_owns_continent_true(self):
        # Player possui todos os territórios
        self.player.receive_territory(Territory("Brasil", "América do Sul"))
        self.player.receive_territory(Territory("Argentina", "América do Sul"))
        self.player.receive_territory(Territory("Peru", "América do Sul"))
        self.assertTrue(player_owns_continent(self.player, 'América do Sul', self.map_data))

    def test_player_owns_continent_inexistente(self):
        self.assertFalse(player_owns_continent(self.player, 'Continente Inexistente', self.map_data))

    def test_get_continent_controller_none(self):
        players = [self.player]
        controller = get_continent_controller('América do Sul', self.map_data, players)
        self.assertIsNone(controller)

    def test_get_continent_controller_found(self):
        self.player.receive_territory(Territory("Brasil", "América do Sul"))
        self.player.receive_territory(Territory("Argentina", "América do Sul"))
        self.player.receive_territory(Territory("Peru", "América do Sul"))
        
        players = [self.player]
        controller = get_continent_controller('América do Sul', self.map_data, players)
        self.assertEqual(controller, self.player)

if __name__ == '__main__':
    unittest.main()