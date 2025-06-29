import pygame
from constants import Constants, Point

class BuildingInfo:
    def __init__(self, game):
        self.building = None
        self.player = game.player
        self.screen = game.screen
        self.game = game
        self.building_msg = ""
        self.msg_set = False
        self.msg_timer = 0
        self.max_msg_time = 1

    def right_bulding(self):
        if self.game.gaming.right_door == True:
            self.building_msg = self.building[0] + ": Good job!"
            self.msg_set = True

    def wrong_building(self):
        if self.game.gaming.left_door == True:
            self.game.ui.show_time_penalty()
            self.building_msg = self.building[0] + ": Wrong one"
            self.msg_set = True

    def set_building_info(self):
        player_point = Point(self.player.data.pos_x, self.player.data.pos_y)
        for building_name, entrances in Constants.entrences_campus_A.items():
            if player_point in entrances:
                self.building = (building_name, entrances)
                return
        for building_name, entrances in Constants.entrences_campus_B.items():
            if player_point in entrances:
                self.building = (building_name, entrances)
                return
        for building_name, entrances in Constants.entrences_campus_C.items():
            if player_point in entrances:
                self.building = (building_name, entrances)
                return
        self.building = None

    def try_draw(self):
        if self.game.gaming.in_door:
            self.msg_timer = self.max_msg_time
        if self.msg_timer > 0:
            if self.msg_timer == self.max_msg_time:
                self.set_building_info()
                self.right_bulding()
                self.wrong_building()
            self.msg_timer -= self.game.dt
            if self.building is None:
                return
            if self.msg_set:
                outline_width = 3
                font = pygame.font.Font("assets/menu/font.ttf", 26)
                text_base = font.render(self.building_msg, True, (255, 255, 255))
                size = (text_base.get_width() + 2 * outline_width, text_base.get_height() + 2 * outline_width)
                text_img = pygame.Surface(size, pygame.SRCALPHA)
                # Outline
                for dx in range(-outline_width, outline_width + 1):
                    for dy in range(-outline_width, outline_width + 1):
                        if dx != 0 or dy != 0:
                            text_img.blit(
                                font.render(self.building_msg, True, (38, 38, 38)),
                                (dx + outline_width, dy + outline_width)
                            )
                text_img.blit(text_base, (outline_width, outline_width))
                self.screen.blit(text_img, (430, 560))
        else:
            self.msg_set = False
