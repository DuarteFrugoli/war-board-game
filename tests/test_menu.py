#!/usr/bin/env python3
"""
Teste simples do menu principal sem inicializar jogo.
"""

import pygame
import sys
import traceback
from war.gui.screens.main_menu import MainMenu
from war.gui.utils.constants import *


def main():
    """Teste apenas do menu."""
    try:
        print("Inicializando pygame...")
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("War - Teste Menu")
        clock = pygame.time.Clock()
        
        print("Criando menu...")
        menu = MainMenu(screen, None)  # None como app temporariamente
        
        print("Entrando no loop principal...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        menu.handle_event(event)
            
            menu.update()
            menu.render()
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()
        print("Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()