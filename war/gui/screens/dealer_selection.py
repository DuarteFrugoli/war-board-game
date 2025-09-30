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

        # Dimensões atuais da tela
        self.screen_width, self.screen_height = screen.get_size()

        # Estado da determinação
        self.phase = "intro"  # "intro", "jogando", "final"
        # Índices dos jogadores ativos
        self.current_players = list(range(len(players_config)))
        self.rolls = {}  # {player_index: roll_value}
        self.dealer_index = None
        self.animation_timer = 0
        self.roll_animation = False
        self.round_number = 1  # Contador de rodadas
        self.show_results = False  # Mostrar resultados após animação

        # Animação de dados - todos os dados ao mesmo tempo
        self.dice_animations = {}  # {player_index: current_dice_value}
        self.final_rolls = {}  # {player_index: final_roll_value}

        # Configurar botões iniciais
        self.setup_buttons()

    def setup_buttons(self):
        """Configura os botões baseado nas dimensões atuais da tela."""
        # Botões com posicionamento proporcional
        button_y_primary = int(self.screen_height * 0.65)  # 65% da altura
        button_y_secondary = int(self.screen_height * 0.72)  # 72% da altura
        button_y_tertiary = int(self.screen_height * 0.79)  # 79% da altura
        # 85% da altura para botão voltar (mais seguro)
        button_y_back = int(self.screen_height * 0.85)

        self.buttons = {
            "start": pygame.Rect(self.screen_width // 2 - 100, button_y_primary, 200, BUTTON_HEIGHT),
            "roll": pygame.Rect(self.screen_width // 2 - 100, button_y_secondary, 200, BUTTON_HEIGHT),
            "continue": pygame.Rect(self.screen_width // 2 - 100, button_y_tertiary, 200, BUTTON_HEIGHT),
            "back": pygame.Rect(int(self.screen_width * 0.05), button_y_back, int(self.screen_width * 0.15), BUTTON_HEIGHT)
        }

    def update_dimensions(self, screen_width, screen_height):
        """Atualiza as dimensões da tela e reconfigura os botões."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.setup_buttons()

    def handle_event(self, event):
        """Processa eventos da tela."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()

                if self.buttons["back"].collidepoint(mouse_pos):
                    self.app.return_to_menu()
                elif self.phase == "intro" and self.buttons["start"].collidepoint(mouse_pos):
                    self.start_rolling()
                elif self.phase == "playing":
                    if not self.roll_animation and not self.show_results:
                        if self.buttons["roll"].collidepoint(mouse_pos):
                            self.roll_all_dice()
                    elif self.show_results:
                        if self.dealer_index is None:  # Empate
                            if self.buttons["roll"].collidepoint(mouse_pos):
                                self.start_next_round()
                        else:  # Temos vencedor
                            if self.buttons["continue"].collidepoint(
                                    mouse_pos):
                                self.start_game()

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                if self.phase == "intro":
                    self.start_rolling()
                elif self.phase == "playing":
                    if not self.roll_animation and not self.show_results:
                        self.roll_all_dice()
                    elif self.show_results:
                        if self.dealer_index is None:
                            self.start_next_round()
                        else:
                            self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.app.return_to_menu()

    def start_rolling(self):
        """Inicia a fase de rolagem dos dados."""
        self.phase = "playing"
        self.rolls.clear()
        self.dice_animations.clear()
        self.final_rolls.clear()
        self.show_results = False

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

                # Mostrar resultados e verificar vencedor automaticamente
                self.show_results = True
                self.check_results()

    def check_results(self):
        """Verifica os resultados e determina o vencedor."""
        max_roll = max(self.rolls.values())
        winners = [player_idx for player_idx,
                   roll in self.rolls.items() if roll == max_roll]

        if len(winners) == 1:
            # Temos um vencedor
            self.dealer_index = winners[0]
        else:
            # Empate - apenas marcar que precisamos de nova rodada
            self.dealer_index = None
            # Os jogadores perdedores são automaticamente eliminados na próxima
            # rodada

    def start_next_round(self):
        """Inicia nova rodada apenas com os jogadores empatados."""
        if self.dealer_index is None and self.rolls:
            # Encontrar jogadores empatados
            max_roll = max(self.rolls.values())
            self.current_players = [
                player_idx for player_idx,
                roll in self.rolls.items() if roll == max_roll]
            self.round_number += 1
            self.rolls.clear()
            self.dice_animations.clear()
            self.final_rolls.clear()
            self.show_results = False

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
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.1)))
        self.screen.blit(title_surface, title_rect)

        if self.phase == "intro":
            self.render_intro()
        elif self.phase == "playing":
            self.render_playing()

        # Renderizar botões
        self.render_buttons()

    def render_playing(self):
        """Renderiza a fase de jogo - dados e resultados na mesma tela."""
        # Título da rodada
        if self.round_number > 1:
            round_text = f"Rodada {self.round_number} - Desempate"
            tied_players = [self.players_config[idx]["name"]
                            for idx in self.current_players]
            subtitle = f"Entre: {', '.join(tied_players)}"
        else:
            round_text = "Todos os jogadores rolam seus dados"
            subtitle = "Quem tirar o maior número será o dealer"

        title_surface = self.font_medium.render(round_text, True, WHITE)
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.17)))
        self.screen.blit(title_surface, title_rect)

        subtitle_surface = self.font_small.render(subtitle, True, GRAY)
        subtitle_rect = subtitle_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.22)))
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Layout dos dados: centralizado em 2 fileiras
        dice_size = 60
        dice_spacing = 100

        # Calcular número de jogadores por fileira
        num_players = len(self.current_players)
        players_per_row = 3 if num_players > 3 else num_players
        row_1_players = players_per_row
        row_2_players = max(0, num_players - players_per_row)

        # Primeira fileira
        if row_1_players > 0:
            total_width_1 = (row_1_players * dice_spacing)
            start_x_1 = (self.screen_width - total_width_1) // 2 + \
                dice_spacing // 2
            y_1 = int(self.screen_height * 0.32)

            for i in range(row_1_players):
                player_idx = self.current_players[i]
                self.render_player_dice(
                    player_idx, start_x_1 + i * dice_spacing, y_1, dice_size)

        # Segunda fileira
        if row_2_players > 0:
            total_width_2 = (row_2_players * dice_spacing)
            start_x_2 = (self.screen_width - total_width_2) // 2 + \
                dice_spacing // 2
            y_2 = int(self.screen_height * 0.48)

            for i in range(row_2_players):
                player_idx = self.current_players[row_1_players + i]
                self.render_player_dice(
                    player_idx, start_x_2 + i * dice_spacing, y_2, dice_size)

        # Mostrar resultados se a animação terminou
        if self.show_results:
            self.render_results_overlay()

    def render_player_dice(self, player_idx, x, y, dice_size):
        """Renderiza um dado individual com nome do jogador."""
        config = self.players_config[player_idx]
        color_rgb = PLAYER_COLORS.get(config["color"], WHITE)

        # Posição central do dado
        dice_rect = pygame.Rect(
            x - dice_size // 2,
            y - dice_size // 2,
            dice_size,
            dice_size)

        # Cor do dado baseada no resultado (se houver)
        if self.show_results and player_idx in self.rolls:
            roll = self.rolls[player_idx]
            max_roll = max(self.rolls.values()) if self.rolls else 0

            if roll == max_roll:
                dice_color = YELLOW  # Vencedor em amarelo
                border_color = WHITE
                border_width = 4
            else:
                dice_color = DARK_GRAY  # Perdedor em cinza escuro
                border_color = GRAY
                border_width = 2
        else:
            dice_color = WHITE
            border_color = color_rgb
            border_width = 3

        # Desenhar dado
        pygame.draw.rect(self.screen, dice_color, dice_rect, border_radius=8)
        pygame.draw.rect(
            self.screen,
            border_color,
            dice_rect,
            border_width,
            border_radius=8)

        # Valor do dado
        if player_idx in self.dice_animations:
            dice_value = self.dice_animations[player_idx]
        else:
            dice_value = "?"

        # Texto do valor do dado
        dice_text = self.font_large.render(
            str(dice_value),
            True,
            BLACK if dice_color == WHITE or dice_color == YELLOW else WHITE)
        dice_text_rect = dice_text.get_rect(center=dice_rect.center)
        self.screen.blit(dice_text, dice_text_rect)

        # Nome do jogador abaixo do dado
        name_text = config["name"]
        if len(name_text) > 10:  # Truncar nome se muito longo
            name_text = name_text[:10] + "..."

        name_surface = self.font_small.render(name_text, True, color_rgb)
        name_rect = name_surface.get_rect(
            center=(dice_rect.centerx, dice_rect.bottom + 20))
        self.screen.blit(name_surface, name_rect)

    def render_results_overlay(self):
        """Renderiza os resultados sobreposto aos dados."""
        if not self.rolls:
            return

        # Fundo semi-transparente para o resultado - posição mais alta para não
        # sobrepor botão
        overlay_y = int(self.screen_height * 0.6)
        overlay_height = int(self.screen_height * 0.1)
        overlay_rect = pygame.Rect(
            0, overlay_y, self.screen_width, overlay_height)
        overlay_surface = pygame.Surface((self.screen_width, overlay_height))
        overlay_surface.set_alpha(180)
        overlay_surface.fill(BLACK)
        self.screen.blit(overlay_surface, overlay_rect)

        # Resultado
        max_roll = max(self.rolls.values())
        winners = [idx for idx, roll in self.rolls.items() if roll == max_roll]

        if len(winners) == 1:
            winner_config = self.players_config[winners[0]]
            result_text = f"🎉 {
                winner_config['name']} será o entregador de cartas! 🎉"
            result_color = PLAYER_COLORS.get(winner_config["color"], WHITE)
        else:
            winner_names = [self.players_config[idx]["name"]
                            for idx in winners]
            result_text = f"Empate entre: {', '.join(winner_names)}"
            result_color = WHITE

        result_surface = self.font_medium.render(
            result_text, True, result_color)
        result_rect = result_surface.get_rect(
            center=(
                self.screen_width // 2,
                overlay_y + overlay_height // 2))
        self.screen.blit(result_surface, result_rect)

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
            text_rect = text_surface.get_rect(
                center=(self.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 40

        # Lista de jogadores
        y += 20
        players_title = "Jogadores participantes:"
        title_surface = self.font_medium.render(players_title, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, y))
        self.screen.blit(title_surface, title_rect)
        y += 40

        for i, config in enumerate(self.players_config):
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)
            player_text = f"{config['name']} ({config['color']})"
            text_surface = self.font_small.render(player_text, True, color_rgb)
            text_rect = text_surface.get_rect(
                center=(self.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 25

    def render_rolling(self):
        """Renderiza a fase de rolagem com todos os dados simultaneamente."""
        # Título da rodada
        if self.round_number > 1:
            round_text = f"Rodada {self.round_number} - Desempate"
            tied_players = [self.players_config[idx]["name"]
                            for idx in self.current_players]
            subtitle = f"Entre: {', '.join(tied_players)}"
        else:
            round_text = "Todos os jogadores rolam seus dados"
            subtitle = "Quem tirar o maior número será o dealer"

        title_surface = self.font_medium.render(round_text, True, WHITE)
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.2)))
        self.screen.blit(title_surface, title_rect)

        subtitle_surface = self.font_small.render(subtitle, True, GRAY)
        subtitle_rect = subtitle_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.25)))
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
            second_row_width = min(3, remaining_players) * \
                dice_spacing_x - dice_spacing_x + dice_size
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
            name_rect = name_surface.get_rect(
                center=(dice_rect.centerx, dice_rect.bottom + 25))
            self.screen.blit(name_surface, name_rect)

    def render_results(self):
        """Renderiza os resultados da rolagem."""
        results_title = "Resultados da rodada:"
        title_surface = self.font_medium.render(results_title, True, WHITE)
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, int(self.screen_height * 0.18)))
        self.screen.blit(title_surface, title_rect)

        y = int(self.screen_height * 0.25)
        max_roll = max(self.rolls.values())

        for player_idx in self.current_players:
            roll = self.rolls[player_idx]
            config = self.players_config[player_idx]
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)

            # Destacar vencedor apenas com troféu, mas manter cor do jogador
            prefix = "🏆 " if roll == max_roll else "   "
            result_text = f"{prefix}{
                config['name']}: {roll} ({
                config['color'].title()})"

            # Todos os jogadores usam sua cor original
            text_surface = self.font_medium.render(
                result_text, True, color_rgb)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 35

    def render_tie(self):
        """Renderiza a tela de empate."""
        tie_title = "Empate!"
        title_surface = self.font_large.render(tie_title, True, RED)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surface, title_rect)

        explanation = "Os seguintes jogadores vão rolar novamente:"
        exp_surface = self.font_medium.render(explanation, True, WHITE)
        exp_rect = exp_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(exp_surface, exp_rect)

        y = 250
        for player_idx in self.current_players:
            config = self.players_config[player_idx]
            color_rgb = PLAYER_COLORS.get(config["color"], WHITE)
            player_text = f"• {config['name']} ({config['color']})"
            text_surface = self.font_medium.render(
                player_text, True, color_rgb)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 35

    def render_final(self):
        """Renderiza o resultado final."""
        if self.dealer_index is not None:
            dealer_config = self.players_config[self.dealer_index]
            color_rgb = PLAYER_COLORS.get(dealer_config["color"], WHITE)

            final_title = "Entregador de Cartas:"
            title_surface = self.font_large.render(final_title, True, WHITE)
            title_rect = title_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(title_surface, title_rect)

            dealer_text = f"🏆 {dealer_config['name']}"
            dealer_surface = self.font_large.render(dealer_text, True, YELLOW)
            dealer_rect = dealer_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 250))
            self.screen.blit(dealer_surface, dealer_rect)

            color_text = f"({dealer_config['color']})"
            color_surface = self.font_medium.render(
                color_text, True, color_rgb)
            color_rect = color_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 290))
            self.screen.blit(color_surface, color_rect)

    def render_buttons(self):
        """Renderiza os botões apropriados para cada fase."""
        visible_buttons = []

        if self.phase == "intro":
            visible_buttons = ["start", "back"]
        elif self.phase == "playing":
            if not self.roll_animation and not self.show_results:
                visible_buttons = ["roll", "back"]
            elif self.show_results:
                if self.dealer_index is None:  # Empate
                    visible_buttons = ["roll", "back"]
                else:  # Vencedor definido
                    visible_buttons = ["continue", "back"]
            else:  # Animando
                visible_buttons = ["back"]

        for button_name in visible_buttons:
            button_rect = self.buttons[button_name]

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
            if button_name == "start":
                button_text = "Começar"
            elif button_name == "roll":
                if self.show_results and self.dealer_index is None:
                    button_text = "Nova Rodada"
                else:
                    button_text = "Rolar Dados"
            elif button_name == "continue":
                button_text = "Iniciar Jogo"
            elif button_name == "back":
                button_text = "Voltar"

            text_surface = self.font_small.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
