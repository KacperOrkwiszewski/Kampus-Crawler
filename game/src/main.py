import pygame
import threading
import src.client.client as Client
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


# Start the network thread to handle player networking
threading.Thread(target=Client.network_thread, args=(player,), daemon=True).start()

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
    #player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt)
    # Draw other players
    with Client.lock:
        for player_id, player_data in Client.all_players.items():
            if str(player_id) != str(player.id):  # Nie rysuj samego siebie
                other_player = Player(player_data['current_animation'])
                other_player.pos_x = player_data['x']
                other_player.pos_y = player_data['y']
                other_player.last_direction = player_data['direction']
                other_player.draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt, other_player.pos_x - player.pos_x, other_player.pos_y - player.pos_y)

    pygame.display.flip()
    pygame.display.update()