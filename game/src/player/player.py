from .player_image_info import PlayerImageInfo

class Player:
  def __init__(self, filename):
    self.pos_x = 400
    self.pos_y = 400
    self.movement_speed = 2
    self.player_img_info = PlayerImageInfo(filename, self.movement_speed)
    self.current_animation = filename
    self.last_direction = 'down'

  def draw(self, screen, screen_x, screen_y, dt, offset_x=0, offset_y=0):
    # Get the current animation frame based on elapsed time (dt)
    frame = self.player_img_info.get_current_frame(dt)
    # Draw the current frame centered on the screen
    screen.blit(frame, (screen_y / 2 - self.player_img_info.scale_size_y / 2 - offset_x,
                        screen_x / 2 - self.player_img_info.scale_size_x / 2 - offset_y))

  def update_position(self, x, y):
    self.pos_x += x
    self.pos_y += y

  def update_map_offset(self, map_offset_x, map_offset_y):
    self.map_offset_x = map_offset_x
    self.map_offset_y = map_offset_y

  def set_animation(self, filename):
    # If the requested animation is already active, do nothing
    if self.current_animation == filename:
        return
    # Otherwise, update the current animation and reload frames
    self.current_animation = filename
    self.player_img_info = PlayerImageInfo(filename, self.movement_speed)

