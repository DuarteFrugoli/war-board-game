class Player:
    def __init__(self, name):
        self.name = name
        self.countryCounters = {}  # Exemplo: {'Brazil': 5, 'Argentina': 3}

    def atacar(self, jogador, unidades):
        # ...lógica de ataque...
        pass

    def adicionarTropas(self, pais, unidades):
        # ...adiciona tropas ao país...
        if pais in self.countryCounters:
            self.countryCounters[pais] += unidades
        else:
            self.countryCounters[pais] = unidades

    def moverTropas(self, pais, unidades):
        # ...move tropas entre países...
        pass

    def trocarCartasPorTropas(self, cartas):
        # ...troca cartas por tropas...
        pass