import pygame
import sys


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        # background
        self.background = pygame.image.load('assets/menu/Background.png')
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

        # buttons
        # position buttons
        self.button_scale = 0.6
        self.start_y = 300
        self.spacing = 10
        # text
        self.button_font_size = 70
        self.title_font_size = 90
        self.font = pygame.font.Font('assets/menu/font.ttf', int(self.button_font_size * self.button_scale))
        self.title_font = pygame.font.Font('assets/menu/font.ttf', self.title_font_size)

        self.buttons = ["Play", "Options", "Quit"]
        self.base_color = (190, 190, 190)  # "a bit darker than #cfcfcf"
        self.hovering_color = (207, 207, 207)  # "#cfcfcf"

        # loading buttons background
        self.bg_images_up = [
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/button_up.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/large_button_up.png').convert_alpha(),
                (600 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/button_up.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
        ]
        # when hovering
        self.bg_images_down = [
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/button_down.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/large_button_down.png').convert_alpha(),
                (600 * self.button_scale, 150 * self.button_scale)),
            pygame.transform.smoothscale(
                pygame.image.load('assets/menu/button_down.png').convert_alpha(),
                (400 * self.button_scale, 150 * self.button_scale)),
        ]

        # default text
        self.texts = [self.font.render(btn, True, self.base_color) for btn in self.buttons]

        start_y = self.start_y

        self.rects = []
        current_y = start_y
        spacing = 40
        for bg in self.bg_images_up:
            rect = bg.get_rect(center=(self.screen.get_width() // 2, current_y + bg.get_height() // 2))
            self.rects.append(rect)
            current_y += bg.get_height() + spacing

    def run(self):
        button_clicked = False
        button_images = self.bg_images_up.copy()  # copy so it can be modified without affecting original variable
        clock = pygame.time.Clock()
        clicked = 10  # clicked is the id of button that was clicked starting value is 10 so no button is recognised
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            button_images[i] = self.bg_images_down[i]
                            print("ok clicker legend")
                            clicked = i
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    button_images = self.bg_images_up.copy()
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            button_images[i] = self.bg_images_down[i]
                            if clicked == i:
                                print("aight")
                                return self.buttons[i].lower()
                    clicked = 10


            self.screen.blit(self.background, (0, 0))

            # drawing Kampus Crawler text
            self.draw_name()

            start_y = self.start_y
            self.rects = []
            current_y = start_y
            spacing = self.spacing
            for bg in button_images:
                rect = bg.get_rect(center=(self.screen.get_width() // 2, current_y + bg.get_height() // 2))
                self.rects.append(rect)
                current_y += bg.get_height() + spacing

            # drawing buttons
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(mouse_pos):
                    bg = button_images[i]
                    text = self.font.render(self.buttons[i], True, self.hovering_color)

                else:
                    bg = button_images[i]
                    text = self.font.render(self.buttons[i], True, self.base_color)
                if clicked == i:
                    text_rect = text.get_rect(center=(rect.centerx - 13 * self.button_scale, rect.centery))
                else:
                    text_rect = text.get_rect(center=(rect.centerx, rect.centery - 13 * self.button_scale))
                self.screen.blit(bg, rect)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(60)
    def draw_name(self):
        title_line1 = self.title_font.render("KAMPUS", True, (207, 207, 207))
        title_line2 = self.title_font.render("CRAWLER", True, (207, 207, 207))
        center_x = self.screen.get_width() // 2
        title_text_top_y = 90
        title_rect1 = title_line1.get_rect(center=(center_x, title_text_top_y))
        title_rect2 = title_line2.get_rect(
            center=(center_x, title_text_top_y + title_line1.get_height() + 15))  # 10 space between lines
        self.screen.blit(title_line1, title_rect1)
        self.screen.blit(title_line2, title_rect2)
