import pygame
import math
from ..utils.constants import *


class GameScreen:
    """Tela principal do jogo."""
    
    def __init__(self, screen, app, game):
        self.screen = screen
        self.app = app
        self.game = game
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        
        # Estado da interface
        self.current_player_index = self.game.start_game()
        if self.current_player_index < len(self.game.players):
            self.current_player = self.game.players[self.current_player_index]
        else:
            print(f"Erro: índice {self.current_player_index} inválido para {len(self.game.players)} jogadores")
            self.current_player = self.game.players[0]  # Fallback para primeiro jogador
        self.game_phase = PHASE_PLACE_ARMIES
        self.armies_to_place = self.game.calculate_armies_to_receive(self.current_player)
        self.territories_conquered_this_turn = 0  # Contador para cartas
        
        # Territórios selecionados
        self.selected_territory = None
        self.target_territory = None
        
        # Posições dos territórios no mapa (simplificado por enquanto)
        self.territory_positions = self.calculate_territory_positions()
        
        # Botões
        self.buttons = {
            "end_phase": pygame.Rect(900, 100, 120, BUTTON_HEIGHT),
            "menu": pygame.Rect(900, 150, 120, BUTTON_HEIGHT)
        }
    
    def calculate_territory_positions(self):
        """Calcula posições dos territórios na tela (versão simplificada)."""
        positions = {}
        
        # Por enquanto, distribuir territórios em grade
        cols = 7
        rows = 6
        start_x = MAP_X + 50
        start_y = MAP_Y + 50
        spacing_x = (MAP_WIDTH - 100) // (cols - 1)
        spacing_y = (MAP_HEIGHT - 100) // (rows - 1)
        
        for i, territory in enumerate(self.game.territories):
            row = i // cols
            col = i % cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            positions[territory.name] = (x, y)
        
        return positions
    
    def handle_event(self, event):
        """Processa eventos da tela do jogo."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                
                # Verificar cliques em botões
                if self.buttons["end_phase"].collidepoint(mouse_pos):
                    self.end_current_phase()
                elif self.buttons["menu"].collidepoint(mouse_pos):
                    self.app.return_to_menu()
                else:
                    # Verificar cliques em territórios
                    clicked_territory = self.get_territory_at_position(mouse_pos)
                    if clicked_territory:
                        self.handle_territory_click(clicked_territory)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.return_to_menu()
    
    def get_territory_at_position(self, pos):
        """Retorna o território na posição clicada."""
        for territory in self.game.territories:
            if territory.name in self.territory_positions:
                territory_pos = self.territory_positions[territory.name]
                distance = math.sqrt((pos[0] - territory_pos[0])**2 + (pos[1] - territory_pos[1])**2)
                if distance <= TERRITORY_RADIUS:
                    return territory
        return None
    
    def handle_territory_click(self, territory):
        """Lida com cliques em territórios baseado na fase atual."""
        if self.game_phase == PHASE_PLACE_ARMIES:
            if territory.owner == self.current_player and self.armies_to_place > 0:
                self.game.place_armies(self.current_player, territory.name, 1)
                self.armies_to_place -= 1
        
        elif self.game_phase == PHASE_ATTACK:
            if self.selected_territory is None:
                if territory.owner == self.current_player and territory.troops > 1:
                    self.selected_territory = territory
            else:
                if territory.owner != self.current_player:
                    if territory.name in self.selected_territory.borders:
                        # Executar ataque
                        self.execute_attack(self.selected_territory, territory)
                    self.selected_territory = None
                else:
                    self.selected_territory = territory if territory.troops > 1 else None
        
        elif self.game_phase == PHASE_MOVE:
            if self.selected_territory is None:
                if territory.owner == self.current_player and territory.troops > 1:
                    self.selected_territory = territory
            else:
                if territory.owner == self.current_player and territory.name in self.selected_territory.borders:
                    # Mover uma tropa
                    if self.selected_territory.troops > 1:
                        self.game.move_troops(self.selected_territory, territory, 1)
                self.selected_territory = None
    
    def execute_attack(self, attacker, defender):
        """Executa um ataque."""
        try:
            conquered = self.game.attack_territory(attacker, defender, 1)
            if conquered:
                self.territories_conquered_this_turn += 1
                print(f"{self.current_player.name} conquistou {defender.name}!")
            # Aqui você pode adicionar animações ou efeitos
        except Exception as e:
            print(f"Erro no ataque: {e}")
    
    def end_current_phase(self):
        """Termina a fase atual."""
        if self.game_phase == PHASE_PLACE_ARMIES:
            if self.armies_to_place == 0:
                self.game_phase = PHASE_ATTACK
        elif self.game_phase == PHASE_ATTACK:
            self.game_phase = PHASE_MOVE
        elif self.game_phase == PHASE_MOVE:
            self.end_turn()
        
        self.selected_territory = None
    
    def end_turn(self):
        """Termina o turno atual."""
        # Verificar se jogador deve receber carta
        card_received = self.game.phase_4_draw_card(self.current_player, self.territories_conquered_this_turn)
        if card_received:
            print(f"{self.current_player.name} recebeu uma carta: {card_received.territory_name or 'Coringa'}")
        
        # Próximo jogador
        self.current_player_index = self.game.get_next_player(self.current_player_index)
        self.current_player = self.game.players[self.current_player_index]
        
        # Resetar para fase 1
        self.game_phase = PHASE_PLACE_ARMIES
        self.armies_to_place = self.game.calculate_armies_to_receive(self.current_player)
        self.territories_conquered_this_turn = 0  # Reset contador
        
        # Verificar fim do jogo
        game_over, winner = self.game.is_game_over()
        if game_over:
            print(f"Jogo terminou! Vencedor: {winner.name if winner else 'Empate'}")
    
    def update(self):
        """Atualiza o estado do jogo."""
        pass
    
    def render(self):
        """Renderiza a tela do jogo."""
        # Fundo
        self.screen.fill(BLACK)
        
        # Área do mapa
        pygame.draw.rect(self.screen, DARK_GRAY, (MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (MAP_X, MAP_Y, MAP_WIDTH, MAP_HEIGHT), 2)
        
        # Territórios
        self.render_territories()
        
        # Interface lateral
        self.render_ui()
        
        # Botões
        self.render_buttons()
    
    def render_territories(self):
        """Renderiza os territórios no mapa."""
        for territory in self.game.territories:
            if territory.name not in self.territory_positions:
                continue
            
            pos = self.territory_positions[territory.name]
            
            # Cor baseada no dono
            if territory.owner:
                color = PLAYER_COLORS.get(territory.owner.color, WHITE)
            else:
                color = GRAY
            
            # Destaque para território selecionado
            if territory == self.selected_territory:
                pygame.draw.circle(self.screen, YELLOW, pos, TERRITORY_RADIUS + 3)
            
            # Território
            pygame.draw.circle(self.screen, color, pos, TERRITORY_RADIUS)
            pygame.draw.circle(self.screen, WHITE, pos, TERRITORY_RADIUS, TERRITORY_BORDER_WIDTH)
            
            # Número de tropas
            troops_text = self.font_small.render(str(territory.troops), True, BLACK)
            troops_rect = troops_text.get_rect(center=pos)
            self.screen.blit(troops_text, troops_rect)
    
    def render_ui(self):
        """Renderiza a interface lateral."""
        x = 900
        y = 50
        
        # Jogador atual
        player_text = f"Turno: {self.current_player.name}"
        text_surface = self.font_medium.render(player_text, True, WHITE)
        self.screen.blit(text_surface, (x, y))
        y += 30
        
        # Fase atual
        phases = {
            PHASE_PLACE_ARMIES: f"Colocar Exércitos ({self.armies_to_place})",
            PHASE_ATTACK: "Atacar",
            PHASE_MOVE: "Mover Tropas"
        }
        phase_text = phases.get(self.game_phase, "Desconhecida")
        text_surface = self.font_small.render(f"Fase: {phase_text}", True, WHITE)
        self.screen.blit(text_surface, (x, y))
        y += 50
        
        # Informações dos jogadores
        for i, player in enumerate(self.game.players):
            color = PLAYER_COLORS.get(player.color, WHITE)
            
            # Nome do jogador
            player_text = f"{player.name}:"
            text_surface = self.font_small.render(player_text, True, color)
            self.screen.blit(text_surface, (x, y))
            y += 20
            
            # Territórios e tropas
            info_text = f"  {len(player.territories)} territórios"
            text_surface = self.font_small.render(info_text, True, WHITE)
            self.screen.blit(text_surface, (x, y))
            y += 20
            
            total_troops = sum(t.troops for t in player.territories)
            troops_text = f"  {total_troops} tropas"
            text_surface = self.font_small.render(troops_text, True, WHITE)
            self.screen.blit(text_surface, (x, y))
            y += 30
    
    def render_buttons(self):
        """Renderiza os botões."""
        for button_name, button_rect in self.buttons.items():
            # Fundo do botão
            pygame.draw.rect(self.screen, DARK_GRAY, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Texto do botão
            if button_name == "end_phase":
                button_text = "Próxima Fase"
            else:
                button_text = "Menu"
            
            text_surface = self.font_small.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)