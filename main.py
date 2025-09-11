# main.py
# Ponto de entrada do jogo War


from war.player import Player
from war.utils import roll_die
from war.enums import Color
from war.game import setup_game, get_first_player_after_dealer


def get_number_of_players():
    """Solicita ao usuário o número de jogadores (3-6)."""
    while True:
        try:
            num_players = int(input("Quantos jogadores (3-6)? "))
            if 3 <= num_players <= 6:
                return num_players
            else:
                print("Número de jogadores deve ser entre 3 e 6.")
        except ValueError:
            print("Por favor, digite um número válido.")


def create_players(num_players):
    """Cria os jogadores com nome e cor."""
    players = []
    available_colors = list(Color)[:6]  # Pega as 6 cores disponíveis
    for i in range(num_players):
        print(f"\nJogador {i + 1}:")
        name = input("Digite o nome: ")
        print("Cores disponíveis:")
        for color in available_colors:
            print(f"{color.value} - {color}")
        while True:
            try:
                color_choice = int(input("Escolha o número da cor: "))
                selected_color = next((c for c in available_colors if c.value == color_choice), None)
                if selected_color:
                    available_colors.remove(selected_color)
                    break
                else:
                    print("Número inválido ou cor já escolhida. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")
        players.append(Player(name, selected_color))
    return players


def determine_card_dealer(players):
    """Determina quem será o entregador de cartas através de dados."""
    print("\n--- Determinando o entregador de cartas ---")
    
    while True:
        # Todos os jogadores rolam dados
        results = []
        for player in players:
            roll = roll_die()
            results.append((player, roll))
            print(f"{player.name} ({player.color}) rolou: {roll}")
        
        # Encontra o maior resultado
        max_roll = max(results, key=lambda x: x[1])[1]
        winners = [result for result in results if result[1] == max_roll]
        
        # Se há apenas um vencedor, ele é o entregador
        if len(winners) == 1:
            dealer = winners[0][0]
            print(f"\n{dealer.name} ({dealer.color}) será o entregador de cartas!")
            return dealer
        
        # Se há empate, apenas os empatados rolam novamente
        print(f"\nEmpate com {max_roll}! Os seguintes jogadores vão rolar novamente:")
        players = [winner[0] for winner in winners]
        for player in players:
            print(f"- {player.name} ({player.color})")
        print()


if __name__ == "__main__":
    print("Bem-vindo ao War!")
    num_players = get_number_of_players()
    players = create_players(num_players)
    dealer = determine_card_dealer(players)
    territories, continents, cards = setup_game(players, dealer)
    print(f"\nJogo configurado com {len(players)} jogadores:")
    for player in players:
        status = " (Entregador)" if player == dealer else ""
        print(f"- {player.name} ({player.color}){status}")
        print(f"  Missão: {player.mission['description']}")
        print(f"  Territórios: {[t.name for t in player.territories]}")
    first_player = get_first_player_after_dealer(players, dealer)
    print(f"\nO jogo pode começar! O primeiro turno é de {first_player.name} ({first_player.color})")
