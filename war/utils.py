import random

def roll_die():
    """Rolls a 6-sided die and returns the result."""
    return random.randint(1, 6)

def roll_multiple_dice(quantity):
    """Rolls several 6-sided dice and returns a list with the results."""
    return [roll_die() for _ in range(quantity)]

# Continent-related utilities
CONTINENT_BONUS = {
    'América do Sul': 2,
    'América do Norte': 5,
    'Europa': 5,
    'África': 3,
    'Ásia': 7,
    'Oceania': 2
}

def get_continent_bonus(continent_name):
    """Retorna o bônus de tropas por controlar um continente."""
    return CONTINENT_BONUS.get(continent_name, 1)

def player_owns_continent(player, continent_name, map_data):
    """Verifica se o player possui todos os territórios de um continente."""
    continent_territories = None
    for continent in map_data['continents']:
        if continent['name'] == continent_name:
            continent_territories = set(continent['territories'])
            break
    
    if not continent_territories:
        return False
    
    player_territory_names = {territory.name for territory in player.territories}
    return continent_territories.issubset(player_territory_names)

def get_continent_controller(continent_name, map_data, all_players):
    """Retorna o player que controla todo o continente, ou None se não houver."""
    for player in all_players:
        if player_owns_continent(player, continent_name, map_data):
            return player
    return None
