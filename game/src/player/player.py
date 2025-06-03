from .player_image_info import PlayerImageInfo
from .movement_manager import MovementManager

class Player:
  def __init__(self, filename):
    self.pos_x = 40
    self.pos_y = 40
    self.movement_speed = 2
    self.player_img_info = PlayerImageInfo(filename, self.movement_speed)
    self.current_animation = filename
    self.last_direction = 'down'
    self.is_moving = False
    self.movement = MovementManager(self)

  def draw(self, screen, screen_x, screen_y, dt):
    # Get the current animation frame based on elapsed time (dt)
    frame = self.player_img_info.get_current_frame(dt)
    # Draw the current frame centered on the screen
    screen.blit(frame, (screen_y / 2 - self.player_img_info.scale_size_y / 2,
                        screen_x / 2 - self.player_img_info.scale_size_x / 2))

  def update_position(self, x, y):
    self.pos_x += x
    self.pos_y += y

  def set_animation(self, filename):
    # If the requested animation is already active, do nothing
    if self.current_animation == filename:
        return
    # Otherwise, update the current animation and reload frames
    self.current_animation = filename
    self.player_img_info = PlayerImageInfo(filename, self.movement_speed)
