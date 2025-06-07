import pygame
import sys

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('src/menu/assets/Background.png')
        self.font = pygame.font.Font('src/menu/assets/font.ttf', 50)

        screen_width, screen_height = screen.get_size()

        self.buttons = ["Play", "Options", "Quit"]
        self.bg_images = [
            pygame.image.load('src/menu/assets/Play.png').convert_alpha(),
            pygame.image.load('src/menu/assets/Options.png').convert_alpha(),
            pygame.image.load('src/menu/assets/Quit.png').convert_alpha()
        ]

        self.texts = [self.font.render(btn, True, (255, 255, 255)) for btn in self.buttons]

        spacing = 40
        total_height = sum(bg.get_height() for bg in self.bg_images) + spacing * (len(self.bg_images) - 1)
        start_y = (screen_height - total_height) // 2

        self.rects = []
        current_y = start_y
        for bg, text in zip(self.bg_images, self.texts):
            # background position
            rect = bg.get_rect(center=(screen_width // 2, current_y + bg.get_height() // 2))
            self.rects.append(rect)
            current_y += bg.get_height() + spacing

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos):
                            return self.buttons[i].lower()

            self.screen.blit(self.background, (0, 0))

            for bg, text, rect in zip(self.bg_images, self.texts, self.rects):
                # drawing background of the button
                self.screen.blit(bg, rect)
                # drawing text centered on the background
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(60)
