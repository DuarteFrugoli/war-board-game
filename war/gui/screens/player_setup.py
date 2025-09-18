import pygame
from ..utils.constants import *


class PlayerSetupScreen:
    """Tela para configuração dos jogadores."""
    
    def __init__(self, screen, app, num_players):
        self.screen = screen
        self.app = app
        self.num_players = num_players
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        
        # Configuração dos jogadores
        self.players_config = []
        self.current_player = 0
        self.current_step = "name"  # "name" ou "color"
        
        # Cores disponíveis
        self.available_colors = ["vermelho", "azul", "verde", "amarelo", "preto", "branco"]
        self.selected_color_index = 0
        
        # Input de texto
        self.text_input = ""
        self.input_active = True
        
        # Botões
        self.setup_buttons()
        
    def setup_buttons(self):
        """Configura os botões da tela."""
        # Posicionamento relativo baseado na altura da tela
        button_y_base = SCREEN_HEIGHT * 0.6  # 60% da altura da tela
        button_y_confirm = SCREEN_HEIGHT * 0.7  # 70% da altura da tela
        button_y_back = SCREEN_HEIGHT * 0.9  # 90% da altura para botão voltar
        
        if self.current_step == "name":
            self.buttons = {
                "confirm": pygame.Rect(SCREEN_WIDTH//2 - 100, int(button_y_confirm), 200, BUTTON_HEIGHT),
                "back": pygame.Rect(SCREEN_WIDTH * 0.05, int(button_y_back), int(SCREEN_WIDTH * 0.15), BUTTON_HEIGHT)
            }
        else:  # color
            # Botões de navegação de cor horizontalmente alinhados
            nav_button_y = int(button_y_base)
            nav_button_width = 120
            spacing = (SCREEN_WIDTH - 2 * nav_button_width) // 3  # Espaçamento igual
            
            self.buttons = {
                "prev_color": pygame.Rect(spacing, nav_button_y, nav_button_width, BUTTON_HEIGHT),
                "next_color": pygame.Rect(SCREEN_WIDTH - spacing - nav_button_width, nav_button_y, nav_button_width, BUTTON_HEIGHT),
                "confirm": pygame.Rect(SCREEN_WIDTH//2 - 100, int(button_y_confirm), 200, BUTTON_HEIGHT),
                "back": pygame.Rect(SCREEN_WIDTH * 0.05, int(button_y_back), int(SCREEN_WIDTH * 0.15), BUTTON_HEIGHT)
            }
    
    def handle_event(self, event):
        """Processa eventos da tela."""
        if event.type == pygame.KEYDOWN:
            if self.current_step == "name":
                if event.key == pygame.K_RETURN:
                    self.confirm_name()
                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.go_back()
                else:
                    # Adicionar caractere se for válido
                    if event.unicode.isalnum() or event.unicode == " ":
                        if len(self.text_input) < 20:
                            self.text_input += event.unicode
            else:  # color
                if event.key == pygame.K_LEFT:
                    self.prev_color()
                elif event.key == pygame.K_RIGHT:
                    self.next_color()
                elif event.key == pygame.K_RETURN:
                    self.confirm_color()
                elif event.key == pygame.K_ESCAPE:
                    self.go_back()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                
                if "confirm" in self.buttons and self.buttons["confirm"].collidepoint(mouse_pos):
                    if self.current_step == "name":
                        self.confirm_name()
                    else:
                        self.confirm_color()
                elif "back" in self.buttons and self.buttons["back"].collidepoint(mouse_pos):
                    self.go_back()
                elif self.current_step == "color":
                    if "prev_color" in self.buttons and self.buttons["prev_color"].collidepoint(mouse_pos):
                        self.prev_color()
                    elif "next_color" in self.buttons and self.buttons["next_color"].collidepoint(mouse_pos):
                        self.next_color()
    
    def prev_color(self):
        """Cor anterior."""
        self.selected_color_index = (self.selected_color_index - 1) % len(self.available_colors)
    
    def next_color(self):
        """Próxima cor."""
        self.selected_color_index = (self.selected_color_index + 1) % len(self.available_colors)
    
    def confirm_name(self):
        """Confirma o nome do jogador."""
        if self.text_input.strip():
            self.current_step = "color"
            self.setup_buttons()
    
    def confirm_color(self):
        """Confirma a cor do jogador."""
        selected_color = self.available_colors[self.selected_color_index]
        
        # Adicionar jogador configurado
        self.players_config.append({
            "name": self.text_input.strip(),
            "color": selected_color
        })
        
        # Remover cor das disponíveis
        self.available_colors.remove(selected_color)
        
        # Próximo jogador ou finalizar
        self.current_player += 1
        if self.current_player >= self.num_players:
            # Todos jogadores configurados
            self.app.start_dealer_selection(self.players_config)
        else:
            # Resetar para próximo jogador
            self.text_input = ""
            self.current_step = "name"
            self.selected_color_index = 0
            self.setup_buttons()
    
    def go_back(self):
        """Volta para a tela anterior."""
        if self.current_step == "color":
            self.current_step = "name"
            self.setup_buttons()
        elif self.current_player > 0:
            # Voltar para jogador anterior
            self.current_player -= 1
            # Restaurar configuração do jogador anterior
            if self.players_config:
                prev_config = self.players_config.pop()
                self.available_colors.append(prev_config["color"])
                self.text_input = prev_config["name"]
                self.current_step = "color"
                # Encontrar índice da cor
                self.selected_color_index = self.available_colors.index(prev_config["color"])
                self.setup_buttons()
        else:
            # Volta ao menu de número de jogadores
            self.app.return_to_menu()
    
    def update(self):
        """Atualiza o estado da tela."""
        pass
    
    def render(self):
        """Renderiza a tela."""
        # Fundo
        self.screen.fill(BLACK)
        
        # Layout baseado em proporções da tela
        title_y = SCREEN_HEIGHT * 0.08  # 8% da altura
        player_info_y = SCREEN_HEIGHT * 0.16  # 16% da altura
        content_y = SCREEN_HEIGHT * 0.25  # 25% da altura para conteúdo principal
        
        # Título
        title_text = f"Configuração dos Jogadores ({self.current_player + 1}/{self.num_players})"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, int(title_y)))
        self.screen.blit(title_surface, title_rect)
        
        # Nome do jogador atual
        player_text = f"Jogador {self.current_player + 1}"
        player_surface = self.font_medium.render(player_text, True, WHITE)
        player_rect = player_surface.get_rect(center=(SCREEN_WIDTH//2, int(player_info_y)))
        self.screen.blit(player_surface, player_rect)
        
        if self.current_step == "name":
            self.render_name_input()
        else:
            self.render_color_selection()
        
        # Renderizar botões
        self.render_buttons()
        
        # Progresso dos jogadores já configurados
        self.render_progress()
    
    def render_name_input(self):
        """Renderiza a entrada de nome."""
        # Posicionamento baseado em proporções
        instruction_y = SCREEN_HEIGHT * 0.32  # 32% da altura
        input_y = SCREEN_HEIGHT * 0.42  # 42% da altura
        
        # Instrução
        instruction = "Digite o nome do jogador:"
        instruction_surface = self.font_medium.render(instruction, True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, int(instruction_y)))
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Campo de entrada - tamanho proporcional à tela
        input_width = min(400, SCREEN_WIDTH * 0.4)  # 40% da largura ou 400px máximo
        input_height = 50
        input_rect = pygame.Rect(SCREEN_WIDTH//2 - input_width//2, int(input_y), int(input_width), input_height)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 3)
        
        # Texto digitado
        if self.text_input:
            text_surface = self.font_medium.render(self.text_input, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.centery = input_rect.centery
            text_rect.x = input_rect.x + 10  # Margem interna
            self.screen.blit(text_surface, text_rect)
        
        # Cursor piscante
        if pygame.time.get_ticks() % 1000 < 500:
            if self.text_input:
                text_surface = self.font_medium.render(self.text_input, True, BLACK)
                cursor_x = input_rect.x + 10 + text_surface.get_width() + 2
            else:
                cursor_x = input_rect.x + 12
            pygame.draw.line(self.screen, BLACK, (cursor_x, input_rect.top + 10), (cursor_x, input_rect.bottom - 10), 2)
    
    def render_color_selection(self):
        """Renderiza a seleção de cor."""
        # Posicionamento baseado em proporções
        instruction_y = SCREEN_HEIGHT * 0.32  # 32% da altura
        color_display_y = SCREEN_HEIGHT * 0.42  # 42% da altura
        color_name_y = SCREEN_HEIGHT * 0.52  # 52% da altura
        nav_instruction_y = SCREEN_HEIGHT * 0.57  # 57% da altura
        
        # Instrução
        instruction = f"Escolha a cor para {self.text_input}:"
        instruction_surface = self.font_medium.render(instruction, True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, int(instruction_y)))
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Cor atual
        current_color = self.available_colors[self.selected_color_index]
        color_rgb = PLAYER_COLORS.get(current_color, WHITE)
        
        # Quadrado da cor - tamanho proporcional
        color_size = min(120, int(SCREEN_WIDTH * 0.08))
        color_rect = pygame.Rect(SCREEN_WIDTH//2 - color_size//2, int(color_display_y), color_size, int(color_size * 0.6))
        pygame.draw.rect(self.screen, color_rgb, color_rect)
        pygame.draw.rect(self.screen, WHITE, color_rect, 3)
        
        # Nome da cor
        color_name_surface = self.font_medium.render(current_color.title(), True, WHITE)
        color_name_rect = color_name_surface.get_rect(center=(SCREEN_WIDTH//2, int(color_name_y)))
        self.screen.blit(color_name_surface, color_name_rect)
        
        # Instruções de navegação
        nav_text = "Use ← → ou clique nos botões para navegar"
        nav_surface = self.font_small.render(nav_text, True, GRAY)
        nav_rect = nav_surface.get_rect(center=(SCREEN_WIDTH//2, int(nav_instruction_y)))
        self.screen.blit(nav_surface, nav_rect)
    
    def render_buttons(self):
        """Renderiza os botões."""
        for button_name, button_rect in self.buttons.items():
            # Fundo do botão
            pygame.draw.rect(self.screen, DARK_GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Texto do botão
            if button_name == "confirm":
                if self.current_step == "name":
                    button_text = "Confirmar Nome" if self.text_input.strip() else "Digite um nome"
                else:
                    button_text = "Confirmar Cor"
            elif button_name == "back":
                button_text = "Voltar"
            elif button_name == "prev_color":
                button_text = "← Anterior"
            elif button_name == "next_color":
                button_text = "Próximo →"
            
            # Cor do texto baseada na disponibilidade
            text_color = WHITE
            if button_name == "confirm" and self.current_step == "name" and not self.text_input.strip():
                text_color = GRAY
            
            text_surface = self.font_small.render(button_text, True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def render_progress(self):
        """Renderiza o progresso dos jogadores já configurados."""
        if not self.players_config:
            return
        
        # Posicionar na lateral direita de forma proporcional
        sidebar_width = SCREEN_WIDTH * 0.25  # 25% da largura para sidebar
        x_start = SCREEN_WIDTH - sidebar_width + 20
        y_start = SCREEN_HEIGHT * 0.25  # Começar em 25% da altura
        
        # Verificar se cabe na tela
        max_height = SCREEN_HEIGHT * 0.4  # Máximo 40% da altura disponível
        item_height = 25
        max_items = int(max_height / item_height)
        
        progress_title = "Configurados:"
        title_surface = self.font_small.render(progress_title, True, WHITE)
        self.screen.blit(title_surface, (int(x_start), int(y_start)))
        y = y_start + 30
        
        # Mostrar apenas os que cabem na tela
        items_to_show = min(len(self.players_config), max_items)
        
        for i in range(items_to_show):
            player_config = self.players_config[i]
            color_rgb = PLAYER_COLORS.get(player_config["color"], WHITE)
            
            # Nome truncado se muito longo
            name = player_config["name"]
            if len(name) > 12:
                name = name[:12] + "..."
                
            player_text = f"{i+1}. {name}"
            text_surface = self.font_small.render(player_text, True, color_rgb)
            self.screen.blit(text_surface, (int(x_start), int(y)))
            
            # Pequeno quadrado da cor
            color_rect = pygame.Rect(int(x_start + 120), int(y + 2), 15, 15)
            pygame.draw.rect(self.screen, color_rgb, color_rect)
            pygame.draw.rect(self.screen, WHITE, color_rect, 1)
            
            y += item_height
        
        # Se há mais jogadores, mostrar indicador
        if len(self.players_config) > max_items:
            more_text = f"+ {len(self.players_config) - max_items} mais..."
            more_surface = self.font_small.render(more_text, True, GRAY)
            self.screen.blit(more_surface, (int(x_start), int(y)))