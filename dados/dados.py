import random

class Dado:
    def __init__(self, lados=6):
        self.lados = lados

    def rolar(self):
        return random.randint(1, self.lados)
    
    def rolar_varias_vezes(self,quantidade):
        resultados = []
        
        for _ in range(quantidade):
            resultados.append(self.rolar())
        return resultados    
