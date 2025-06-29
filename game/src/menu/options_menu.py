import pygame
import sys
from sound.sound_type import SoundEffectType
from sound.sound_manager import SoundManager


class OptionsMenu:
    def __init__(self, screen, player):
        self.hovered_button = None
        self.player = player

        self.ok = False
        self.screen = screen

        # to implement functionality innit these values with parameters given in constructor
        self.effects_volume = 5  # changes from 1 to 10 by 1
        self.music_volume = 5  # changes from 1 to 10 by 1
        self.game_speed = 4  # changes from 1 to 10 by 2

        self.x_center = self.screen.get_width() // 2
        self.arrow_offset = 180

        # text
        self.button_scale = 0.6
        self.button_font_size = 60
        self.title_font_size = 70
        self.description_font_size = 25
        self.font = pygame.font.Font('assets/menu/font.ttf', int(self.button_font_size * self.button_scale))
        self.title_font = pygame.font.Font('assets/menu/font.ttf', self.title_font_size)
        self.description_font = pygame.font.Font('assets/menu/font.ttf', self.description_font_size)
        self.indicator_font = pygame.font.Font('assets/menu/PIXEAB__.ttf', 30)
        self.buttons = ["Play", "Options", "Quit"]
        self.base_color = (190, 190, 190)  # "a bit darker than #cfcfcf"
        self.hovering_color = (207, 207, 207)  # "#cfcfcf"
        self.dark_gray = (38, 38, 38)  # #262626
        self.spacing = 30
        self.start_y = 230
        self.y_pos = []
        current_y = self.start_y
        for i in range(0, 3):
            self.y_pos.append(current_y)
            current_y += self.spacing + 150 * self.button_scale
        self.y_pos.append(current_y - self.spacing)
        self.clicked = 12
        self.down = 12
        self.background = pygame.image.load('assets/menu/Background_options.png')
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.bg_images_up = [
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/round_button_up.png').convert_alpha(),
                (150 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/button_up.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/large_button_down.png').convert_alpha(),
                (400 * self.button_scale, 120 * self.button_scale))
        ]
        self.bg_images_down = [
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/round_button_down.png').convert_alpha(),
                (150 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/button_down.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale))
        ]
        self.buttons = [
            {"label": "<", "x": self.x_center - self.arrow_offset, "y": self.y_pos[0], "action": lambda: self.modify_option(-1, 0), "button": 0},
            {"label": " >", "x": self.x_center + self.arrow_offset, "y": self.y_pos[0], "action": lambda: self.modify_option(1, 0), "button": 0},
            {"label": "<", "x": self.x_center - self.arrow_offset, "y": self.y_pos[1], "action": lambda: self.modify_option(-1, 1), "button": 0},
            {"label": " >", "x": self.x_center + self.arrow_offset, "y": self.y_pos[1], "action": lambda: self.modify_option(1, 1), "button": 0},
            {"label": "<", "x": self.x_center - self.arrow_offset, "y": self.y_pos[2], "action": lambda: self.modify_option(-1, 2), "button": 0},
            {"label": " >", "x": self.x_center + self.arrow_offset, "y": self.y_pos[2], "action": lambda: self.modify_option(1, 2), "button": 0},
            {"label": "OK", "x": self.x_center, "y": self.y_pos[3], "action": lambda: self.say_ok(), "button": 1}

        ]
        self.rects = []
        for button in self.buttons:
            rect = self.bg_images_up[button["button"]].get_rect(center=(button["x"], button["y"]))
            self.rects.append(rect)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # drawing title text
        self.draw_title()
        mouse_pos = pygame.mouse.get_pos()
        # drawing buttons
        for i, rect in enumerate(self.rects):
            button = self.buttons[i]
            if not i == self.down:
                bg = self.bg_images_up[button["button"]]
            else:
                bg = self.bg_images_down[button["button"]]
            if rect.collidepoint(mouse_pos):
                text = self.font.render(self.buttons[i]["label"], True, self.hovering_color)
                if self.hovered_button != i:
                    SoundManager.play_effect(SoundEffectType.Hover)
                    self.hovered_button = i
            else:
                text = self.font.render(self.buttons[i]["label"], True, self.base_color)
                if self.hovered_button == i:
                  self.hovered_button = None
            if self.down == i:
                text_rect = text.get_rect(center=(rect.centerx - 13 * self.button_scale, rect.centery))
            else:
                text_rect = text.get_rect(center=(rect.centerx, rect.centery - 13 * self.button_scale))
            self.screen.blit(bg, rect)
            self.screen.blit(text, text_rect)
            self.draw_option_values()

    def handle_input(self,event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(mouse_pos):
                    self.down = i
                    self.clicked = i
                    SoundManager.play_effect(SoundEffectType.Click)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(mouse_pos):
                    if self.clicked == i:
                        self.down = 12
                        self.clicked = 12
                        return self.buttons[i]["action"]
            self.down = 12
            self.clicked = 12

    def modify_option(self, direction, option_index):
        if option_index == 1:
            self.effects_volume = max(0, min(10, self.effects_volume + direction))
            SoundManager.set_effect_volume(self.effects_volume / 10)
        elif option_index == 0:
            self.music_volume = max(0, min(10, self.music_volume + direction))
            SoundManager.set_music_volume(self.music_volume / 10)
        elif option_index == 2:
            self.game_speed = max(2, min(10, self.game_speed + direction * 2))
            self.player.movement.base_movement_speed = int(pow(2, self.game_speed / 2 - 1)) #magic calculation 2 4 6 8 10 -> 1 2 4 8 16
            self.player.movement.sprint_movement_speed = self.player.movement.base_movement_speed * 2
            self.player.data.movement_speed = self.player.movement.sprint_movement_speed if self.player.data.is_sprinting else self.player.movement.base_movement_speed

    def say_ok(self):
        self.ok = True

    def draw_option_values(self):
        texts = [
            "music vol:",
            "sfx vol:",
            "game speed:"
        ]
        indicator = "|"
        values =[
            indicator*self.music_volume,
            indicator*self.effects_volume,
            indicator*self.game_speed
        ]
        i = 0
        for y in self.y_pos[0:3]:
            bg = self.bg_images_up[2]
            rect = bg.get_rect(center=(self.x_center, y))
            text = self.description_font.render(texts[i], True, self.dark_gray)
            text_rect = text.get_rect(center=(rect.midtop[0],rect.midtop[1] - self.description_font_size * 0.6))
            value_txt = self.indicator_font.render(values[i], True, self.base_color)
            value_txt = pygame.transform.scale(value_txt, (int(value_txt.get_width() * 2), value_txt.get_height()))
            value_rect = value_txt.get_rect(midleft=(rect.left + 15, rect.centery - 3))
            i += 1
            self.screen.blit(bg, rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(value_txt,value_rect)

    def draw_title(self):
        title = self.title_font.render("OPTIONS", True, (207, 207, 207))
        center_x = self.screen.get_width() // 2
        title_text_top_y = 70
        title_rect = title.get_rect(center=(center_x, title_text_top_y))
        self.screen.blit(title, title_rect)

    def run(self):
        self.ok = False
        clock = pygame.time.Clock()
        while not self.ok:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.ok = True  # quit if esc
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    # handle mouse clicks
                    action = self.handle_input(event)
                    if action:
                        action()
            self.draw()
            clock.tick(60)
            pygame.display.flip()

