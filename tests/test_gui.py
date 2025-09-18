#!/usr/bin/env python3
"""Script para testar a interface gráfica do War."""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo war
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from war.gui.game_app import GameApp

def main():
    """Testa a interface gráfica."""
    try:
        print("Iniciando interface gráfica...")
        app = GameApp()
        app.run()
    except Exception as e:
        print(f"Erro na interface gráfica: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()