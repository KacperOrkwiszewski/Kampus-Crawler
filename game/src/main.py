import pygame
import threading
from client_server.server import Server
from client_server.client import Client
from constants import Constants
from sound.sound_type import MusicType, SoundEffectType
from map.game_map import GameMap
from player.player import Player
from player.player_state import PlayerState, PlayerCharacter
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
        pygame.display.set_icon(pygame.image.load('assets/logo/logo_icon.png'))

        self.map_data = GameMap("assets/map_data/campusA.tmx")
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

        self.msg_typing = False
        self.msg = ""

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
                    self.client.player_objects[player_id] = Player(other_player_data.state, other_player_data.character)

                if self.client.player_objects[player_id].data.state != other_player_data.state:
                    self.client.player_objects[player_id].set_animation(other_player_data.state)

                self.client.player_objects[player_id].data = other_player_data
                offset_x = other_player_data.pos_x - self.player.data.pos_x
                offset_y = other_player_data.pos_y - self.player.data.pos_y

                self.client.player_objects[player_id].draw(
                    self.screen, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, dt, offset_x, offset_y
                )
        
        # Msg input box
        if self.msg_typing:
            font = pygame.font.SysFont("arial", 22)
            input_surf = font.render(self.msg + "|", True, (255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 0), (40, Constants.WINDOW_HEIGHT - 50, 600, 40))
            self.screen.blit(input_surf, (50, Constants.WINDOW_HEIGHT - 45))

        pygame.display.flip()

    def handle_events(self, pause_menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle chat message input
            if self.msg_typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.msg.strip():
                            self.player.data.chat_message = self.msg
                            self.player.data.chat_timer = 180
                        self.msg = ""
                        self.msg_typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.msg = self.msg[:-1]
                    else:
                        if len(self.msg) < 60:
                            self.msg += event.unicode
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

                if not self.paused:
                    self.player.movement.handle_down(event.key)
                
                if event.key == pygame.K_RETURN:
                    self.msg_typing = True
                    self.msg = ""

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
        SoundManager.stop_music()
        SoundManager.play_music(MusicType.Game)
        walking_sound_channel = None

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
                self.player.movement.move_player()
                if self.player.movement.is_moving: # is the player moving?
                  if walking_sound_channel == None: # check for null
                      walking_sound_channel = SoundManager.play_effect(SoundEffectType.Walking)
                  elif not walking_sound_channel.get_busy(): # check if the sound is not currently played
                    walking_sound_channel = SoundManager.play_effect(SoundEffectType.Walking)
                self.draw_game(dt)

            if self.player.data.chat_timer > 0:
                self.player.data.chat_timer -= 1

        return "quit"

    def run(self):
        while True:
            choice = MainMenu(self.screen).run()
            print(f"Main menu choice: {choice}")
            if choice == "play":
                self.character_menu.run()
                self.player = Player(PlayerState.IDLE_DOWN, PlayerCharacter(self.character_menu.selected_character))
                self.paused = False
                result = self.game_loop()
                if result == "quit":
                    break
                elif result == "main_menu":
                    SoundManager.stop_music()
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
