import pygame
import pytmx
import sys
import os

COUNT_SHIP = 1
tile_w, tile_h = 40, 40
board_w, board_h = 25, 20
size = w, h = tile_w * board_w, tile_h * board_h
pygame.init()
game_screen = pygame.display.set_mode(size)
pygame.display.set_caption('A little farm')
MAPS_DIR = "map"
PIC_DIR = "pictures"
cell_size = 40

animals = pygame.sprite.Group()
ships = pygame.sprite.Group()
wolfs = pygame.sprite.Group()
dogs = pygame.sprite.Group()
cowboys = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join(PIC_DIR, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Fild:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}", )
        self.h = self.map.height
        self.w = self.map.width
        self.tile_size = self.map.tilewidth

    def render(self, screen):
        ti = self.map.get_tile_image_by_gid
        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        screen.blit(tile, (x*self.tile_size, y*self.tile_size))


class It(pygame.sprite.Sprite):

    def __init__(self, x, y, image_name, *group,  hp=1, count=1):
        super().__init__(*group)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x*cell_size
        self.rect.y = y*cell_size
        self.hp = hp
        self.count = count

    def update(self, event, move=cell_size):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect = self.rect.move(-move, 0)
            elif event.key == pygame.K_RIGHT:
                self.rect = self.rect.move(move, 0)
            elif event.key == pygame.K_UP:
                self.rect = self.rect.move(0, -move)
            elif event.key == pygame.K_DOWN:
                self.rect = self.rect.move(0, move)


class Ship(It):
    def __init__(self, x, y, *group, image_name="ship.png"):
        super().__init__(x, y, image_name, *group)
        self.type = "s"
        self.add(animals)


class Wolf(It):
    def __init__(self, x, y, *group, image_name="wolf.png"):
        super().__init__(x, y, image_name, *group)
        self.type = "w"
        self.add(animals)


class Dog(It):
    def __init__(self, x, y, *group, image_name="dog.png"):
        super().__init__(x, y, image_name, *group, count=2)
        self.type = "d"
        self.add(animals)

    def move(self, x, y, x_ch, y_ch):
        with open("saved_map.txt", "r", encoding="utf-8") as file:
            f = file.readlines()
        if self.count > 0 and f[y][x] == "f":
            with open("heroes.txt", 'r', encoding="utf-8") as file:
                f = file.readlines()
            f[y] = f[y][:x] + "d" + f[y][x + 1:]
            f[y_ch] = f[y_ch][:x_ch] + "n" + f[y_ch][x_ch + 1:]
            with open("heroes.txt", 'w', encoding="utf-8") as file:
                for i in f:
                    file.write(i)
            self.rect.x = x * cell_size
            self.rect.y = y * cell_size
            self.count -= 1


class Cowboy(It):
    def __init__(self, x, y, *group, image_name="cowboy.png"):
        super().__init__(x, y, image_name, *group, count=3)
        self.type = "c"


    def move(self, x, y, x_ch, y_ch):
        with open("saved_map.txt", "r", encoding="utf-8") as file:
            f = file.readlines()
        if self.count > 0 and f[y][x] == "f":
            with open("heroes.txt", 'r', encoding="utf-8") as file:
                f = file.readlines()
            f[y] = f[y][:x] + "c" + f[y][x+1:]
            f[y_ch] = f[y_ch][:x_ch] + "n" + f[y_ch][x_ch+1:]
            with open("heroes.txt", 'w', encoding="utf-8") as file:
                for i in f:
                    file.write(i)
            self.rect.x = x * cell_size
            self.rect.y = y * cell_size
            self.count -= 1


class Fild:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}", )
        self.h = self.map.height
        self.w = self.map.width
        self.tile_size = self.map.tilewidth

    def render(self, screen):
        ti = self.map.get_tile_image_by_gid
        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        screen.blit(tile, (x*self.tile_size, y*self.tile_size))
