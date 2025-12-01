# test_utils_data.py
# Testes para funções de carregamento de dados JSON

import unittest
import json
from pathlib import Path
from war.utils_data import load_map_data, load_missions


class TestUtilsData(unittest.TestCase):
    """Testes para funções de carregamento de dados."""

    def test_load_map_data_returns_dict(self):
        """Testa se load_map_data retorna um dicionário."""
        data = load_map_data()
        self.assertIsInstance(data, dict)

    def test_load_map_data_has_required_keys(self):
        """Testa se o mapa contém as chaves obrigatórias."""
        data = load_map_data()
        self.assertIn('continents', data)
        self.assertIn('territories', data)

    def test_load_map_data_continents_structure(self):
        """Testa a estrutura dos continentes."""
        data = load_map_data()
        continents = data['continents']
        
        self.assertIsInstance(continents, list)
        self.assertGreater(len(continents), 0, "Deve ter pelo menos um continente")
        
        # Verifica estrutura do primeiro continente
        first_continent = continents[0]
        self.assertIn('name', first_continent)
        self.assertIn('territories', first_continent)
        self.assertIsInstance(first_continent['territories'], list)

    def test_load_map_data_territories_structure(self):
        """Testa a estrutura dos territórios."""
        data = load_map_data()
        territories = data['territories']
        
        self.assertIsInstance(territories, list)
        self.assertGreater(len(territories), 0, "Deve ter pelo menos um território")
        
        # Verifica estrutura do primeiro território
        first_territory = territories[0]
        self.assertIn('name', first_territory)
        self.assertIn('continent', first_territory)
        self.assertIn('borders', first_territory)
        self.assertIn('symbol', first_territory)
        
        # Verifica tipos
        self.assertIsInstance(first_territory['name'], str)
        self.assertIsInstance(first_territory['continent'], str)
        self.assertIsInstance(first_territory['borders'], list)
        self.assertIsInstance(first_territory['symbol'], str)

    def test_load_map_data_territory_count(self):
        """Testa se há a quantidade esperada de territórios (42 no WAR clássico)."""
        data = load_map_data()
        territories = data['territories']
        
        # WAR tem 42 territórios
        self.assertEqual(len(territories), 42, 
                        "Mapa deve ter 42 territórios (regra do WAR)")

    def test_load_map_data_continent_count(self):
        """Testa se há 6 continentes (regra do WAR)."""
        data = load_map_data()
        continents = data['continents']
        
        self.assertEqual(len(continents), 6, 
                        "Deve ter 6 continentes (América do Sul, América do Norte, Europa, África, Ásia, Oceania)")

    def test_load_map_data_borders_are_valid(self):
        """Testa se todas as fronteiras apontam para territórios existentes."""
        data = load_map_data()
        territories = data['territories']
        
        # Cria set com todos os nomes de territórios
        territory_names = {t['name'] for t in territories}
        
        # Verifica se todas as fronteiras são válidas
        for territory in territories:
            for border in territory['borders']:
                self.assertIn(border, territory_names, 
                             f"Fronteira '{border}' de '{territory['name']}' não existe")

    def test_load_map_data_symbols_are_valid(self):
        """Testa se os símbolos das cartas são válidos."""
        data = load_map_data()
        territories = data['territories']
        
        valid_symbols = {'quadrado', 'círculo', 'triângulo'}
        
        for territory in territories:
            symbol = territory['symbol']
            self.assertIn(symbol, valid_symbols, 
                         f"Símbolo '{symbol}' do território '{territory['name']}' é inválido")

    def test_load_missions_returns_list(self):
        """Testa se load_missions retorna uma lista."""
        missions = load_missions()
        self.assertIsInstance(missions, list)

    def test_load_missions_has_minimum_count(self):
        """Testa se há pelo menos 10 missões (mínimo para 6 jogadores)."""
        missions = load_missions()
        self.assertGreaterEqual(len(missions), 10, 
                               "Deve ter pelo menos 10 missões")

    def test_load_missions_structure(self):
        """Testa a estrutura das missões."""
        missions = load_missions()
        
        self.assertGreater(len(missions), 0, "Deve ter pelo menos uma missão")
        
        # Verifica estrutura da primeira missão
        first_mission = missions[0]
        self.assertIn('id', first_mission)
        self.assertIn('description', first_mission)
        
        # Verifica tipos
        self.assertIsInstance(first_mission['id'], int)
        self.assertIsInstance(first_mission['description'], str)

    def test_load_missions_unique_ids(self):
        """Testa se os IDs das missões são únicos."""
        missions = load_missions()
        
        ids = [m['id'] for m in missions]
        unique_ids = set(ids)
        
        self.assertEqual(len(ids), len(unique_ids), 
                        "IDs das missões devem ser únicos")

    def test_load_missions_descriptions_not_empty(self):
        """Testa se as descrições das missões não estão vazias."""
        missions = load_missions()
        
        for mission in missions:
            self.assertTrue(mission['description'].strip(), 
                           f"Missão {mission['id']} tem descrição vazia")

    def test_load_map_data_file_exists(self):
        """Testa se o arquivo map.json existe."""
        map_path = Path(__file__).parent.parent / 'data' / 'map.json'
        self.assertTrue(map_path.exists(), 
                       f"Arquivo {map_path} não encontrado")

    def test_load_missions_file_exists(self):
        """Testa se o arquivo missions.json existe."""
        missions_path = Path(__file__).parent.parent / 'data' / 'missions.json'
        self.assertTrue(missions_path.exists(), 
                       f"Arquivo {missions_path} não encontrado")

    def test_load_map_data_valid_json(self):
        """Testa se map.json é um JSON válido."""
        map_path = Path(__file__).parent.parent / 'data' / 'map.json'
        
        try:
            with open(map_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"map.json não é um JSON válido: {e}")

    def test_load_missions_valid_json(self):
        """Testa se missions.json é um JSON válido."""
        missions_path = Path(__file__).parent.parent / 'data' / 'missions.json'
        
        try:
            with open(missions_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"missions.json não é um JSON válido: {e}")


if __name__ == '__main__':
    unittest.main()
