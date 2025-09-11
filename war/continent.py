# continent.py
class Continent:
	def __init__(self, name, territories):
		self.name = name
		self.territories = territories  # Lista de nomes dos territórios

	def __repr__(self):
		return f"<Continent {self.name}>"
