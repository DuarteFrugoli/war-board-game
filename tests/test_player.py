
import unittest
from war.player import Player
from war.territory import Territory

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Thiago", "Vermelho")
        self.territory1 = Territory("Brasil", "América do Sul", ["Argentina", "Peru"])
        self.territory2 = Territory("Argentina", "América do Sul", ["Brasil"])

    def test_nome_do_jogador(self):
        self.assertEqual(self.player.name, "Thiago")

    def test_cor_do_jogador(self):
        self.assertEqual(self.player.color, "Vermelho")

    def test_receive_mission(self):
        mission = {"id": 1, "description": "Conquistar a América do Sul"}
        self.player.receive_mission(mission)
        self.assertEqual(self.player.mission, mission)

    def test_receive_territory(self):
        self.player.receive_territory(self.territory1)
        self.assertIn(self.territory1, self.player.territories)
        self.assertEqual(len(self.player.territories), 1)

    def test_get_territory_count(self):
        self.assertEqual(self.player.get_territory_count(), 0)
        self.player.receive_territory(self.territory1)
        self.player.receive_territory(self.territory2)
        self.assertEqual(self.player.get_territory_count(), 2)

    def test_get_total_troops(self):
        self.territory1.troops = 5
        self.territory2.troops = 3
        self.player.receive_territory(self.territory1)
        self.player.receive_territory(self.territory2)
        self.assertEqual(self.player.get_total_troops(), 8)

    def test_adicionar_tropas_territorio_valido(self):
        self.player.receive_territory(self.territory1)
        self.player.adicionarTropas("Brasil", 5)
        self.assertEqual(self.territory1.troops, 5)

    def test_adicionar_tropas_territorio_inexistente(self):
        with self.assertRaises(ValueError):
            self.player.adicionarTropas("França", 3)

    def test_owns_continent(self):
        map_data = {
            'continents': [
                {'name': 'América do Sul', 'territories': ['Brasil', 'Argentina']}
            ]
        }
        # Não possui continente completo
        self.player.receive_territory(self.territory1)
        self.assertFalse(self.player.owns_continent('América do Sul', map_data))
        
        # Possui continente completo
        self.player.receive_territory(self.territory2)
        self.assertTrue(self.player.owns_continent('América do Sul', map_data))

if __name__ == '__main__':
    unittest.main()

