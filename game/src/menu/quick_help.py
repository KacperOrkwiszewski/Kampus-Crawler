import pygame
import sys


class QuickHelp:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("assets/menu/quick_help.png").convert()
        self.clock = pygame.time.Clock()

        self.screen_rect = screen.get_rect()
        self.image_rect = self.image.get_rect()
        self.offset = [0, 0]  # image offset


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
            pygame.display.flip()
            self.clock.tick(60)

