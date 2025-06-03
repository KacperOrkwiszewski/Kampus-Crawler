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

  def align_to_tiles(self, tile_size, map_scale):
    if self.is_moving:
        return

    # store current position in local variables
    finalx = self.player.pos_x
    finaly = self.player.pos_y

    # perform operations to calculate the middle of a tile
    finalx -= self.player.pos_x % (tile_size * map_scale) - (tile_size / 2 * map_scale)
    finaly -= self.player.pos_y % (tile_size * map_scale) - (tile_size / 2 * map_scale)

    # update position if player didn't reach the middle
    if self.player.pos_x != finalx:
      self.player.update_position(-self.player.movement_speed if finalx < self.player.pos_x else self.player.movement_speed, 0)
    if self.player.pos_y != finaly:
      self.player.update_position(0, -self.player.movement_speed if finaly < self.player.pos_y else self.player.movement_speed)