import pygame
import random
from ..utils.constants import *


class DealerSelectionScreen:
    """Tela para determinar quem será o entregador de cartas."""
    
    def __init__(self, screen, app, players_config):
        self.screen = screen
        self.app = app
        self.players_config = players_config
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        
        # Estado da determinação
        self.phase = "intro"  # "intro", "rolling", "results", "final"
        self.current_players = list(range(len(players_config)))  # Índices dos jogadores ativos
        self.rolls = {}  # {player_index: roll_value}
        self.dealer_index = None
        self.animation_timer = 0
        self.roll_animation = False
        self.round_number = 1  # Contador de rodadas
        
        # Animação de dados - todos os dados ao mesmo tempo
        self.dice_animations = {}  # {player_index: current_dice_value}
        self.final_rolls = {}  # {player_index: final_roll_value}
        
        # Botões com posicionamento proporcional
        button_y_primary = int(SCREEN_HEIGHT * 0.65)  # 65% da altura
        button_y_secondary = int(SCREEN_HEIGHT * 0.72)  # 72% da altura  
        button_y_tertiary = int(SCREEN_HEIGHT * 0.79)  # 79% da altura
        button_y_back = int(SCREEN_HEIGHT * 0.9)  # 90% da altura para botão voltar
        
        self.buttons = {
            "start": pygame.Rect(SCREEN_WIDTH//2 - 100, button_y_primary, 200, BUTTON_HEIGHT),
            "roll": pygame.Rect(SCREEN_WIDTH//2 - 100, button_y_secondary, 200, BUTTON_HEIGHT),
            "continue": pygame.Rect(SCREEN_WIDTH//2 - 100, button_y_tertiary, 200, BUTTON_HEIGHT),
            "back": pygame.Rect(int(SCREEN_WIDTH * 0.05), button_y_back, int(SCREEN_WIDTH * 0.15), BUTTON_HEIGHT)
        }
    
    def handle_event(self, event):
        """Processa eventos da tela."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                
                if self.buttons["back"].collidepoint(mouse_pos):
                    self.app.return_to_menu()
                elif self.phase == "intro" and self.buttons["start"].collidepoint(mouse_pos):
                    self.start_rolling()
                elif self.phase == "rolling" and self.buttons["roll"].collidepoint(mouse_pos):
                    self.roll_all_dice()
                elif self.phase in ["results", "final"] and self.buttons["continue"].collidepoint(mouse_pos):
                    if self.phase == "results":
                        self.check_results()
                    else:  # final
                        self.start_game()
        
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                if self.phase == "intro":
                    self.start_rolling()
                elif self.phase == "rolling":
                    self.roll_all_dice()
                elif self.phase in ["results", "final"]:
                    if self.phase == "results":
                        self.check_results()
                    else:
                        self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.app.return_to_menu()
    
    def start_rolling(self):
        """Inicia a fase de rolagem dos dados."""
        self.phase = "rolling"
        self.rolls.clear()
        self.dice_animations.clear()
        self.final_rolls.clear()
    
    def roll_all_dice(self):
        """Rola todos os dados simultaneamente."""
        if self.roll_animation:
            return
        
        # Gerar valores finais para todos os jogadores ativos
        for player_idx in self.current_players:
            self.final_rolls[player_idx] = random.randint(1, 6)
            self.dice_animations[player_idx] = random.randint(1, 6)
        
        # Iniciar animação
        self.roll_animation = True
        self.animation_timer = pygame.time.get_ticks()
    
    def update_animation(self):
        """Atualiza a animação de rolagem de dados."""
        if self.roll_animation:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.animation_timer
            
            if elapsed < 1500:  # Animação por 1.5 segundos
                # Mudar valores de todos os dados rapidamente
                if elapsed % 100 < 50:  # Muda a cada 100ms
                    for player_idx in self.current_players:
                        self.dice_animations[player_idx] = random.randint(1, 6)
            else:
                # Finalizar animação - usar valores finais
                self.roll_animation = False
                for player_idx in self.current_players:
                    self.rolls[player_idx] = self.final_rolls[player_idx]
                    self.dice_animations[player_idx] = self.final_rolls[player_idx]
                
                self.phase = "results"
    
    def check_results(self):
        """Verifica os resultados e determina o vencedor."""
        max_roll = max(self.rolls.values())
        winners = [player_idx for player_idx, roll in self.rolls.items() if roll == max_roll]
        
        if len(winners) == 1:
            # Temos um vencedor
            self.dealer_index = winners[0]
            self.phase = "final"
        else:
            # Empate - preparar nova rodada apenas com os empatados
            self.current_players = winners
            self.round_number += 1
            self.rolls.clear()
            self.dice_animations.clear()
            self.final_rolls.clear()
            self.phase = "rolling"
    
    def start_game(self):
        """Inicia o jogo com o dealer determinado."""
        # Passar apenas os dados de configuração e o índice do dealer
        self.app.start_game_with_dealer(self.players_config, self.dealer_index)
    
    def update(self):
        """Atualiza o estado da tela."""
        self.update_animation()
    
    def render(self):
        """Renderiza a tela."""
        # Fundo
        self.screen.fill(BLACK)
        
        # Título
        title_text = "Determinando o Entregador de Cartas"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title_surface, title_rect)
        
        if self.phase == "intro":
            self.render_intro()
        elif self.phase == "rolling":
            self.render_rolling()
        elif self.phase == "results":
            self.render_results()
        elif self.phase == "final":
            self.render_final()
        
        # Renderizar botões
        self.render_buttons()
    
    def render_intro(self):
        """Renderiza a tela de introdução."""
        explanation = [
            "Todos os jogadores rolam dados simultaneamente.",
            "Quem tirar o maior número será o entregador de cartas.",
            "Em caso de empate, apenas os empatados rolarão novamente."
        ]
        
        y = 150
        for line in explanation:
            text_surface = self.font_medium.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
            self.screen.blit(text_surface, text_rect)
            y += 40
        
        # Lista de jogadores
        y += 20
        players_title = "Jogadores participantes:"
        title_surface = self.font_medium.render(players_title, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(title_surface, title_rect)
        y += 40
        
        for i, config in enumerate(self.players_config):
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)
            player_text = f"{config['name']} ({config['color']})"
            text_surface = self.font_small.render(player_text, True, color_rgb)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
            self.screen.blit(text_surface, text_rect)
            y += 25
    
    def render_rolling(self):
        """Renderiza a fase de rolagem com todos os dados simultaneamente."""
        # Título da rodada
        if self.round_number > 1:
            round_text = f"Rodada {self.round_number} - Desempate"
            tied_players = [self.players_config[idx]["name"] for idx in self.current_players]
            subtitle = f"Entre: {', '.join(tied_players)}"
        else:
            round_text = "Todos os jogadores rolam seus dados"
            subtitle = "Quem tirar o maior número será o dealer"
        
        title_surface = self.font_medium.render(round_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.2)))
        self.screen.blit(title_surface, title_rect)
        
        subtitle_surface = self.font_small.render(subtitle, True, GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, int(SCREEN_HEIGHT * 0.25)))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Layout dos dados: 2 fileiras de 3 dados cada
        dice_size = 80
        dice_spacing_x = 150  # Espaçamento horizontal entre dados
        dice_spacing_y = 140  # Espaçamento vertical entre fileiras
        
        # Primeira fileira: sempre 3 dados centralizados
        first_row_width = 3 * dice_spacing_x - dice_spacing_x + dice_size
        start_x_row1 = (SCREEN_WIDTH - first_row_width) // 2
        start_y_row1 = int(SCREEN_HEIGHT * 0.35)
        
        # Segunda fileira: centralizada baseada no número restante
        remaining_players = len(self.current_players) - 3
        if remaining_players > 0:
            second_row_width = min(3, remaining_players) * dice_spacing_x - dice_spacing_x + dice_size
            start_x_row2 = (SCREEN_WIDTH - second_row_width) // 2
            start_y_row2 = start_y_row1 + dice_spacing_y
        
        for i, player_idx in enumerate(self.current_players):
            config = self.players_config[player_idx]
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)
            
            if i < 3:
                # Primeira fileira (primeiros 3 jogadores)
                dice_x = start_x_row1 + i * dice_spacing_x
                dice_y = start_y_row1
            else:
                # Segunda fileira (jogadores restantes)
                dice_x = start_x_row2 + (i - 3) * dice_spacing_x
                dice_y = start_y_row2
            
            # Desenhar dado
            dice_rect = pygame.Rect(dice_x, dice_y, dice_size, dice_size)
            pygame.draw.rect(self.screen, WHITE, dice_rect)
            pygame.draw.rect(self.screen, color_rgb, dice_rect, 4)
            
            # Valor do dado
            if player_idx in self.dice_animations:
                dice_value = self.dice_animations[player_idx]
                dice_color = RED if self.roll_animation else BLACK
            else:
                dice_value = "?"
                dice_color = GRAY
            
            dice_text = str(dice_value)
            dice_surface = self.font_large.render(dice_text, True, dice_color)
            dice_text_rect = dice_surface.get_rect(center=dice_rect.center)
            self.screen.blit(dice_surface, dice_text_rect)
            
            # Nome do jogador abaixo do dado - centralizado
            name_text = config["name"][:10]  # Permitir nomes um pouco maiores
            name_surface = self.font_small.render(name_text, True, color_rgb)
            name_rect = name_surface.get_rect(center=(dice_rect.centerx, dice_rect.bottom + 25))
            self.screen.blit(name_surface, name_rect)
    
    def render_results(self):
        """Renderiza os resultados da rolagem."""
        results_title = "Resultados da rodada:"
        title_surface = self.font_medium.render(results_title, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_surface, title_rect)
        
        y = 200
        max_roll = max(self.rolls.values())
        
        for player_idx in self.current_players:
            roll = self.rolls[player_idx]
            config = self.players_config[player_idx]
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)
            
            # Destacar vencedor apenas com troféu, mas manter cor do jogador
            prefix = "🏆 " if roll == max_roll else "   "
            result_text = f"{prefix}{config['name']}: {roll} ({config['color'].title()})"
            
            # Todos os jogadores usam sua cor original
            text_surface = self.font_medium.render(result_text, True, color_rgb)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
            self.screen.blit(text_surface, text_rect)
            y += 35
    
    def render_tie(self):
        """Renderiza a tela de empate."""
        tie_title = "Empate!"
        title_surface = self.font_large.render(tie_title, True, RED)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_surface, title_rect)
        
        explanation = "Os seguintes jogadores vão rolar novamente:"
        exp_surface = self.font_medium.render(explanation, True, WHITE)
        exp_rect = exp_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(exp_surface, exp_rect)
        
        y = 250
        for player_idx in self.current_players:
            config = self.players_config[player_idx]
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)
            player_text = f"• {config['name']} ({config['color']})"
            text_surface = self.font_medium.render(player_text, True, color_rgb)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
            self.screen.blit(text_surface, text_rect)
            y += 35
    
    def render_final(self):
        """Renderiza o resultado final."""
        if self.dealer_index is not None:
            dealer_config = self.players_config[self.dealer_index]
            color_rgb = PLAYER_COLORS.get(dealer_config["color"], WHITE)
            
            final_title = "Entregador de Cartas:"
            title_surface = self.font_large.render(final_title, True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(title_surface, title_rect)
            
            dealer_text = f"🏆 {dealer_config['name']}"
            dealer_surface = self.font_large.render(dealer_text, True, YELLOW)
            dealer_rect = dealer_surface.get_rect(center=(SCREEN_WIDTH//2, 250))
            self.screen.blit(dealer_surface, dealer_rect)
            
            color_text = f"({dealer_config['color']})"
            color_surface = self.font_medium.render(color_text, True, color_rgb)
            color_rect = color_surface.get_rect(center=(SCREEN_WIDTH//2, 290))
            self.screen.blit(color_surface, color_rect)
    
    def render_buttons(self):
        """Renderiza os botões apropriados para cada fase."""
        visible_buttons = []
        
        if self.phase == "intro":
            visible_buttons = ["start", "back"]
        elif self.phase == "rolling":
            if not self.roll_animation:
                visible_buttons = ["roll", "back"]
            else:
                visible_buttons = ["back"]
        elif self.phase in ["results", "tie"]:
            visible_buttons = ["continue", "back"]
        elif self.phase == "final":
            visible_buttons = ["continue", "back"]
        
        for button_name in visible_buttons:
            button_rect = self.buttons[button_name]
            
            # Fundo do botão
            pygame.draw.rect(self.screen, DARK_GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Texto do botão
            if button_name == "start":
                button_text = "Começar"
            elif button_name == "roll":
                button_text = "Rolar Dados"
            elif button_name == "continue":
                if self.phase == "results":
                    button_text = "Ver Resultado"
                elif self.phase == "final":
                    button_text = "Iniciar Jogo"
                else:
                    button_text = "Continuar"
            elif button_name == "back":
                button_text = "Voltar"
            
            text_surface = self.font_small.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)