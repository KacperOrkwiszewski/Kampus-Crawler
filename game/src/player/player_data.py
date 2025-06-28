class PlayerData:
    def __init__(self, state, character):
        self.id = None
        self.pos_x = 40
        self.pos_y = 40
        self.movement_speed = 2
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

        self.stamina = 100  # current stamina
        self.max_stamina = 100
        self.stamina_drain_rate = 15  # stamina drain per second
        self.stamina_regen_rate = 10  # stamina regen per second
        self.stamina_regen_delay = 1.0  # regeneration delay
        self.stamina_regen_timer = 0.0
        self.is_sprinting = False

        self.lives = 3
        self.max_lives = 3
        self.ects = 15
