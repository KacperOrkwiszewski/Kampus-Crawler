import pygame
import sys

from sound.sound_manager import SoundManager
from sound.sound_type import SoundEffectType


class PauseMenu:
    def __init__(self, screen):
        self.rects = None
        self.bg_images = None
        self.title_rect = None
        self.title_text = None
        self.background = None

        self.screen = screen

        self.button_scale = 0.6
        self.button_font_size = 70
        self.title_font_size = 120
        self.load_assets()
        self.font = pygame.font.Font('src/menu/assets/font.ttf', int(self.button_font_size * self.button_scale))
        self.title_font = pygame.font.Font('src/menu/assets/font.ttf', int(self.title_font_size * self.button_scale))

        self.base_color = (190, 190, 190)  # "a bit darker than #cfcfcf"
        self.hovering_color = (207, 207, 207)  # "#cfcfcf"

        self.buttons = ["Resume", "Options", "Main Menu","Quit"]
        self.spacing = 10

        self.hovered_button = None

        self.update_layout()

    def load_assets(self):
        self.background = pygame.image.load('src/menu/assets/Background_pause.png')
        self.bg_images_up = [
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/large_button_up.png').convert_alpha(),
                (550 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/large_button_up.png').convert_alpha(),
                (600 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/extra_large_button_up.png').convert_alpha(),
                (750 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/button_up.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
        ]
        self.bg_images_down = [
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/large_button_down.png').convert_alpha(),
                (550 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/large_button_down.png').convert_alpha(),
                (600 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/extra_large_button_down.png').convert_alpha(),
                (750 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/button_down.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
        ]

    def update_layout(self):
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        screen_width, screen_height = self.screen.get_size()
        self.title_text = self.title_font.render("PAUSED", True, (207, 207, 207))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 80))

        start_y = 185

        self.rects = []
        current_y = start_y
        for bg in self.bg_images_up:
            rect = bg.get_rect(center=(screen_width // 2, current_y + bg.get_height() // 2))
            self.rects.append(rect)
            current_y += bg.get_height() + self.spacing

    def run(self):
        button_images = self.bg_images_up.copy() # copy so it can be modified without affecting original variable
        clicked = 10  # clicked is the id of button that was clicked starting value is 10 so no button is recognised
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_layout()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            button_images[i] = self.bg_images_down[i]
                            clicked = i
                            SoundManager.play_effect(SoundEffectType.Click)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    button_images = self.bg_images_up.copy()
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            button_images[i] = self.bg_images_down[i]
                            if clicked == i:
                                return self.buttons[i].lower()
                    clicked = 10

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # press escape to leave pause menu
                        return "resume"

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title_text, self.title_rect)

            for i, rect in enumerate(self.rects):
                if rect.collidepoint(mouse_pos):
                    bg = button_images[i]
                    text = self.font.render(self.buttons[i], True, self.hovering_color)
                    if self.hovered_button != i:
                      SoundManager.play_effect(SoundEffectType.Hover)
                      self.hovered_button = i
                else:
                    bg = button_images[i]
                    text = self.font.render(self.buttons[i], True, self.base_color)
                    if self.hovered_button == i:
                        self.hovered_button = None
                if clicked == i:
                    text_rect = text.get_rect(center=(rect.centerx - 13 * self.button_scale, rect.centery))
                else:
                    text_rect = text.get_rect(center=(rect.centerx, rect.centery - 13 * self.button_scale))
                self.screen.blit(bg, rect)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(60)
