from enum import Enum

class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    BLACK = 5
    WHITE = 6
    
    def __str__(self):
        color_names = {
            1: "Vermelho",
            2: "Azul", 
            3: "Verde",
            4: "Amarelo",
            5: "Preto",
            6: "Branco"
        }
        return color_names[self.value]
