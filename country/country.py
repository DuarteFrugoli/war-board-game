class Country:
    def __init__(self, name, troops=0, neighboors=None, dominantePlayer=None):
        self.name = name
        self.troops = troops
        self.neighboors = neighboors if neighboors is not None else []
        self.dominantePlayer = dominantePlayer