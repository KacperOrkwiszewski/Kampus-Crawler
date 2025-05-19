from .player_image_info import PlayerImageInfo

class Player:
  def __init__(self, filename):
    self.player_img_info = PlayerImageInfo(filename)
    self.pos_x = 400
    self.pos_y = 400
    self.movement_speed = 0.05

  def draw(self, screen):
    screen.blit(self.player_img_info.player_image,
                (self.pos_x - self.player_img_info.scale_size_x / 2,
                self.pos_y - self.player_img_info.scale_size_y / 2))

  def update_position(self, x, y):
    self.pos_x += x
    self.pos_y += y