# test_territory.py
# Testes para a classe Territory

import unittest
from war.Territory import Territory
from war.Player import Player

class TestTerritory(unittest.TestCase):

    def setUp(self):
        self.territory = Territory("Brasil", "América do Sul", ["Argentina", "Peru", "Venezuela"])
        self.player = Player("João", "Azul")

    def test_inicializacao(self):
        self.assertEqual(self.territory.name, "Brasil")
        self.assertEqual(self.territory.continent, "América do Sul")
        self.assertEqual(self.territory.borders, ["Argentina", "Peru", "Venezuela"])
        self.assertEqual(self.territory.troops, 0)
        self.assertIsNone(self.territory.owner)

    def test_sem_fronteiras(self):
        territory_isolated = Territory("Ilha", "Oceania")
        self.assertEqual(territory_isolated.borders, [])

    def test_is_border_with(self):
        self.assertTrue(self.territory.is_border_with("Argentina"))
        self.assertTrue(self.territory.is_border_with("Peru"))
        self.assertFalse(self.territory.is_border_with("França"))

    def test_set_owner(self):
        self.territory.owner = self.player
        self.assertEqual(self.territory.owner, self.player)

    def test_set_troops(self):
        self.territory.troops = 5
        self.assertEqual(self.territory.troops, 5)

    def test_repr(self):
        expected = "<Territory Brasil (América do Sul)>"
        self.assertEqual(repr(self.territory), expected)

if __name__ == '__main__':
    unittest.main()
