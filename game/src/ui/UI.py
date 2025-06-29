import pygame
from constants import Constants
from menu.pause_menu import PauseMenu
from menu.options_menu import OptionsMenu
from menu.quick_help import QuickHelp


class UI:
    def __init__(self, screen, options_menu, player=None):
        self.player = player
        self.screen = screen
        self.font_path = "assets/menu/font.ttf"

        self.font_main = pygame.font.Font(self.font_path, 14)
        self.font_large = pygame.font.Font(self.font_path, 26)
        self.font_nick = pygame.font.Font(self.font_path, 18)

        self.text_color = (255, 255, 255)

        icon_scale_factor = 0.5
        ects_icon_scale_factor = 2
        hearts_scale_factor = 0.4
        self.hs = hearts_scale_factor
        self.icons = {
            'ects': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/ects.png').convert_alpha(),
                ects_icon_scale_factor),
            'time': pygame.image.load('assets/tiles/icons/time.png').convert_alpha(),
            'heart_full': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/sprite_4.png').convert_alpha(),
                hearts_scale_factor),
            'heart_empty': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/sprite_3.png').convert_alpha(),
                hearts_scale_factor),
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
        self.left_border_img = pygame.transform.smoothscale(pygame.image.load('assets/tiles/borders/left_border.png')
                                                            .convert_alpha(), (150, 90))
        self.right_border_img = pygame.transform.smoothscale(pygame.image.load('assets/tiles/borders/right_border.png')
                                                             .convert_alpha(), (150, 90))
        self.middle_border_img = pygame.transform.smoothscale(
            pygame.image.load('assets/tiles/borders/middle_border.png')
            .convert_alpha(), (400, 120))

        end_cap_scale_factor = 1.5
        middle_border_img = pygame.image.load('assets/tiles/borders/middle_border.png').convert_alpha()
        new_middle_height = int(middle_border_img.get_height() * end_cap_scale_factor)

        self.bar_height = new_middle_height - 8

        self.options_button_rect = None
        self.pause_button_rect = None
        self.help_button_rect = None

        self.help_menu = QuickHelp(self.screen)
        self.options_menu = options_menu
        self.paused = False

        self.objective_text = "OBJECTIVE:"

        self.floating_time_msg = None
        self.floating_time_timer = 0
        self.floating_time_y_offset = 0

    def show_time_penalty(self, seconds=-30):
        self.floating_time_msg = f"{seconds}s"
        self.floating_time_timer = 1.0  # ile sekund ma być widoczne
        self.floating_time_y_offset = 0

    def handle_click(self, mouse_pos):
        if self.pause_button_rect and self.pause_button_rect.collidepoint(mouse_pos):
            self.paused = True
        elif self.options_button_rect and self.options_button_rect.collidepoint(mouse_pos):
            self.options_menu.run()
        elif self.help_button_rect and self.help_button_rect.collidepoint(mouse_pos):
            self.help_menu.run()

    def draw(self, objective, max_time, time_left):
        self.draw_player_info()
        self.draw_icons()
        self.draw_objective_panel(objective, max_time, time_left)

    def draw_icons(self):
        self.screen.blit(self.right_border_img, (self.screen.get_width() - self.right_border_img.get_width(), 0))
        start_x_icons = 650
        current_x_right = start_x_icons + 15
        icon_margin = 5
        base_icon_y = 40

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
        # border
        self.screen.blit(self.left_border_img, (0, 0))
        # hearts
        hearts_start_x = 15
        heart_width = 50
        hearts_y = 15
        hearts_spacing = 15
        for i in range(self.player.data.max_lives):
            heart_x = hearts_start_x + i * (self.hs * heart_width + hearts_spacing)
            heart_icon = self.icons['heart_full'] if i < self.player.data.lives else self.icons['heart_empty']
            self.screen.blit(heart_icon, (heart_x, hearts_y))
        # stamina
        stamina_bar_height = 12
        stamina_bar_width = 100
        stamina_rect_x_left_panel = 15
        stamina_rect_y_left_panel = 55
        stamina_rect_left_panel = pygame.Rect(stamina_rect_x_left_panel, stamina_rect_y_left_panel,
                                              stamina_bar_width, stamina_bar_height)
        stamina_ratio = self.player.data.stamina / self.player.data.max_stamina
        fill_width_stamina = (stamina_rect_left_panel.width - 4) * stamina_ratio
        fill_rect_stamina = pygame.Rect(stamina_rect_left_panel.x + 2, stamina_rect_left_panel.y + 2,
                                        fill_width_stamina, stamina_rect_left_panel.height - 4)
        pygame.draw.rect(self.screen, (20, 20, 20), stamina_rect_left_panel, border_radius=3)
        pygame.draw.rect(self.screen, (207, 207, 207), stamina_rect_left_panel, width=2, border_radius=3)
        pygame.draw.rect(self.screen, (3, 127, 140), fill_rect_stamina, border_radius=3)

    def draw_objective_panel(self, objective, max_time, time_left):
        game_time_seconds = time_left
        # border
        self.screen.blit(self.middle_border_img,
                         (self.screen.get_width() // 2 - self.middle_border_img.get_width() // 2, 0))
        # objective text
        objective_text = self.objective_text + objective[0]
        outline_width = 2
        base = self.font_large.render(objective_text, True, self.text_color)
        size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
        img = pygame.Surface(size, pygame.SRCALPHA)
        obj_x = self.screen.get_width() // 2
        obj_y = 30

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    img.blit(
                        self.font_large.render(objective_text, True, (38, 38, 38)),
                        (dx + outline_width, dy + outline_width)
                    )
        img.blit(base, (outline_width, outline_width))
        draw_x = obj_x - img.get_width() // 2
        draw_y = obj_y - img.get_height() // 2
        self.screen.blit(img, (draw_x, draw_y))
        # ects count
        outline_width = 3
        ects_text = f"{self.player.data.ects}/30 ECTS"
        ects_base = self.font_large.render(ects_text, True, self.text_color)
        size = (ects_base.get_width() + 2 * outline_width, ects_base.get_height() + 2 * outline_width)
        ects_img = pygame.Surface(size, pygame.SRCALPHA)

        # Outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    ects_img.blit(
                        self.font_large.render(ects_text, True, (38, 38, 38)),
                        (dx + outline_width, dy + outline_width)
                    )
        ects_img.blit(ects_base, (outline_width, outline_width))
        self.screen.blit(self.icons['ects'], (0, 554))
        self.screen.blit(ects_img, (38, 560))
        #  timer
        time_text_surf = self.font_main.render(f"{int(game_time_seconds) // 60:02d}:{int(game_time_seconds) % 60:02d}",
                                               True, self.text_color)
        bar_width = 320
        bar_height = 14
        time_rect = pygame.Rect(
            (self.screen.get_width() - bar_width) // 2,
            58,
            bar_width,
            bar_height
        )
        time_ratio = game_time_seconds / max_time
        fill_rect_time = pygame.Rect(
            time_rect.x,
            time_rect.y,
            int(bar_width * time_ratio),
            bar_height
        )
        # change color with time
        # do not if time > half
        if time_ratio > 0.5:
            bar_color = (57, 115, 48)  # original color
        else:
            t = time_ratio * 2  # scale 0..0.5 to 0..1
            r = int((1 - t) * 255 + t * 57)
            g = int((1 - t) * 50 + t * 115)
            b = int((1 - t) * 50 + t * 48)
            bar_color = (r, g, b)
        pygame.draw.rect(self.screen, (20, 20, 20), time_rect, border_radius=3)
        pygame.draw.rect(self.screen, bar_color, fill_rect_time, border_radius=3)
        pygame.draw.rect(self.screen, (207, 207, 207), time_rect, width=2, border_radius=3)
        self.screen.blit(self.icons['time'], (
            self.screen.get_width() // 2 - time_text_surf.get_width() + 20, 82))
        self.screen.blit(time_text_surf, (self.screen.get_width() // 2 - time_text_surf.get_width() // 2 + 10, 86))

        # floating time penalty
        if self.floating_time_msg and self.floating_time_timer > 0:
            font = self.font_large
            color = (255, 60, 60)
            text = font.render(self.floating_time_msg, True, color)
            x = self.screen.get_width() // 2 + bar_width // 2 + 40
            y = 100 - self.floating_time_y_offset
            self.screen.blit(text, (x, y))
            # animacja: przesuwanie w górę i znikanie
            self.floating_time_y_offset += 60 * self.screen.get_height() / 1080 * (1/60)  # dostosuj szybkość
            self.floating_time_timer -= 1/60
            if self.floating_time_timer <= 0:
                self.floating_time_msg = None
                self.floating_time_y_offset = 0
