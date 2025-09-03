import unittest
from unittest.mock import patch
from war.utils import roll_die, roll_multiple_dice

class TestUtilsFailures(unittest.TestCase):

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

    def test_roll_multiple_dice_valores_invalidos(self):
        resultados = roll_multiple_dice(10)
        for valor in resultados:
            self.assertBetween(valor, 1, 6)  

    def assertBetween(self, value, min_val, max_val):
        
        self.assertGreaterEqual(value, min_val)
        self.assertLessEqual(value, max_val)

if __name__ == '__main__':
    unittest.main()