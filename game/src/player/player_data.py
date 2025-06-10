from .player_state import PlayerState


class PlayerData:
    def __init__(self):
        self.id = None
        self.pos_x = 40
        self.pos_y = 40
        self.movement_speed = 2
        self.state = PlayerState.IDLE_DOWN
        self.last_direction = PlayerState.IDLE_DOWN
        self.is_moving = False
        self.during_diagonal_alignment = False
