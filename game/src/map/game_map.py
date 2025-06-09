import pytmx
import pygame
from constants import Constants

class GameMap:

  def __init__(self, filename):
    self.filename = filename
    self.tmx_data = pytmx.load_pygame(filename)

  def draw(self, screen, scale, map_offset_x, map_offset_y):
          for layer in self.tmx_data.visible_layers:
              if isinstance(layer, pytmx.TiledTileLayer):
                  for x, y, gid in layer:
                      tile = self.tmx_data.get_tile_image_by_gid(gid)
                      if tile:
                          # Skaluj kafelek
                          scaled_tile = pygame.transform.scale(tile, (
                              self.tmx_data.tilewidth * scale,
                              self.tmx_data.tileheight * scale
                          ))
                          screen.blit(scaled_tile, (
                              x * self.tmx_data.tilewidth * scale + map_offset_x,
                              y * self.tmx_data.tileheight * scale + map_offset_y
                          ))