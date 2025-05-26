import pygame
import threading
from src.client.client import network_thread, other_players, other_players_lock
from src.constants import Constants
from src.map.game_map import GameMap
from src.player.player import Player

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

# Start the network thread to handle player networking
threading.Thread(target=network_thread, args=(player,), daemon=True).start()

# Movement related variables
playerUP_change = 0
playerDOWN_change = 0
playerLEFT_change = 0
playerRIGHT_change = 0

print("git")

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
    #player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)
    # Draw other players
    with other_players_lock:
        for position in other_players:
            print(f"Drawing other player at {position.x}, {position.y}")
            other_player = Player('idle_down.gif')
            other_player.draw(screen, position.x, position.y, dt)

    pygame.display.flip()
    pygame.display.update()