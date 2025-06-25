import pygame
from game.src.constants import Constants


class UI:
    def __init__(self, screen, player=None):
        self.player = player
        self.screen = screen
        self.font_path = "assets/menu/font.ttf"

        self.font_main = pygame.font.Font(self.font_path, 14)
        self.font_nick = pygame.font.Font(self.font_path, 16)


        self.text_color = (255, 255, 255)

        self.icons = {
            'ects': pygame.image.load('assets/tiles/icons/ects.png').convert_alpha(),
            'time': pygame.image.load('assets/tiles/icons/time.png').convert_alpha(),
            'heart_full': pygame.image.load('assets/tiles/icons/sprite_4.png').convert_alpha(),
            'heart_empty': pygame.image.load('assets/tiles/icons/sprite_3.png').convert_alpha(),
            'quit': pygame.image.load('assets/tiles/icons/quit.png').convert_alpha(),
            'options': pygame.image.load('assets/tiles/icons/gear.png').convert_alpha(),
            'pause': pygame.image.load('assets/tiles/icons/icons1.png').convert_alpha(),
            'help': pygame.image.load('assets/tiles/icons/icons0.png').convert_alpha()
        }

        # SKALOWANIE RAMEK (szerokość i wysokość)
        end_cap_scale_factor = 1.5

        left_border_img = pygame.image.load('assets/tiles/borders/borders_0.png').convert_alpha()
        right_border_img = pygame.image.load('assets/tiles/borders/borders_1.png').convert_alpha()
        middle_border_img = pygame.image.load('assets/tiles/borders/border2_3.png').convert_alpha()

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

        self.borders = {
            'left': pygame.transform.scale(left_border_img, (new_left_width, new_left_height)),
            'middle': pygame.transform.scale(middle_border_img, (middle_border_img.get_width(), new_middle_height)),
            'right': pygame.transform.scale(right_border_img, (new_right_width, new_right_height))
        }

        # Wysokość panelu jest zdeterminowana przez wysokość jego części
        self.bar_height = self.borders[
            'middle'].get_height()

    def _draw_top_bar(self, x, y, width):
        """Rysuje jeden, długi panel na górze ekranu."""

        # Lewe zakończenie
        self.screen.blit(self.borders['left'], (x, y))

        # Środek
        middle_width = self.borders['middle'].get_width()
        current_x = x + self.borders['left'].get_width()
        if middle_width == 0:
            print("Ostrzeżenie: Szerokość środkowej ramki wynosi 0. Nie będzie rysowana.")
        else:
            while current_x < x + width - self.borders['right'].get_width():
                self.screen.blit(self.borders['middle'], (current_x, y))
                current_x += middle_width
                if current_x + self.borders['right'].get_width() > x + width:
                    break

        self.screen.blit(self.borders['right'], (x + width - self.borders['right'].get_width(), y))

        return pygame.Rect(x, y, width, self.bar_height)

    def draw(self, player_data, time_left, objective_text):
        """Główna metoda rysująca UI, dostosowana do zamienionych wymiarów."""

        actual_screen_width = Constants.WINDOW_HEIGHT
        bar_rect = self._draw_top_bar(0, 0, actual_screen_width)

        # Marginesy WEWNĄTRZ panelu
        padding_h = 25
        padding_v = 8

        # SEKCJA LEWA (ECTS, Czas, Stamina)
        left_section_x = bar_rect.left + padding_h

        offset_down_left_panel = 15

        # ECTS (górna linia)
        ects_y = bar_rect.top + padding_v + offset_down_left_panel
        self.screen.blit(self.icons['ects'], (left_section_x, ects_y))
        ects_text = self.font_main.render(f"{player_data.ects} ECTS", True, self.text_color)
        self.screen.blit(ects_text, (left_section_x + self.icons['ects'].get_width() + 5, ects_y + 1))

        # Czas (środkowa linia)
        time_y = bar_rect.top + padding_v + 22 + offset_down_left_panel
        self.screen.blit(self.icons['time'], (left_section_x, time_y))
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        time_text = self.font_main.render(f"{minutes:02d}:{seconds:02d}", True, self.text_color)
        self.screen.blit(time_text, (left_section_x + self.icons['time'].get_width() + 5, time_y + 1))

        # Stamina (dolna linia)
        stamina_y = bar_rect.top + padding_v + 44 + offset_down_left_panel
        stamina_rect = pygame.Rect(left_section_x, stamina_y, 140, 12)
        pygame.draw.rect(self.screen, (40, 40, 40), stamina_rect, border_radius=3)
        stamina_ratio = player_data.stamina / player_data.max_stamina
        fill_width = (stamina_rect.width - 4) * stamina_ratio
        fill_rect = pygame.Rect(stamina_rect.x + 2, stamina_rect.y + 2, fill_width, stamina_rect.height - 4)
        pygame.draw.rect(self.screen, (50, 200, 50), fill_rect, border_radius=3)
        pygame.draw.rect(self.screen, (200, 200, 200), stamina_rect, 1, border_radius=3)

        # SEKCJA ŚRODKOWA (Życia i Nick)
        nick_surf = self.font_nick.render(player_data.player_name, True, self.text_color)
        nick_rect = nick_surf.get_rect()

        heart_width = self.icons['heart_full'].get_width()
        hearts_width = player_data.max_lives * heart_width + (player_data.max_lives - 1) * 5

        # Ustalenie wspólnego środka pionowego dla sekcji środkowej
        center_y_for_middle_section = bar_rect.centery

        offset_up_middle_panel = 10

        # Obliczanie pozycji startowej X dla całej sekcji środkowej (pozostaje bez zmian)
        total_middle_elements_width = nick_rect.width + 20 + hearts_width
        start_x_for_middle_section = bar_rect.centerx - (total_middle_elements_width // 2)

        # Ustawienie pozycji nicku
        nick_rect.topleft = (
        start_x_for_middle_section, center_y_for_middle_section - nick_rect.height // 2 - offset_up_middle_panel)
        self.screen.blit(nick_surf, nick_rect)

        # Ustawienie pozycji serc
        hearts_start_x = nick_rect.right + 20
        for i in range(player_data.max_lives):
            heart_x = hearts_start_x + i * (heart_width + 5)
            self.screen.blit(
                self.icons['heart_full'] if i < player_data.lives else self.icons['heart_empty'],
                (heart_x, center_y_for_middle_section - heart_width // 2 - offset_up_middle_panel)
            )



        # SEKCJA PRAWA (Pozostałe ikony)
        icon_y = bar_rect.centery - self.icons['quit'].get_height() // 2
        icon_margin = 8

        quit_x = bar_rect.right - padding_h - self.icons['quit'].get_width()
        self.screen.blit(self.icons['quit'], (quit_x, icon_y))

        options_x = quit_x - icon_margin - self.icons['options'].get_width()
        self.screen.blit(self.icons['options'], (options_x, icon_y))

        pause_x = options_x - icon_margin - self.icons['pause'].get_width()
        self.screen.blit(self.icons['pause'], (pause_x, icon_y))

        help_x = pause_x - icon_margin - self.icons['help'].get_width()
        self.screen.blit(self.icons['help'], (help_x, icon_y))

        # DODANIE OBJECTIVE TEXT
        objective_surf = self.font_main.render(objective_text, True, self.text_color)
        objective_rect = objective_surf.get_rect(
            center=(bar_rect.centerx, bar_rect.bottom - padding_v - objective_surf.get_height() // 2))
        self.screen.blit(objective_surf, objective_rect)