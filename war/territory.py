# territory.py
class Territory:
	def __init__(self, name, continent):
		self.name = name
		self.continent = continent
		self.owner = None  # Player que possui o território
		self.troops = 0

	def __repr__(self):
		return f"<Territory {self.name} ({self.continent})>"
