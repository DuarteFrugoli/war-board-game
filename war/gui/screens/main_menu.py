import pygame
from ..utils.constants import *


class MainMenu:
    """Tela do menu principal."""

    def __init__(self, screen, app):
        self.screen = screen
        self.app = app
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)

        # Dimensões atuais da tela
        self.screen_width, self.screen_height = screen.get_size()

        # Configurar botões iniciais
        self.setup_buttons()

        self.selected_players = 3  # Padrão: 3 jogadores

    def setup_buttons(self):
        """Configura os botões baseado nas dimensões atuais da tela."""
        # Botões principais
        self.buttons = {
            "new_game": pygame.Rect(
                self.screen_width // 2 - 100,
                self.screen_height * 0.5,
                200,
                BUTTON_HEIGHT),
            "quit": pygame.Rect(
                self.screen_width // 2 - 100,
                self.screen_height * 0.575,
                200,
                BUTTON_HEIGHT)}

        # Botões para seleção de número de jogadores
        self.player_buttons = {}
        button_width = 80
        button_height = 50  # Altura maior para melhor visual
        button_spacing = 25
        num_buttons = 4
        total_width = (num_buttons * button_width) + \
            ((num_buttons - 1) * button_spacing)
        start_x = (self.screen_width - total_width) // 2
        button_y = int(self.screen_height * 0.325)  # Posição Y mais centrada

        for i, num in enumerate([3, 4, 5, 6]):
            x = start_x + i * (button_width + button_spacing)
            self.player_buttons[num] = pygame.Rect(
                x, button_y, button_width, button_height)

    def update_dimensions(self, screen_width, screen_height):
        """Atualiza as dimensões da tela e reconfigura os botões."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.setup_buttons()

    def handle_event(self, event):
        """Processa eventos do menu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()

                # Verificar cliques nos botões principais
                if self.buttons["new_game"].collidepoint(mouse_pos):
                    self.start_new_game()
                elif self.buttons["quit"].collidepoint(mouse_pos):
                    self.app.quit_game()

                # Verificar cliques nos botões de seleção de jogadores
                for num_players, button_rect in self.player_buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        self.selected_players = num_players

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.selected_players = 3
            elif event.key == pygame.K_4:
                self.selected_players = 4
            elif event.key == pygame.K_5:
                self.selected_players = 5
            elif event.key == pygame.K_6:
                self.selected_players = 6
            elif event.key == pygame.K_RETURN:
                self.start_new_game()
            elif event.key == pygame.K_ESCAPE:
                self.app.quit_game()

    def update(self):
        """Atualiza o estado do menu."""
        pass

    def render(self):
        """Renderiza o menu."""
        # Fundo
        self.screen.fill(BLACK)

        # Título
        title_text = self.font_large.render(
            "WAR - Jogo de Estratégia", True, WHITE)
        title_rect = title_text.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.15)))
        self.screen.blit(title_text, title_rect)

        # Subtítulo
        subtitle_text = "Escolha o número de jogadores:"
        subtitle_surface = self.font_medium.render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.25)))
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Botões de seleção de jogadores
        for num_players, button_rect in self.player_buttons.items():
            # Cor do botão (destacar o selecionado)
            if num_players == self.selected_players:
                button_color = BLUE
                border_color = WHITE
                text_color = WHITE
                border_width = 4
            else:
                button_color = DARK_GRAY
                border_color = GRAY
                text_color = LIGHT_GRAY
                border_width = 2

            # Desenhar botão com bordas arredondadas
            pygame.draw.rect(
                self.screen,
                button_color,
                button_rect,
                border_radius=8)
            pygame.draw.rect(
                self.screen,
                border_color,
                button_rect,
                border_width,
                border_radius=8)

            # Texto do botão
            text_surface = self.font_medium.render(
                str(num_players), True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

        # Informação do número selecionado
        info_text = f"Jogadores selecionados: {self.selected_players}"
        info_surface = self.font_medium.render(info_text, True, WHITE)
        info_rect = info_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.41)))
        self.screen.blit(info_surface, info_rect)

        # Botões principais
        for button_name, button_rect in self.buttons.items():
            # Fundo do botão
            pygame.draw.rect(
                self.screen,
                DARK_GRAY,
                button_rect,
                border_radius=8)
            pygame.draw.rect(
                self.screen,
                WHITE,
                button_rect,
                2,
                border_radius=8)

            # Texto do botão
            if button_name == "new_game":
                button_text = "Iniciar Jogo"
            else:
                button_text = "Sair"

            text_surface = self.font_medium.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

        # Instruções
        instructions = [
            "• Clique nos números ou use as teclas 3-6",
            "• Enter para iniciar • ESC para sair",
            "• F11 para alternar tela cheia"
        ]
        y = int(self.screen_height * 0.65)
        for instruction in instructions:
            inst_surface = pygame.font.Font(
                None, 18).render(
                instruction, True, GRAY)
            inst_rect = inst_surface.get_rect(
                center=(self.screen_width // 2, y))
            self.screen.blit(inst_surface, inst_rect)
            y += 20

    def start_new_game(self):
        """Inicia a configuração de um novo jogo."""
        # Ir para tela de configuração de jogadores
        self.app.start_player_setup(self.selected_players)
