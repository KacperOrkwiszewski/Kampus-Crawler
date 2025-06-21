import pygame
import threading
from client_server.server import Server
from client_server.client import Client
from constants import Constants
from sound.sound_type import MusicType
from map.game_map import GameMap
from player.player import Player
from player.player_state import PlayerState
from menu.main_menu import MainMenu
from menu.pause_menu import PauseMenu
from menu.options_menu import OptionsMenu
from menu.character_menu import CharacterMenu
from intro.intro_screen import IntroScreen
from sound.sound_manager import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Constants.WINDOW_HEIGHT, Constants.WINDOW_WIDTH))
        pygame.display.set_caption("Kampus Crawler")
        pygame.display.set_icon(pygame.image.load('logo_icon.png'))

        self.map_data = GameMap("map_data/campusA.tmx")
        self.player = Player(PlayerState.IDLE_DOWN)

        self.client = None
        self.server = None
        self.running = True
        self.paused = False

        self.options_menu = OptionsMenu(self.screen)
        self.character_menu = CharacterMenu(self.screen, self.player)

        IntroScreen.play(self.screen)

        SoundManager.init()
        SoundManager.play_music(MusicType.Menu)

    def start_networking(self):
        # Start server
        self.server = Server('0.0.0.0', 12345)
        server_thread = threading.Thread(target=self.server.run_server, daemon=True)
        server_thread.start()

        # Start client
        self.client = Client("localhost", 12345)
        client_thread = threading.Thread(target=Client.network_thread, args=(self.client, self.player), daemon=True)
        client_thread.start()

    def draw_game(self, dt):
        self.screen.fill((0, 0, 0))
        self.map_data.draw(self.screen, Constants.MAP_SCALE, self.player.data.pos_x, self.player.data.pos_y)

        # Draw other players
        with self.client.lock:
            for player_id, other_player_data in self.client.all_players.items():
                if player_id not in self.client.player_objects:
                    self.client.player_objects[player_id] = Player(other_player_data.state)

                if self.client.player_objects[player_id].data.state != other_player_data.state:
                    self.client.player_objects[player_id].set_animation(other_player_data.state)

                self.client.player_objects[player_id].data = other_player_data
                offset_x = other_player_data.pos_x - self.player.data.pos_x
                offset_y = other_player_data.pos_y - self.player.data.pos_y

                self.client.player_objects[player_id].draw(
                    self.screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt, offset_x, offset_y
                )

        pygame.display.flip()

    def handle_events(self, pause_menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if not self.paused:
                    self.player.movement.handle_down(event.key)

            if event.type == pygame.KEYUP:
                if not self.paused:
                    self.player.movement.handle_up(event.key)
                else:
                    result = pause_menu.run()
                    if result == "resume":
                        self.paused = False
                    elif result == "options":
                        self.options_menu.run()
                        self.paused = False
                    elif result == "main menu":
                        self.client.is_connected = False  # disconnect client
                        return "main_menu"
                    elif result == "quit":
                        self.running = False
        return None

    def game_loop(self):
        self.start_networking()
        pause_menu = PauseMenu(self.screen)

        while self.running:
            # when server is closed become new server or join another
            if not self.client.is_connected:
                print("connection lost, establishing new one")
                self.start_networking()
            dt = self.clock.tick(60) / 1000

            result = self.handle_events(pause_menu)
            if result == "main_menu":
                return "main_menu"

            if not self.paused:
                SoundManager.stop_music()
                self.player.movement.move_player()
                self.draw_game(dt)
            else:
                SoundManager.play_music(MusicType.Menu)

        return "quit"

    def run(self):
        while True:
            choice = MainMenu(self.screen).run()


            if choice == "play":
                self.player = Player(PlayerState.IDLE_DOWN)
                self.character_menu.run()
                self.paused = False
                SoundManager.stop_music()
                result = self.game_loop()
                if result == "quit":
                    break
                elif result == "main_menu":
                    SoundManager.play_music(MusicType.Menu)
                    continue
            elif choice == "options":
                self.options_menu.run()
            elif choice == "quit":
                pygame.quit()
                break


if __name__ == "__main__":
    game = Game()
    game.run()
