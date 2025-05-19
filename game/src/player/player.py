from .player_image_info import PlayerImageInfo

class Player:
  def __init__(self, filename):
    self.player_img_info = PlayerImageInfo(filename)
    self.pos_x = 400
    self.pos_y = 400
    self.movement_speed = 2

  def draw(self, screen, screen_x, screen_y):
    screen.blit(self.player_img_info.player_image, (screen_y / 2 - self.player_img_info.scale_size_y / 2, screen_x / 2 - self.player_img_info.scale_size_x / 2))

  def update_position(self, x, y):
    self.pos_x += x
    self.pos_y += y