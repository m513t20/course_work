import pygame
import time
import sys

from Config import WIDTH, HEIGHT, FPS
from Network import NetworkManager
from Render import Renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Client")
    clock = pygame.time.Clock()

    network = NetworkManager()
    renderer = Renderer(screen)
    
    state = network.get_start_state(False)
    last_tyme_sync = time.time()

    running = True
    while running:
        current_time = time.time()

        if state:
            if current_time - last_tyme_sync > 1.0:
                state = network.get_board_state()
                last_tyme_sync = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        renderer.draw_board(state)
        pygame.display.flip()
        
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()