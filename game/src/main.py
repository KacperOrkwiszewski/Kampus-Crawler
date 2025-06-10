import pygame
import threading
from client_server.server import Server
from client_server.client import Client
from constants import Constants
from map.game_map import GameMap
from player.player import Player
from player.player_state import PlayerState
from menu.main_menu import MainMenu
from menu.pause_menu import PauseMenu
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

choice = MainMenu(screen).run()

# Initialize player
player = Player(PlayerState.IDLE_DOWN)

if choice == "play":
    # server
    server = Server('0.0.0.0', 12345)
    server_thread = threading.Thread(target=server.run_server, daemon=True)  # thread ends if server is already open
    server_thread.start()  # if server is already online function run_server doesn't create new one
    # client
    client = Client("localhost",12345)
    client_thread = threading.Thread(target=Client.network_thread, args=(client, player), daemon=True)
    client_thread.start()
    # Game loop
    running = True
    paused = False
    pause_menu = PauseMenu(screen)

    while running:

        dt = clock.tick(60) / 1000  # dt in seconds

        for event in pygame.event.get():
          #event handler (the top right X button is pressed)
          if event.type == pygame.QUIT:
              running = False

          #keyboard events
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_ESCAPE:
                  paused = not paused

              if not paused:
                  player.movement.handle_down(event.key)

          if event.type == pygame.KEYUP:
              if not paused:
                  player.movement.handle_up(event.key)

              if paused:
                  result = pause_menu.run()
                  if result == "resume":
                      paused = False
                  elif result == "options":
                      pass  # temporary solution
                  elif result == "main menu":
                      choice = MainMenu(screen).run()
                      if choice == "play":
                          player = Player(PlayerState.IDLE_DOWN)
                          paused = False
                      else:
                          running = False
                  continue

        x_change, y_change = player.movement.calculate_final_change()

        # check if player is currently moving
        player.movement.is_moving = not (x_change == 0 and y_change == 0)
        # try to align the player to the middle of a tile
        player.update_position(x_change, y_change)
        player.movement.align_to_tiles(Constants.TILE_HEIGHT, Constants.MAP_SCALE)


        # Change animation according to movement
        if player.data.during_diagonal_alignment == False:
            if x_change < 0:
                player.set_animation(PlayerState.MOVE_RIGHT)
            elif x_change > 0:
                player.set_animation(PlayerState.MOVE_LEFT)
            elif y_change < 0:
                player.set_animation(PlayerState.MOVE_DOWN)
            elif y_change > 0:
                player.set_animation(PlayerState.MOVE_UP)


        screen.fill((0, 0, 0))
        map.draw(screen, Constants.MAP_SCALE, player.data.pos_x, player.data.pos_y)
        # Dispaly other players
        with client.lock:
            for player_id, other_player_data in client.all_players.items():
                if player_id not in client.player_objects: # create new player if doesn t exist
                    client.player_objects[player_id] = Player(other_player_data.state)
                if client.player_objects[player_id].data.state != other_player_data.state:
                    client.player_objects[player_id].set_animation(other_player_data.state)
                client.player_objects[player_id].data = other_player_data
                offset_x = (other_player_data.pos_x - player.data.pos_x)
                offset_y = (other_player_data.pos_y - player.data.pos_y)
                client.player_objects[player_id].draw(screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt, offset_x, offset_y)

        pygame.display.flip()
        pygame.display.update()
elif choice == "options":
    pygame.quit()  # temporary solution
elif choice == "quit":
    pygame.quit()
