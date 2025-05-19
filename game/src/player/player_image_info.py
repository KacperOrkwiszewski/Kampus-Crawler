import pygame

class PlayerImageInfo:

  def __init__(self, filename):
    self.filename = filename

    self.scale_size_x = 80
    self.scale_size_y = 80

    self.player_image = pygame.image.load(filename)
    self.player_image = pygame.transform.scale(self.player_image, (self.scale_size_x, self.scale_size_y))