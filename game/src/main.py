import pygame
from constants import Constants
from map.game_map import GameMap
from player.player import Player

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH))
pygame.display.set_caption("Kampus Crawler")
pygame.display.set_icon(pygame.image.load('logo_icon.png'))

map = GameMap("map_data/simple_map.tmx")
player = Player('idle_down.gif')

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    keys = pygame.key.get_pressed()
    if not player.is_moving:
        if keys[pygame.K_DOWN]:
            player.move_to_offset(0, -1)
        if keys[pygame.K_UP]:
            player.move_to_offset(0, 1)
        if keys[pygame.K_LEFT]:
            player.move_to_offset(1, 0)
        if keys[pygame.K_RIGHT]:
            player.move_to_offset(-1, 0)

    player.update_position(dt)

    # Ustaw animację idle, jeśli skończył ruch
    if not player.is_moving:
        match player.last_direction:
            case "down":
                player.set_animation("idle_down.gif")
            case "up":
                player.set_animation("idle_up.gif")
            case "left":
                player.set_animation("idle_left.gif")
            case "right":
                player.set_animation("idle_right.gif")

    map.draw(screen, Constants.MAP_SCALE, player.pos_x, player.pos_y)
    player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)

    pygame.display.flip()
