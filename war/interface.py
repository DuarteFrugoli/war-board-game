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

def create_players(num_players, colors, Player):
    """Cria os jogadores com nome e cor."""
    players = []
    available_colors = colors.copy()  # Copia a lista de cores
    for i in range(num_players):
        print(f"\nJogador {i + 1}:")
        name = input("Digite o nome: ")
        print("Cores disponíveis:")
        for idx, color in enumerate(available_colors, 1):
            print(f"{idx} - {color}")
        while True:
            try:
                color_choice = int(input("Escolha o número da cor: "))
                if 1 <= color_choice <= len(available_colors):
                    selected_color = available_colors[color_choice - 1]
                    available_colors.remove(selected_color)
                    break
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")
        players.append(Player(name, selected_color))
    return players

def determine_card_dealer(players, roll_die):
    """Determina quem será o entregador de cartas através de dados."""
    print("\n--- Determinando o entregador de cartas ---")
    while True:
        results = []
        for player in players:
            roll = roll_die()
            results.append((player, roll))
            print(f"{player.name} ({player.color}) rolou: {roll}")
        max_roll = max(results, key=lambda x: x[1])[1]
        winners = [result for result in results if result[1] == max_roll]
        if len(winners) == 1:
            dealer = winners[0][0]
            print(f"\n{dealer.name} ({dealer.color}) será o entregador de cartas!")
            return dealer
        print(f"\nEmpate com {max_roll}! Os seguintes jogadores vão rolar novamente:")
        players = [winner[0] for winner in winners]
        for player in players:
            print(f"- {player.name} ({player.color})")
        print()
