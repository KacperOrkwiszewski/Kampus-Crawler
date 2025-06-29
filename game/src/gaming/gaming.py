import random
from constants import Constants, Point
from sound.sound_manager import SoundManager
from sound.sound_type import SoundEffectType


class Gaming:
    def __init__(self, game):
        self.game = game
        self.buliding_count = 0
        self.in_door = False
        self.right_door = False
        self.left_door = False
        self.multiple_door_enter_prot_flag = False

    def reset(self):
        self.game.player.data.ects = 0
        self.game.player.data.lives = 3
        self.buliding_count = 0
        self.new_objective()

    def new_objective(self):
        self.game.game_time_seconds = self.game.max_game_time
        self.game.current_objective = self.random_entrance_campus(self.random_campus())
    
    def right_bulding(self):
        self.right_door = True
        self.buliding_count += 1
        self.game.player.data.ects += random.randint(1, 5)
        if self.game.player.data.ects > 30:
            self.game.player.data.ects = 30
        self.new_objective()
    
    def wrong_building(self):
        self.left_door = True
        if self.game.game_time_seconds > 30:
            self.game.game_time_seconds -= 30
        else:
            self.game.game_time_seconds = 0

    def update_data(self):
        self.out_of_time()
        player_point = Point(self.game.player.data.pos_x, self.game.player.data.pos_y)
        all_entrances = list(Constants.entrences_campus_A.values()) + \
                        list(Constants.entrences_campus_B.values()) + \
                        list(Constants.entrences_campus_C.values())
        if any(player_point in entrance for entrance in all_entrances):
            if self.in_door:
                return
            self.in_door = True
        else:
            self.in_door = False
            self.right_door = False
            self.left_door = False
            self.multiple_door_enter_prot_flag = False

    def check_building(self):
        if not self.in_door:
            return
        player_point = Point(self.game.player.data.pos_x, self.game.player.data.pos_y)
        all_entrances = list(Constants.entrences_campus_A.values()) + \
                        list(Constants.entrences_campus_B.values()) + \
                        list(Constants.entrences_campus_C.values())
        if any(player_point in entrance for entrance in all_entrances):
            if self.multiple_door_enter_prot_flag:
                return
            SoundManager.play_effect(SoundEffectType.DoorOpen)
            self.multiple_door_enter_prot_flag = True
            if player_point in self.game.current_objective[1]:
                self.right_bulding()
                self.new_objective()
            else:
                SoundManager.play_effect(SoundEffectType.WrongDoor)
                self.wrong_building()
    
    def out_of_time(self):
        if self.game.game_time_seconds <= 0:
            self.game.player.data.lives -= 1
            self.game.player.data.ects -= random.randint(1, 5)
            if self.game.player.data.ects < 0:
                self.game.player.data.ects = 0
            SoundManager.play_effect(SoundEffectType.EctsLoss)
            if self.game.player.data.lives <= 0:
                self.game.player.data.lives = 0
                self.game.game_over = True
                SoundManager.play_effect(SoundEffectType.GameOver)
            else:
                self.new_objective()

    def random_campus(self):
        campuses = ['A', 'B', 'C']
        return random.choice(campuses)

    def random_entrance_campus(self, campus):
        if campus == 'A':
            return random.choice(list(Constants.entrences_campus_A.items()))
        elif campus == 'B':
            return random.choice(list(Constants.entrences_campus_B.items()))
        elif campus == 'C':
            return random.choice(list(Constants.entrences_campus_C.items()))
        else:
            raise ValueError("Invalid campus identifier. Use 'A', 'B', or 'C'.")