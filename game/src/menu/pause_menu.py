import pygame
import sys

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.load_assets()

        self.font = pygame.font.Font('src/menu/assets/font.ttf', 70)
        self.title_font = pygame.font.Font('src/menu/assets/font.ttf', 80)

        self.base_color = (215, 252, 212)
        self.hovering_color = (255, 255, 255)

        self.buttons = ["Resume", "Options", "Main Menu"]
        self.spacing = 40

        self.update_layout()

    def load_assets(self):
        self.background = pygame.image.load('src/menu/assets/Background.png')
        self.bg_images = [
            pygame.image.load('src/menu/assets/Resume.png').convert_alpha(),
            pygame.image.load('src/menu/assets/Options.png').convert_alpha(),
            pygame.image.load('src/menu/assets/Mainmenu.png').convert_alpha()
        ]

    def update_layout(self):
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

        screen_width, screen_height = self.screen.get_size()
        self.title_text = self.title_font.render("PAUSE", True, (182, 143, 64))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 60))

        start_y = 180

        self.rects = []
        current_y = start_y
        for bg in self.bg_images:
            rect = bg.get_rect(center=(screen_width // 2, current_y + bg.get_height() // 2))
            self.rects.append(rect)
            current_y += bg.get_height() + self.spacing

    def run(self):
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
                            return self.buttons[i].lower()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Escape też powoduje wyjście z pauzy
                        return "resume"

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title_text, self.title_rect)

            for i, (bg, rect) in enumerate(zip(self.bg_images, self.rects)):
                self.screen.blit(bg, rect)

                color = self.hovering_color if rect.collidepoint(mouse_pos) else self.base_color
                text = self.font.render(self.buttons[i], True, color)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(60)
