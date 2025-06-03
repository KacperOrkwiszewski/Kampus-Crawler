import pygame
from constants import Constants
from map.game_map import GameMap
from player.player import Player

clock = pygame.time.Clock()

# Initialize pygame in order for program to work
pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH))

# Load the map
map = GameMap("map_data/simple_map.tmx")

# Title and icon
pygame.display.set_caption("Kampus Crawler")
pygame.display.set_icon(pygame.image.load('logo_icon.png'))

# Initialize player
player = Player('idle_down.gif')

# Movement related variables
playerUP_change = 0
playerDOWN_change = 0
playerLEFT_change = 0
playerRIGHT_change = 0
ignore_horizontal_movement = False
ignore_vertical_movement = False

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
          if event.key == pygame.K_DOWN:
              playerDOWN_change = player.movement_speed
              ignore_horizontal_movement = True
              ignore_vertical_movement = False
          if event.key == pygame.K_UP:
              playerUP_change = player.movement_speed
              ignore_horizontal_movement = True
              ignore_vertical_movement = False
          if event.key == pygame.K_LEFT:
              playerLEFT_change = player.movement_speed
              ignore_vertical_movement = True
              ignore_horizontal_movement = False
          if event.key == pygame.K_RIGHT:
              playerRIGHT_change = player.movement_speed
              ignore_vertical_movement = True
              ignore_horizontal_movement = False

      #stop moving if key is no longer pressed
      if event.type == pygame.KEYUP:
          if event.key == pygame.K_DOWN:
              playerDOWN_change = 0
              ignore_vertical_movement = False
              player.last_direction = 'down'
          if event.key == pygame.K_UP:
              playerUP_change = 0
              player.last_direction = 'up'
              ignore_vertical_movement = False
          if event.key == pygame.K_LEFT:
              playerLEFT_change = 0
              player.last_direction = 'left'
              ignore_horizontal_movement = False
          if event.key == pygame.K_RIGHT:
              playerRIGHT_change = 0
              player.last_direction = 'right'
              ignore_horizontal_movement = False

    if ignore_horizontal_movement:
        playerX_change = 0
    else:
        playerX_change = -playerRIGHT_change + playerLEFT_change

    if ignore_vertical_movement:
        playerY_change = 0
    else:
        playerY_change = -playerDOWN_change+playerUP_change


    #move player
    player.update_position(playerX_change, playerY_change)

    if playerX_change == 0 and playerY_change == 0:
        player.is_moving = False
    else:
        player.is_moving = True

    player.align_to_tiles()

    # Change animation according to movement
    if playerX_change < 0:
        player.set_animation('right.gif')
    elif playerX_change > 0:
        player.set_animation('left.gif')
    elif playerY_change < 0:
        player.set_animation('down.gif')
    elif playerY_change > 0:
        player.set_animation('up.gif')
    elif (playerX_change == 0 and playerY_change == 0):
        player.set_animation(f'idle_{player.last_direction}.gif')


    screen.fill((0, 0, 0))
    map.draw(screen, Constants.MAP_SCALE, player.pos_x, player.pos_y)
    player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)

    pygame.display.flip()
    pygame.display.update()