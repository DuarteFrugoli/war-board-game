# test_card.py
# Testes para a classe Card

import unittest
from war.Card import Card

class TestCard(unittest.TestCase):

    def test_card_initialization(self):
        card = Card("Brasil", "quadrado")
        self.assertEqual(card.territory_name, "Brasil")
        self.assertEqual(card.symbol, "quadrado")

    def test_joker_card(self):
        joker = Card(None, "coringa")
        self.assertIsNone(joker.territory_name)
        self.assertEqual(joker.symbol, "coringa")

    def test_card_repr(self):
        card = Card("França", "círculo")
        expected = "<Card França [círculo]>"
        self.assertEqual(repr(card), expected)

    def test_joker_repr(self):
        joker = Card(None, "coringa")
        expected = "<Card None [coringa]>"
        self.assertEqual(repr(joker), expected)

if __name__ == '__main__':
    unittest.main()