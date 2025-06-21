import pytmx
import pygame


class GameMap:
    def __init__(self, filename):
        self.filename = filename
        self.tmx_data = pytmx.load_pygame(filename)

    def draw(self, screen, scale, map_offset_x, map_offset_y):
      screen_rect = screen.get_rect()
      for layer in self.tmx_data.visible_layers:
          if isinstance(layer, pytmx.TiledTileLayer):
              for x, y, gid in layer:
                  px = x * self.tmx_data.tilewidth * scale + map_offset_x
                  py = y * self.tmx_data.tileheight * scale + map_offset_y
                  tile_rect = pygame.Rect(px, py,
                                          self.tmx_data.tilewidth * scale,
                                          self.tmx_data.tileheight * scale)
                  if not screen_rect.colliderect(tile_rect):
                      continue # skip tiles which are out of the screen

                  tile = self.tmx_data.get_tile_image_by_gid(gid)
                  if tile:
                      scaled_tile = pygame.transform.scale(tile, (
                          self.tmx_data.tilewidth * scale,
                          self.tmx_data.tileheight * scale
                      ))
                      screen.blit(scaled_tile, (px, py))
