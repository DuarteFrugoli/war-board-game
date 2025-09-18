import pygame
import sys

def test_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Teste Pygame")
    clock = pygame.time.Clock()
    
    print("Pygame inicializado com sucesso")
    
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
        except Exception as e:
            print(f"Erro no loop de eventos: {e}")
            running = False
        
        screen.fill((50, 50, 50))
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("Teste concluído")

if __name__ == "__main__":
    test_pygame()