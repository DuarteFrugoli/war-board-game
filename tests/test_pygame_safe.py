#!/usr/bin/env python3
"""
Teste com pygame mais defensivo.
"""

import pygame
import sys
import traceback
from war.gui.utils.constants import *


def safe_event_get():
    """Versão segura do pygame.event.get()"""
    try:
        return pygame.event.get()
    except Exception as e:
        print(f"Erro ao obter eventos: {e}")
        return []


def main():
    """Teste defensivo do pygame."""
    try:
        print("Inicializando pygame...")
        pygame.init()
        
        # Forçar inicialização de todos os módulos
        pygame.font.init()
        pygame.mixer.init()
        
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("War - Teste Defensivo")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)
        
        print("Entrando no loop principal...")
        running = True
        frame_count = 0
        
        while running and frame_count < 300:  # Limitar frames para teste
            # Usar versão segura dos eventos
            events = safe_event_get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Renderizar
            screen.fill((50, 50, 100))
            
            # Texto de teste
            text = font.render(f"Frame: {frame_count}", True, WHITE)
            screen.blit(text, (10, 10))
            
            text2 = font.render("Pressione ESC para sair", True, WHITE)
            screen.blit(text2, (10, 50))
            
            pygame.display.flip()
            clock.tick(60)
            frame_count += 1
        
        pygame.quit()
        print("Teste concluído!")
        
    except Exception as e:
        print(f"Erro: {e}")
        traceback.print_exc()
        if pygame.get_init():
            pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()