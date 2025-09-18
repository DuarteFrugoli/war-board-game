import pygame
from ..utils.constants import *


class MainMenu:
    """Tela do menu principal."""
    
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        
        # Botões
        self.buttons = {
            "new_game": pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, BUTTON_HEIGHT),
            "quit": pygame.Rect(SCREEN_WIDTH//2 - 100, 360, 200, BUTTON_HEIGHT)
        }
        
        self.selected_players = 3  # Padrão: 3 jogadores
        
    def handle_event(self, event):
        """Processa eventos do menu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                
                if self.buttons["new_game"].collidepoint(mouse_pos):
                    self.start_new_game()
                elif self.buttons["quit"].collidepoint(mouse_pos):
                    self.app.quit_game()
        
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
    
    def update(self):
        """Atualiza o estado do menu."""
        pass
    
    def render(self):
        """Renderiza o menu."""
        # Fundo
        self.screen.fill(BLACK)
        
        # Título
        title_text = self.font_large.render("WAR - Jogo de Estratégia", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Instruções de jogadores
        players_text = self.font_medium.render(f"Jogadores: {self.selected_players} (Pressione 3-6)", True, WHITE)
        players_rect = players_text.get_rect(center=(SCREEN_WIDTH//2, 220))
        self.screen.blit(players_text, players_rect)
        
        # Botões
        for button_name, button_rect in self.buttons.items():
            # Fundo do botão
            pygame.draw.rect(self.screen, DARK_GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Texto do botão
            if button_name == "new_game":
                button_text = "Novo Jogo"
            else:
                button_text = "Sair"
            
            text_surface = self.font_medium.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def start_new_game(self):
        """Inicia a configuração de um novo jogo."""
        # Ir para tela de configuração de jogadores
        self.app.start_player_setup(self.selected_players)