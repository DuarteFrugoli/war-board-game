import unittest
from war.game import *

class TestGame(unittest.TestCase):

    def test_load_map_data_real(self):
        data = load_map_data()
        self.assertTrue(isinstance(data, (dict, list)))
        self.assertGreater(len(data), 0)  # garante que não está vazio

    def test_load_missions_real(self):
        data = load_missions()
        self.assertTrue(isinstance(data, (dict, list)))
        self.assertGreater(len(data), 0) 

    def setUp(self):
        # Mock de dados semelhantes ao map.json
        self.map_data = {
            "territories": [
                {"name": "Brazil", "continent": "South America"},
                {"name": "Argentina", "continent": "South America"}
            ],
            "continents": [
                {"name": "South America", "territories": ["Brazil", "Argentina"]}
            ]
        }

    # cria objetos Territory e Continent a partir dos dados mockados
    def test_create_territories(self): 
        territories = create_territories(self.map_data)
        self.assertEqual(len(territories), 2)
        self.assertIsInstance(territories[0], Territory)
        self.assertEqual(territories[0].name, "Brazil")
        self.assertEqual(territories[0].continent, "South America")

    def test_create_continents(self):
        continents = create_continents(self.map_data)
        self.assertEqual(len(continents), 1)
        self.assertIsInstance(continents[0], Continent)
        self.assertEqual(continents[0].name, "South America")
        self.assertIn("Brazil", continents[0].territories)
    
    #mock para o teste de cards
    def setUp(self):
        self.territories = [
            Territory("Brazil", "South America"),
            Territory("Argentina", "South America"),
            Territory("Chile", "South America"),
            Territory("Peru", "South America"),
        ]        

    def test_create_cards_length_and_type(self):
        cards = create_cards(self.territories)
        self.assertEqual(len(cards), len(self.territories))
        self.assertIsInstance(cards[0], Card)

    def test_create_cards_symbols_cycle(self):
        cards = create_cards(self.territories)
        expected_symbols = ['quadrado', 'círculo', 'triângulo', 'quadrado']  # ciclo reinicia
        result_symbols = [card.symbol for card in cards]
        self.assertEqual(result_symbols, expected_symbols)

    def test_create_cards_correct_territory_names(self):
        cards = create_cards(self.territories)
        names_from_cards = [card.territory for card in cards]
        names_from_territories = [t.name for t in self.territories]
        self.assertEqual(names_from_cards, names_from_territories)


if __name__ == "__main__":
    unittest.main()
