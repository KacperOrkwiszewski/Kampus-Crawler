import pygame
from .player_state import ANIMATION_FILES, CHARACTERS_FILES, PlayerCharacter
from .player_image_info import PlayerImageInfo
from .movement_manager import MovementManager
from .player_data import PlayerData


class Player:
    def __init__(self, state, character=PlayerCharacter.DAVID, base_ms=2):
        self.data = PlayerData(state, base_ms, character)
        self.player_img_info = PlayerImageInfo(self.data.folder + self.gif_name(), self.data.movement_speed)
        self.current_animation = self.gif_name()
        self.movement = MovementManager(self)
        self.data.pos_x = -4200
        self.data.pos_y = -200

    def draw(self, screen, screen_x, screen_y, dt, offset_x=0, offset_y=0):
        if not 'idle' in self.gif_name():
          if self.data.is_sprinting:
              self.player_img_info.animation_speed = 0.2 / self.movement.sprint_movement_speed
          else:
              self.player_img_info.animation_speed = 0.2 / self.movement.base_movement_speed
        else:
            self.player_img_info.animation_speed = 0.5

        # Get the current animation frame based on elapsed time (dt)
        frame = self.player_img_info.get_current_frame(dt)
        # Draw the current frame centered on the screen
        screen.blit(frame, ((screen_y / 2) - (self.player_img_info.scale_size_y / 2) - offset_x,
            (screen_x / 2) - (self.player_img_info.scale_size_x / 2) - offset_y))
        if self.data.chat_message != "" and self.data.chat_timer > 0:
            # Draw the chat message above the player
            font = pygame.font.Font("assets/menu/font.ttf", 10)
            text_surface = font.render(self.data.chat_message, True, (38, 38, 38))
            text_rect = text_surface.get_rect(center=(screen_y / 2 - (self.player_img_info.scale_size_y / 2) - offset_x + 40, (screen_x / 2) - (self.player_img_info.scale_size_x / 2) - offset_y - 20))
            bubble_rect = text_rect.inflate(16, 8)
            outline_rect = bubble_rect.inflate(4, 4)
            pygame.draw.rect(screen, (100, 100, 100), outline_rect, border_radius=10)
            pygame.draw.rect(screen, (207, 207, 207), bubble_rect, border_radius=8)
            screen.blit(text_surface, text_rect)
        else:
            outline_width = 2
            font = pygame.font.Font("assets/menu/font.ttf", 10)
            text_surface = font.render(self.data.player_name, True, (207, 207, 207))
            size = (text_surface.get_width() + 2 * outline_width, text_surface.get_height() + 2 * outline_width)
            text_img = pygame.Surface(size, pygame.SRCALPHA)
            text_rect = text_surface.get_rect(center=(screen_y / 2 - (self.player_img_info.scale_size_y / 2) - offset_x + 40, (screen_x / 2) - (self.player_img_info.scale_size_x / 2) - offset_y - 20))
            # Outline
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        text_img.blit(
                            font.render(self.data.player_name, True, (38, 38, 38)),
                            (dx + outline_width, dy + outline_width)
                        )
            text_img.blit(text_surface, (outline_width, outline_width))
            screen.blit(text_img, text_rect)
            
    def update_position(self, x, y):
        self.data.pos_x += x
        self.data.pos_y += y

    def update_animation(self):
        self.set_animation(self.data.state)

    def set_animation(self, state):
        filename = str(CHARACTERS_FILES[self.data.character]) + "_" + str(ANIMATION_FILES[state])
        # If the requested animation is already active, do nothing
        if self.current_animation == filename:
            return
        # Otherwise, update the current animation and reload frames
        self.data.state = state
        self.current_animation = filename
        self.player_img_info.update_image_info(self.data.folder + filename, self.data.movement_speed)

    def gif_name(self):
        return str(CHARACTERS_FILES[self.data.character]) + "_" + str(ANIMATION_FILES[self.data.state])
