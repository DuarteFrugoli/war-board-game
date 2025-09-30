class Player:
    def __init__(self, name, color, mission=None):
        self.name = name
        self.color = color  # String com nome da cor
        self.territories = []  # Lista de Territory
        self.cards = []  # Lista de Card
        self.mission = mission

    def receive_mission(self, mission):
        self.mission = mission

    def receive_card(self, card):
        self.cards.append(card)

    def receive_territory(self, territory):
        self.territories.append(territory)

    def get_territory_count(self):
        """Retorna quantos territórios o player possui."""
        return len(self.territories)

    def get_total_troops(self):
        """Retorna o total de tropas do player."""
        return sum(territory.troops for territory in self.territories)

    def owns_continent(self, continent_name, map_data):
        """Verifica se o player possui todos os territórios de um continente."""
        continent_territories = None
        for continent in map_data['continents']:
            if continent['name'] == continent_name:
                continent_territories = set(continent['territories'])
                break

        if not continent_territories:
            return False

        player_territory_names = {
            territory.name for territory in self.territories}
        return continent_territories.issubset(player_territory_names)

    def atacar(self, jogador, unidades):
        # ...lógica de ataque...
        pass

    def adicionarTropas(self, territory_name, unidades):
        """Adiciona tropas ao território especificado."""
        for territory in self.territories:
            if territory.name == territory_name:
                territory.troops += unidades
                return
        raise ValueError(
            f"Territory {territory_name} not owned by player {
                self.name}")

    def moverTropas(self, from_territory, to_territory, unidades):
        """Move tropas entre territórios do jogador."""
        # ...implementar lógica de movimento...
        pass

    def trocarCartasPorTropas(self, cartas):
        # ...troca cartas por tropas...
        pass
