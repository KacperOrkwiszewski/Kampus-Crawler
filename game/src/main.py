import pygame
from constants import Constants
from game.src.map.game_map import GameMap
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
          if event.key == pygame.K_UP:
              playerUP_change = player.movement_speed
          if event.key == pygame.K_LEFT:
              playerLEFT_change = player.movement_speed
          if event.key == pygame.K_RIGHT:
              playerRIGHT_change = player.movement_speed

      #stop moving if key is no longer pressed
      if event.type == pygame.KEYUP:
          if event.key == pygame.K_DOWN:
              playerDOWN_change = 0
              player.last_direction = 'down'
          if event.key == pygame.K_UP:
              playerUP_change = 0
              player.last_direction = 'up'
          if event.key == pygame.K_LEFT:
              playerLEFT_change = 0
              player.last_direction = 'left'
          if event.key == pygame.K_RIGHT:
              playerRIGHT_change = 0
              player.last_direction = 'right'


    playerX_change = -playerRIGHT_change+playerLEFT_change
    playerY_change = -playerDOWN_change+playerUP_change


    #move player
    player.update_position(playerX_change, playerY_change)

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
        match player.last_direction:
            case 'down':
                player.set_animation('idle_down.gif')
            case 'up':
                player.set_animation('idle_up.gif')
            case 'left':
                player.set_animation('idle_left.gif')
            case 'right':
                player.set_animation('idle_right.gif')


    screen.fill((0, 0, 0))
    map.draw(screen, Constants.MAP_SCALE, player.pos_x, player.pos_y)
    player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)

    pygame.display.flip()
    pygame.display.update()