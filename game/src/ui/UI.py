import pygame
from game.src.constants import Constants


class UI:
    def __init__(self, screen, player=None):
        self.player = player
        self.screen = screen
        self.font_path = "assets/menu/font.ttf"

        self.font_main = pygame.font.Font(self.font_path, 14)
        self.font_large = pygame.font.Font(self.font_path, 20)
        self.font_nick = pygame.font.Font(self.font_path, 18)

        self.text_color = (255, 255, 255)

        # Współczynnik skalowania dla ikon
        icon_scale_factor = 2.25
        ects_icon_scale_factor = 1.5

        # Załadowanie i opcjonalne przeskalowanie ikon
        self.icons = {
            'ects': pygame.transform.scale_by(
                pygame.image.load('assets/tiles/icons/ects.png').convert_alpha(),
                ects_icon_scale_factor),
            'time': pygame.image.load('assets/tiles/icons/time.png').convert_alpha(),
            'heart_full': pygame.image.load('assets/tiles/icons/sprite_4.png').convert_alpha(),
            'heart_empty': pygame.image.load('assets/tiles/icons/sprite_3.png').convert_alpha(),
            'quit': pygame.image.load('assets/tiles/icons/quit.png').convert_alpha(),
            # Przeskalowanie ikon na prawym panelu
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

        # SKALOWANIE RAMEK (szerokość i wysokość)
        end_cap_scale_factor = 1.5

        left_border_img = pygame.image.load('assets/tiles/borders/left_border.png').convert_alpha()
        right_border_img = pygame.image.load('assets/tiles/borders/right_border.png').convert_alpha()
        middle_border_img = pygame.image.load('assets/tiles/borders/middle_border.png').convert_alpha()

        original_left_height = left_border_img.get_height()
        original_left_width = left_border_img.get_width()
        original_right_height = right_border_img.get_height()
        original_right_width = right_border_img.get_width()
        original_middle_height = middle_border_img.get_height()

        # Obliczamy nowe wymiary dla lewej i prawej ramki
        new_left_width = int(original_left_width * end_cap_scale_factor)
        new_left_height = int(original_left_height * end_cap_scale_factor)
        new_right_width = int(original_right_width * end_cap_scale_factor)
        new_right_height = int(original_right_height * end_cap_scale_factor)
        new_middle_height = int(original_middle_height * end_cap_scale_factor)

        self.bar_height = new_middle_height - 8

        self.borders = {
            'left': pygame.transform.scale(left_border_img, (new_left_width, new_left_height)),
            'middle_original': pygame.transform.scale(middle_border_img,
                                                      (middle_border_img.get_width(), self.bar_height)),
            'right': pygame.transform.scale(right_border_img, (new_right_width, new_right_height))
        }

    def _draw_top_bar(self, x, y, width):
        self.screen.blit(self.borders['left'], (x, y))

        left_end_x = x + self.borders['left'].get_width()
        right_start_x = x + width - self.borders['right'].get_width()
        stretch_width = max(0, right_start_x - left_end_x)
        stretched_middle_img = pygame.transform.scale(
            self.borders['middle_original'],
            (stretch_width, self.bar_height)
        )

        self.screen.blit(stretched_middle_img, (left_end_x, y))
        self.screen.blit(self.borders['right'], (x + width - self.borders['right'].get_width(), y))

        return pygame.Rect(x, y, width, self.bar_height)

    def draw(self, player_data, time_left, objective_text):
        actual_screen_width = Constants.WINDOW_HEIGHT
        bar_rect = self._draw_top_bar(0, 0, actual_screen_width)

        # SEKCJA LEWA (Nick i Życia)
        left_section_area_width = self.borders['left'].get_width()
        left_section_start_x = bar_rect.left

        nick_surf = self.font_large.render(player_data.player_name, True, self.text_color)
        heart_width = self.icons['heart_full'].get_width()
        hearts_spacing = 5
        hearts_height = heart_width

        # Całkowita wysokość bloku z nickiem i sercami (nick + przerwa + serca)
        total_left_elements_height = nick_surf.get_height() + hearts_spacing + hearts_height

        # Wyśrodkuj pionowo: start Y = góra paska + (wysokość paska - wysokość bloku) / 2
        start_y_left_section = bar_rect.top + (self.bar_height - total_left_elements_height) // 2

        # Wyśrodkuj nick poziomo w obrębie lewej ramki
        nick_x = left_section_start_x + (left_section_area_width - nick_surf.get_width()) // 2 - 10
        nick_y = start_y_left_section - 30
        self.screen.blit(nick_surf, (nick_x, nick_y))

        # Serca wyśrodkuj poziomo w tej samej szerokości
        hearts_total_width = player_data.max_lives * heart_width + (player_data.max_lives - 1) * hearts_spacing
        hearts_start_x = left_section_start_x + (left_section_area_width - hearts_total_width) // 2 - 10
        hearts_y = nick_y + nick_surf.get_height() + hearts_spacing

        for i in range(player_data.max_lives):
            heart_x = hearts_start_x + i * (heart_width + hearts_spacing)
            heart_icon = self.icons['heart_full'] if i < player_data.lives else self.icons['heart_empty']
            self.screen.blit(heart_icon, (heart_x, hearts_y))

        # SEKCJA ŚRODKOWA (Objective, ECTS, Stamina, Time)
        middle_section_start_x = bar_rect.left + self.borders['left'].get_width()
        middle_section_end_x = bar_rect.right - self.borders['right'].get_width()
        middle_section_area_width = middle_section_end_x - middle_section_start_x

        # Odstępy między elementami pionowo w środkowej sekcji
        element_spacing_middle = 5

        # Przygotuj powierzchnie tekstowe i uzyskaj ich wymiary
        objective_surf = self.font_large.render(objective_text, True, self.text_color)
        ects_text_surf = self.font_large.render(f"{player_data.ects} ECTS", True, self.text_color)
        time_text_surf = self.font_main.render(f"{int(time_left) // 60:02d}:{int(time_left) % 60:02d}", True,
                                               self.text_color)

        top_margin_objective = 20
        current_y_middle = bar_rect.top + top_margin_objective

        # 1. Cel (Objective) – NA GÓRZE
        objective_x = middle_section_start_x + (middle_section_area_width - objective_surf.get_width()) // 2
        self.screen.blit(objective_surf, (objective_x, current_y_middle))

        current_y_middle += objective_surf.get_height() + element_spacing_middle

        # 2. ECTS + ikona
        ects_offset_y = 14
        ects_block_width = self.icons['ects'].get_width() + 5 + ects_text_surf.get_width()
        ects_block_x = middle_section_start_x + (middle_section_area_width - ects_block_width) // 2
        self.screen.blit(self.icons['ects'], (
            ects_block_x,
            current_y_middle + (ects_text_surf.get_height() - self.icons['ects'].get_height()) / 2 + ects_offset_y))
        self.screen.blit(ects_text_surf, (
            ects_block_x + self.icons['ects'].get_width() + 5, current_y_middle + ects_offset_y))

        current_y_middle += max(ects_text_surf.get_height(), self.icons['ects'].get_height()) + element_spacing_middle

        # 3. Pasek staminy
        stamina_bar_height = 16
        stamina_bar_margin_bottom = 60
        stamina_bar_width = int(middle_section_area_width * 0.75)

        stamina_rect_x = middle_section_start_x + (middle_section_area_width - stamina_bar_width) // 2
        stamina_rect_y = bar_rect.bottom - stamina_bar_margin_bottom - stamina_bar_height

        stamina_rect = pygame.Rect(stamina_rect_x, stamina_rect_y, stamina_bar_width, stamina_bar_height)
        pygame.draw.rect(self.screen, (20, 20, 20), stamina_rect, border_radius=3)
        pygame.draw.rect(self.screen, (80, 80, 80), stamina_rect, width=2, border_radius=3)

        stamina_ratio = player_data.stamina / player_data.max_stamina
        fill_width = (stamina_rect.width - 4) * stamina_ratio
        fill_rect = pygame.Rect(stamina_rect.x + 2, stamina_rect.y + 2, fill_width, stamina_rect.height - 4)
        pygame.draw.rect(self.screen, (50, 200, 50), fill_rect, border_radius=3)

        # 4. Czas
        bottom_margin_time = 25
        time_block_width = time_text_surf.get_width() + self.icons['time'].get_width() + 5
        time_block_x = middle_section_start_x + (middle_section_area_width - time_block_width) // 2

        time_y = bar_rect.bottom - bottom_margin_time - max(time_text_surf.get_height(),
                                                            self.icons['time'].get_height())

        self.screen.blit(self.icons['time'],
                         (time_block_x, time_y + (time_text_surf.get_height() - self.icons['time'].get_height()) / 2))
        self.screen.blit(time_text_surf, (time_block_x + self.icons['time'].get_width() + 5, time_y))

        # SEKCJA PRAWA (Pozostałe ikony)
        right_section_start_x = bar_rect.right - self.borders['right'].get_width()
        right_section_area_width = self.borders['right'].get_width()

        icon_margin = 8  # Odstęp między ikonami

        total_right_icons_width = (
                self.icons['options'].get_width() + icon_margin +
                self.icons['pause'].get_width() + icon_margin +
                self.icons['help'].get_width()
        )

        # Wyśrodkuj cały blok ikon poziomo w prawej sekcji
        start_x_right_section = right_section_start_x + (right_section_area_width - total_right_icons_width) // 2

        current_x_right = start_x_right_section + 15
        base_icon_y = bar_rect.centery + (-20)

        # Ikona 'help'
        help_icon_y = base_icon_y - self.icons['help'].get_height() // 2
        self.screen.blit(self.icons['help'], (current_x_right, help_icon_y))
        current_x_right += self.icons['help'].get_width() + icon_margin

        # Ikona 'pause'
        pause_icon_y = base_icon_y - self.icons['pause'].get_height() // 2
        self.screen.blit(self.icons['pause'], (current_x_right, pause_icon_y))
        current_x_right += self.icons['pause'].get_width() + icon_margin

        # Ikona 'options'
        options_icon_y = base_icon_y - self.icons['options'].get_height() // 2
        self.screen.blit(self.icons['options'], (current_x_right, options_icon_y))
        current_x_right += self.icons['options'].get_width() + icon_margin
