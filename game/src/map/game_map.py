import pygame
import pytmx

from constants import Constants

class GameMap:
    def __init__(self, filename, scale=1.0):
        self.filename = filename
        self.tmx_data = pytmx.load_pygame(filename)
        self.scale = scale
        self.tile_width = 80
        self.tile_height = 80
        self.map_surface = self._render_map()
        self.collision_rects = self._generate_collision_rects("buildings_1")

    def _render_map(self):
        map_width = self.tmx_data.width * self.tile_width
        map_height = self.tmx_data.height * self.tile_height

        surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tile_width, self.tile_height))
                        px = x * self.tile_width
                        py = y * self.tile_height
                        surface.blit(tile, (px, py))

        return surface

    def _generate_collision_rects(self, target_layer_name):
          collision_rects = []

          def find_layers(layers):
              for layer in layers:
                  if isinstance(layer, pytmx.TiledTileLayer) and layer.name == target_layer_name:
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
        screen.blit(self.map_surface, (offset_x, offset_y))
