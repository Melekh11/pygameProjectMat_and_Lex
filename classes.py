import pygame
import pytmx

MAPS_DIR = "map"

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

    # def make_map(self):
    #     surface = pygame.Surface((self.w, self.h))
    #     self.render(surface)
    #     return surface