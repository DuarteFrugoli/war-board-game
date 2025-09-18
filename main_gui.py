#!/usr/bin/env python3
"""
Arquivo principal para execução do jogo War com interface gráfica Pygame.
"""

import sys
import traceback
from war.gui.game_app import GameApp


def main():
    """Ponto de entrada principal do jogo."""
    try:
        print("Iniciando aplicação...")
        app = GameApp()
        print("Aplicação criada, iniciando loop...")
        app.run()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        print("Traceback completo:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()