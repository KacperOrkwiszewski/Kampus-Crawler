from .player_image_info import PlayerImageInfo
import pygame

class Player:
    def __init__(self, filename):
        self.pos_x = 16 * 5  # start na środku kafelka
        self.pos_y = 16 * 5
        self.movement_speed = 2  # piksele na sekundę
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

    def set_direction_animation(self):
        match self.last_direction:
            case "up":
                self.set_animation("up.gif")
            case "down":
                self.set_animation("down.gif")
            case "left":
                self.set_animation("left.gif")
            case "right":
                self.set_animation("right.gif")

    def set_idle_animation(self):
        match self.last_direction:
            case "up":
                self.set_animation("idle_up.gif")
            case "down":
                self.set_animation("idle_down.gif")
            case "left":
                self.set_animation("idle_left.gif")
            case "right":
                self.set_animation("idle_right.gif")

    def move_to_offset(self, dx, dy):
        if not self.is_moving:
            tile_size = 16 * 5
            current_tile_x = int(self.pos_x // tile_size)
            current_tile_y = int(self.pos_y // tile_size)

            new_tile_x = current_tile_x + dx
            new_tile_y = current_tile_y + dy

            self.target_pos = pygame.Vector2(
                new_tile_x * tile_size + tile_size // 2,
                new_tile_y * tile_size + tile_size // 2
            )
            self.set_direction_animation()
            self.is_moving = True
