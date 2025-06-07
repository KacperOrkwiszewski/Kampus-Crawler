import pygame
from constants import Constants
from map.game_map import GameMap
from player.player import Player
from intro.intro_screen import IntroScreen

clock = pygame.time.Clock()

# Initialize pygame in order for program to work
pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH))

# Play intro
IntroScreen.play(screen)

# Load the map
map = GameMap("map_data/simple_map.tmx")

# Title and icon
pygame.display.set_caption("Kampus Crawler")
pygame.display.set_icon(pygame.image.load('logo_icon.png'))

# Initialize player
player = Player('idle_down.gif')

# Game loop
running = True
while running:

    dt = clock.tick(60) / 1000  # dt in seconds

    for event in pygame.event.get():
      #event handler (the top right X button is pressed)
      if event.type == pygame.QUIT:
          running = False

      #keyboard events
      if event.type == pygame.KEYDOWN:
        player.movement.handle_down(event.key)

      if event.type == pygame.KEYUP:
        player.movement.handle_up(event.key)

    x_change, y_change = player.movement.calculate_final_change()

    # check if player is currently moving
    player.movement.is_moving = not (x_change == 0 and y_change == 0)
    # try to align the player to the middle of a tile
    player.update_position(x_change, y_change)
    player.movement.align_to_tiles(Constants.TILE_HEIGHT, Constants.MAP_SCALE)


    # Change animation according to movement
    if player.during_diagonal_alignment == False:
        if x_change < 0:
            player.set_animation('right.gif')
        elif x_change > 0:
            player.set_animation('left.gif')
        elif y_change < 0:
            player.set_animation('down.gif')
        elif y_change > 0:
            player.set_animation('up.gif')


    screen.fill((0, 0, 0))
    map.draw(screen, Constants.MAP_SCALE, player.pos_x, player.pos_y)
    player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)

    pygame.display.flip()
    pygame.display.update()