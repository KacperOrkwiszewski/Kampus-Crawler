from .player_image_info import PlayerImageInfo
#from ..constants import Constants

class Player:
  def __init__(self, filename):
    self.pos_x = 400
    self.pos_y = 400
    self.movement_speed = 2
    self.player_img_info = PlayerImageInfo(filename, self.movement_speed)
    self.current_animation = filename
    self.last_direction = 'down'
    self.is_moving = False

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

  def align_to_tiles(self):
    if not self.is_moving:
        finalx = self.pos_x
        finaly = self.pos_y

        #finalx -= self.pos_x % (Constants.TILE_WIDTH * Constants.MAP_SCALE) - (Constants.TILE_WIDTH / 2 * Constants.MAP_SCALE)
        #finaly -= self.pos_y % (Constants.TILE_WIDTH * Constants.MAP_SCALE) - (Constants.TILE_WIDTH / 2 * Constants.MAP_SCALE)

        finalx -= self.pos_x % (16 * 5) - 40
        finaly -= self.pos_y % (16 * 5) - 40

        if self.pos_x != finalx:
          if finalx < self.pos_x:
            self.update_position(-self.movement_speed, 0)
          else:
            self.update_position(self.movement_speed, 0)
        if self.pos_y != finaly:
          if finaly < self.pos_y:
           self.update_position(0, -self.movement_speed)
          else:
            self.update_position(0, self.movement_speed)
