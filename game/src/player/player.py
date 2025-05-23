from .player_image_info import PlayerImageInfo
import pygame

class Player:
    def __init__(self, filename, start_pos):
        self.pos = start_pos  # start at the middle of a tile
        self.target_pos = start_pos
        self.movement_speed = 100
        self.player_img_info = PlayerImageInfo(filename, self.movement_speed)
        self.current_animation = filename
        self.last_direction = 'down'
        self.is_moving = False

    def draw(self, screen, screen_x, screen_y, dt):
        frame = self.player_img_info.get_current_frame(dt)
        draw_x = screen_y / 2 - self.player_img_info.scale_size_y / 2
        draw_y = screen_x / 2 - self.player_img_info.scale_size_x / 2
        screen.blit(frame, (draw_x, draw_y))

    def update_position(self, dt):
        if self.is_moving:
            direction = self.target_pos - self.pos
            distance = self.movement_speed * dt
            if direction.length() <= distance:
                self.pos_x, self.pos.y = self.target_pos.x, self.target_pos.y
                self.is_moving = False
            else:
                direction = direction.normalize() * distance
                self.pos.x += direction.x
                self.pos.y += direction.y

    def set_animation(self, filename):
        if self.current_animation == filename:
            return
        self.current_animation = filename
        self.player_img_info = PlayerImageInfo(filename, self.movement_speed)

    def move_to_offset(self, dx, dy, tile_size_x, tile_size_y):
        if not self.is_moving:
            current_tile_x = int(self.pos.x // tile_size_x)
            current_tile_y = int(self.pos.y // tile_size_y)

            new_tile_x = current_tile_x + dx
            new_tile_y = current_tile_y + dy

            self.target_pos = pygame.Vector2(
                new_tile_x * tile_size_x + tile_size_x // 2,
                new_tile_y * tile_size_y + tile_size_y // 2
            )
            self.set_animation(f"{self.last_direction}.gif")
            self.is_moving = True
