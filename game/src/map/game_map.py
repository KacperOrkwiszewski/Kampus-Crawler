import pygame
import pytmx

from constants import Constants

class GameMap:
    def __init__(self, filename, scale=1.0):
        self.filename = filename
        self.tmx_data = pytmx.load_pygame(filename)
        self.scale = scale
        self.tile_width = Constants.TILE_WIDTH * Constants.MAP_SCALE
        self.tile_height = Constants.TILE_HEIGHT * Constants.MAP_SCALE
        self.collision_rects = self._generate_collision_rects(["buildings_1", "objects", "borders"])

        self.map_as_image = pygame.image.load("assets/map_data/map_all.png").convert()

    def _generate_collision_rects(self, target_layer_names):
          collision_rects = []

          def find_layers(layers):
              for layer in layers:
                  if isinstance(layer, pytmx.TiledTileLayer) and (layer.name in target_layer_names):
                      for x, y, gid in layer:
                          if gid != 0:
                              rect = pygame.Rect(
                                  -x * self.tile_width + Constants.MAP_ORIGIN_X,
                                  -y * self.tile_height + Constants.MAP_ORIGIN_Y,
                                  self.tile_width,
                                  self.tile_height
                              )
                              collision_rects.append(rect)
                  elif hasattr(layer, "layers"):
                      find_layers(layer.layers)

          find_layers(self.tmx_data.layers)
          return collision_rects

    def get_collision_rects(self):
        return self.collision_rects

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.map_as_image, (offset_x, offset_y))