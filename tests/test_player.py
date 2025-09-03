
from war.player import Player
import unittest


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Thiago", "Red")

    def test_adicionar_tropas_novo_pais(self):
        self.player.adicionarTropas("Brazil", 5)
        self.assertEqual(self.player.countryCounters["Brazil"], 5)

    def test_adicionar_tropas_existente(self):
        self.player.adicionarTropas("Brazil", 3)
        self.player.adicionarTropas("Brazil", 2)
        self.assertEqual(self.player.countryCounters["Brazil"], 5)

    def test_nome_do_jogador(self):
        self.assertEqual(self.player.name, "Thiago")

    def test_cor_do_jogador(self):
        self.assertEqual(self.player.color, "Red")


if __name__ == '__main__':
    unittest.main()

