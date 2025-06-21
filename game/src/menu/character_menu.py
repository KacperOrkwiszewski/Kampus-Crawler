import pygame
import sys
from sound.SoundManager import SoundManager
from sound.sound_type import SoundEffectType
from player.player import Player
import pygame_textinput


class CharacterMenu:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        # background
        self.background = pygame.image.load('src/menu/assets/Background_character.png')
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

        # buttons
        # position buttons
        self.button_scale = 0.6
        self.start_y = 350
        self.spacing = 50
        self.arrow_spacing = 300
        # text
        self.button_font_size = 70
        self.title_font_size = 50
        self.font = pygame.font.Font('src/menu/assets/font.ttf', int(self.button_font_size * self.button_scale))
        self.title_font = pygame.font.Font('src/menu/assets/font.ttf', self.title_font_size)

        self.buttons = ["<", ">", "Confirm"]
        self.base_color = (190, 190, 190)  # "a bit darker than #cfcfcf"
        self.hovering_color = (207, 207, 207)  # "#cfcfcf"
        self.locked_color = (100,100,100)  # "#cfcfcf"


        #name input
        self.input_font_size = 70
        self.input_scale = 0.3
        self.textinput_y = 180

        self.textinput = pygame_textinput.TextInputVisualizer(
            font_object=pygame.font.Font('src/menu/assets/font.ttf', int(self.input_font_size * self.input_scale)),
            font_color=(38, 38, 38),
            cursor_color=(207, 207, 207)
        )
        # self.textinput.value = "username"
        self.input_box_image = pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/inputbox.png').convert_alpha(),
                (900 * self.input_scale, 208 * self.input_scale))
        self.input_box_rect = self.input_box_image.get_rect(
            center=(self.screen.get_width() // 2, self.textinput_y + self.input_font_size * self.input_scale /2))
        # placeholder text (when input empty)
        self.placeholder_surface = self.textinput.font_object.render("username", True,self.locked_color)  # placeholer
        self.placeholder_rect = self.placeholder_surface.get_rect(center=(
            self.screen.get_width() // 2,
            self.textinput_y + self.textinput.surface.get_height() // 2
        ))
        #characters
        self.selected_character = 0
        self.number_of_characters = 3
        self.character_y = 260
        self.character_scale = 1
        #loading player models
        self.characters = [
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/brandon.gif').convert_alpha(),
                (160 * self.character_scale, 160 * self.character_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/david.gif').convert_alpha(),
                (160 * self.character_scale, 160 * self.character_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/jane.gif').convert_alpha(),
                (160 * self.character_scale, 160 * self.character_scale)),
        ]
        # loading buttons background
        self.bg_images_up = [
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/round_button_up.png').convert_alpha(),
                (150 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/round_button_up.png').convert_alpha(),
                (150* self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/button_up.png').convert_alpha(),
                (500 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/button_up_locked.png').convert_alpha(),
                (500 * self.button_scale, 150 * self.button_scale))
        ]
        # when hovering
        self.bg_images_down = [
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/round_button_down.png').convert_alpha(),
                (150 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/round_button_down.png').convert_alpha(),
                (150 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('src/menu/assets/button_down.png').convert_alpha(),
                (500 * self.button_scale, 150 * self.button_scale)),
        ]

        # default text
        self.texts = [self.font.render(btn, True, self.base_color) for btn in self.buttons]

        start_y = self.start_y

        self.rects = []
        current_y = start_y
        spacing = self.spacing
        bg = self.bg_images_up[0]
        rect1 = bg.get_rect(center=(self.screen.get_width() // 2 - self.arrow_spacing // 2, current_y + bg.get_height() // 2))
        self.rects.append(rect1)
        bg = self.bg_images_up[1]
        rect2 = bg.get_rect(
            center=(self.screen.get_width() // 2 + self.arrow_spacing // 2, current_y + bg.get_height() // 2))
        self.rects.append(rect2)
        current_y += bg.get_height() + spacing
        bg = self.bg_images_up[2]
        rect3 = bg.get_rect(
            center=(self.screen.get_width() // 2, current_y + bg.get_height() // 2))
        self.rects.append(rect3)

    def run(self):
        button_clicked = False
        button_images = self.bg_images_up.copy()  # copy so it can be modified without affecting original variable
        clock = pygame.time.Clock()
        clicked = 10  # clicked is the id of button that was clicked starting value is 10 so no button is recognised

        while True:
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            self.textinput.update(events)
            self.textinput.value = self.textinput.value[:11] #max username length
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            if i == 2 and self.textinput.value == "":  # block blank username
                                continue
                            button_images[i] = self.bg_images_down[i]
                            clicked = i
                            SoundManager.play_effect(SoundEffectType.Click)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    button_images = self.bg_images_up.copy()
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            if clicked == i:
                                if i == 2:  # 'confirm' button
                                    if not self.textinput.value == "":
                                        self.player.data.player_name = self.textinput
                                        self.player.data.character_id = self.selected_character
                                        return self.buttons[i].lower()
                                if i == 1:
                                    self.selected_character = (self.selected_character + 1) % 3
                                if i == 0:
                                    self.selected_character = (self.selected_character - 1) % 3
                    clicked = 10

            self.screen.blit(self.background, (0, 0))
            # draw character
            self.screen.blit(self.characters[self.selected_character],(self.screen.get_width() // 2 - (160 / 2 * self.character_scale), self.character_y))
            # drawing Title text
            self.draw_name()
            # drawing buttons
            for i, rect in enumerate(self.rects):
                # center '<' text on the button
                if i == 1:
                    left_arrow_shift = 13 * self.button_scale
                else:
                    left_arrow_shift = 0
                if rect.collidepoint(mouse_pos):
                    bg = button_images[i]
                    text = self.font.render(self.buttons[i], True, self.hovering_color)

                    if i == 2 and self.textinput.value == "":  # do not change color if button not active
                        bg = button_images[i+1]
                        text = self.font.render(self.buttons[i], True, self.locked_color)


                else:
                    bg = button_images[i]
                    text = self.font.render(self.buttons[i], True, self.base_color)

                    if i == 2 and self.textinput.value == "":  # do not change color if button not active
                        bg = button_images[i+1]
                        text = self.font.render(self.buttons[i], True, self.locked_color)

                if clicked == i:
                    text_rect = text.get_rect(center=(rect.centerx - 13 * self.button_scale + left_arrow_shift, rect.centery))
                else:
                    text_rect = text.get_rect(center=(rect.centerx + left_arrow_shift, rect.centery - 13 * self.button_scale))
                self.screen.blit(bg, rect)
                self.screen.blit(text, text_rect)
                #inputbox
                self.screen.blit(self.input_box_image, self.input_box_rect)
                if self.textinput.value == "":
                    # if no username entered - show placeholder
                    self.screen.blit(self.placeholder_surface, self.placeholder_rect)
                else:
                    self.screen.blit(self.textinput.surface, (self.screen.get_width() // 2 - self.textinput.surface.get_width() // 2 + self.input_font_size*self.input_scale //2, self.textinput_y))  # input pos
            pygame.display.flip()
            clock.tick(60)
            if button_clicked:
                return

    def draw_name(self):
        title_line1 = self.title_font.render("CHARACTER", True, (207, 207, 207))
        title_line2 = self.title_font.render("CUSTOMIZATION", True, (207, 207, 207))
        center_x = self.screen.get_width() // 2
        title_text_top_y = 50
        title_rect1 = title_line1.get_rect(center=(center_x, title_text_top_y))
        title_rect2 = title_line2.get_rect(
            center=(center_x, title_text_top_y + title_line1.get_height() + 15))  # 10 space between lines
        self.screen.blit(title_line1, title_rect1)
        self.screen.blit(title_line2, title_rect2)