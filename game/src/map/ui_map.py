import pygame
import sys


class MapViewer:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("assets/map_data/map_all_LEGEND.png").convert()
        # scale image
        scale_factor = 0.5
        new_width = int(self.image.get_width() * scale_factor)
        new_height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.smoothscale(self.image, (new_width, new_height))

        self.title_font_size = 40
        self.title_font = pygame.font.Font('assets/menu/font.ttf', self.title_font_size)
        self.clock = pygame.time.Clock()

        self.screen_rect = screen.get_rect()
        self.image_rect = self.image.get_rect()
        self.offset = [-360, -180]  # image offset
        self.dragging = False
        self.last_mouse_pos = (0, 0)

    def clamp_offset(self):
        # don't drag image away from screen
        max_x = 0
        max_y = 0
        min_x = self.screen_rect.width - self.image_rect.width
        min_y = self.screen_rect.height - self.image_rect.height

        self.offset[0] = max(min(self.offset[0], max_x), min_x)
        self.offset[1] = max(min(self.offset[1], max_y), min_y)

    def run(self):
        print(self.offset)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                        return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.dragging = True
                        self.last_mouse_pos = event.pos

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False

                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.offset[0] += dx
                    self.offset[1] += dy
                    self.last_mouse_pos = event.pos

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.offset[0] += 5
            if keys[pygame.K_RIGHT]:
                self.offset[0] -= 5
            if keys[pygame.K_UP]:
                self.offset[1] += 5
            if keys[pygame.K_DOWN]:
                self.offset[1] -= 5

            self.clamp_offset()

            #  self.screen.fill((0, 0, 0))
            self.screen.blit(self.image, self.offset)
            self.draw_ui_border()
            self.draw_title()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_ui_border(self):
        # dark border
        border_thickness = 16
        border_color = (38, 38, 38)
        pygame.draw.rect(self.screen, border_color, pygame.Rect(0, 0, self.screen.get_width(), border_thickness))
        pygame.draw.rect(self.screen, border_color,
                         pygame.Rect(0, self.screen.get_height() - border_thickness, self.screen.get_width(),
                                     border_thickness))
        pygame.draw.rect(self.screen, border_color, pygame.Rect(0, 0, border_thickness, self.screen.get_height()))
        pygame.draw.rect(self.screen, border_color,
                         pygame.Rect(self.screen.get_width() - border_thickness, 0, border_thickness,
                                     self.screen.get_height()))
        # light border
        border_thickness = 8
        border_color = (23, 23, 23)
        pygame.draw.rect(self.screen, border_color, pygame.Rect(0, 0, self.screen.get_width(), border_thickness))
        pygame.draw.rect(self.screen, border_color,
                         pygame.Rect(0, self.screen.get_height() - border_thickness, self.screen.get_width(),
                                     border_thickness))
        pygame.draw.rect(self.screen, border_color, pygame.Rect(0, 0, border_thickness, self.screen.get_height()))
        pygame.draw.rect(self.screen, border_color,
                         pygame.Rect(self.screen.get_width() - border_thickness, 0, border_thickness,
                                     self.screen.get_height()))


    def draw_title(self):
        text = "MAP"
        text_color = (207, 207, 207)
        outline_color = (38, 38, 38)
        outline_width = 3
        center_x = self.screen.get_width() // 2
        title_text_top_y = 40
        base_text = self.title_font.render(text, True, text_color)
        base_rect = base_text.get_rect(center=(center_x, title_text_top_y))

        # border -> text with offset in 8 directions
        for dx in [-outline_width, 0, outline_width]:
            for dy in [-outline_width, 0, outline_width]:
                if dx != 0 or dy != 0:
                    outline_text = self.title_font.render(text, True, outline_color)
                    outline_rect = outline_text.get_rect(center=(center_x + dx, title_text_top_y + dy))
                    self.screen.blit(outline_text, outline_rect)

        self.screen.blit(base_text, base_rect)