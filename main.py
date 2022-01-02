import pygame
import pytmx
from classes import *

tile_w, tile_h = 40, 40
board_w, board_h = 25, 20
size = w, h = tile_w * board_w, tile_h * board_h

FPS = 15


# map = pytmx.load_pygame(f"{MAPS_DIR}/")
def main():
    pygame.init()
    game_screen = pygame.display.set_mode(size)
    pygame.display.set_caption('A little farm')
    fild = Fild("final_fild.tmx")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fild.render(game_screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()