import random
from constants import Constants, Point
from sound.sound_manager import SoundManager
from sound.sound_type import SoundEffectType


class Gaming:
    def __init__(self, game):
        self.game = game
        self.buliding_count = 0

    def reset(self):
        self.game.player.data.ects = 0
        self.game.player.data.lives = 3
        self.buliding_count = 0
        self.new_objective()

    def new_objective(self):
        self.game.game_time_seconds = self.game.max_game_time
        self.game.current_objective = Constants.random_entrance_campus(Constants.random_campus())
    
    def right_bulding(self):
        self.buliding_count += 1
        self.game.player.data.ects += random.randint(1, 5)
        if self.game.player.data.ects > 30:
            self.game.player.data.ects = 30
        self.new_objective()
    
    def wrong_building(self):
        self.game.game_time_seconds -= 30

    def check_building(self):
        if [Point(self.game.player.data.pos_x, self.game.player.data.pos_y)] in Constants.entrences_campus_A.values() or \
           [Point(self.game.player.data.pos_x, self.game.player.data.pos_y)] in Constants.entrences_campus_B.values() or \
           [Point(self.game.player.data.pos_x, self.game.player.data.pos_y)] in Constants.entrences_campus_C.values():
            SoundManager.play_effect(SoundEffectType.DoorOpen)
            if [Point(self.game.player.data.pos_x, self.game.player.data.pos_y)] == self.game.current_objective:
                self.right_bulding()
                self.new_objective()
            else:
                SoundManager.play_effect(SoundEffectType.WrongDoor)
                self.wrong_building()
    
    def out_of_time(self):
        if self.game.game_time_seconds <= 0:
            self.game.player.data.lives -= 1
            self.game.player.data.ects -= random.randint(1, 5)
            SoundManager.play_effect(SoundEffectType.EctsLoss)
            if self.game.player.data.lives <= 0:
                self.game.player.data.lives = 0
                self.game.game_over = True
                SoundManager.play_effect(SoundEffectType.GameOver)
            else:
                self.new_objective()