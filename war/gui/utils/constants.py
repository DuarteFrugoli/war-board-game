"""
Constantes utilizadas na interface gráfica do jogo War.
"""

# Dimensões da tela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# FPS
FPS = 60

# Cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 20)
BLUE = (20, 20, 220)
GREEN = (20, 220, 20)
YELLOW = (220, 220, 20)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Cores dos jogadores
PLAYER_COLORS = {
    "vermelho": RED,
    "azul": BLUE,
    "verde": GREEN,
    "amarelo": YELLOW,
    "preto": BLACK,
    "branco": LIGHT_GRAY  # Usar cinza claro para visibilidade
}

# Configurações do mapa
MAP_X = 50
MAP_Y = 50
MAP_WIDTH = 800
MAP_HEIGHT = 600

# Configurações dos territórios
TERRITORY_RADIUS = 15
TERRITORY_BORDER_WIDTH = 2

# Configurações dos botões
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10

# Configurações das fontes
FONT_LARGE = 32
FONT_MEDIUM = 24
FONT_SMALL = 16

# Estados do jogo
GAME_STATE_MENU = "menu"
GAME_STATE_SETUP = "setup"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER = "game_over"

# Fases do turno
PHASE_PLACE_ARMIES = 1
PHASE_ATTACK = 2
PHASE_MOVE = 3
PHASE_DRAW_CARD = 4