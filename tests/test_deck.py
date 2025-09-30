# test_deck.py
# Testes para a classe Deck

import unittest
from war.card import Card
from war.deck import Deck

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.cards = [
            Card("Brasil", "quadrado"),
            Card("Argentina", "círculo"),
            Card("França", "triângulo")
        ]
        self.deck = Deck(self.cards.copy())

    def test_deck_initialization_empty(self):
        empty_deck = Deck()
        self.assertEqual(len(empty_deck.cards), 0)
        self.assertTrue(empty_deck.is_empty())

    def test_deck_initialization_with_cards(self):
        self.assertEqual(len(self.deck.cards), 3)
        self.assertFalse(self.deck.is_empty())

    def test_draw_card(self):
        original_size = len(self.deck.cards)
        card = self.deck.draw()
        
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.deck.cards), original_size - 1)

    def test_draw_from_empty_deck(self):
        empty_deck = Deck()
        card = empty_deck.draw()
        self.assertIsNone(card)

    def test_peek_card(self):
        original_size = len(self.deck.cards)
        top_card = self.deck.peek()
        
        self.assertIsInstance(top_card, Card)
        self.assertEqual(len(self.deck.cards), original_size)  # Size unchanged

    def test_peek_empty_deck(self):
        empty_deck = Deck()
        card = empty_deck.peek()
        self.assertIsNone(card)

    def test_add_card(self):
        new_card = Card("Alemanha", "quadrado")
        original_size = len(self.deck.cards)
        
        self.deck.add_card(new_card)
        self.assertEqual(len(self.deck.cards), original_size + 1)
        self.assertEqual(self.deck.cards[-1], new_card)

    def test_add_cards(self):
        new_cards = [
            Card("Itália", "círculo"),
            Card("Espanha", "triângulo")
        ]
        original_size = len(self.deck.cards)
        
        self.deck.add_cards(new_cards)
        self.assertEqual(len(self.deck.cards), original_size + 2)

    def test_shuffle(self):
        # Difícil testar randomização, mas podemos verificar que não quebra
        original_cards = self.deck.cards.copy()
        self.deck.shuffle()
        
        self.assertEqual(len(self.deck.cards), len(original_cards))
        # Verifica que ainda contém as mesmas cartas (em alguma ordem)
        self.assertEqual(set(card.territory_name for card in self.deck.cards),
                         set(card.territory_name for card in original_cards))

    def test_is_empty(self):
        self.assertFalse(self.deck.is_empty())
        
        # Draw all cards
        while not self.deck.is_empty():
            self.deck.draw()
            
        self.assertTrue(self.deck.is_empty())

if __name__ == '__main__':
    unittest.main()