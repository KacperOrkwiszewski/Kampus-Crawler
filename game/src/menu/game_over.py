import pygame
import sys
from player.player_state import PlayerCharacter

class GameOver:
    def __init__(self, screen, character):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("assets/menu/game_over_david.png").convert()
        if character == PlayerCharacter.BRANDON:
            self.image = pygame.image.load("assets/menu/game_over_brandon.png").convert()
        elif character == PlayerCharacter.JANE:
            self.image = pygame.image.load("assets/menu/game_over_jane.png").convert()
        self.image = pygame.transform.smoothscale(self.image, (self.screen.get_width() - 16,self.screen.get_height() - 16))
        self.screen_rect = screen.get_rect()
        self.image_rect = self.image.get_rect()
        self.offset = [16, 16]  # image offset


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                # return also if mouse clicked
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return
            #  self.screen.fill((0, 0, 0))
            self.screen.blit(self.image, self.offset)
            self.draw_ui_border()
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