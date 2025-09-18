#!/usr/bin/env python3
"""
War - Interface Gráfica
=======================

Jogo de tabuleiro War com interface gráfica usando Pygame.

Para jogar:
1. Execute: python run_gui.py
2. Use as setas ou mouse para navegar
3. Configure os jogadores com nomes e cores
4. Assista à seleção do dealer
5. Jogue!
"""

from war.gui.game_app import GameApp

def main():
    """Função principal para executar o jogo."""
    print("=" * 50)
    print("WAR - JOGO DE TABULEIRO")
    print("=" * 50)
    print("Iniciando interface gráfica...")
    print()
    
    try:
        app = GameApp()
        app.run()
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Verifique se todas as dependências estão instaladas.")

if __name__ == "__main__":
    main()