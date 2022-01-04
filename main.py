import pygame
import pytmx
import os
import sys
from classes import *


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, 'n'), level_map))



tile_w, tile_h = 40, 40
board_w, board_h = 25, 20
size = w, h = tile_w * board_w, tile_h * board_h
pygame.init()
game_screen = pygame.display.set_mode(size)
pygame.display.set_caption('A little farm')


MAPS_DIR = "map"
PIC_DIR = "pictures"
cell_size = 40


def main():
    fild = Fild("final_fild.tmx")
    clock = pygame.time.Clock()
    running = True
    fps = 30
    # ship = Ship(6, 17, ships)
    # wolf = Wolf(3, 3, wolfs)
    # dog = Dog(15, 15, dogs)
    # cowboy = Cowboy(6, 6, cowboys)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fild.render(game_screen)
        animals_map = load_level("heroes.txt")
        for i in range(len(animals_map)):
            for j in range(len(animals_map[i])):
                if animals_map[i][j] == "s":
                    Ship(j, i, ships)
                elif animals_map[i][j] == "w":
                    Wolf(j, i, wolfs)
                elif animals_map[i][j] == "d":
                    Dog(j, i, dogs)
                elif animals_map[i][j] == "c":
                    Cowboy(j, i, cowboys)
        animals.draw(game_screen)
        cowboys.draw(game_screen)
        animals.update(event)
        cowboys.update(event)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()