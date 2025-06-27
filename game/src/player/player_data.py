class PlayerData:
    def __init__(self, state, character):
        self.id = None
        self.pos_x = 40
        self.pos_y = 40
        self.movement_speed = 20
        self.folder = "assets/characters/"
        self.state = state
        self.character = character
        self.last_direction = state
        self.is_moving = False
        self.during_diagonal_alignment = False
        self.character_id = 1
        self.player_name = "unnamed"
        self.chat_message = ""
        self.chat_timer = 0
