import pygame
from .player_state import PlayerState
from constants import Constants


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
            self.player.data.last_direction = 'down'
        if key == pygame.K_UP:
            self.playerUP_change = 0
            self.player.data.last_direction = 'up'
            self.ignore_vertical_movement = False
        if key == pygame.K_LEFT:
            self.playerLEFT_change = 0
            self.player.data.last_direction = 'left'
            self.ignore_horizontal_movement = False
        if key == pygame.K_RIGHT:
            self.playerRIGHT_change = 0
            self.player.data.last_direction = 'right'
            self.ignore_horizontal_movement = False

    def handle_down(self, key):
        if key == pygame.K_DOWN:
            self.playerDOWN_change = self.player.data.movement_speed
            self.ignore_horizontal_movement = True
            self.ignore_vertical_movement = False
        if key == pygame.K_UP:
            self.playerUP_change = self.player.data.movement_speed
            self.ignore_horizontal_movement = True
            self.ignore_vertical_movement = False
        if key == pygame.K_LEFT:
            self.playerLEFT_change = self.player.data.movement_speed
            self.ignore_vertical_movement = True
            self.ignore_horizontal_movement = False
        if key == pygame.K_RIGHT:
            self.playerRIGHT_change = self.player.data.movement_speed
            self.ignore_vertical_movement = True
            self.ignore_horizontal_movement = False

    def calculate_final_change(self):
        player_x_change = 0
        player_y_change = 0

        if not self.ignore_horizontal_movement:
            player_x_change = -self.playerRIGHT_change + self.playerLEFT_change
        if not self.ignore_vertical_movement:
            player_y_change = -self.playerDOWN_change + self.playerUP_change

        return player_x_change, player_y_change

    def get_movement_axis(self):
        x, y = self.calculate_final_change()
        if x == 0 and y != 0:
            return "vertical"
        elif x != 0 and y == 0:
            return "horizontal"

    def align_to_tiles(self, tile_size, map_scale):
        center_x = self.get_x_middle(map_scale, tile_size)
        center_y = self.get_y_middle(map_scale, tile_size)
        ms = self.player.data.movement_speed

        if self.is_moving:
            self.align_diagonal(center_x, center_y, ms)
        else:
            # go to the middle of the tile and set appropriate animations
            if self.player.data.pos_x != center_x:
                self.align_horizontal(center_x, ms)
            elif self.player.data.pos_y != center_y:
                self.align_vertical(center_y, ms)

            # if the player has reached the middle, set animation to idle of last direction
            if self.player.data.pos_x == center_x and self.player.data.pos_y == center_y:
                self.player.data.during_diagonal_alignment = False
                if self.player.data.last_direction == "down":
                    self.player.set_animation(PlayerState.IDLE_DOWN)
                elif self.player.data.last_direction == "up":
                    self.player.set_animation(PlayerState.IDLE_UP)
                elif self.player.data.last_direction == "left":
                    self.player.set_animation(PlayerState.IDLE_LEFT)
                elif self.player.data.last_direction == "right":
                    self.player.set_animation(PlayerState.IDLE_RIGHT)

    def get_y_middle(self, map_scale, tile_size):
        return self.player.data.pos_y - (self.player.data.pos_y % (tile_size * map_scale)) + (tile_size / 2 * map_scale)

    def get_x_middle(self, map_scale, tile_size):
        return self.player.data.pos_x - (self.player.data.pos_x % (tile_size * map_scale)) + (tile_size / 2 * map_scale)

    def align_vertical(self, center_y, ms):
        if center_y < self.player.data.pos_y:
            self.player.set_animation(PlayerState.MOVE_DOWN)
            self.player.data.last_direction = "down"
            self.player.update_position(0, -ms)
        else:
            self.player.set_animation(PlayerState.MOVE_UP)
            self.player.data.last_direction = "up"
            self.player.update_position(0, ms)

    def align_horizontal(self, center_x, ms):
        if center_x < self.player.data.pos_x:
            self.player.set_animation(PlayerState.MOVE_RIGHT)
            self.player.data.last_direction = "right"
            self.player.update_position(-ms, 0)
        else:
            self.player.set_animation(PlayerState.MOVE_LEFT)
            self.player.data.last_direction = "left"
            self.player.update_position(ms, 0)

    def align_diagonal(self, center_x, center_y, ms):
        axis = self.get_movement_axis()
        self.player.data.during_diagonal_alignment = False

        # Align to horizontal when moving vertically
        if axis == "vertical":
            diff_x = center_x - self.player.data.pos_x
            if diff_x != 0:  # if the difference is 0
                self.player.data.during_diagonal_alignment = True
                # (self.playerDOWN_change - self.playerUP_change) counteracts vertical change
                self.player.update_position(ms if diff_x > 0 else -ms, (self.playerDOWN_change - self.playerUP_change))
                self.player.set_animation(PlayerState.MOVE_LEFT) if diff_x > 0 else self.player.set_animation(
                  PlayerState.MOVE_RIGHT)

        # Align to vertical when moving horizontally
        elif axis == "horizontal":
            diff_y = center_y - self.player.data.pos_y
            if diff_y != 0:  # if the difference is 0
                self.player.data.during_diagonal_alignment = True
                # (-self.playerLEFT_change +self.playerRIGHT_change) counteracts horizontal change
                self.player.update_position((-self.playerLEFT_change + self.playerRIGHT_change),
                                            ms if diff_y > 0 else -ms)
                self.player.set_animation(PlayerState.MOVE_UP) if diff_y > 0 else self.player.set_animation(
                  PlayerState.MOVE_DOWN)

    # final movement function combining all functionalities
    def move_player(self):
        x_change, y_change = self.player.movement.calculate_final_change()
        # check if player is currently moving
        self.player.movement.is_moving = not (x_change == 0 and y_change == 0)
        # try to align the player to the middle of a tile
        self.player.update_position(x_change, y_change)
        self.player.movement.align_to_tiles(Constants.TILE_HEIGHT, Constants.MAP_SCALE)
        # Change animation according to movement
        if not self.player.data.during_diagonal_alignment:
            if x_change < 0:
                self.player.set_animation(PlayerState.MOVE_RIGHT)
            elif x_change > 0:
                self.player.set_animation(PlayerState.MOVE_LEFT)
            elif y_change < 0:
                self.player.set_animation(PlayerState.MOVE_DOWN)
            elif y_change > 0:
                self.player.set_animation(PlayerState.MOVE_UP)