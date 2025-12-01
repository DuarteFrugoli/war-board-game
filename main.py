from war.player import Player
from war.utils import roll_die
from war.enums import COLORS
from war.game import Game
from war.interface import get_number_of_players, create_players, determine_card_dealer


if __name__ == "__main__":
    print("Bem-vindo ao War!")
    num_players = get_number_of_players()
    players = create_players(num_players, COLORS, Player)
    dealer = determine_card_dealer(players, roll_die)
    game = Game(players, dealer)
    print(f"\nJogo configurado com {len(players)} jogadores:")
    for player in players:
        status = " (Entregador)" if player == dealer else ""
        print(f"- {player.name} ({player.color}){status}")
        print(f"  Missão: {player.mission['description']}")
        print(f"  Territórios: {[t.name for t in player.territories]}")
    first_player = game.get_first_player_after_dealer()
    print(f"\nO jogo pode começar! O primeiro turno é de {first_player.name} ({first_player.color})")
