# territory.py
class Territory:
	def __init__(self, name, continent, borders=None):
		self.name = name
		self.continent = continent
		self.owner = None  # Player que possui o território
		self.troops = 0
		self.borders = borders or []  # Lista de territórios vizinhos

	def __repr__(self):
		return f"<Territory {self.name} ({self.continent})>"

	def is_border_with(self, territory_name):
		"""Verifica se este território faz fronteira com outro."""
		return territory_name in self.borders
