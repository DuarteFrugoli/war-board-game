import pygame
import sys
from typing import Optional
from war.Game import Game
from war.Player import Player
from .screens.main_menu import MainMenu
from .screens.player_setup import PlayerSetupScreen
from .screens.dealer_selection import DealerSelectionScreen
from .screens.game_screen import GameScreen
from .utils.constants import *


class GameApp:
    """Aplicação principal do jogo War com Pygame."""

    def __init__(self):
        """Inicializa a aplicação."""
        # Inicializar pygame primeiro
        pygame.init()
        pygame.mixer.pre_init()

        # Configuração da tela
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("War - Jogo de Estratégia")

        # Clock para controlar FPS
        self.clock = pygame.time.Clock()

        # Estado da aplicação
        self.running = True
        self.current_screen = "menu"
        self.game: Optional[Game] = None

        # Telas (inicializar depois do pygame)
        self.main_menu = MainMenu(self.screen, self)
        self.player_setup: Optional[PlayerSetupScreen] = None
        self.dealer_selection: Optional[DealerSelectionScreen] = None
        self.game_screen: Optional[GameScreen] = None

        # Fonte padrão
        self.default_font = pygame.font.Font(None, 32)

    def run(self):
        """Loop principal da aplicação."""
        while self.running:
            # Processar eventos de forma segura
            events = self.safe_event_get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)

            # Atualizar
            self.update()

            # Renderizar
            self.render()

            # Controlar FPS
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def safe_event_get(self):
        """Versão segura do pygame.event.get() para contornar bug."""
        try:
            return pygame.event.get()
        except Exception as e:
            print(f"Aviso: Erro ao obter eventos pygame: {e}")
            return []

    def handle_event(self, event):
        """Processa eventos baseado na tela atual."""
        # Eventos globais
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()

        # Eventos específicos da tela
        if self.current_screen == "menu":
            self.main_menu.handle_event(event)
        elif self.current_screen == "player_setup" and self.player_setup:
            self.player_setup.handle_event(event)
        elif self.current_screen == "dealer_selection" and self.dealer_selection:
            self.dealer_selection.handle_event(event)
        elif self.current_screen == "game" and self.game_screen:
            self.game_screen.handle_event(event)

    def update(self):
        """Atualiza o estado da aplicação."""
        if self.current_screen == "menu":
            self.main_menu.update()
        elif self.current_screen == "player_setup" and self.player_setup:
            self.player_setup.update()
        elif self.current_screen == "dealer_selection" and self.dealer_selection:
            self.dealer_selection.update()
        elif self.current_screen == "game" and self.game_screen:
            self.game_screen.update()

    def render(self):
        """Renderiza a tela atual."""
        if self.current_screen == "menu":
            self.main_menu.render()
        elif self.current_screen == "player_setup" and self.player_setup:
            self.player_setup.render()
        elif self.current_screen == "dealer_selection" and self.dealer_selection:
            self.dealer_selection.render()
        elif self.current_screen == "game" and self.game_screen:
            self.game_screen.render()

        pygame.display.flip()

    def toggle_fullscreen(self):
        """Alterna entre modo janela e tela cheia."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Obter novas dimensões da tela
        screen_width, screen_height = self.screen.get_size()

        # Atualizar referência da tela e dimensões em todas as telas
        self.main_menu.screen = self.screen
        self.main_menu.update_dimensions(screen_width, screen_height)
        if self.player_setup:
            self.player_setup.screen = self.screen
            self.player_setup.update_dimensions(screen_width, screen_height)
        if self.dealer_selection:
            self.dealer_selection.screen = self.screen
            self.dealer_selection.update_dimensions(
                screen_width, screen_height)
        if self.game_screen:
            self.game_screen.screen = self.screen
            self.game_screen.update_dimensions(screen_width, screen_height)

    def start_player_setup(self, num_players):
        """Inicia a tela de configuração dos jogadores."""
        self.player_setup = PlayerSetupScreen(self.screen, self, num_players)
        self.current_screen = "player_setup"

    def start_dealer_selection(self, players_config):
        """Inicia a tela de seleção do dealer."""
        self.dealer_selection = DealerSelectionScreen(
            self.screen, self, players_config)
        self.current_screen = "dealer_selection"

    def start_game_with_dealer(self, players_config, dealer_index):
        """Inicia o jogo com o dealer definido."""
        # Criar jogadores
        players = []
        dealer = None

        for i, config in enumerate(players_config):
            player = Player(config["name"], config["color"])
            players.append(player)
            # Identificar o dealer pelo índice
            if i == dealer_index:
                dealer = player

        # Criar jogo com dealer específico
        self.game = Game(players, dealer)

        # Criar tela do jogo
        self.game_screen = GameScreen(self.screen, self, self.game)

        # Mudar para tela do jogo
        self.current_screen = "game"

    def start_game(self, players_config):
        """Inicia um novo jogo."""
        # Criar jogadores
        players = []
        for i, config in enumerate(players_config):
            player = Player(config["name"], config["color"])
            players.append(player)

        # Criar jogo
        self.game = Game(players, players[0])  # Primeiro jogador é o dealer

        # Criar tela do jogo
        self.game_screen = GameScreen(self.screen, self, self.game)

        # Mudar para tela do jogo
        self.current_screen = "game"

    def return_to_menu(self):
        """Volta ao menu principal."""
        self.current_screen = "menu"
        self.game = None
        self.game_screen = None
        self.player_setup = None
        self.dealer_selection = None

    def quit_game(self):
        """Encerra a aplicação."""
        self.running = False
