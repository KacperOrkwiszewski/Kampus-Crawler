from .player_state import ANIMATION_FILES, CHARACTERS_FILES, PlayerCharacter
from .player_image_info import PlayerImageInfo
from .movement_manager import MovementManager
from .player_data import PlayerData


class Player:
    def __init__(self, state, character=PlayerCharacter.DAVID):
        self.data = PlayerData(state, character)
        self.player_img_info = PlayerImageInfo(self.data.folder + self.gif_name(), self.data.movement_speed)
        self.current_animation = self.gif_name()
        self.movement = MovementManager(self)

    def draw(self, screen, screen_x, screen_y, dt, offset_x=0, offset_y=0):
        # Get the current animation frame based on elapsed time (dt)
        frame = self.player_img_info.get_current_frame(dt)
        # Draw the current frame centered on the screen
        screen.blit(frame, ((screen_y / 2) - (self.player_img_info.scale_size_y / 2) - offset_x,
            (screen_x / 2) - (self.player_img_info.scale_size_x / 2) - offset_y))

    def update_position(self, x, y):
        self.data.pos_x += x
        self.data.pos_y += y

    def update_animation(self):
        self.set_animation(self.data.state)

    def set_animation(self, state):
        filename = str(CHARACTERS_FILES[self.data.character]) + "_" + str(ANIMATION_FILES[state])
        # If the requested animation is already active, do nothing
        if self.current_animation == filename:
            return
        # Otherwise, update the current animation and reload frames
        self.data.state = state
        self.current_animation = filename
        self.player_img_info = PlayerImageInfo(self.data.folder + filename, self.data.movement_speed)
    
    def gif_name(self):
        return str(CHARACTERS_FILES[self.data.character]) + "_" + str(ANIMATION_FILES[self.data.state])
