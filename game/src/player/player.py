from .player_image_info import PlayerImageInfo
import pygame

class Player:
    def __init__(self, filename):
        self.tile_size = 16
        self.pos_x = self.tile_size * 5  # start na środku kafelka
        self.pos_y = self.tile_size * 5
        self.movement_speed = 100  # piksele na sekundę
        self.player_img_info = PlayerImageInfo(filename, self.movement_speed)
        self.current_animation = filename
        self.last_direction = 'down'
        self.is_moving = False
        self.target_pos = pygame.Vector2(self.pos_x, self.pos_y)

    def draw(self, screen, screen_x, screen_y, dt):
        frame = self.player_img_info.get_current_frame(dt)
        draw_x = screen_y / 2 - self.player_img_info.scale_size_y / 2
        draw_y = screen_x / 2 - self.player_img_info.scale_size_x / 2
        screen.blit(frame, (draw_x, draw_y))

    def update_position(self, dt):
        if self.is_moving:
            direction = self.target_pos - pygame.Vector2(self.pos_x, self.pos_y)
            distance = self.movement_speed * dt
            if direction.length() <= distance:
                self.pos_x, self.pos_y = self.target_pos.x, self.target_pos.y
                self.is_moving = False
            else:
                direction = direction.normalize() * distance
                self.pos_x += direction.x
                self.pos_y += direction.y

    def set_animation(self, filename):
        if self.current_animation == filename:
            return
        self.current_animation = filename
        self.player_img_info = PlayerImageInfo(filename, self.movement_speed)

    def move_to_offset(self, dx, dy):
        if not self.is_moving:
            new_x = round((self.pos_x + dx * self.tile_size) / self.tile_size) * self.tile_size
            new_y = round((self.pos_y + dy * self.tile_size) / self.tile_size) * self.tile_size
            self.target_pos = pygame.Vector2(new_x, new_y)
            self.is_moving = True

            # animacje kierunkowe
            if dx == -1:
                self.set_animation("right.gif")
                self.last_direction = "right"
            elif dx == 1:
                self.set_animation("left.gif")
                self.last_direction = "left"
            elif dy == -1:
                self.set_animation("down.gif")
                self.last_direction = "down"
            elif dy == 1:
                self.set_animation("up.gif")
                self.last_direction = "up"
