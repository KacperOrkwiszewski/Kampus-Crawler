import pygame

class MovementManager:
  def __init__(self, player):
    self.is_moving = False
    self.playerUP_change = 0
    self.playerDOWN_change = 0
    self.playerLEFT_change = 0
    self.playerRIGHT_change = 0
    self.ignore_horizontal_movement = False
    self.ignore_vertical_movement = False
    self.player = player

  def handle_up(self, key):
    if key == pygame.K_DOWN:
      self.playerDOWN_change = 0
      self.ignore_vertical_movement = False
      self.player.last_direction = 'down'
    if key == pygame.K_UP:
      self.playerUP_change = 0
      self.player.last_direction = 'up'
      self.ignore_vertical_movement = False
    if key == pygame.K_LEFT:
      self.playerLEFT_change = 0
      self.player.last_direction = 'left'
      self.ignore_horizontal_movement = False
    if key == pygame.K_RIGHT:
      self.playerRIGHT_change = 0
      self.player.last_direction = 'right'
      self.ignore_horizontal_movement = False

  def handle_down(self, key):
    if key == pygame.K_DOWN:
      self.playerDOWN_change = self.player.movement_speed
      self.ignore_horizontal_movement = True
      self.ignore_vertical_movement = False
    if key == pygame.K_UP:
      self.playerUP_change = self.player.movement_speed
      self.ignore_horizontal_movement = True
      self.ignore_vertical_movement = False
    if key == pygame.K_LEFT:
      self.playerLEFT_change = self.player.movement_speed
      self.ignore_vertical_movement = True
      self.ignore_horizontal_movement = False
    if key == pygame.K_RIGHT:
      self.playerRIGHT_change = self.player.movement_speed
      self.ignore_vertical_movement = True
      self.ignore_horizontal_movement = False

  def calculate_final_change(self):
    playerX_change = 0
    playerY_change = 0

    if not self.ignore_horizontal_movement:
      playerX_change = -self.playerRIGHT_change + self.playerLEFT_change

    if not self.ignore_vertical_movement:
      playerY_change = -self.playerDOWN_change + self.playerUP_change

    return playerX_change, playerY_change

  def get_movement_axis(self):
    x, y = self.calculate_final_change()
    if x == 0 and y != 0:
      return "vertical"
    elif x != 0 and y == 0:
      return "horizontal"

  def align_to_tiles(self, tile_size, map_scale):

    center_x = self.player.pos_x - (self.player.pos_x % (tile_size * map_scale)) + (tile_size / 2 * map_scale)
    center_y = self.player.pos_y - (self.player.pos_y % (tile_size * map_scale)) + (tile_size / 2 * map_scale)
    ms = self.player.movement_speed

    if self.is_moving:

      axis = self.get_movement_axis()

      self.player.during_diagonal_alignment = False
      # Align to horizontal when moving vertically
      if axis == "vertical":
        diff_x = center_x - self.player.pos_x
        if diff_x != 0:  # if the difference is 0
          self.player.during_diagonal_alignment = True
          # (self.playerDOWN_change - self.playerUP_change) counteracts vertical change so the player never moves diagonally
          self.player.update_position(ms if diff_x > 0 else -ms, (self.playerDOWN_change - self.playerUP_change))
          self.player.set_animation("left.gif") if diff_x > 0 else self.player.set_animation("right.gif")

      # Align to vertical when moving horizontally
      elif axis == "horizontal":
        diff_y = center_y - self.player.pos_y
        if diff_y != 0:  # if the difference is 0
          self.player.during_diagonal_alignment = True
          # (-self.playerLEFT_change +self.playerRIGHT_change) counteracts vertical change so the player never moves diagonally
          self.player.update_position((-self.playerLEFT_change + self.playerRIGHT_change),
                                      ms if diff_y > 0 else -ms)
          self.player.set_animation("up.gif") if diff_y > 0 else self.player.set_animation("down.gif")
    else:
      # go to the middle of the tile and set appropriate animations
      if self.player.pos_x != center_x:
        if center_x < self.player.pos_x:
            self.player.set_animation("right.gif")
            self.player.last_direction = "right"
            self.player.update_position(-ms, 0)
        else:
            self.player.set_animation("left.gif")
            self.player.last_direction = "left"
            self.player.update_position(ms, 0)

      elif self.player.pos_y != center_y:
        if center_y < self.player.pos_y:
            self.player.set_animation("down.gif")
            self.player.last_direction = "down"
            self.player.update_position(0, -ms)
        else:
            self.player.set_animation("up.gif")
            self.player.last_direction = "up"
            self.player.update_position(0, ms)

      # if the player reached the middle, set animation to idle of last direction
      if self.player.pos_x == center_x and self.player.pos_y == center_y:
        self.player.during_diagonal_alignment = False
        self.player.set_animation(f"idle_{self.player.last_direction}.gif")