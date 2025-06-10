import pygame
import sys


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('src/menu/assets/Background.png')
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.font = pygame.font.Font('src/menu/assets/font.ttf', 70)
        self.title_font = pygame.font.Font('src/menu/assets/font.ttf', 80)

        screen_width, screen_height = screen.get_size()

        self.buttons = ["Play", "Options", "Quit"]
        self.base_color = (255, 255, 255)  # light blue color
        self.hovering_color = (215, 252, 212)  # white

        # loading buttons background
        self.bg_images = [
            pygame.image.load('src/menu/assets/Play.png').convert_alpha(),
            pygame.image.load('src/menu/assets/Options.png').convert_alpha(),
            pygame.image.load('src/menu/assets/Quit.png').convert_alpha()
        ]

        # default text
        self.texts = [self.font.render(btn, True, self.base_color) for btn in self.buttons]

        spacing = 40
        total_height = sum(bg.get_height() for bg in self.bg_images) + spacing * (len(self.bg_images) - 1)
        start_y = (screen_height - total_height) // 2

        self.rects = []
        current_y = start_y
        for bg in self.bg_images:
            rect = bg.get_rect(center=(screen_width // 2, current_y + bg.get_height() // 2))
            self.rects.append(rect)
            current_y += bg.get_height() + spacing

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            return self.buttons[i].lower()

            self.screen.blit(self.background, (0, 0))

            # drawing MAIN MENU text
            title_text = self.title_font.render("MAIN MENU", True, (182, 143, 64))  # "#b68f40"
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 60))

            start_y = 180

            self.rects = []
            current_y = start_y
            spacing = 40
            for bg in self.bg_images:
                rect = bg.get_rect(center=(self.screen.get_width() // 2, current_y + bg.get_height() // 2))
                self.rects.append(rect)
                current_y += bg.get_height() + spacing
            self.screen.blit(title_text, title_rect)

            # drawing buttons
            for i, (bg, rect) in enumerate(zip(self.bg_images, self.rects)):
                self.screen.blit(bg, rect)

                # text color change when hovering
                if rect.collidepoint(mouse_pos):
                    text = self.font.render(self.buttons[i], True, self.hovering_color)
                else:
                    text = self.font.render(self.buttons[i], True, self.base_color)

                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(60)
