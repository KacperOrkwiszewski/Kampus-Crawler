from game.src.player.player_state import ANIMATION_FILES
from game.src.player.player_image_info import PlayerImageInfo
from game.src.player.movement_manager import MovementManager
from game.src.player.player_data import PlayerData


class Player:
    def __init__(self, state):
        self.data = PlayerData()
        self.player_img_info = PlayerImageInfo(ANIMATION_FILES[state], self.data.movement_speed)
        self.current_animation = ANIMATION_FILES[state]
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
        filename = ANIMATION_FILES[state]
        # If the requested animation is already active, do nothing
        if self.current_animation == filename:
            return
        # Otherwise, update the current animation and reload frames
        self.data.state = state
        self.current_animation = filename
        self.player_img_info = PlayerImageInfo(filename, self.data.movement_speed)
