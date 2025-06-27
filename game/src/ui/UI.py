import pygame
from constants import Constants
from menu.pause_menu import PauseMenu
from menu.options_menu import OptionsMenu
from menu.quick_help import QuickHelp


class UI:
    def __init__(self, screen,options_menu, player=None):
        self.player = player
        self.screen = screen
        self.font_path = "assets/menu/font.ttf"

        self.font_main = pygame.font.Font(self.font_path, 14)
        self.font_large = pygame.font.Font(self.font_path, 20)
        self.font_nick = pygame.font.Font(self.font_path, 18)

        self.text_color = (255, 255, 255)

        icon_scale_factor = 0.8
        ects_icon_scale_factor = 1.5

        self.icons = {
            'ects': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/ects.png').convert_alpha(),
                ects_icon_scale_factor),
            'time': pygame.image.load('assets/tiles/icons/time.png').convert_alpha(),
            'heart_full': pygame.image.load('assets/tiles/icons/sprite_4.png').convert_alpha(),
            'heart_empty': pygame.image.load('assets/tiles/icons/sprite_3.png').convert_alpha(),
            'quit': pygame.image.load('assets/tiles/icons/quit.png').convert_alpha(),
            'options': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/gear.png').convert_alpha(),
                icon_scale_factor),
            'pause': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/icons1.png').convert_alpha(),
                icon_scale_factor),
            'help': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/icons0.png').convert_alpha(),
                icon_scale_factor)
        }

        end_cap_scale_factor = 1.5
        middle_border_img = pygame.image.load('assets/tiles/borders/middle_border.png').convert_alpha()
        new_middle_height = int(middle_border_img.get_height() * end_cap_scale_factor)

        self.bar_height = new_middle_height - 8

        self.options_button_rect = None
        self.pause_button_rect = None
        self.help_button_rect = None

        self.help_menu = QuickHelp(self.screen)
        self.options_menu = options_menu
        self.pause_menu = PauseMenu(self.screen)

        self.objective_text = "OBJECTIVE : pog"
        self.game_time_seconds = 100

    def handle_click(self, mouse_pos):
        if self.pause_button_rect and self.pause_button_rect.collidepoint(mouse_pos):
            self.pause_menu.run()

        elif self.options_button_rect and self.options_button_rect.collidepoint(mouse_pos):
            self.options_menu.run()
        elif self.help_button_rect and self.help_button_rect.collidepoint(mouse_pos):
            self.help_menu.run()

    def draw(self):



        self.draw_icons()



    def draw_icons(self):
        start_x_icons = 580
        current_x_right = start_x_icons + 15
        icon_margin = 5
        base_icon_y = 35

        # 'help'
        help_icon_y = base_icon_y - self.icons['help'].get_height() // 2
        self.help_button_rect = pygame.Rect(current_x_right, help_icon_y, self.icons['help'].get_width(),
                                            self.icons['help'].get_height())
        self.screen.blit(self.icons['help'], self.help_button_rect)
        current_x_right += self.icons['help'].get_width() + icon_margin
        # 'pause'
        pause_icon_y = base_icon_y - self.icons['pause'].get_height() // 2
        self.pause_button_rect = pygame.Rect(current_x_right, pause_icon_y, self.icons['pause'].get_width(),
                                             self.icons['pause'].get_height())
        self.screen.blit(self.icons['pause'], self.pause_button_rect)
        current_x_right += self.icons['pause'].get_width() + icon_margin
        # 'options'
        options_icon_y = base_icon_y - self.icons['options'].get_height() // 2
        self.options_button_rect = pygame.Rect(current_x_right, options_icon_y, self.icons['options'].get_width(),
                                               self.icons['options'].get_height())
        self.screen.blit(self.icons['options'], self.options_button_rect)
        current_x_right += self.icons['options'].get_width() + icon_margin

    def draw_player_info(self):
        left_section_start_x = 10
        nick_surf = self.font_large.render(self.player.data.player_name, True, self.text_color)
        heart_width = 50
        hearts_spacing = 5
        hearts_height = heart_width
        stamina_bar_height = 16
        stamina_bar_margin_top_hearts = 10
        start_y_left_section = 20
        nick_x = 10
        nick_y = 10
        self.screen.blit(nick_surf, (nick_x, nick_y))
        hearts_start_x = 10
        hearts_y = 30
        for i in range(self.player.data.max_lives):
            heart_x = hearts_start_x + i * (heart_width + hearts_spacing)
            heart_icon = self.icons['heart_full'] if i < self.player.data.lives else self.icons['heart_empty']
            self.screen.blit(heart_icon, (heart_x, hearts_y))
        stamina_bar_width = 100
        stamina_rect_x_left_panel = 100
        stamina_rect_y_left_panel = 100
        stamina_rect_left_panel = pygame.Rect(stamina_rect_x_left_panel, stamina_rect_y_left_panel,
                                              stamina_bar_width, stamina_bar_height)
        pygame.draw.rect(self.screen, (20, 20, 20), stamina_rect_left_panel, border_radius=3)
        pygame.draw.rect(self.screen, (80, 80, 80), stamina_rect_left_panel, width=2, border_radius=3)
        stamina_ratio = self.player.data.stamina / self.player.data.max_stamina
        fill_width_stamina = (stamina_rect_left_panel.width - 4) * stamina_ratio
        fill_rect_stamina = pygame.Rect(stamina_rect_left_panel.x + 2, stamina_rect_left_panel.y + 2,
                                        fill_width_stamina, stamina_rect_left_panel.height - 4)
        pygame.draw.rect(self.screen, (0, 0, 255), fill_rect_stamina, border_radius=3)

    def draw_objective_panel(self):
        middle_section_start_x = 500
        middle_section_end_x = 900
        middle_section_area_width = middle_section_end_x - middle_section_start_x
        objective_surf = self.font_large.render(self.objective_text, True, self.text_color)
        ects_text_surf = self.font_large.render(f"{self.player.data.ects} ECTS", True, self.text_color)
        time_text_surf = self.font_main.render(f"{int(self.game_time_seconds) // 60:02d}:{int(self.game_time_seconds) % 60:02d}",
                                               True, self.text_color)
        self.screen.blit(objective_surf, (objective_x, current_y_middle))
        #self.screen.blit(self.icons['ects'], (
        #    ects_block_x, current_y_middle + (ects_text_surf.get_height() - self.icons['ects'].get_height()) / 2 + 14))
        #self.screen.blit(ects_text_surf, (ects_block_x + self.icons['ects'].get_width() + 5, current_y_middle + 14))
        #pygame.draw.rect(self.screen, (20, 20, 20), time_rect, border_radius=3)
        #pygame.draw.rect(self.screen, (80, 80, 80), time_rect, width=2, border_radius=3)
        time_ratio = self.game_time_seconds / 600
        #pygame.draw.rect(self.screen, (50, 200, 50), fill_rect_time, border_radius=3)
        #self.screen.blit(self.icons['time'], (
        #    time_block_x, time_y_text + (time_text_surf.get_height() - self.icons['time'].get_height()) / 2))
        #self.screen.blit(time_text_surf, (time_block_x + self.icons['time'].get_width() + 5, time_y_text))