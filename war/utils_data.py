import json
from pathlib import Path


def load_map_data():
    with open(Path(__file__).parent.parent / 'data' / 'map.json', encoding='utf-8') as f:
        return json.load(f)


def load_missions():
    with open(Path(__file__).parent.parent / 'data' / 'missions.json', encoding='utf-8') as f:
        return json.load(f)
